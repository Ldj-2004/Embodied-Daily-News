from __future__ import annotations

import argparse

from openai import OpenAI

from embodied_daily.config import RuntimeSettings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--probe",
        action="store_true",
        help="Send a minimal chat request after listing models.",
    )
    args = parser.parse_args()
    settings = RuntimeSettings.from_env()
    settings.validate_for_ai()
    client = OpenAI(
        api_key=settings.api_key,
        base_url=settings.api_base,
        timeout=30.0,
        max_retries=1,
    )
    models = sorted(model.id for model in client.models.list().data)
    print("API 连接成功。当前账号可用模型：")
    for model in models:
        print(f"- {model}")
    if args.probe:
        response = client.chat.completions.create(
            model=settings.model,
            messages=[{"role": "user", "content": "只回复 OK"}],
            max_tokens=128,
        )
        message = response.choices[0].message
        content = (message.content or "").strip()
        reasoning = str(getattr(message, "reasoning_content", "") or "").strip()
        if not content and not reasoning:
            raise RuntimeError("模型返回了空内容。")
        print(f"模型调用成功：{settings.model}")


if __name__ == "__main__":
    main()
