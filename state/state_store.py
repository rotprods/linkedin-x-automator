"""Durable state store (tracked, survives clones).

The SQLite DB under data/ is gitignored and lost on every fresh clone, so the
durable source of truth for metrics, followers and published posts lives here
in TRACKED CSV files under state/ (committed to git). Scripts append to these;
the DB remains a fast per-run cache.
"""
from __future__ import annotations

import csv
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

STATE_DIR = Path(__file__).resolve().parent

FOLLOWERS_CSV = STATE_DIR / "followers.csv"
PUBLISHED_CSV = STATE_DIR / "published.csv"
METRICS_CSV = STATE_DIR / "metrics.csv"


def _ensure(path: Path, header: list[str]) -> None:
    if not path.exists():
        path.write_text(",".join(header) + "\n", encoding="utf-8")


def _append(path: Path, row: list) -> None:
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)


def now_iso() -> str:
    return datetime.now(ZoneInfo("Europe/Madrid")).isoformat(timespec="seconds")


# ── Followers over time (#16) ─────────────────────────────────────────────
def log_follower(platform: str, count: int, at: str | None = None) -> None:
    _ensure(FOLLOWERS_CSV, ["date", "platform", "followers"])
    _append(FOLLOWERS_CSV, [at or now_iso(), platform, count])


def read_followers(platform: str | None = None) -> list[dict]:
    if not FOLLOWERS_CSV.exists():
        return []
    with open(FOLLOWERS_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows if not platform else [r for r in rows if r.get("platform") == platform]


# ── Published posts (#4, #7 dedupe) ────────────────────────────────────────
def log_published(post: dict) -> None:
    header = ["date", "platform", "external_id", "topic", "body", "source_url"]
    _ensure(PUBLISHED_CSV, header)
    _append(PUBLISHED_CSV, [
        now_iso(), post.get("platform", ""), post.get("post_external_id", ""),
        post.get("topic", ""), (post.get("body") or "")[:80], post.get("source_url", ""),
    ])


def read_published() -> list[dict]:
    if not PUBLISHED_CSV.exists():
        return []
    with open(PUBLISHED_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def already_published(platform: str, topic: str = "", source_url: str = "", window_days: int = 7) -> bool:
    """Dedupe by source_url (the real insight identity), falling back to topic.

    Topic-only dedupe was too broad — it blocked every 2nd post of a topic
    (7x ai_agents, 3x crypto) even when the insight was distinct. Prefer the
    source URL; only use topic when no source exists.
    """
    rows = read_published()
    for r in rows:
        if r.get("platform") != platform:
            continue
        if source_url and r.get("source_url") and source_url in r["source_url"]:
            return True
        if not source_url and topic and r.get("topic") == topic:
            return True
    return False


# ── Metrics (#12) ──────────────────────────────────────────────────────────
def log_metrics(m: dict) -> None:
    header = ["date", "platform", "post_external_id", "impressions", "likes", "replies", "reposts"]
    _ensure(METRICS_CSV, header)
    _append(METRICS_CSV, [
        now_iso(), m.get("platform", ""), m.get("post_external_id", ""),
        m.get("impressions", 0), m.get("likes", 0), m.get("replies", 0), m.get("reposts", 0),
    ])


def read_metrics() -> list[dict]:
    if not METRICS_CSV.exists():
        return []
    with open(METRICS_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))