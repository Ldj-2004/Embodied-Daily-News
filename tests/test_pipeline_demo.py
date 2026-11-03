from embodied_daily.pipeline import run_pipeline


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

