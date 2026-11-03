from __future__ import annotations

import base64
import hashlib
import hmac
import time
from typing import Any
from urllib.parse import urlparse

import httpx

from embodied_daily.models import Digest


def build_signature(timestamp: str, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}"
    digest = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def build_feishu_payload(digest: Digest, secret: str = "") -> dict[str, Any]:
    content: list[list[dict[str, str]]] = []
    for item in digest.items:
        content.append(
            [
                {"tag": "text", "text": f"{item.rank}. "},
                {"tag": "a", "text": item.title, "href": item.url},
            ]
        )
        content.append([{"tag": "text", "text": item.summary}])
        content.append([{"tag": "text", "text": f"为什么重要：{item.why_it_matters}"}])
        content.append([{"tag": "text", "text": f"来源：{item.source}\n"}])

    payload: dict[str, Any] = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"{digest.title}｜{digest.date}",
                    "content": content,
                }
            }
        },
    }
    if secret:
        timestamp = str(int(time.time()))
        payload["timestamp"] = timestamp
        payload["sign"] = build_signature(timestamp, secret)
    return payload


def send_to_feishu(webhook: str, digest: Digest, secret: str = "") -> None:
    if not webhook:
        return
    parsed = urlparse(webhook)
    if parsed.scheme != "https" or parsed.netloc != "open.feishu.cn":
        raise ValueError("FEISHU_WEBHOOK 必须是 https://open.feishu.cn/ 下的地址。")
    payload = build_feishu_payload(digest, secret)
    with httpx.Client(timeout=20.0) as client:
        response = client.post(webhook, json=payload)
        response.raise_for_status()
    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError("飞书返回了无法解析的响应。") from exc
    code = body.get("code", body.get("StatusCode", 0))
    if code not in {0, "0", None}:
        message = body.get("msg") or body.get("StatusMessage") or str(body)
        raise RuntimeError(f"飞书推送失败：{message}")

