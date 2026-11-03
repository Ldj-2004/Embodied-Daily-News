from __future__ import annotations

import argparse
import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from embodied_daily.models import Digest, DigestItem
from embodied_daily.render import write_digest
from embodied_daily.screenshots import capture_digest_screenshots
from embodied_daily.site import build_site

SHANGHAI = ZoneInfo("Asia/Shanghai")
TEST_DATE = "2026-10-30"


def _published(day: int, hour: int = 9) -> datetime:
    return datetime(2026, 10, day, hour, 0, tzinfo=SHANGHAI)


def create_test_digest() -> Digest:
    items = [
        DigestItem(
            rank=1,
            candidate_id="agibot-ai-wave-2026",
            title="智元启动 AI WAVE，连续发布七项具身 AI 成果",
            summary=(
                "智元宣布从 10 月 22 日起连续发布数据集、作业平台、机器人本体、"
                "Agent 框架、仿真平台、基座大模型与群体经验学习范式等七项成果，"
                "集中展示从数据、模型到机器人部署的全栈具身 AI 技术布局。"
            ),
            why_it_matters=(
                "具身智能竞争正从单点模型能力转向数据、平台、本体和部署协同的完整技术体系。"
            ),
            url="https://www.agibot.com.cn/article/315/detail/250.html",
            source="智元创新 AGIBOT",
            source_kind="company",
            published_at=_published(22, 10),
            importance_score=9.6,
        ),
        DigestItem(
            rank=2,
            candidate_id="nvidia-isaac-platform-2026",
            title="NVIDIA 扩展 Isaac 平台并推出参考人形机器人",
            summary=(
                "NVIDIA 发布 Isaac OS、Isaac Lab 3.0、Human 1M 数据集等更新，"
                "并联合 Agile Robots 推出搭载 Jetson Thor 与 Isaac GR00T 的 Agile ONE SN。"
                "这套参考平台计划于 2027 年初面向研究机构提供。"
            ),
            why_it_matters=(
                "数据、仿真、训练、部署和机器人本体被整合到同一技术栈，降低研究团队的系统集成成本。"
            ),
            url=(
                "https://nvidianews.nvidia.com/news/nvidia-advances-isaac-platform-for-"
                "general-purpose-robotics-with-new-reference-humanoid-frameworks-"
                "simulation-pipelines-and-data"
            ),
            source="NVIDIA Newsroom",
            source_kind="company",
            published_at=_published(21, 16),
            importance_score=9.4,
        ),
        DigestItem(
            rank=3,
            candidate_id="mitsubishi-humanoid-cnc-physical-ai",
            title="三菱电机让人形机器人通过 Physical AI 协作 CNC 机床",
            summary=(
                "三菱电机开发人形机器人与 CNC 机床协同加工系统。操作员只需给出基本工作指令，"
                "系统即可规划并执行装夹、清洁、成品搬运、检测和异常处置等任务，"
                "目标是减少传统机加工现场的复杂集成工作。"
            ),
            why_it_matters=(
                "这是 Physical AI 从演示走向传统制造流程的具体案例，强调机器人与工业设备的协同。"
            ),
            url="https://www.mitsubishielectric.com/en/pr/2026/1021_rd/",
            source="Mitsubishi Electric",
            source_kind="company",
            published_at=_published(21, 9),
            importance_score=9.1,
        ),
        DigestItem(
            rank=4,
            candidate_id="agility-digit-5-nvidia-thor",
            title="Agility 为 Digit 5 统一采用 NVIDIA IGX Thor",
            summary=(
                "Agility 宣布下一代 Digit 5 将把 NVIDIA IGX Thor 作为标准机载计算平台，"
                "并计划结合 Isaac GR00T、Isaac Lab 和 Halos 安全体系，"
                "为更大规模的商业部署统一计算、学习和安全基础。"
            ),
            why_it_matters="统一软硬件栈有助于人形机器人从少量试点走向可复制的商业部署。",
            url=(
                "https://www.agilityrobotics.com/content/agility-robotics-expands-nvidia-"
                "collaboration-as-it-prepares-digit-5-for-commercial-scale"
            ),
            source="Agility Robotics",
            source_kind="company",
            published_at=_published(22, 9),
            importance_score=8.5,
        ),
        DigestItem(
            rank=5,
            candidate_id="tsinghua-embodied-intelligence-report-2026",
            title="《具身智能发展报告（2026年）》发布",
            summary=(
                "中国信通院与清华大学相关团队发布报告，判断行业正从实验室验证向试点应用过渡。"
                "截至 10 月 8 日，国内相关企业达 405 家，但规模化落地、连续作业和商业闭环"
                "仍面临明显约束。"
            ),
            why_it_matters="报告同时呈现产业热度与实际落地差距，有助于校准行业判断。",
            url="https://www.tsinghua.edu.cn/info/1182/128871.htm",
            source="清华大学",
            source_kind="university",
            published_at=_published(22, 18),
            importance_score=8.3,
        ),
    ]
    return Digest(
        title="具身智能日报",
        date=TEST_DATE,
        generated_at=datetime(2026, 10, 30, 8, 0, tzinfo=SHANGHAI),
        items=items,
        edition="test",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="生成 2026-10-30 大屏测试版。")
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--dist-dir", default="dist")
    parser.add_argument("--skip-screenshots", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    digest = create_test_digest()
    if not args.skip_screenshots:
        capture_digest_screenshots(digest, args.output_dir)
    paths = write_digest(digest, args.output_dir)
    site = build_site(output_dir=args.output_dir, dist_dir=args.dist_dir)

    print(f"测试日报：{Path(paths[0]).resolve()}")
    print(f"大屏站点：{site.resolve()}")
    for item in digest.items:
        print(f"{item.rank}. {item.screenshot_status}: {item.screenshot or '未生成截图'}")


if __name__ == "__main__":
    main()
