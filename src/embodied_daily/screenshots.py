from __future__ import annotations

import html
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

from embodied_daily.models import Digest

LOGGER = logging.getLogger(__name__)

BLOCKED_MARKERS = (
    "access denied",
    "verify you are human",
    "captcha",
    "403 forbidden",
    "page not found",
)
ARXIV_PATH_RE = re.compile(r"/(?:abs|pdf|html)/([^/?#]+)", re.IGNORECASE)


def _safe_domain(url: str) -> str:
    return urlparse(url).netloc.removeprefix("www.") or "原始信源"


def arxiv_html_url(url: str) -> str | None:
    """Convert an arXiv abstract/PDF URL to its HTML paper view."""
    parsed = urlparse(url)
    if not parsed.netloc.lower().endswith("arxiv.org"):
        return None
    match = ARXIV_PATH_RE.search(parsed.path)
    if not match:
        return None
    paper_id = match.group(1).removesuffix(".pdf")
    return f"https://arxiv.org/html/{paper_id}"


def capture_arxiv_figure(page, url: str, path: Path, timeout_ms: int) -> None:
    """Capture the largest useful figure from arXiv HTML, including its caption."""
    html_url = arxiv_html_url(url)
    if not html_url:
        raise RuntimeError("论文链接不是可识别的 arXiv 地址")
    page.goto(html_url, wait_until="domcontentloaded", timeout=timeout_ms)
    page.wait_for_timeout(2_000)
    figures = page.locator("figure")
    best = None
    best_score = 0.0
    for index in range(min(figures.count(), 16)):
        figure = figures.nth(index)
        metrics = figure.evaluate(
            """element => ({
              width: element.scrollWidth,
              height: element.scrollHeight,
              visuals: element.querySelectorAll('img, svg, canvas').length
            })"""
        )
        width = float(metrics.get("width", 0))
        height = float(metrics.get("height", 0))
        if metrics.get("visuals", 0) < 1 or width < 320 or height < 160:
            continue
        if height > 1_800:
            continue
        score = min(width, 1_200) * min(height, 900)
        if score > best_score:
            best = figure
            best_score = score
    if best is None:
        raise RuntimeError("arXiv HTML 中没有找到尺寸合适的论文图表")
    best.scroll_into_view_if_needed(timeout=5_000)
    best.screenshot(path=str(path), timeout=timeout_ms)


