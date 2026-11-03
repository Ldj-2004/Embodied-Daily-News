import json

from embodied_daily.feishu import build_feishu_payload
from embodied_daily.render import render_markdown, write_digest


def test_markdown_contains_exactly_five_numbered_items(digest) -> None:
    markdown = render_markdown(digest)
    assert sum(1 for line in markdown.splitlines() if line.startswith("## ")) == 5
    assert "模型与算法" not in markdown
    assert "产品与部署" not in markdown


def test_feishu_payload_is_flat_five_item_list(digest) -> None:
    payload = build_feishu_payload(digest)
    content = payload["content"]["post"]["zh_cn"]["content"]
    links = [element for row in content for element in row if element.get("tag") == "a"]
    assert len(links) == 5
    serialized = json.dumps(payload, ensure_ascii=False)
    assert "模型与算法" not in serialized
    assert "产品与部署" not in serialized


def test_write_digest_creates_latest_and_dated_files(tmp_path, digest) -> None:
    paths = write_digest(digest, tmp_path)
    assert len(paths) == 4
    assert (tmp_path / "latest.md").exists()
    assert (tmp_path / "2026-10-03.json").exists()
    parsed = json.loads((tmp_path / "latest.json").read_text(encoding="utf-8"))
    assert len(parsed["items"]) == 5

