from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from embodied_daily.models import Candidate


class SeenState:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.items: dict[str, str] = {}

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.items = dict(data.get("seen", {}))
        except (json.JSONDecodeError, OSError, TypeError):
            self.items = {}

    def filter_unseen(self, candidates: list[Candidate]) -> list[Candidate]:
        return [candidate for candidate in candidates if candidate.id not in self.items]

    def mark_seen(self, candidates: list[Candidate]) -> None:
        now = datetime.now(UTC).isoformat()
        for candidate in candidates:
            self.items[candidate.id] = now

    def prune(self, retention_days: int = 90) -> None:
        cutoff = datetime.now(UTC) - timedelta(days=retention_days)
        kept: dict[str, str] = {}
        for key, value in self.items.items():
            try:
                if datetime.fromisoformat(value) >= cutoff:
                    kept[key] = value
            except ValueError:
                continue
        self.items = kept

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": 1, "seen": self.items}
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.path)

