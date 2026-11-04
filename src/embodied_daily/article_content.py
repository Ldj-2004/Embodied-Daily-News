from __future__ import annotations

import html
import logging
import re

import httpx

from embodied_daily.models import DigestItem

LOGGER = logging.getLogger(__name__)

BLOCK_RE = re.compile(
    r"<(script|style|noscript|svg|nav|footer|header)\b[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)
ARTICLE_RE = re.compile(r"<(article|main)\b[^>]*>(.*?)</\1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def extract_article_text(document: str, limit: int = 6_000) -> str:
    """Extract readable article text without adding a heavy parsing dependency."""
    cleaned = BLOCK_RE.sub(" ", document)
    matches = [match.group(2) for match in ARTICLE_RE.finditer(cleaned)]
    if matches:
        cleaned = max(matches, key=len)
    cleaned = html.unescape(TAG_RE.sub(" ", cleaned))
    return SPACE_RE.sub(" ", cleaned).strip()[:limit]


def collect_article_texts(
    items: list[DigestItem],
    *,
    timeout_seconds: float = 20,
) -> dict[str, str]:
    """Fetch final ordinary-news pages for the second-pass API summary."""
    output: dict[str, str] = {}
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        )
    }
    with httpx.Client(
        timeout=timeout_seconds,
        follow_redirects=True,
        headers=headers,
    ) as client:
        for item in items:
            if item.source_kind == "research":
                continue
            try:
                response = client.get(item.url)
                response.raise_for_status()
                if "html" not in response.headers.get("content-type", "").lower():
                    continue
                text = extract_article_text(response.text)
                if len(text) >= 200:
                    output[item.candidate_id] = text
            except Exception as exc:
                LOGGER.warning("无法读取新闻正文，将沿用候选摘要：%s (%s)", item.url, exc)
    return output
