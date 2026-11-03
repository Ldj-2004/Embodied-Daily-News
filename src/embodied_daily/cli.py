from __future__ import annotations

import argparse
import logging

from embodied_daily.config import RuntimeSettings
from embodied_daily.pipeline import check_sources, run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成五条具身智能日报并推送到飞书。")
    parser.add_argument("--settings", default="config/settings.yaml", help="主配置文件路径")
    parser.add_argument("--sources", default="config/sources.yaml", help="信源配置文件路径")
    parser.add_argument("--output-dir", default="output", help="日报输出目录")
    parser.add_argument("--state", default="data/state.json", help="去重状态文件路径")
    parser.add_argument("--skip-feishu", action="store_true", help="只生成文件，不推送飞书")
    parser.add_argument("--ignore-state", action="store_true", help="忽略历史去重，仅用于调试")
    parser.add_argument(
        "--skip-screenshots",
        action="store_true",
        help="跳过网页截图（适合快速测试或浏览器尚未安装时）",
    )
    parser.add_argument(
        "--no-build-display",
        action="store_true",
        help="不构建 dist 大屏页面",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="不访问网络和模型，使用演示数据验证输出",
    )
    parser.add_argument(
        "--check-sources",
        action="store_true",
        help="仅检查信源，不调用模型或飞书",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    runtime = RuntimeSettings.from_env()
    logging.basicConfig(
        level=getattr(logging, runtime.log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    try:
        if args.check_sources:
            check_sources(
                settings_path=args.settings,
                sources_path=args.sources,
                output_dir=args.output_dir,
            )
            return
        run_pipeline(
            settings_path=args.settings,
            sources_path=args.sources,
            output_dir=args.output_dir,
            state_path=args.state,
            skip_feishu=args.skip_feishu,
            ignore_state=args.ignore_state,
            demo=args.demo,
            skip_screenshots=args.skip_screenshots,
            build_display=not args.no_build_display,
        )
    except Exception as exc:
        logging.getLogger(__name__).error("运行失败：%s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
