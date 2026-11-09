from __future__ import annotations

import base64
import json
import logging
from pathlib import Path
from typing import Any

from openai import OpenAI

from embodied_daily.config import RuntimeSettings

LOGGER = logging.getLogger(__name__)

POSITIVE_VISUAL_TERMS = (
    "robot",
    "robotics",
    "humanoid",
    "manipulator",
    "robot arm",
    "robotic arm",
    "gripper",
    "dexterous",
    "warehouse",
    "factory",
    "assembly",
    "teleoperation",
    "机器人",
    "人形",
    "机械臂",
    "灵巧手",
    "夹爪",
    "操作",
    "装配",
    "工厂",
    "仓储",
)
NEGATIVE_VISUAL_TERMS = (
    "logo",
    "icon",
    "avatar",
    "headshot",
    "portrait",
    "author",
    "speaker",
    "conference",
    "banner",
    "advert",
    "sponsor",
    "二维码",
    "头像",
    "肖像",
    "演讲",
    "会议",
    "广告",
)

VISION_PROMPT = """你是机器人新闻的视觉编辑。请从候选图片中选择最适合实验室大屏展示的一张。
优先级：机器人或机械臂正在操作物体、执行任务、与环境交互；其次是真实产品或部署现场。
必须拒绝人物肖像、公司 Logo、纯文字截图、网页导航、广告、会议合影、无机器人主体的装饰图。
如果没有合格画面，selected_index 返回 0。visual_score 使用 0 到 10，只有清晰且与机器人技术直接相关的图片才能达到 6 分。
只返回 JSON：
{"selected_index":1,"visual_score":8.5,"reason":"简短理由"}"""


def visual_metadata_score(metadata: dict[str, Any]) -> tuple[float, int, int]:
    text = " ".join(
        str(metadata.get(key, "") or "")
        for key in ("alt", "title", "caption", "nearby")
    ).lower()
    positive_hits = sum(term in text for term in POSITIVE_VISUAL_TERMS)
    negative_hits = sum(term in text for term in NEGATIVE_VISUAL_TERMS)
    width = max(
        float(metadata.get("natural_width", 0) or 0),
        float(metadata.get("rendered_width", 0) or 0),
    )
    height = max(
        float(metadata.get("natural_height", 0) or 0),
        float(metadata.get("rendered_height", 0) or 0),
    )
    area_score = min(5.0, (width * height) / 240_000)
    score = area_score + positive_hits * 2.8 - negative_hits * 3.2
    if metadata.get("in_article"):
        score += 1.5
    if metadata.get("in_figure"):
        score += 1.0
    aspect = width / height if height else 0
    if aspect < 0.45 or aspect > 3.2:
        score -= 3
    return score, positive_hits, negative_hits


def _load_images_across_page(page) -> None:
    for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
        try:
            page.evaluate(
                "fraction => window.scrollTo(0, "
                "Math.max(0, document.body.scrollHeight - innerHeight) * fraction)",
                fraction,
            )
            page.wait_for_timeout(350)
        except Exception:
            return


def _collect_visual_candidates(
    page,
    *,
    timeout_ms: int,
    max_candidates: int = 4,
) -> list[dict[str, Any]]:
    _load_images_across_page(page)
    images = page.locator("img")
    ranked: list[dict[str, Any]] = []
    seen_sources: set[str] = set()

    for index in range(min(images.count(), 160)):
        image = images.nth(index)
        try:
            metadata = image.evaluate(
                """element => {
                  const rect = element.getBoundingClientRect();
                  const style = getComputedStyle(element);
                  const figure = element.closest('figure');
                  const container = element.closest('article, main, [role="main"]');
                  const parentText = (element.parentElement?.innerText || '').slice(0, 500);
                  return {
                    src: element.currentSrc || element.src || '',
                    alt: element.alt || '',
                    title: element.title || '',
                    caption: figure?.querySelector('figcaption')?.innerText || '',
                    nearby: parentText,
                    natural_width: element.naturalWidth || 0,
                    natural_height: element.naturalHeight || 0,
                    rendered_width: rect.width || 0,
                    rendered_height: rect.height || 0,
                    in_article: Boolean(container),
                    in_figure: Boolean(figure),
                    visible: style.display !== 'none' &&
                      style.visibility !== 'hidden' &&
                      Number(style.opacity || 1) > 0 &&
                      rect.width > 0 && rect.height > 0
                  };
                }"""
            )
        except Exception:
            continue

        source = str(metadata.get("src", ""))
        width = max(
            float(metadata.get("natural_width", 0) or 0),
            float(metadata.get("rendered_width", 0) or 0),
        )
        height = max(
            float(metadata.get("natural_height", 0) or 0),
            float(metadata.get("rendered_height", 0) or 0),
        )
        if (
            not metadata.get("visible")
            or not source
            or source in seen_sources
            or width < 420
            or height < 240
        ):
            continue
        seen_sources.add(source)
        score, positive_hits, negative_hits = visual_metadata_score(metadata)
        ranked.append(
            {
                "locator": image,
                "metadata": metadata,
                "heuristic_score": score,
                "positive_hits": positive_hits,
                "negative_hits": negative_hits,
            }
        )

    ranked.sort(key=lambda item: item["heuristic_score"], reverse=True)
    output: list[dict[str, Any]] = []
    for item in ranked[: max_candidates * 2]:
        try:
            item["locator"].scroll_into_view_if_needed(timeout=5_000)
            page.wait_for_timeout(150)
            preview = item["locator"].screenshot(
                type="jpeg",
                quality=76,
                timeout=min(timeout_ms, 10_000),
            )
            if len(preview) < 8_000:
                continue
            item["preview"] = preview
            output.append(item)
            if len(output) >= max_candidates:
                break
        except Exception:
            continue
    return output


