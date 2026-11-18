from __future__ import annotations

from datetime import UTC, datetime, timedelta

from embodied_daily.models import Candidate


def demo_candidates() -> list[Candidate]:
    now = datetime.now(UTC)
    paper_topics = ["VLA", "世界模型", "VLN", "机械臂操作", "灵巧操作", "模仿学习", "遥操作", "长程任务", "无人机", "飞行机器人"]
    news_topics = ["基础模型发布", "工厂部署", "训练代码开源", "量产交付", "海外企业产品升级"]
    rows = [
        (f"{topic}研究取得新进展", f"研究团队公开{topic}方法、实验与评测结果。", "research")
        for topic in paper_topics
    ] + [
        (f"机器人{topic}", f"企业披露机器人{topic}的具体进展与应用场景。", "primary")
        for topic in news_topics
    ]
    output: list[Candidate] = []
    for index, (title, summary, source_kind) in enumerate(rows, start=1):
        output.append(
            Candidate(
                id=f"demo-{index}",
                title=title,
                url=f"https://example.com/demo-{index}",
                source="演示信源",
                source_kind=source_kind,
                published_at=now - timedelta(hours=index),
                fetched_at=now,
                summary=summary,
                source_weight=2,
                relevance_score=8 - index,
            )
        )
    return output


