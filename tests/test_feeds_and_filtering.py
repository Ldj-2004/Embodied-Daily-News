from datetime import UTC, datetime, timedelta
from time import struct_time
from zoneinfo import ZoneInfo

from embodied_daily.feeds import (
    canonicalize_url,
    parse_entry_datetime,
    parse_gdelt_datetime,
)
from embodied_daily.filtering import (
    apply_daily_date_policy,
    deduplicate,
    keyword_score,
    prefilter,
)


def test_canonicalize_url_removes_tracking() -> None:
    result = canonicalize_url(
        "HTTPS://Example.COM/article/?utm_source=test&id=7&utm_campaign=daily#part"
    )
    assert result == "https://example.com/article?id=7"


def test_deduplicate_similar_titles(candidates) -> None:
    duplicate = candidates[0]
    duplicate.id = "duplicate"
    duplicate.url = "https://another.example.com/same-story"
    duplicate.title = candidates[1].title
    result = deduplicate(candidates)
    assert len(result) == 5


def test_keyword_score_rewards_embodied_terms(candidates) -> None:
    config = {
        "keywords": {
            "high": ["具身智能"],
            "medium": ["机器人"],
            "entities": [],
        },
        "negative_keywords": [],
    }
    assert keyword_score(candidates[0], config) >= 10


def test_ancient_feed_date_does_not_use_platform_timestamp() -> None:
    ancient = struct_time((1, 1, 1, 0, 0, 0, 0, 1, 0))
    fallback = datetime.now(UTC)
    result = parse_entry_datetime({"published_parsed": ancient}, fallback)
    assert result.year == 1


def test_parse_gdelt_datetime() -> None:
    fallback = datetime.now(UTC)
    result = parse_gdelt_datetime("20261103T091500Z", fallback)
    assert result == datetime(2026, 11, 3, 9, 15, tzinfo=UTC)


def test_daily_policy_keeps_two_day_news_and_latest_paper_date(candidates) -> None:
    timezone = ZoneInfo("Asia/Shanghai")
    now = datetime(2026, 11, 7, 9, 30, tzinfo=timezone)
    today_news = candidates[0]
    today_news.published_at = now.astimezone(UTC) - timedelta(hours=1)

    yesterday_news = candidates[1]
    yesterday_news.published_at = now.astimezone(UTC) - timedelta(days=1)

    old_news = candidates[4]
    old_news.published_at = now.astimezone(UTC) - timedelta(days=2)

    latest_paper = candidates[2]
    latest_paper.source_kind = "research"
    latest_paper.published_at = now.astimezone(UTC) - timedelta(days=1)

    older_paper = candidates[3]
    older_paper.source_kind = "research"
    older_paper.published_at = now.astimezone(UTC) - timedelta(days=4)

    result = apply_daily_date_policy(candidates[:5], now)

    assert today_news in result
    assert yesterday_news in result
    assert old_news not in result
    assert latest_paper in result
    assert older_paper not in result


def test_prefilter_preserves_old_research_when_recent_news_pool_is_full(
    candidates,
) -> None:
    now = datetime.now(UTC)
    for candidate in candidates[:5]:
        candidate.published_at = now - timedelta(hours=1)
    paper = candidates[5]
    paper.source_kind = "research"
    paper.published_at = now - timedelta(days=3)
    config = {
        "digest": {
            "recent_hours": 36,
            "item_count": 5,
            "minimum_keyword_score": 0,
            "max_candidates_for_ai": 5,
            "max_candidates_per_source": 20,
        },
        "keywords": {"high": [], "medium": [], "entities": []},
        "negative_keywords": [],
    }

    result = prefilter(candidates, config, now)

    assert paper in result
