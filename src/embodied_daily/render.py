from __future__ import annotations

import json
from pathlib import Path

from embodied_daily.models import Digest


def render_markdown(digest: Digest) -> str:
    lines = [f"# {digest.title}｜{digest.date}", ""]
    for item in digest.items:
        published = item.published_at.astimezone(digest.generated_at.tzinfo).strftime(
            "%Y-%m-%d %H:%M"
        )
        lines.extend(
            [
                f"## {item.rank}. [{item.title}]({item.url})",
                "",
                item.summary,
                "",
                f"**为什么重要：** {item.why_it_matters}",
                "",
                f"> 来源：{item.source}｜发布时间：{published}",
                "",
            ]
        )
    lines.extend(
        [
            "---",
            "",
            f"生成时间：{digest.generated_at.isoformat(timespec='seconds')}",
            "",
            "本日报由自动化系统辅助整理，重要信息请以原始来源为准。",
            "",
        ]
    )
    return "\n".join(lines)


def write_digest(digest: Digest, output_dir: str | Path) -> list[Path]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    markdown = render_markdown(digest)
    json_text = json.dumps(digest.to_dict(), ensure_ascii=False, indent=2) + "\n"
    targets = {
        directory / f"{digest.date}.md": markdown,
        directory / f"{digest.date}.json": json_text,
        directory / "latest.md": markdown,
        directory / "latest.json": json_text,
    }
    for path, content in targets.items():
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)
    return list(targets)


def write_source_health(records: list[dict], output_dir: str | Path) -> Path:
    path = Path(output_dir) / "source-health.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
