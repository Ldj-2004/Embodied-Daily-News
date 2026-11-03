from __future__ import annotations

import re
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from difflib import SequenceMatcher

from embodied_daily.feeds import canonicalize_url
from embodied_daily.models import Candidate

NON_WORD_RE = re.compile(r"[^\w\u4e00-\u9fff]+", re.UNICODE)


def normalize_title(title: str) -> str:
    return NON_WORD_RE.sub("", title.lower())


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
) -> list[Candidate]:
    """Keep today/yesterday news and papers from the latest arXiv update day.

    Non-research items may match the digest date or the previous local date.
    Research items prefer that same date; when arXiv has no update that day, all
    eligible papers from the most recent research date are retained instead.
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
    papers = [
        candidate
        for candidate in candidates
        if candidate.source_kind == "research"
        and _date_in_timezone(candidate, timezone) <= target_date
    ]
    if papers:
        paper_dates = {
            candidate.id: _date_in_timezone(candidate, timezone)
            for candidate in papers
        }
        latest_paper_date = max(paper_dates.values())
        selected_papers = [
            candidate
            for candidate in papers
            if paper_dates[candidate.id] == latest_paper_date
        ]
    else:
        selected_papers = []

    eligible = news + selected_papers
    eligible.sort(
        key=lambda item: (item.relevance_score, item.source_weight, item.published_at),
        reverse=True,
    )
    return eligible


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
    pool = recent if len(recent) >= int(digest_config.get("item_count", 5)) else scored
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
    newest_research = sorted(
        research_candidates,
        key=lambda item: item.published_at,
        reverse=True,
    )[:2]
    balanced_ids = {candidate.id for candidate in balanced}
    for research_candidate in newest_research:
        if research_candidate.id not in balanced_ids:
            # Preserve two papers even when a full pool of recent ordinary news
            # would otherwise push them out on weekends or holidays.
            balanced.append(research_candidate)
            balanced_ids.add(research_candidate.id)
    return balanced
