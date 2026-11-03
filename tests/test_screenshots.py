from embodied_daily.screenshots import write_fallback_svg


def test_fallback_svg_contains_story_context(tmp_path) -> None:
    target = tmp_path / "fallback.svg"
    write_fallback_svg(
        target,
        title="具身智能测试标题",
        source="测试信源",
        url="https://example.com/news",
    )
    content = target.read_text(encoding="utf-8")
    assert "具身智能测试标题" in content
    assert "测试信源" in content
    assert "example.com" in content

