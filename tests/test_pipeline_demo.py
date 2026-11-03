from datetime import UTC, datetime

from embodied_daily.llm import fallback_item
from embodied_daily.models import Digest
from embodied_daily.pipeline import replace_items_with_failed_screenshots, run_pipeline


def test_demo_pipeline_writes_five_items_without_network(tmp_path) -> None:
    digest = run_pipeline(
        output_dir=tmp_path / "output",
        state_path=tmp_path / "state.json",
        skip_feishu=True,
        demo=True,
        skip_screenshots=True,
        build_display=False,
    )
    assert len(digest.items) == 5
    assert (tmp_path / "output" / "latest.md").exists()


def test_failed_screenshot_story_is_replaced(monkeypatch, tmp_path, candidates) -> None:
    candidates[-2].source_kind = "research"
    candidates[-1].source_kind = "research"
    bad_id = candidates[0].id
    initial_candidates = [*candidates[:3], *candidates[-2:]]
    digest = Digest(
        title="具身智能日报",
        date="2026-11-03",
        generated_at=datetime.now(UTC),
        items=[
            fallback_item(candidate, rank)
            for rank, candidate in enumerate(initial_candidates, start=1)
        ],
    )

    capture_rounds: list[list[str]] = []

    def fake_capture(current_digest, output_dir, *, fallback_on_failure=True):
        assert fallback_on_failure is False
        capture_rounds.append(
            [item.candidate_id for item in current_digest.items]
        )
        for item in current_digest.items:
            item.screenshot_status = (
                "failed" if item.candidate_id == bad_id else "captured"
            )
            item.screenshot = "" if item.screenshot_status == "failed" else "ok.png"
        return []

    class FakeSelector:
        def select(self, available):
            news = [item for item in available if item.source_kind != "research"][:3]
            papers = [item for item in available if item.source_kind == "research"][:2]
            selected = news + papers
            return [
                fallback_item(candidate, rank)
                for rank, candidate in enumerate(selected, start=1)
            ]

    monkeypatch.setattr(
        "embodied_daily.pipeline.capture_digest_screenshots",
        fake_capture,
    )
    result = replace_items_with_failed_screenshots(
        digest,
        candidates,
        FakeSelector(),
        tmp_path,
    )

    assert len(capture_rounds) == 2
    assert bad_id not in {item.candidate_id for item in result.items}
    assert candidates[3].id in {item.candidate_id for item in result.items}
    assert all(item.screenshot_status == "captured" for item in result.items)
