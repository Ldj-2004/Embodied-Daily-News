from embodied_daily.config import RuntimeSettings


def test_plain_http_requires_explicit_opt_in() -> None:
    settings = RuntimeSettings(
        api_key="sk-test",
        api_base="http://example.com/v1/",
        model="test-model",
        allow_insecure_api_base=False,
        feishu_webhook="",
        feishu_secret="",
        timezone="Asia/Shanghai",
        log_level="INFO",
    )
    try:
        settings.validate_for_ai()
    except ValueError as exc:
        assert "明文 HTTP" in str(exc)
    else:
        raise AssertionError("HTTP endpoint should require explicit opt-in")


def test_https_is_allowed() -> None:
    settings = RuntimeSettings(
        api_key="sk-test",
        api_base="https://example.com/v1/",
        model="test-model",
        allow_insecure_api_base=False,
        feishu_webhook="",
        feishu_secret="",
        timezone="Asia/Shanghai",
        log_level="INFO",
    )
    settings.validate_for_ai()

