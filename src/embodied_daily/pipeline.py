from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from embodied_daily.article_content import collect_article_texts
from embodied_daily.config import RuntimeSettings, load_yaml
from embodied_daily.demo import demo_candidates
from embodied_daily.feeds import collect_candidates
from embodied_daily.feishu import send_to_feishu
from embodied_daily.filtering import apply_daily_date_policy, prefilter
from embodied_daily.llm import DigestSelector, fallback_item, heuristic_select
from embodied_daily.models import Candidate, Digest
from embodied_daily.render import write_digest, write_source_health
from embodied_daily.screenshots import capture_digest_screenshots, write_fallback_svg
from embodied_daily.site import build_site
from embodied_daily.specials import append_special_items
from embodied_daily.state import SeenState

LOGGER = logging.getLogger(__name__)


def _require_fixed_composition(
    candidates: list[Candidate],
    research_required: int = 10,
    news_required: int = 5,
) -> None:
    research_count = sum(
        candidate.source_kind == "research" for candidate in candidates
    )
    news_count = len(candidates) - research_count
    if research_count < research_required:
        raise RuntimeError(
            f"具有可用代表图的论文候选不足{research_required}篇，无法保持论文配额。"
        )
    if news_count < news_required:
        raise RuntimeError(
            f"具有可用网页图片的普通新闻候选不足{news_required}条，无法保持新闻配额。"
        )


def replace_items_with_failed_screenshots(
    digest: Digest,
    candidates: list[Candidate],
    selector: DigestSelector,
    output_dir: str | Path,
    vision_settings: RuntimeSettings | None = None,
) -> Digest:
    """Replace only failed visual items while preserving successful captures."""
    rejected_ids: set[str] = set()
    replacement_attempts = 0
    max_replacement_attempts = 6

    def write_news_fallback(item) -> None:
        root = Path(output_dir)
        svg_path = root / "assets" / digest.date / f"{item.rank:02d}.svg"
        write_fallback_svg(
            svg_path,
            title=item.title,
            source=item.source,
            url=item.url,
        )
        item.screenshot = svg_path.relative_to(root).as_posix()
        item.screenshot_status = "fallback"

    capture_digest_screenshots(
        digest,
        output_dir,
        fallback_on_failure=False,
        vision_settings=vision_settings,
    )

    while True:
        failed_items = [
            item
            for item in digest.items
            if item.screenshot_status not in {"captured", "fallback"}
        ]
        if not failed_items:
            return digest

        selected_foreign = sum(selector.is_foreign_news(item) for item in digest.items)
        for item in list(failed_items):
            if (
                selector.is_foreign_news(item)
                and selected_foreign <= selector.foreign_news_minimum
            ):
                write_news_fallback(item)
                failed_items.remove(item)
        if not failed_items:
            return digest

        if replacement_attempts >= max_replacement_attempts:
            news_failures = [
                item for item in failed_items if item.source_kind != "research"
            ]
            research_failures = [
                item for item in failed_items if item.source_kind == "research"
            ]
            if research_failures:
                raise RuntimeError("论文候选已耗尽，仍无法获取合格的代表图。")
            for item in news_failures:
                write_news_fallback(item)
            LOGGER.warning(
                "新闻图片替换达到上限，%s 条使用统一视觉兜底图。",
                len(news_failures),
            )
            return digest

        selected_ids = {item.candidate_id for item in digest.items}
        replacements = []
        for failed in failed_items:
            rejected_ids.add(failed.candidate_id)
            is_research = failed.source_kind == "research"
            replacement_pool = [
                candidate
                for candidate in candidates
                if candidate.id not in selected_ids
                and candidate.id not in rejected_ids
                and (candidate.source_kind == "research") == is_research
            ]
            remaining_foreign = sum(
                selector.is_foreign_news(item)
                for item in digest.items
                if item.candidate_id != failed.candidate_id
            )
            if not is_research and remaining_foreign < selector.foreign_news_minimum:
                replacement_pool = [
                    candidate
                    for candidate in replacement_pool
                    if selector.is_foreign_news(candidate)
                ]
            replacement = next(iter(replacement_pool), None)
            if replacement is None:
                if is_research:
                    raise RuntimeError("没有更多论文候选可用于替换失败的代表图。")
                replacement_attempts = max_replacement_attempts
                continue
            selected_ids.remove(failed.candidate_id)
            selected_ids.add(replacement.id)
            new_item = fallback_item(replacement, failed.rank)
            digest.items[failed.rank - 1] = new_item
            replacements.append(new_item)
            replacement_attempts += 1

        if not replacements:
            continue
        LOGGER.warning(
            "有 %s 项视觉素材不合格，仅替换这些项并保留其余已完成内容。",
            len(replacements),
        )
        probe = Digest(
            title=digest.title,
            date=digest.date,
            generated_at=digest.generated_at,
            items=replacements,
            edition=digest.edition,
        )
        capture_digest_screenshots(
            probe,
            output_dir,
            fallback_on_failure=False,
            vision_settings=vision_settings,
        )


