from embodied_daily.specials import append_special_items


def test_append_special_item_only_on_matching_date(tmp_path, digest) -> None:
    config = tmp_path / "special_items.yaml"
    config.write_text(
        """
special_items:
  - date: "2026-10-03"
    id: "special-test"
    title: "特别关注"
    summary: "这是经过核实的特别关注摘要。"
    why_it_matters: "用于验证第六页只在指定日期出现。"
    url: "https://example.com/statement"
    source: "官方声明"
    published_at: "2026-10-03T08:00:00+08:00"
    screenshot: "assets/special/test.jpg"
""".strip(),
        encoding="utf-8",
    )

    assert append_special_items(digest, config) == 1
    assert len(digest.items) == 6
    assert digest.items[-1].rank == 6
    assert digest.items[-1].source_kind == "special"
    assert digest.items[-1].screenshot_status == "provided"
    assert append_special_items(digest, config) == 0