def write_fallback_svg(
    path: Path,
    *,
    title: str,
    source: str,
    url: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    escaped_title = html.escape(title)
    escaped_source = html.escape(source)
    escaped_domain = html.escape(_safe_domain(url))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
  width="1440" height="1000" viewBox="0 0 1440 1000">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#111d33"/>
      <stop offset="1" stop-color="#24395c"/>
    </linearGradient>
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M 48 0 L 0 0 0 48" fill="none" stroke="#8ba7d1" stroke-opacity=".12"/>
    </pattern>
  </defs>
  <rect width="1440" height="1000" fill="url(#bg)"/>
  <rect width="1440" height="1000" fill="url(#grid)"/>
  <circle cx="1220" cy="160" r="220" fill="#36d6c2" fill-opacity=".10"/>
  <text x="96" y="130" font-family="Arial, Microsoft YaHei, sans-serif"
    font-size="34" fill="#79e0d4">WEB CAPTURE FALLBACK</text>
  <text x="96" y="225" font-family="Arial, Microsoft YaHei, sans-serif"
    font-size="28" fill="#a9bad4">{escaped_domain}</text>
  <foreignObject x="96" y="300" width="1160" height="360">
    <div xmlns="http://www.w3.org/1999/xhtml"
      style="font:700 64px/1.35 Arial,'Microsoft YaHei',sans-serif;
      color:#f5f8ff;overflow-wrap:anywhere;">{escaped_title}</div>
  </foreignObject>
  <line x1="96" y1="760" x2="1344" y2="760" stroke="#9db2d3" stroke-opacity=".3"/>
  <text x="96" y="835" font-family="Arial, Microsoft YaHei, sans-serif"
    font-size="30" fill="#d5deec">来源：{escaped_source}</text>
  <text x="96" y="895" font-family="Arial, Microsoft YaHei, sans-serif"
    font-size="24" fill="#91a4c3">网页截图暂时不可用，原文链接仍可访问</text>
</svg>"""
    path.write_text(svg, encoding="utf-8")


def capture_digest_screenshots(
    digest: Digest,
    output_dir: str | Path,
    *,
    timeout_ms: int = 30_000,
    fallback_on_failure: bool = True,
) -> list[Path]:
    """Capture the first viewport for each article and attach paths to digest items.

    When ``fallback_on_failure`` is false, an article-level capture failure is
    recorded as ``failed`` instead of producing an SVG placeholder.  The
    pipeline uses that status to reject the story and select another candidate.
    """
    root = Path(output_dir)
    assets_dir = root / "assets" / digest.date
    assets_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        LOGGER.warning("Playwright 未安装，全部使用截图占位图。")
        sync_playwright = None

    playwright_context = sync_playwright() if sync_playwright else None
    playwright = None
    browser = None
    if playwright_context:
        try:
            playwright = playwright_context.start()
            launch_options = {
                "headless": True,
                "args": ["--disable-dev-shm-usage", "--no-sandbox"],
            }
            try:
                browser = playwright.chromium.launch(**launch_options)
            except Exception:
                LOGGER.info("Playwright Chromium 不可用，尝试使用系统 Microsoft Edge。")
                browser = playwright.chromium.launch(channel="msedge", **launch_options)
        except Exception as exc:
            LOGGER.warning("Chromium 启动失败，将使用占位图：%s", exc)

    try:
        if not browser and not fallback_on_failure:
            raise RuntimeError(
                "截图浏览器不可用，无法验证候选新闻的网页图片。"
                "请安装 Playwright Chromium，或使用 --skip-screenshots 跳过严格验证。"
            )
        for item in digest.items:
            png_path = assets_dir / f"{item.rank:02d}.png"
            svg_path = assets_dir / f"{item.rank:02d}.svg"
            png_path.unlink(missing_ok=True)
            svg_path.unlink(missing_ok=True)
            relative_png = png_path.relative_to(root).as_posix()
            captured = False
            if browser:
                page = browser.new_page(
                    viewport={"width": 1440, "height": 1000},
                    device_scale_factor=1,
                    locale="zh-CN",
                    user_agent=(
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
                    ),
                )
                try:
                    if item.source_kind == "research":
                        capture_arxiv_figure(page, item.url, png_path, timeout_ms)
                    else:
                        page.goto(
                            item.url,
                            wait_until="domcontentloaded",
                            timeout=timeout_ms,
                        )
                        page.wait_for_timeout(2_000)
                        page.add_style_tag(
                            content="""
                            [class*='cookie' i], [id*='cookie' i],
                            [class*='consent' i], [id*='consent' i],
                            [aria-label*='cookie' i] { display: none !important; }
                            """
                        )
                        text = page.locator("body").inner_text(timeout=5_000).lower()[:2_000]
                        if len(text.strip()) < 80:
                            raise RuntimeError("页面可见正文过少，疑似空白页")
                        if any(marker in text for marker in BLOCKED_MARKERS):
                            raise RuntimeError("页面返回了访问限制或错误提示")
                        page.screenshot(path=str(png_path), full_page=False)
                    item.screenshot = relative_png
                    item.screenshot_status = "captured"
                    written.append(png_path)
                    captured = True
                    LOGGER.info("视觉素材截取完成：%s", item.url)
                except Exception as exc:
                    LOGGER.warning("网页截图失败：%s (%s)", item.url, exc)
                finally:
                    page.close()

            if not captured and fallback_on_failure:
                write_fallback_svg(
                    svg_path,
                    title=item.title,
                    source=item.source,
                    url=item.url,
                )
                item.screenshot = svg_path.relative_to(root).as_posix()
                item.screenshot_status = "fallback"
                written.append(svg_path)
            elif not captured:
                item.screenshot = ""
                item.screenshot_status = "failed"
    finally:
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
    return written

