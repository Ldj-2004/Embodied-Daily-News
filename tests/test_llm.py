from embodied_daily.config import RuntimeSettings
from embodied_daily.llm import DigestSelector, extract_json


def settings() -> RuntimeSettings:
    return RuntimeSettings(
        api_key="sk-test",
        api_base="https://example.com/v1/",
        model="test-model",
        allow_insecure_api_base=False,
        feishu_webhook="",
        feishu_secret="",
        timezone="Asia/Shanghai",
        log_level="INFO",
    )


def test_extract_json_from_code_fence() -> None:
    result = extract_json('```json\n{"items": []}\n```')
    assert result == {"items": []}


def test_hydration_uses_candidate_links_and_fills_to_five(candidates) -> None:
    candidates[-2].source_kind = "research"
    candidates[-1].source_kind = "research"
    parsed = {
        "items": [
            {
                "id": candidates[0].id,
                "title": "模型写的中文标题",
                "summary": "模型摘要",
                "why_it_matters": "模型说明",
                "importance_score": 9.5,
            },
            {"id": "invented-id", "title": "伪造候选"},
        ]
    }
    items = DigestSelector(settings())._validate_and_hydrate(parsed, candidates)
    assert len(items) == 5
    assert items[0].url == candidates[0].url
    assert all(item.candidate_id != "invented-id" for item in items)


def test_hydration_forces_exactly_two_research_items(candidates) -> None:
    candidates[-2].source_kind = "research"
    candidates[-1].source_kind = "research"
    parsed = {
        "items": [
            {
                "id": candidate.id,
                "title": candidate.title,
                "summary": candidate.summary,
                "why_it_matters": "重要",
                "importance_score": 8,
            }
            for candidate in candidates[:-1]
        ]
    }

    items = DigestSelector(settings())._validate_and_hydrate(parsed, candidates)

    assert len(items) == 5
    assert sum(item.source_kind == "research" for item in items) == 2
    assert sum(item.source_kind != "research" for item in items) == 3
    assert [item.rank for item in items] == [1, 2, 3, 4, 5]

