from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from embodied_daily.config import RuntimeSettings
from embodied_daily.feeds import candidate_id
from embodied_daily.llm import DigestSelector
from embodied_daily.models import Candidate, Digest
from embodied_daily.render import write_digest
from embodied_daily.screenshots import capture_digest_screenshots
from embodied_daily.site import build_site

TIMEZONE = ZoneInfo("Asia/Shanghai")


def candidate(
    title: str,
    url: str,
    source: str,
    source_kind: str,
    published_at: datetime,
    summary: str,
    score: int,
) -> Candidate:
    return Candidate(
        id=candidate_id(url, title),
        title=title,
        url=url,
        source=source,
        source_kind=source_kind,
        published_at=published_at,
        fetched_at=datetime.now(TIMEZONE),
        summary=summary,
        source_weight=4 if source_kind in {"primary", "research"} else 3,
        relevance_score=score,
    )


def main() -> None:
    candidates = [
        candidate(
            "Pixel: A Co-Designed Full-Stack Robot System for Learning "
            "General-Purpose Mobile Manipulation",
            "https://arxiv.org/abs/2611.03648v1",
            "arXiv Robotics",
            "research",
            datetime(2026, 11, 3, 2, 59, tzinfo=TIMEZONE),
            "Pixel协同设计低成本轮式人形硬件、遥操作数据采集、全身控制与统一策略学习流程。",
            10,
        ),
        candidate(
            "D&A: Decoupling Description and Assessment Enables VLMs "
            "as Zero-Shot Robotic Reward Models",
            "https://arxiv.org/abs/2611.03622v1",
            "arXiv Robotics",
            "research",
            datetime(2026, 11, 3, 2, 52, tzinfo=TIMEZONE),
            "D&A将任务描述与评估解耦，使VLM无需机器人专用训练即可作为零样本奖励模型。",
            9,
        ),
        candidate(
            "Cities Worldwide Build and Scale AI Services With NVIDIA Physical and Agentic AI",
            "https://blogs.nvidia.com/blog/cities-physical-agentic-ai-applications/",
            "NVIDIA Blog",
            "primary",
            datetime(2026, 11, 3, 15, 0, tzinfo=TIMEZONE),
            "NVIDIA介绍多地城市利用物理AI、数字孪生和视觉智能体建设交通、基础设施与公共服务。",
            9,
        ),
        candidate(
            "智元精灵G2进入便利店开展24小时真实岗位测试",
            "https://www.jushenhome.com/news/2241",
            "具身之家（来源：智元）",
            "media",
            datetime(2026, 11, 3, 14, 5, tzinfo=TIMEZONE),
            "六台智元精灵G2在上海便利店承担迎宾、咖啡、理货、收银与清洁任务，接受连续24小时测试。",
            9,
        ),
        candidate(
            "优必选发布Thinker-Sim具身智能仿真平台",
            "https://theroboradar.com/news/ubtech-thinker-sim-launch-de887a",
            "TheRoboRadar（来源：优必选）",
            "media",
            datetime(2026, 11, 2, 10, 0, tzinfo=TIMEZONE),
            "Thinker-Sim以Real2Sim2Real为核心，覆盖场景数字化、仿真数据合成与机器人能力评测。",
            8,
        ),
    ]
    items = DigestSelector(RuntimeSettings.from_env(), 5).select(candidates)
    digest = Digest(
        title="具身智能日报",
        date="2026-11-03",
        generated_at=datetime.now(TIMEZONE),
        items=items,
    )
    output_dir = Path("output")
    capture_digest_screenshots(digest, output_dir)
    write_digest(digest, output_dir)
    build_site(output_dir=output_dir)
    research_count = sum(item.source_kind == "research" for item in digest.items)
    news_count = len(digest.items) - research_count
    print(f"测试日报生成成功：{research_count} 篇论文 + {news_count} 条普通新闻")


if __name__ == "__main__":
    main()
