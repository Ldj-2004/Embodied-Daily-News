from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description="截取本地大屏预览图。")
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--output", default="artifacts/showcase-preview.png")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True)
        except Exception:
            browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(args.url, wait_until="networkidle", timeout=30_000)
        page.screenshot(path=str(output), full_page=False)
        browser.close()
    print(f"预览图已保存：{output.resolve()}")


if __name__ == "__main__":
    main()
