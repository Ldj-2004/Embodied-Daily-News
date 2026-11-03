from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import yaml
from dotenv import load_dotenv

DEFAULT_BASE_URL = "http://35.220.164.252:3888/v1/"


def load_yaml(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class RuntimeSettings:
    api_key: str
    api_base: str
    model: str
    allow_insecure_api_base: bool
    feishu_webhook: str
    feishu_secret: str
    timezone: str
    log_level: str

    @classmethod
    def from_env(cls) -> RuntimeSettings:
        load_dotenv()
        return cls(
            api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            api_base=(os.getenv("OPENAI_BASE_URL", DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL),
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini",
            allow_insecure_api_base=env_bool("ALLOW_INSECURE_API_BASE"),
            feishu_webhook=os.getenv("FEISHU_WEBHOOK", "").strip(),
            feishu_secret=os.getenv("FEISHU_SECRET", "").strip(),
            timezone=os.getenv("TIMEZONE", "Asia/Shanghai").strip() or "Asia/Shanghai",
            log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO",
        )

    def validate_for_ai(self) -> None:
        if not self.api_key:
            raise ValueError(
                "缺少 OPENAI_API_KEY。请在本地 .env 或 GitHub Actions Secret 中设置。"
            )
        scheme = urlparse(self.api_base).scheme.lower()
        if scheme not in {"http", "https"}:
            raise ValueError("OPENAI_BASE_URL 必须以 http:// 或 https:// 开头。")
        if scheme == "http" and not self.allow_insecure_api_base:
            raise ValueError(
                "OPENAI_BASE_URL 使用明文 HTTP，API 密钥可能在传输中泄露。"
                "请优先改用 HTTPS；若你明确接受风险，再设置 ALLOW_INSECURE_API_BASE=true。"
            )

