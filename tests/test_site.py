import json

from embodied_daily.render import write_digest
from embodied_daily.site import build_site


def test_build_site_copies_digest_and_assets(tmp_path, digest) -> None:
    output = tmp_path / "output"
    web = tmp_path / "web"
    dist = tmp_path / "dist"
    web.mkdir()
    (web / "index.html").write_text("<!doctype html><title>test</title>", encoding="utf-8")
    (web / "app.js").write_text("console.log('test')", encoding="utf-8")

    asset = output / "assets" / digest.date / "01.svg"
    asset.parent.mkdir(parents=True)
    asset.write_text("<svg xmlns='http://www.w3.org/2000/svg'></svg>", encoding="utf-8")
    digest.items[0].screenshot = f"assets/{digest.date}/01.svg"
    write_digest(digest, output)

    result = build_site(web_dir=web, output_dir=output, dist_dir=dist)

    assert result == dist
    assert (dist / "index.html").exists()
    assert (dist / "data" / "latest.json").exists()
    assert (dist / "assets" / digest.date / "01.svg").exists()
    payload = json.loads((dist / "data" / "latest.json").read_text(encoding="utf-8"))
    assert len(payload["items"]) == 5




def test_build_site_accepts_one_date_bound_special_page(tmp_path, digest) -> None:
    output = tmp_path / "output"
    web = tmp_path / "web"
    dist = tmp_path / "dist"
    web.mkdir()
    (web / "index.html").write_text("<!doctype html><title>test</title>", encoding="utf-8")
    digest.items.append(
        type(digest.items[0])(
            rank=6,
            candidate_id="special-test",
            title="特别关注",
            summary="经过核实的特别关注摘要。",
            why_it_matters="验证第六页。",
            url="https://example.com/statement",
            source="官方声明",
            source_kind="special",
            published_at=digest.generated_at,
            screenshot="assets/special/test.jpg",
            screenshot_status="provided",
        )
    )
    write_digest(digest, output)

    build_site(web_dir=web, output_dir=output, dist_dir=dist)

    payload = json.loads((dist / "data" / "latest.json").read_text(encoding="utf-8"))
    assert len(payload["items"]) == 6
