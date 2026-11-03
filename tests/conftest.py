from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from embodied_daily.models import Candidate, Digest, DigestItem


@pytest.fixture
def candidates() -> list[Candidate]:
    now = datetime.now(UTC)
    titles = [
        "具身智能基础模型发布",
        "人形机器人进入工厂部署",
        "VLA方法提升长程操作能力",
        "灵巧手训练数据集正式开源",
        "仿真到现实迁移出现新进展",
        "机器人企业完成新一轮融资",
    ]
    return [
        Candidate(
            id=f"item-{index}",
            title=titles[index - 1],
            url=f"https://example.com/news/{index}?utm_source=test",
            source=f"信源 {index}",
            source_kind="primary" if index % 2 else "media",
            published_at=now - timedelta(hours=index),
            fetched_at=now,
            summary=f"这是第 {index} 条机器人新闻的事实摘要。",
            source_weight=3,
            relevance_score=8 - index,
        )
        for index in range(1, 7)
    ]


@pytest.fixture
def digest(candidates: list[Candidate]) -> Digest:
    generated = datetime(2026, 10, 3, 7, 30, tzinfo=UTC)
    items = [
        DigestItem(
            rank=index,
            candidate_id=candidate.id,
            title=candidate.title,
            summary=candidate.summary,
            why_it_matters="有助于理解具身智能的最新进展。",
            url=candidate.url,
            source=candidate.source,
            source_kind=candidate.source_kind,
            published_at=candidate.published_at,
            importance_score=9 - index,
        )
        for index, candidate in enumerate(candidates[:5], start=1)
    ]
    return Digest(
        title="具身智能日报",
        date="2026-10-03",
        generated_at=generated,
        items=items,
    )
