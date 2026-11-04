from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Candidate:
    id: str
    title: str
    url: str
    source: str
    source_kind: str
    published_at: datetime
    fetched_at: datetime
    summary: str = ""
    source_weight: int = 1
    relevance_score: int = 0

    def to_prompt_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "source_kind": self.source_kind,
            "published_at": self.published_at.isoformat(),
            "summary": self.summary[:400],
            "relevance_score": self.relevance_score,
        }


@dataclass(slots=True)
class DigestItem:
    rank: int
    candidate_id: str
    title: str
    summary: str
    why_it_matters: str
    url: str
    source: str
    source_kind: str
    published_at: datetime
    importance_score: float = 0.0
    screenshot: str = ""
    screenshot_status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["published_at"] = self.published_at.isoformat()
        return data


@dataclass(slots=True)
class Digest:
    title: str
    date: str
    generated_at: datetime
    items: list[DigestItem]
    edition: str = "daily"

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "date": self.date,
            "generated_at": self.generated_at.isoformat(),
            "edition": self.edition,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(slots=True)
class SourceHealth:
    name: str
    url: str
    ok: bool
    item_count: int = 0
    error: str = ""
    checked_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.checked_at:
            data["checked_at"] = self.checked_at.isoformat()
        return data


@dataclass(slots=True)
class CollectionResult:
    candidates: list[Candidate] = field(default_factory=list)
    health: list[SourceHealth] = field(default_factory=list)

