from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from embodied_daily.config import RuntimeSettings, load_yaml
from embodied_daily.demo import demo_candidates
from embodied_daily.feeds import collect_candidates
from embodied_daily.feishu import send_to_feishu
from embodied_daily.filtering import apply_daily_date_policy, prefilter
from embodied_daily.llm import DigestSelector, heuristic_select
from embodied_daily.models import Digest
from embodied_daily.render import write_digest, write_source_health
from embodied_daily.screenshots import capture_digest_screenshots
from embodied_daily.site import build_site
from embodied_daily.state import SeenState

LOGGER = logging.getLogger(__name__)


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
    filtered = apply_daily_date_policy(filtered, now_local)
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
    timezone_name = runtime.timezone or digest_config.get("timezone", "Asia/Shanghai")
    timezone = ZoneInfo(timezone_name)
    now_local = datetime.now(timezone)
    item_count = int(digest_config.get("item_count", 5))

    if item_count != 5:
        raise ValueError("本项目当前产品约束为每天恰好五条，请保持 digest.item_count=5。")

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
        candidates = apply_daily_date_policy(candidates, now_local)
        research_candidates = [
            candidate for candidate in candidates if candidate.source_kind == "research"
        ]
        news_candidates = [
            candidate for candidate in candidates if candidate.source_kind != "research"
        ]
        if len(research_candidates) < 2:
            raise RuntimeError(
                "没有找到至少两篇可用的 arXiv 论文候选，日报不会降低论文配额。"
                "请检查 output/source-health.json 中的 arXiv Robotics 信源。"
            )
        if len(news_candidates) < 3:
            raise RuntimeError(
                "当天及前一天的普通新闻合计不足三条。"
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
                if selected_research < 2:
                    candidates = [
                        candidate
                        for candidate in research_candidates
                        if candidate.id not in selected_ids
                    ] + candidates
                if selected_news < 3:
                    candidates = [
                        candidate
                        for candidate in news_candidates
                        if candidate.id not in selected_ids
                    ] + candidates
            else:
                LOGGER.warning("未读候选不足五条，本次允许复用时间窗口内的旧候选。")
        if len(candidates) < item_count:
            raise RuntimeError(
                f"两日内新闻与最近 arXiv 更新日论文合计只有 {len(candidates)} 条候选。"
                "为遵守日期规则，本次不会用更早的普通新闻补齐；"
                "请检查 output/source-health.json 或补充当天信源。"
            )

        LOGGER.info("送入模型的有效候选：%s 条。", len(candidates))
        selector = DigestSelector(runtime, item_count)
        items = selector.select(candidates)

    digest = Digest(
        title=str(digest_config.get("title", "具身智能日报")),
        date=now_local.date().isoformat(),
        generated_at=now_local,
        items=items,
    )
    if not skip_screenshots:
        capture_digest_screenshots(digest, output_dir)
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
