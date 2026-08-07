#!/usr/bin/env python3
"""One 4-hour research cycle.

Usage:
    python3 -m signal_pipeline.run_every_4h [--feed path/to/feed.json]

In autonomous mode the scheduled job performs live research and writes the feed;
a research subagent can also drop a feed file here. This orchestrator ingests,
scores, stores, and prints a digest of top signals for the content engine.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from signal_pipeline import store  # noqa: E402
from signal_pipeline import config as cfg  # noqa: E402
from signal_pipeline.sources import ingest_feed, ingest_x_timeline  # noqa: E402
from contentdb_client import add_signal as db_add_signal  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", default=None, help="JSON feed of raw signals")
    args = ap.parse_args()

    plat = cfg.platforms()
    cad = cfg.cadence()
    conn = store.connect()

    result = ingest_feed(conn, args.feed) if args.feed else {"added": 0, "skipped": 0, "total": 0}

    # Escribir todas las señales nuevas a la BD central (durable)
    for s in store.list_signals(conn, limit=500):
        db_add_signal(s)

    top = store.list_signals(conn, limit=int(cad["pipeline_4h"].get("digest_n", 10)), unused_only=True)
    print(f"Cycle complete. Feed: {result}")
    print(f"Auto-publish: {plat['auto_publish']}")
    print(f"Top unused signals:")
    for s in top:
        print(f"  [{s['score']:.2f}] {s['topic']:>28} | {s['title'][:80]}")
    conn.close()


if __name__ == "__main__":
    main()