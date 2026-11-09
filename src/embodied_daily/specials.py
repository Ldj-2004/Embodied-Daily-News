from __future__ import annotations

from datetime import datetime
from pathlib import Path

from embodied_daily.config import load_yaml
from embodied_daily.models import Digest, DigestItem


def append_special_items(
    digest: Digest,
    config_path: str | Path = "config/special_items.yaml",
) -> int:
    """Append at most one date-bound editorial page after the five-item digest."""
    path = Path(config_path)
    if not path.exists():
        return 0
    payload = load_yaml(path)
    rows = payload.get("special_items", [])
    if not isinstance(rows, list):
        return 0

    existing_ids = {item.candidate_id for item in digest.items}
    added = 0
    for raw in rows:
        if (
            not isinstance(raw, dict)
            or str(raw.get("date", "")) != digest.date
            or len(digest.items) >= 6
        ):
            continue
        candidate_id = str(raw.get("id", "")).strip()
        if not candidate_id or candidate_id in existing_ids:
            continue
        published_at = datetime.fromisoformat(str(raw["published_at"]))
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=digest.generated_at.tzinfo)
        digest.items.append(
            DigestItem(
                rank=len(digest.items) + 1,
                candidate_id=candidate_id,
                title=str(raw["title"]).strip(),
                summary=str(raw["summary"]).strip(),
                why_it_matters=str(raw["why_it_matters"]).strip(),
                url=str(raw["url"]).strip(),
                source=str(raw["source"]).strip(),
                source_kind="special",
                published_at=published_at,
                importance_score=float(raw.get("importance_score", 8.0)),
                screenshot=str(raw["screenshot"]).strip(),
                screenshot_status="provided",
            )
        )
        existing_ids.add(candidate_id)
        added += 1
    return added
