from __future__ import annotations

import re
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from difflib import SequenceMatcher
from urllib.parse import urlparse

from embodied_daily.feeds import canonicalize_url
from embodied_daily.models import Candidate

NON_WORD_RE = re.compile(r"[^\w\u4e00-\u9fff]+", re.UNICODE)


def normalize_title(title: str) -> str:
    return NON_WORD_RE.sub("", title.lower())


def _contains_named_entity(text: str, alias: str) -> bool:
    """Match Chinese aliases by substring and Latin aliases by word boundary."""
    term = str(alias).strip().lower()
    if not term:
        return False
    if re.fullmatch(r"[a-z0-9][a-z0-9 .&+_-]*", term):
        return bool(
            re.search(
                rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])",
                text,
            )
        )
    return term in text


def prominent_company_score(text: str, ranking: dict) -> int:
    """Reward distinct prominent companies without counting aliases twice."""
    groups = ranking.get("prominent_companies", {})
    if not isinstance(groups, dict):
        return 0
    hits = sum(
        1
        for aliases in groups.values()
        if isinstance(aliases, list)
        and any(_contains_named_entity(text, alias) for alias in aliases)
    )
    per_company = int(ranking.get("prominent_company_bonus", 6))
    cap = int(ranking.get("prominent_company_bonus_cap", 12))
    return min(cap, hits * per_company)


def matches_foreign_source(candidate: Candidate, terms: tuple[str, ...]) -> bool:
    source = candidate.source.lower()
    host = (urlparse(candidate.url).hostname or "").lower()
    return any(
        term in source or host == term or host.endswith(f".{term}")
        for term in terms
    )


def keyword_score(candidate: Candidate, config: dict) -> int:
    text = f"{candidate.title} {candidate.summary}".lower()
    if any(term.lower() in text for term in config.get("negative_keywords", [])):
        return -100

    keywords = config.get("keywords", {})
    score = candidate.source_weight
    score += sum(5 for term in keywords.get("high", []) if term.lower() in text)
    score += sum(2 for term in keywords.get("medium", []) if term.lower() in text)
    score += sum(2 for term in keywords.get("entities", []) if term.lower() in text)
    if candidate.source_kind in {"primary", "research"}:
        score += 2
    if candidate.source_kind == "research":
        focus = config.get("research_focus", {})
        tracks = focus.get("tracks", {})
        track_hits = sum(
            any(str(term).lower() in text for term in terms)
            for terms in tracks.values()
            if isinstance(terms, list)
        )
        minimum_hits = int(focus.get("minimum_track_hits", 1))
        if tracks and track_hits < minimum_hits:
            return -100
        score += track_hits * 5
    if candidate.source_kind != "research":
        ranking = config.get("ranking_preferences", {})

        def adjustment(group: str, per_hit: int, cap: int) -> int:
            hits = sum(
                1
                for term in ranking.get(group, [])
                if term.lower() in text
            )
            return min(cap, hits * per_hit)

        score += adjustment("product_progress", per_hit=2, cap=8)
        score += prominent_company_score(text, ranking)
        score -= adjustment("policy_macro", per_hit=3, cap=9)
        score -= adjustment("events", per_hit=4, cap=8)
        score -= adjustment("finance", per_hit=2, cap=6)
    candidate.relevance_score = score
    return score


def deduplicate(candidates: list[Candidate]) -> list[Candidate]:
    ordered = sorted(
        candidates,
        key=lambda item: (item.source_weight, item.published_at),
        reverse=True,
    )
    kept: list[Candidate] = []
    seen_urls: set[str] = set()
    normalized_titles: list[str] = []
    for candidate in ordered:
        url = canonicalize_url(candidate.url)
        if url in seen_urls:
            continue
        normalized = normalize_title(candidate.title)
        if normalized and any(
            SequenceMatcher(None, normalized, prior).ratio() >= 0.88
            for prior in normalized_titles
        ):
            continue
        seen_urls.add(url)
        normalized_titles.append(normalized)
        kept.append(candidate)
    return kept


def _date_in_timezone(candidate: Candidate, timezone) -> date:
    published_at = candidate.published_at
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=UTC)
    return published_at.astimezone(timezone).date()


