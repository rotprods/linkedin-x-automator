#!/usr/bin/env python3
"""Daily consolidation: writes durable state (followers, metrics, published),
computes topic performance (learning), and prints a report + LinkedIn sheet rows.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from signal_pipeline import store  # noqa: E402
from signal_pipeline import config as cfg  # noqa: E402
from state import state_store  # noqa: E402
from learning_loop import learn  # noqa: E402
from learning_loop.calibrate import sync_to_calibrator  # noqa: E402


def log_today(conn, x_followers: int | None = None) -> dict:
    """Persist durable state and return a summary dict."""
    # Followers history (#16)
    if x_followers is not None:
        state_store.log_follower("x", x_followers)

    # Metrics for all posts with data in the DB (#4) — dedupe: skip external_ids
    # already present in metrics.csv (the daily tick used to log duplicates).
    rows = conn.execute(
        "SELECT platform, post_external_id, impressions, likes, replies, reposts "
        "FROM metrics WHERE collected_at >= date('now','-1 day')"
    ).fetchall()
    existing = {r.get("post_external_id") for r in state_store.read_metrics()}
    for r in rows:
        if r["post_external_id"] in existing:
            continue
        state_store.log_metrics(dict(r))
        existing.add(r["post_external_id"])

    # Topic performance via learning loop (#11) — lower threshold
    min_pts = cfg.cadence().get("learning", {}).get("min_data_points", 5)
    weights = learn.compute_topic_weights(conn, min_data_points=min_pts)

    published = state_store.read_published()
    pub_x = [p for p in published if p.get("platform") == "x"]
    pub_li = [p for p in published if p.get("platform") == "linkedin"]

    return {
        "x_followers": x_followers,
        "published_x": len(pub_x),
        "published_li": len(pub_li),
        "topic_weights": weights,
    }


def main() -> None:
    conn = store.connect()
    # x_followers should be passed by the caller pulling get_x_profile; None = skip.
    summary = log_today(conn, x_followers=None)

    print("# Daily report")
    print(f"Seguidores X (último): {state_store.read_followers('x')[-1:] }")
    print(f"Publicados: X={summary['published_x']} · LinkedIn={summary['published_li']}")
    # Calibración automática (gradient descent) — pesos centrales en hardness
    cal = sync_to_calibrator()
    print(f"Calibración: {cal.get('status')} ({cal.get('added_datapoints', 0)} datapoints)")

    print(f"Topic weights (learning): {summary['topic_weights'] or 'sin datos aún'}")
    print("\nFila para hoja de LinkedIn (tracking externo):")
    print("  (el job envía a Google Sheets via connector google_sheets-upsert-row)")
    conn.close()


if __name__ == "__main__":
    main()