def check_sources(
    settings_path: str | Path = "config/settings.yaml",
    sources_path: str | Path = "config/sources.yaml",
    output_dir: str | Path = "output",
) -> tuple[int, int, int]:
    """Check source availability without calling the model or Feishu."""
    app_config = load_yaml(settings_path)
    sources_config = load_yaml(sources_path)
    fallback_hours = int(app_config["digest"].get("fallback_hours", 168))
    result = collect_candidates(
        sources_config,
        app_config.get("collection", {}),
        fallback_hours,
    )
    write_source_health([record.to_dict() for record in result.health], output_dir)
    timezone = ZoneInfo(app_config["digest"].get("timezone", "Asia/Shanghai"))
    now_local = datetime.now(timezone)
    filtered = prefilter(result.candidates, app_config, datetime.now(UTC))
    filtered = apply_daily_date_policy(
        filtered,
        now_local,
        research_required=int(app_config["digest"].get("research_count", 10)),
    )
    available = sum(1 for record in result.health if record.ok)
    LOGGER.info(
        "信源检查完成：%s/%s 可用，抓取 %s 条，筛选后 %s 条。",
        available,
        len(result.health),
        len(result.candidates),
        len(filtered),
    )
    return available, len(result.health), len(filtered)


def run_pipeline(
    settings_path: str | Path = "config/settings.yaml",
    sources_path: str | Path = "config/sources.yaml",
    output_dir: str | Path = "output",
    state_path: str | Path = "data/state.json",
    *,
    skip_feishu: bool = False,
    ignore_state: bool = False,
    demo: bool = False,
    skip_screenshots: bool = False,
    build_display: bool = True,
) -> Digest:
    app_config = load_yaml(settings_path)
    sources_config = load_yaml(sources_path)
    runtime = RuntimeSettings.from_env()
    digest_config = app_config["digest"]
    source_policy = app_config.get("news_source_policy", {})
    foreign_terms = tuple(
        str(term).lower()
        for term in (
            list(source_policy.get("trusted_foreign_sources", []))
            + list(source_policy.get("trusted_foreign_domains", []))
        )
    )
    timezone_name = runtime.timezone or digest_config.get("timezone", "Asia/Shanghai")
    timezone = ZoneInfo(timezone_name)
    now_local = datetime.now(timezone)
    item_count = int(digest_config.get("item_count", 15))
    research_required = int(digest_config.get("research_count", 10))
    news_required = int(digest_config.get("news_count", 5))

    if (item_count, research_required, news_required) != (15, 10, 5):
        raise ValueError("本项目产品约束为每天15条：10篇论文和5条新闻。")

    if demo:
        candidates = demo_candidates()
        items = heuristic_select(candidates, item_count)
    else:
        fallback_hours = int(digest_config.get("fallback_hours", 168))
        result = collect_candidates(
            sources_config,
            app_config.get("collection", {}),
            fallback_hours,
        )
        health_records = [record.to_dict() for record in result.health]
        write_source_health(health_records, output_dir)
        LOGGER.info(
            "信源完成：%s/%s 可用，抓取候选 %s 条。",
            sum(1 for item in result.health if item.ok),
            len(result.health),
            len(result.candidates),
        )

        candidates = prefilter(result.candidates, app_config, datetime.now(UTC))
        candidates = apply_daily_date_policy(
            candidates,
            now_local,
            research_required=research_required,
            foreign_source_terms=foreign_terms,
            foreign_news_minimum=int(digest_config.get("foreign_news_minimum", 3)),
            foreign_news_fallback_days=int(
                digest_config.get("foreign_news_fallback_days", 7)
            ),
        )
        research_candidates = [
            candidate for candidate in candidates if candidate.source_kind == "research"
        ]
        news_candidates = [
            candidate for candidate in candidates if candidate.source_kind != "research"
        ]
        if len(research_candidates) < research_required:
            raise RuntimeError(
                f"没有找到至少{research_required}篇聚焦研究方向的 arXiv 论文候选，"
                "日报不会降低论文配额。"
                "请检查 output/source-health.json 中的 arXiv Robotics 信源。"
            )
        if len(news_candidates) < news_required:
            raise RuntimeError(
                f"当天及前一天的普通新闻合计不足{news_required}条。"
                "为遵守日期规则，本次不会使用更早新闻补齐。"
            )
        state = SeenState(state_path)
        state.load()
        if not ignore_state:
            unseen = state.filter_unseen(candidates)
            if len(unseen) >= item_count:
                candidates = unseen
                selected_ids = {candidate.id for candidate in candidates}
                selected_research = sum(
                    candidate.source_kind == "research" for candidate in candidates
                )
                selected_news = sum(
                    candidate.source_kind != "research" for candidate in candidates
                )
                if selected_research < research_required:
                    candidates = [
                        candidate
                        for candidate in research_candidates
                        if candidate.id not in selected_ids
                    ] + candidates
                if selected_news < news_required:
                    candidates = [
                        candidate
                        for candidate in news_candidates
                        if candidate.id not in selected_ids
                    ] + candidates
            else:
                LOGGER.warning("未读候选不足十五条，本次允许复用时间窗口内的旧候选。")
        if len(candidates) < item_count:
            raise RuntimeError(
                f"两日内新闻与最近 arXiv 更新日论文合计只有 {len(candidates)} 条候选。"
                "为遵守日期规则，本次不会用更早的普通新闻补齐；"
                "请检查 output/source-health.json 或补充当天信源。"
            )

        LOGGER.info("送入模型的有效候选：%s 条。", len(candidates))
        selector = DigestSelector(
            runtime,
            item_count,
            research_count=research_required,
            foreign_news_minimum=int(digest_config.get("foreign_news_minimum", 3)),
            foreign_source_terms=foreign_terms,
        )
        items = selector.select(candidates)

    digest = Digest(
        title=str(digest_config.get("title", "具身智能日报")),
        date=now_local.date().isoformat(),
        generated_at=now_local,
        items=items,
    )
    if not skip_screenshots:
        if demo:
            capture_digest_screenshots(digest, output_dir)
        else:
            digest = replace_items_with_failed_screenshots(
                digest,
                candidates,
                selector,
                output_dir,
                vision_settings=runtime,
            )
    if not demo:
        try:
            article_texts = collect_article_texts(
                digest.items,
                timeout_seconds=float(
                    app_config.get("collection", {}).get("timeout_seconds", 20)
                ),
            )
            selector.expand_summaries(digest.items, article_texts)
            LOGGER.info("已使用 API 完成十五条内容的扩展摘要。")
        except Exception as exc:
            LOGGER.warning("扩展摘要失败，将保留初选摘要：%s", exc)
        special_count = append_special_items(digest)
        if special_count:
            LOGGER.info("已为 %s 追加一页日期限定的特别关注。", digest.date)
    paths = write_digest(digest, output_dir)
    LOGGER.info("已生成日报：%s", ", ".join(str(path) for path in paths))
    if build_display:
        display_path = build_site(output_dir=output_dir)
        LOGGER.info("已构建大屏页面：%s", display_path)

    if not skip_feishu and runtime.feishu_webhook:
        send_to_feishu(runtime.feishu_webhook, digest, runtime.feishu_secret)
        LOGGER.info("飞书推送成功。")
    elif not skip_feishu:
        LOGGER.info("未配置 FEISHU_WEBHOOK，仅生成本地日报。")

    if not demo:
        state.mark_seen(candidates)
        state.prune()
        state.save()
    return digest

