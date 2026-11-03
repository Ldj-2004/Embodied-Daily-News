from __future__ import annotations

import hashlib
import html
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime, timedelta
from time import struct_time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import httpx

from embodied_daily.models import Candidate, CollectionResult, SourceHealth

LOGGER = logging.getLogger(__name__)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "gclid",
    "fbclid",
}


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(TAG_RE.sub(" ", value))
    return SPACE_RE.sub(" ", value).strip()


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = urlencode(
        [
            (key, value)
            for key, value in parse_qsl(parts.query)
            if key.lower() not in TRACKING_PARAMS
        ]
    )
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ""))


def parse_entry_datetime(entry: dict, fallback: datetime) -> datetime:
    parsed: struct_time | None = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        try:
            return datetime(
                parsed.tm_year,
                parsed.tm_mon,
                parsed.tm_mday,
                parsed.tm_hour,
                parsed.tm_min,
                parsed.tm_sec,
                tzinfo=UTC,
            )
        except (TypeError, ValueError):
            return fallback
    return fallback


def build_google_news_url(item: dict) -> str:
    params = {
        "q": item["query"],
        "hl": item.get("language", "zh-CN"),
        "gl": item.get("country", "CN"),
        "ceid": item.get("ceid", "CN:zh-Hans"),
    }
    return f"https://news.google.com/rss/search?{urlencode(params)}"


def candidate_id(url: str, title: str) -> str:
    payload = f"{canonicalize_url(url)}\n{clean_text(title).lower()}".encode()
    return hashlib.sha1(payload).hexdigest()[:16]


def parse_gdelt_datetime(value: str, fallback: datetime) -> datetime:
    try:
        return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)
    except (TypeError, ValueError):
        return fallback


def _fetch_gdelt(
    source: dict,
    collection_config: dict,
    cutoff: datetime,
) -> CollectionResult:
    now = datetime.now(UTC)
    endpoint = "https://api.gdeltproject.org/api/v2/doc/doc"
    health = SourceHealth(
        name=source["name"],
        url=endpoint,
        ok=False,
        checked_at=now,
    )
    try:
        timeout = float(collection_config.get("timeout_seconds", 20))
        headers = {"User-Agent": collection_config.get("user_agent", "EmbodiedDailyNews/0.1")}
        params = {
            "query": source["query"],
            "mode": "ArtList",
            "format": "json",
            "sort": "DateDesc",
            "timespan": source.get("timespan", "3d"),
            "maxrecords": int(source.get("max_results", 75)),
        }
        with httpx.Client(timeout=timeout, follow_redirects=True, headers=headers) as client:
            response = client.get(endpoint, params=params)
            response.raise_for_status()
            payload = response.json()

        candidates: list[Candidate] = []
        for article in payload.get("articles", []):
            title = clean_text(article.get("title"))
            link = (article.get("url") or "").strip()
            if not title or not link:
                continue
            published_at = parse_gdelt_datetime(article.get("seendate", ""), now)
            if published_at < cutoff:
                continue
            source_name = clean_text(article.get("domain")) or source["name"]
            candidates.append(
                Candidate(
                    id=candidate_id(link, title),
                    title=title,
                    url=canonicalize_url(link),
                    source=source_name,
                    source_kind="search",
                    published_at=published_at,
                    fetched_at=now,
                    summary=title,
                    source_weight=int(source.get("weight", 2)),
                )
            )
        health.ok = True
        health.item_count = len(candidates)
        return CollectionResult(candidates=candidates, health=[health])
    except Exception as exc:
        health.error = f"{type(exc).__name__}: {exc}"[:500]
        LOGGER.warning("信源抓取失败：%s (%s)", source["name"], health.error)
        return CollectionResult(health=[health])


def _fetch_one(source: dict, collection_config: dict, cutoff: datetime) -> CollectionResult:
    now = datetime.now(UTC)
    url = source["url"]
    health = SourceHealth(name=source["name"], url=url, ok=False, checked_at=now)
    try:
        timeout = float(collection_config.get("timeout_seconds", 20))
        headers = {"User-Agent": collection_config.get("user_agent", "EmbodiedDailyNews/0.1")}
        with httpx.Client(timeout=timeout, follow_redirects=True, headers=headers) as client:
            response = client.get(url)
            response.raise_for_status()
        parsed = feedparser.parse(response.content)
        if getattr(parsed, "bozo", False) and not parsed.entries:
            raise ValueError(str(getattr(parsed, "bozo_exception", "无法解析 Feed")))

        candidates: list[Candidate] = []
        for entry in parsed.entries:
            title = clean_text(entry.get("title"))
            link = (entry.get("link") or "").strip()
            if not title or not link:
                continue
            published_at = parse_entry_datetime(entry, now)
            # Research feeds are intentionally exempt from the general lookback.
            # arXiv has no Friday/Saturday announcement and can defer mailings on
            # holidays, so the newest available paper may be older than the news
            # window. The daily-date policy later keeps only its latest update day.
            if published_at < cutoff and source.get("kind") != "research":
                continue
            contents = entry.get("content") or []
            content_value = ""
            if contents and isinstance(contents[0], dict):
                content_value = contents[0].get("value", "")
            summary = clean_text(
                entry.get("summary")
                or entry.get("description")
                or content_value
            )
            source_name = source["name"]
            entry_source = entry.get("source")
            if source.get("kind") == "search" and isinstance(entry_source, dict):
                source_name = clean_text(entry_source.get("title")) or source_name
            candidates.append(
                Candidate(
                    id=candidate_id(link, title),
                    title=title,
                    url=canonicalize_url(link),
                    source=source_name,
                    source_kind=source.get("kind", "media"),
                    published_at=published_at,
                    fetched_at=now,
                    summary=summary[:2000],
                    source_weight=int(source.get("weight", 1)),
                )
            )
        health.ok = True
        health.item_count = len(candidates)
        return CollectionResult(candidates=candidates, health=[health])
    except Exception as exc:  # one broken source must not stop the full digest
        health.error = f"{type(exc).__name__}: {exc}"[:500]
        LOGGER.warning("信源抓取失败：%s (%s)", source["name"], health.error)
        return CollectionResult(health=[health])


def collect_candidates(
    sources_config: dict,
    collection_config: dict,
    fallback_hours: int,
) -> CollectionResult:
    sources = [dict(item) for item in sources_config.get("direct_feeds", [])]
    for item in sources_config.get("google_news_queries", []):
        source = dict(item)
        source["url"] = build_google_news_url(source)
        source["kind"] = "search"
        sources.append(source)
    for item in sources_config.get("gdelt_queries", []):
        source = dict(item)
        source["url"] = "https://api.gdeltproject.org/api/v2/doc/doc"
        source["kind"] = "search"
        source["collector"] = "gdelt"
        sources.append(source)
    cutoff = datetime.now(UTC) - timedelta(hours=fallback_hours)
    aggregate = CollectionResult()
    workers = max(1, int(collection_config.get("max_workers", 8)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}
        for source in sources:
            fetcher = _fetch_gdelt if source.get("collector") == "gdelt" else _fetch_one
            futures[executor.submit(fetcher, source, collection_config, cutoff)] = source
        for future in as_completed(futures):
            result = future.result()
            aggregate.candidates.extend(result.candidates)
            aggregate.health.extend(result.health)
    return aggregate
