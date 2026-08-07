#!/usr/bin/env python3
"""First run: initialize the store, seed a small signal feed, build demo drafts.
This does NOT publish (auto_publish is false by default).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from signal_pipeline import store  # noqa: E402
from signal_pipeline.sources import ingest_feed  # noqa: E402
from content_engine import builders  # noqa: E402


def demo_feed() -> list[dict]:
    return [
        {"topic": "ai_agents", "kind": "news", "title": "Agentic MCP ecosystem expands",
         "summary": "More tools adopt MCP; agent orchestration becomes the default integration layer.",
         "url": "https://example.com/agent-mcp", "published_at": "2026-08-05T00:00:00+00:00",
         "confidence": 0.8, "novelty": 0.8, "virality_potential": 0.8, "source": "web"},
        {"topic": "stocks", "kind": "market", "title": "AI capex supercycle continues",
         "summary": "Hyperscalers keep raising capex; the bet is that AI spend converts to revenue.",
         "url": "https://example.com/capex", "published_at": "2026-08-05T00:00:00+00:00",
         "confidence": 0.7, "novelty": 0.6, "virality_potential": 0.7, "source": "web"},
        {"topic": "bretton_woods", "kind": "policy", "title": "De-dollarization pace",
         "summary": "Central banks keep diversifying reserves; gold and digital assets gain share.",
         "url": "https://example.com/reserves", "published_at": "2026-08-04T00:00:00+00:00",
         "confidence": 0.6, "novelty": 0.7, "virality_potential": 0.6, "source": "web"},
    ]


def main() -> None:
    conn = store.connect()
    feed = demo_feed()
    res = ingest_feed(conn, Path(ROOT / "data" / "seed_feed.json")) if False else {"added": 0}
    # ingest directly from the in-memory list
    added = 0
    for it in feed:
        from signal_pipeline.score import score_signal
        from signal_pipeline.sources import signal_id
        scored = score_signal({**it, "id": signal_id(it["topic"], it["title"], it["published_at"])})
        if store.add_signal(conn, scored):
            added += 1
    conn.commit()
    print(f"Seeded {added} demo signals.")

    top = store.list_signals(conn, limit=5, unused_only=True)
    print("\nDemo drafts (not published):")
    for s in top:
        x = builders.build_x(s)
        li = builders.build_linkedin(s)
        print(f"\n--- [{s['topic']}] {s['title'][:50]}")
        print(f"  X (EN):      {x['body'][:100]}…")
        print(f"  LinkedIn(ES): {li['body'][:100]}…")
    conn.close()


if __name__ == "__main__":
    main()