#!/usr/bin/env python3
"""Learning loop bootstrap from DURABLE state (CSVs), not the ephemeral SQLite.

The SQLite DB (data/signals.db) is gitignored and lost on every fresh clone, so
learning that reads only the DB silently produces nothing (learn.py bug from the
audit: metrics.csv was stuck, topic_performance empty). This script:

  1. Rebuilds the metrics table from state/metrics.csv (durable).
  2. Rebuilds the posts table from state/published.csv + state/queue.json.
  3. Computes per-topic weights (impressions-share * engagement) and returns a
     proposed reweight for config/topics.yaml.

Usage: python3 scripts/learn_from_state.py [--apply]
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from signal_pipeline import config as cfg  # noqa: E402
from signal_pipeline import store  # noqa: E402


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    apply = "--apply" in sys.argv
    conn = store.connect()

    # 1. Metrics desde el CSV durable
    metrics = _read_csv(ROOT / "state" / "metrics.csv")
    conn.execute("DELETE FROM metrics")
    for m in metrics:
        try:
            store.add_metrics(conn, {
                "platform": m.get("platform", "x"),
                "post_external_id": m.get("post_external_id", ""),
                "impressions": int(m.get("impressions") or 0),
                "likes": int(m.get("likes") or 0),
                "replies": int(m.get("replies") or 0),
                "reposts": int(m.get("reposts") or 0),
                "profile_visits": 0,
                "engagement_rate": None,
            })
        except Exception:
            continue

    # 2. Posts desde published.csv + queue.json (ambos durables)
    posts = _read_csv(ROOT / "state" / "published.csv")
    try:
        queue_items = json.loads((ROOT / "state" / "queue.json").read_text(encoding="utf-8"))
    except Exception:
        queue_items = []
    conn.execute("DELETE FROM posts")
    for p in posts:
        store.add_post(conn, {
            "id": f"csv-{p.get('date','')}-{p.get('external_id','')}",
            "signal_id": None, "platform": p.get("platform", "x"),
            "language": "en" if p.get("platform") == "x" else "es",
            "topic": p.get("topic", ""), "hook": "", "body": p.get("body", ""),
            "image_url": "", "status": "published",
            "post_external_id": p.get("external_id", ""), "metrics": None,
            "created_at": p.get("date", ""), "published_at": p.get("date", ""),
        })
    for qi in queue_items:
        if qi.get("status") == "published":
            store.add_post(conn, {
                "id": f"queue-{qi['id']}", "signal_id": None,
                "platform": qi.get("platform", "x"),
                "language": "en" if qi.get("platform") == "x" else "es",
                "topic": qi.get("topic", ""), "hook": "", "body": qi.get("body", ""),
                "image_url": qi.get("image_url", ""), "status": "published",
                "post_external_id": qi.get("external_id", ""), "metrics": None,
                "created_at": qi.get("created_at", ""), "published_at": qi.get("published_at", ""),
            })

    # 3. Calcular pesos
    min_pts = cfg.cadence().get("learning", {}).get("min_data_points", 5)
    weights = None
    from learning_loop import learn
    weights = learn.compute_topic_weights(conn, min_data_points=min_pts)

    print(f"posts={len(posts)} metrics={len(metrics)} min_data_points={min_pts}")
    if not weights:
        print("NO hay datos suficientes por topic para reweight (umbral no alcanzado).")
        conn.commit()
        return 0

    print("PESOS PROPUESTOS por topic (topics.yaml):")
    for t, w in sorted(weights.items(), key=lambda kv: -kv[1]):
        print(f"  {t:30} -> {w}")

    if apply:
        learn.apply_weights(conn)
        print("APLICADO a topic_performance (BD).")
    conn.commit()
    return 0


if __name__ == "__main__":
    sys.exit(main())