def apply_daily_date_policy(
    candidates: list[Candidate],
    now: datetime,
    research_required: int = 10,
    foreign_source_terms: tuple[str, ...] = (),
    foreign_news_minimum: int = 3,
    foreign_news_fallback_days: int = 7,
) -> list[Candidate]:
    """Keep today/yesterday news and enough papers from recent arXiv update days.

    Non-research items may match the digest date or the previous local date.
    Research items start with the newest update day and expand backward by whole
    update days only when the newest day cannot satisfy the configured quota.
    """
    if now.tzinfo is None:
        raise ValueError("now 必须包含时区，才能判断日报的当天日期。")

    target_date = now.date()
    earliest_news_date = target_date - timedelta(days=1)
    timezone = now.tzinfo
    news = [
        candidate
        for candidate in candidates
        if candidate.source_kind != "research"
        and earliest_news_date
        <= _date_in_timezone(candidate, timezone)
        <= target_date
    ]
    if foreign_source_terms:
        foreign_count = sum(
            matches_foreign_source(candidate, foreign_source_terms)
            for candidate in news
        )
        earliest_foreign_date = target_date - timedelta(
            days=max(1, foreign_news_fallback_days - 1)
        )
        older_foreign = sorted(
            (
                candidate
                for candidate in candidates
                if candidate.source_kind != "research"
                and candidate not in news
                and earliest_foreign_date
                <= _date_in_timezone(candidate, timezone)
                <= target_date
                and matches_foreign_source(candidate, foreign_source_terms)
            ),
            key=lambda item: item.published_at,
            reverse=True,
        )
        news.extend(
            older_foreign[: max(0, foreign_news_minimum - foreign_count)]
        )
    papers = [
        candidate
        for candidate in candidates
        if candidate.source_kind == "research"
        and _date_in_timezone(candidate, timezone) <= target_date
    ]
    paper_dates = {
        candidate.id: _date_in_timezone(candidate, timezone)
        for candidate in papers
    }
    selected_papers: list[Candidate] = []
    for paper_date in sorted(set(paper_dates.values()), reverse=True):
        selected_papers.extend(
            candidate
            for candidate in papers
            if paper_dates[candidate.id] == paper_date
        )
        if len(selected_papers) >= research_required:
            break

    eligible = news + selected_papers
    eligible.sort(
        key=lambda item: (item.relevance_score, item.source_weight, item.published_at),
        reverse=True,
    )
    return eligible


def extend_with_research_fallbacks(
    primary_candidates: list[Candidate],
    available_candidates: list[Candidate],
    now: datetime,
    fallback_days: int = 7,
) -> list[Candidate]:
    """Add recent papers for screenshot replacement without widening AI input."""
    if now.tzinfo is None:
        raise ValueError("now 必须包含时区，才能判断论文补救时间窗。")

    earliest_date = now.date() - timedelta(days=max(1, fallback_days) - 1)
    result = list(primary_candidates)
    result_ids = {candidate.id for candidate in result}
    recent_papers = sorted(
        (
            candidate
            for candidate in available_candidates
            if candidate.source_kind == "research"
            and candidate.id not in result_ids
            and earliest_date
            <= _date_in_timezone(candidate, now.tzinfo)
            <= now.date()
        ),
        key=lambda item: item.published_at,
        reverse=True,
    )
    result.extend(recent_papers)
    return result


def prefilter(
    candidates: list[Candidate],
    app_config: dict,
    now: datetime,
) -> list[Candidate]:
    digest_config = app_config["digest"]
    recent_hours = int(digest_config.get("recent_hours", 36))
    threshold = int(digest_config.get("minimum_keyword_score", 2))
    max_candidates = int(digest_config.get("max_candidates_for_ai", 80))
    per_source_limit = int(digest_config.get("max_candidates_per_source", 20))

    scored = [
        candidate
        for candidate in candidates
        if keyword_score(candidate, app_config) >= threshold
    ]
    scored = deduplicate(scored)
    recent = [
        candidate
        for candidate in scored
        if (now - candidate.published_at).total_seconds() <= recent_hours * 3600
    ]
    pool = recent if len(recent) >= int(digest_config.get("item_count", 15)) else scored
    pool.sort(
        key=lambda item: (item.relevance_score, item.source_weight, item.published_at),
        reverse=True,
    )
    balanced: list[Candidate] = []
    counts: defaultdict[str, int] = defaultdict(int)
    for candidate in pool:
        if counts[candidate.source] >= per_source_limit:
            continue
        counts[candidate.source] += 1
        balanced.append(candidate)
        if len(balanced) >= max_candidates:
            break
    research_candidates = [
        candidate for candidate in scored if candidate.source_kind == "research"
    ]
    required_research = int(digest_config.get("research_count", 10))
    research_fallback_days = int(digest_config.get("research_fallback_days", 7))
    research_cutoff = now - timedelta(days=max(1, research_fallback_days))
    newest_research = sorted(
        research_candidates,
        key=lambda item: item.published_at,
        reverse=True,
    )
    preserved_research = newest_research[:required_research]
    preserved_research.extend(
        candidate
        for candidate in newest_research[required_research:]
        if candidate.published_at >= research_cutoff
    )
    balanced_ids = {candidate.id for candidate in balanced}
    for research_candidate in preserved_research:
        if research_candidate.id not in balanced_ids:
            # Preserve the paper quota even when a full pool of recent ordinary news
            # would otherwise push them out on weekends or holidays.
            balanced.append(research_candidate)
            balanced_ids.add(research_candidate.id)

    source_policy = app_config.get("news_source_policy", {})
    foreign_terms = tuple(
        str(term).lower()
        for term in (
            list(source_policy.get("trusted_foreign_sources", []))
            + list(source_policy.get("trusted_foreign_domains", []))
        )
    )
    foreign_minimum = int(digest_config.get("foreign_news_minimum", 3))
    selected_foreign = sum(
        candidate.source_kind != "research"
        and matches_foreign_source(candidate, foreign_terms)
        for candidate in balanced
    )
    foreign_candidates = sorted(
        (
            candidate
            for candidate in scored
            if candidate.source_kind != "research"
            and candidate.id not in balanced_ids
            and matches_foreign_source(candidate, foreign_terms)
        ),
        key=lambda item: (item.published_at, item.relevance_score),
        reverse=True,
    )
    for foreign_candidate in foreign_candidates[: max(0, foreign_minimum - selected_foreign)]:
        balanced.append(foreign_candidate)
        balanced_ids.add(foreign_candidate.id)
    return balanced

