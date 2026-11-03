from __future__ import annotations

from datetime import UTC, datetime, timedelta

from embodied_daily.models import Candidate


def demo_candidates() -> list[Candidate]:
    now = datetime.now(UTC)
    rows = [
        ("机器人基础模型发布演示版", "实验室发布机器人基础模型，并展示多任务操作能力。"),
        ("人形机器人进入汽车工厂试点", "企业披露人形机器人在真实产线中的阶段性部署。"),
        ("新型VLA方法提升长程操作表现", "研究团队公开新的视觉语言动作方法及评测结果。"),
        ("灵巧手数据集与训练代码开源", "项目开放灵巧操作数据集、模型权重和训练流程。"),
        ("机器人仿真到现实迁移取得进展", "新方法减少真实机器人训练所需的人工数据。"),
        ("具身智能企业完成新一轮融资", "资金计划投入机器人量产和数据采集体系。"),
    ]
    output: list[Candidate] = []
    for index, (title, summary) in enumerate(rows, start=1):
        output.append(
            Candidate(
                id=f"demo-{index}",
                title=title,
                url=f"https://example.com/demo-{index}",
                source="演示信源",
                source_kind="demo",
                published_at=now - timedelta(hours=index),
                fetched_at=now,
                summary=summary,
                source_weight=2,
                relevance_score=8 - index,
            )
        )
    return output

