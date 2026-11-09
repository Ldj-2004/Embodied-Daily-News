from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def build_site(
    web_dir: str | Path = "web",
    output_dir: str | Path = "output",
    dist_dir: str | Path = "dist",
) -> Path:
    web = Path(web_dir)
    output = Path(output_dir)
    dist = Path(dist_dir)
    latest = output / "latest.json"
    if not latest.exists():
        raise FileNotFoundError("缺少 output/latest.json，请先生成日报。")
    if not (web / "index.html").exists():
        raise FileNotFoundError("缺少 web/index.html。")

    if dist.exists():
        try:
            shutil.rmtree(dist)
        except PermissionError:
            # Windows may keep a directory handle open after a local preview.
            # Overwriting the generated files is safe and keeps local builds usable.
            pass
    shutil.copytree(web, dist, dirs_exist_ok=True)
    data_dir = dist / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(latest, data_dir / "latest.json")
    latest_md = output / "latest.md"
    if latest_md.exists():
        shutil.copy2(latest_md, data_dir / "latest.md")
    assets = output / "assets"
    if assets.exists():
        shutil.copytree(assets, dist / "assets", dirs_exist_ok=True)

    payload = json.loads((data_dir / "latest.json").read_text(encoding="utf-8"))
    item_count = len(payload.get("items", []))
    if item_count not in {5, 6}:
        raise ValueError("大屏页面要求五条常规内容，或五条加一页日期限定的特别关注。")
    (dist / ".nojekyll").write_text("", encoding="utf-8")
    return dist


def main() -> None:
    parser = argparse.ArgumentParser(description="构建具身智能日报大屏静态站点。")
    parser.add_argument("--web-dir", default="web")
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--dist-dir", default="dist")
    args = parser.parse_args()
    path = build_site(args.web_dir, args.output_dir, args.dist_dir)
    print(f"站点已构建：{path.resolve()}")


if __name__ == "__main__":
    main()

