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
        "多模态世界模型预测机器人动作结果",
        "视觉语言导航系统完成陌生环境评测",
        "机械臂学习透明物体抓取策略",
        "无人机在复杂气流中实现自主规划",
        "双臂机器人完成长程装配任务",
        "触觉反馈提升灵巧手操作稳定性",
        "移动机器人学习开放场景语义地图",
        "人形机器人全身控制方法公开",
        "仿真平台加入可变形物体操作基准",
        "遥操作数据支持跨机器人策略迁移",
        "机器人奖励模型改进在线决策",
        "飞行机械臂执行空中接触任务",
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
        for index in range(1, 19)
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
        for index, candidate in enumerate(candidates[:15], start=1)
    ]
    return Digest(
        title="具身智能日报",
        date="2026-10-03",
        generated_at=generated,
        items=items,
    )

