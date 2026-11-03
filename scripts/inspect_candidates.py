from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from embodied_daily.config import load_yaml
from embodied_daily.feeds import collect_candidates
from embodied_daily.filtering import apply_daily_date_policy, prefilter


def main() -> None:
    app_config = load_yaml("config/settings.yaml")
    sources_config = load_yaml("config/sources.yaml")
    result = collect_candidates(
        sources_config,
        app_config.get("collection", {}),
        int(app_config["digest"].get("fallback_hours", 168)),
    )
    candidates = prefilter(result.candidates, app_config, datetime.now(UTC))
    timezone = ZoneInfo(app_config["digest"].get("timezone", "Asia/Shanghai"))
    candidates = apply_daily_date_policy(candidates, datetime.now(timezone))
    for candidate in candidates:
        local_time = candidate.published_at.astimezone(timezone)
        print(
            f"[{candidate.source_kind}] {local_time:%Y-%m-%d %H:%M} | "
            f"{candidate.source} | {candidate.title}"
        )


if __name__ == "__main__":
    main()
