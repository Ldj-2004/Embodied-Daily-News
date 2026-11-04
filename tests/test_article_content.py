from embodied_daily.article_content import extract_article_text


def test_extract_article_text_prefers_article_and_removes_scripts() -> None:
    document = """
    <html><body><nav>导航内容</nav><script>恶意脚本</script>
    <article><h1>机器人新品发布</h1><p>企业公布了量产与交付计划。</p></article>
    <footer>页脚内容</footer></body></html>
    """

    result = extract_article_text(document)

    assert "机器人新品发布" in result
    assert "量产与交付计划" in result
    assert "恶意脚本" not in result
    assert "导航内容" not in result
