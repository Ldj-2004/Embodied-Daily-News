from embodied_daily.config import RuntimeSettings
from embodied_daily.llm import (
    DigestSelector,
    company_short_name,
    extract_json,
    fallback_item,
    limit_candidates_for_prompt,
)


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


def test_prompt_pool_is_bounded_and_keeps_fixed_composition(candidates) -> None:
    candidates[-2].source_kind = "research"
    candidates[-1].source_kind = "research"

    pool = limit_candidates_for_prompt(
        candidates,
        max_count=5,
        required_research=2,
        required_news=3,
    )

    assert len(pool) == 5
    assert sum(item.source_kind == "research" for item in pool) == 2
    assert sum(item.source_kind != "research" for item in pool) == 3


def test_fallback_keeps_complete_research_title(candidates) -> None:
    candidate = candidates[0]
    candidate.source_kind = "research"
    candidate.title = (
        "A Complete Vision-Language-Action Framework for Long-Horizon "
        "Dexterous Robot Manipulation in Unstructured Homes"
    )

    item = fallback_item(candidate, 1)

    assert item.title == candidate.title
    assert item.company_short_name == ""


def test_company_short_name_uses_news_subject(candidates) -> None:
    candidate = candidates[0]
    candidate.title = "Hyundai Motor Group expands Boston Dynamics production"
    candidate.source = "Global News Wire"

    assert company_short_name(candidate) == "Hyundai"


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
    items = DigestSelector(
        settings(), item_count=5, research_count=2, foreign_news_minimum=0
    )._validate_and_hydrate(parsed, candidates)
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

    items = DigestSelector(
        settings(), item_count=5, research_count=2, foreign_news_minimum=0
    )._validate_and_hydrate(parsed, candidates)

    assert len(items) == 5
    assert sum(item.source_kind == "research" for item in items) == 2
    assert sum(item.source_kind != "research" for item in items) == 3
    assert [item.rank for item in items] == [1, 2, 3, 4, 5]


def test_expanded_summary_updates_only_known_items(monkeypatch, candidates) -> None:
    candidates[-2].source_kind = "research"
    candidates[-1].source_kind = "research"
    selector = DigestSelector(
        settings(), item_count=5, research_count=2, foreign_news_minimum=0
    )
    items = selector._validate_and_hydrate({"items": []}, candidates)

    class Message:
        content = (
            '{"items":[{"id":"item-1","title":"机器人企业发布新一代操作模型",'
            '"company_short_name":"Unitree","summary":"'
            + "这是基于网页正文生成的更完整事实概述。" * 4
            + '","why_it_matters":"该进展展示了机器人产品从模型能力走向真实部署的重要路径。"}]}'
        )

    class FakeCompletions:
        def create(self, **kwargs):
            return type("Response", (), {"choices": [type("Choice", (), {"message": Message()})]})

    fake_client = type(
        "FakeClient",
        (),
        {"chat": type("Chat", (), {"completions": FakeCompletions()})()},
    )()
    monkeypatch.setattr("embodied_daily.llm.OpenAI", lambda **kwargs: fake_client)

    selector.expand_summaries(items, {"item-1": "网页正文" * 100})

    assert len(items[0].summary) > 40
    assert "真实部署" in items[0].why_it_matters
    assert items[0].title == "机器人企业发布新一代操作模型"
    assert items[0].company_short_name == "Unitree"

def test_select_falls_back_when_model_returns_non_json(monkeypatch, candidates) -> None:
    candidates[-2].source_kind = "research"
    candidates[-1].source_kind = "research"

    class Message:
        content = "抱歉，我无法按要求输出结构化内容。"

    class FakeCompletions:
        def create(self, **kwargs):
            return type(
                "Response",
                (),
                {"choices": [type("Choice", (), {"message": Message()})]},
            )()

    fake_client = type(
        "FakeClient",
        (),
        {"chat": type("Chat", (), {"completions": FakeCompletions()})()},
    )()
    monkeypatch.setattr("embodied_daily.llm.OpenAI", lambda **kwargs: fake_client)

    items = DigestSelector(
        settings(), item_count=5, research_count=2, foreign_news_minimum=0
    ).select(candidates)

    assert len(items) == 5
    assert sum(item.source_kind == "research" for item in items) == 2
    assert sum(item.source_kind != "research" for item in items) == 3


