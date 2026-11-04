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


def test_product_progress_ranks_above_policy_event_news(candidates) -> None:
    product = candidates[0]
    product.source_kind = "media"
    product.title = "机器人企业发布新模型并完成工厂量产部署"
    product.summary = "产品已经交付客户，并公布性能提升结果。"

    policy = candidates[1]
    policy.source_kind = "media"
    policy.title = "机器人产业政策论坛暨实景实训挑战赛举行"
    policy.summary = "有关方面介绍产业规划、投资规模和政策支持。"

    config = {
        "keywords": {
            "high": ["机器人"],
            "medium": [],
            "entities": [],
        },
        "ranking_preferences": {
            "product_progress": ["发布", "模型", "量产", "部署", "交付", "性能提升"],
            "policy_macro": ["政策", "规划", "投资规模"],
            "events": ["论坛", "挑战赛"],
            "finance": [],
        },
        "negative_keywords": [],
    }

    product_score = keyword_score(product, config)
    policy_score = keyword_score(policy, config)

    assert product_score > policy_score
    assert policy_score > -100


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

def test_prominent_company_bonus_applies_only_to_ordinary_news(candidates) -> None:
    prominent_news = candidates[0]
    prominent_news.source_kind = "media"
    prominent_news.source_weight = 1
    prominent_news.title = "宇树科技发布具身智能机器人教育解决方案"
    prominent_news.summary = "机器人产品已经完成部署。"

    small_news = candidates[1]
    small_news.source_kind = "media"
    small_news.source_weight = 1
    small_news.title = "某小型企业发布具身智能机器人教育解决方案"
    small_news.summary = "机器人产品已经完成部署。"

    prominent_paper = candidates[2]
    prominent_paper.source_kind = "research"
    prominent_paper.source_weight = 1
    prominent_paper.title = "宇树科技具身智能机器人研究"
    prominent_paper.summary = "论文介绍机器人学习方法。"

    other_paper = candidates[3]
    other_paper.source_kind = "research"
    other_paper.source_weight = 1
    other_paper.title = "具身智能机器人研究"
    other_paper.summary = "论文介绍机器人学习方法。"

    config = {
        "keywords": {
            "high": ["具身智能"],
            "medium": ["机器人"],
            "entities": [],
        },
        "ranking_preferences": {
            "prominent_company_bonus": 6,
            "prominent_company_bonus_cap": 12,
            "prominent_companies": {
                "unitree": ["宇树科技", "宇树", "unitree"],
            },
            "product_progress": [],
            "policy_macro": [],
            "events": [],
            "finance": [],
        },
        "negative_keywords": [],
    }

    news_bonus = keyword_score(prominent_news, config) - keyword_score(
        small_news, config
    )
    paper_difference = keyword_score(prominent_paper, config) - keyword_score(
        other_paper, config
    )

    assert news_bonus == 6
    assert paper_difference == 0

