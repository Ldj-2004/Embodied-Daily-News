from embodied_daily.screenshots import (
    arxiv_html_url,
    paper_figure_score,
    write_fallback_svg,
)


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


def test_arxiv_html_url_converts_abstract_and_pdf_links() -> None:
    assert (
        arxiv_html_url("https://arxiv.org/abs/2611.01234v2")
        == "https://arxiv.org/html/2611.01234v2"
    )
    assert (
        arxiv_html_url("https://export.arxiv.org/pdf/2611.01234.pdf")
        == "https://arxiv.org/html/2611.01234"
    )
    assert arxiv_html_url("https://example.com/paper") is None


def test_overview_figure_outranks_large_ablation_plot() -> None:
    overview = paper_figure_score(
        "Overview of our vision-language-action framework and training pipeline",
        index=1,
        width=900,
        height=500,
    )
    ablation = paper_figure_score(
        "Ablation results on the benchmark",
        index=8,
        width=1400,
        height=900,
    )
    assert overview > ablation


