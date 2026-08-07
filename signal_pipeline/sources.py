"""Signal sources: ingest research feeds and X timeline/markets into the store.

In autonomous operation the scheduled 4h job performs the live research
(web_search, X timeline via connector, trend research) and writes a JSON feed;
this module ingests that feed, scores it, and persists it for the content engine.
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

from . import store
from .score import score_signal


def _slug(text: str, n: int = 40) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")[:n]


def signal_id(topic: str, title: str, published_at: str | None = None) -> str:
    base = f"{topic}:{_slug(title)}"
    return f"{base}-{published_at or 'na'}"


def ingest_feed(conn, feed_path: str | Path, weights: dict | None = None) -> dict:
    """Ingest a JSON feed of raw signals. Each item:
    {topic, kind, title, summary, url, published_at, confidence, novelty,
     virality_potential, source}
    Returns counts {added, skipped, total}.
    """
    path = Path(feed_path)
    if not path.exists():
        return {"added": 0, "skipped": 0, "total": 0}
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw if isinstance(raw, list) else raw.get("signals", [])

    added = skipped = 0
    for it in items:
        sid = it.get("id") or signal_id(it.get("topic", "misc"), it.get("title", ""), it.get("published_at"))
        scored = score_signal({**it, "id": sid}, weights)
        if store.add_signal(conn, scored):
            added += 1
        else:
            skipped += 1
    conn.commit()
    return {"added": added, "skipped": skipped, "total": len(items)}


def ingest_x_timeline(conn, tweets: list[dict]) -> dict:
    """Convert interesting X posts from the timeline into signals."""
    added = 0
    for tw in tweets:
        text = tw.get("text", "").strip()
        if not text or len(text) < 20:
            continue
        sid = f"x:{tw.get('id')}"
        sig = {
            "id": sid, "topic": "news", "kind": "viral_post",
            "title": text[:140], "summary": text, "url": f"https://x.com/i/status/{tw.get('id')}",
            "published_at": tw.get("created_at"), "confidence": 0.5,
            "novelty": 0.5, "virality_potential": 0.5, "source": "x_timeline",
        }
        if store.add_signal(conn, sig):
            added += 1
    conn.commit()
    return {"added": added}