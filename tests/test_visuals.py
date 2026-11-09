from embodied_daily.visuals import visual_metadata_score


def test_robot_operation_image_outranks_portrait() -> None:
    robot = {
        "alt": "Humanoid robot uses a robotic arm to assemble parts in a factory",
        "caption": "Robot manipulation deployment",
        "natural_width": 1400,
        "natural_height": 900,
        "rendered_width": 1000,
        "rendered_height": 640,
        "in_article": True,
        "in_figure": True,
    }
    portrait = {
        "alt": "CEO portrait and conference speaker headshot",
        "natural_width": 1400,
        "natural_height": 900,
        "rendered_width": 1000,
        "rendered_height": 640,
        "in_article": True,
        "in_figure": False,
    }

    robot_score, robot_hits, _ = visual_metadata_score(robot)
    portrait_score, _, portrait_negative = visual_metadata_score(portrait)

    assert robot_hits >= 2
    assert portrait_negative >= 2
    assert robot_score > portrait_score