def _extract_json(text: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("视觉模型没有返回 JSON")
    parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("视觉模型 JSON 顶层必须是对象")
    return parsed


def _vision_select(
    candidates: list[dict[str, Any]],
    *,
    title: str,
    settings: RuntimeSettings,
) -> tuple[dict[str, Any], float] | None:
    if not settings.api_key:
        return None
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                f"新闻标题：{title}\n"
                "下面依次给出候选图片。请严格判断是否展示机器人操作、产品或部署现场。"
            ),
        }
    ]
    for index, candidate in enumerate(candidates, start=1):
        metadata = candidate["metadata"]
        description = {
            "index": index,
            "alt": str(metadata.get("alt", ""))[:220],
            "caption": str(metadata.get("caption", ""))[:220],
            "nearby": str(metadata.get("nearby", ""))[:220],
            "width": metadata.get("natural_width", 0),
            "height": metadata.get("natural_height", 0),
        }
        encoded = base64.b64encode(candidate["preview"]).decode("ascii")
        content.extend(
            [
                {
                    "type": "text",
                    "text": "候选图片 " + json.dumps(description, ensure_ascii=False),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded}"},
                },
            ]
        )

    client = OpenAI(
        api_key=settings.api_key,
        base_url=settings.api_base,
        timeout=90.0,
        max_retries=1,
    )
    response = client.chat.completions.create(
        model=settings.model,
        max_completion_tokens=800,
        reasoning_effort="high",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": VISION_PROMPT},
            {"role": "user", "content": content},
        ],
    )
    raw = response.choices[0].message.content or ""
    parsed = _extract_json(raw if isinstance(raw, str) else json.dumps(raw))
    selected_index = int(parsed.get("selected_index", 0) or 0)
    visual_score = float(parsed.get("visual_score", 0) or 0)
    if 1 <= selected_index <= len(candidates) and visual_score >= 6:
        LOGGER.info(
            "视觉模型选中候选图 %s，评分 %.1f：%s",
            selected_index,
            visual_score,
            str(parsed.get("reason", ""))[:160],
        )
        return candidates[selected_index - 1], visual_score
    LOGGER.info(
        "视觉模型判定该新闻没有合格展示图：%s",
        str(parsed.get("reason", ""))[:160],
    )
    return None


def capture_best_article_visual(
    page,
    path: Path,
    *,
    title: str,
    settings: RuntimeSettings | None,
    timeout_ms: int,
) -> float:
    candidates = _collect_visual_candidates(page, timeout_ms=timeout_ms)
    if not candidates:
        raise RuntimeError("网页中没有找到尺寸足够的展示图片")

    selected: tuple[dict[str, Any], float] | None = None
    if settings is not None:
        try:
            selected = _vision_select(candidates, title=title, settings=settings)
        except Exception as exc:
            LOGGER.warning("多模态图片判断失败，改用语义与尺寸规则：%s", exc)

    if selected is None:
        fallback = next(
            (
                item
                for item in candidates
                if item["positive_hits"] > 0
                and item["negative_hits"] == 0
                and item["heuristic_score"] >= 6
            ),
            None,
        )
        if fallback is None:
            raise RuntimeError("网页中没有机器人操作、产品或部署相关的合格图片")
        selected = (fallback, min(7.0, max(6.0, fallback["heuristic_score"])))

    item, score = selected
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(item["preview"])
    return score
