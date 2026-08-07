"""Robust publish queue (JSON, tracked). Replaces the fragile .md queue.

Each item has a unique id so marking is atomic and unambiguous (fixes #15).
The queue is read/written by scripts and the scheduled jobs.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

QUEUE_FILE = Path(__file__).resolve().parent / "queue.json"
MAD = ZoneInfo("Europe/Madrid")


def _now() -> str:
    """Own timestamps in Europe/Madrid, not UTC (fixes the 2h best_hours drift)."""
    return datetime.now(MAD).isoformat(timespec="seconds")


def _load() -> list[dict]:
    if not QUEUE_FILE.exists():
        return []
    try:
        return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _save(items: list[dict]) -> None:
    QUEUE_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def add(platform: str, topic: str, body: str, source_url: str = "", image_url: str = "", kind: str = "news") -> dict:
    """Append a pending item. Returns the item.

    kind: 'news' (cite the source_url) or 'opinion' (original thought-post,
    e.g. checklists/takes — source_url optional). The watchdog only requires a
    source for kind='news'.
    """
    items = _load()
    item = {
        "id": uuid.uuid4().hex[:12],
        "platform": platform,
        "topic": topic,
        "body": body,
        "source_url": source_url,
        "image_url": image_url,
        "kind": kind,
        "status": "pending",
        "created_at": _now(),
    }
    items.append(item)
    _save(items)
    return item


def next_pending(platform: str | None = None) -> dict | None:
    """First pending item (optionally filtered by platform)."""
    items = _load()
    for it in items:
        if it.get("status") != "pending":
            continue
        if platform and it.get("platform") != platform:
            continue
        return it
    return None


def mark_published(item_id: str, external_id: str) -> bool:
    items = _load()
    for it in items:
        if it.get("id") == item_id and it.get("status") == "pending":
            it["status"] = "published"
            it["external_id"] = external_id
            it["published_at"] = _now()
            _save(items)
            return True
    return False


def list_pending() -> list[dict]:
    return [it for it in _load() if it.get("status") == "pending"]


def list_published() -> list[dict]:
    return [it for it in _load() if it.get("status") == "published"]


def count() -> dict:
    items = _load()
    return {"pending": sum(1 for i in items if i.get("status") == "pending"),
            "published": sum(1 for i in items if i.get("status") == "published"),
            "total": len(items)}