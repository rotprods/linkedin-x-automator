"""Content calendar: pick which signals to publish when, respecting cadence + dedupe."""
from __future__ import annotations

from datetime import date, datetime, timedelta

from signal_pipeline import store


def pick_today(conn, per_platform: dict, min_confidence: float = 0.6) -> dict:
    """Pick signals for today's posts. Returns {platform: [signal, ...]}."""
    unused = store.list_signals(conn, limit=200, unused_only=True)
    unused = [s for s in unused if s["confidence"] >= min_confidence]

    picks = {}
    for platform, n in per_platform.items():
        picks[platform] = unused[:n]
        unused = unused[n:]
    return picks


def schedule_slots(platform_cfg: dict, target_date: date | None = None) -> list[str]:
    """Return today's posting slots sorted, based on best_hours (fixes #6)."""
    hours = platform_cfg.get("best_hours", ["09:00", "18:00"])
    return sorted(hours)


def is_optimal_hour(platform_cfg: dict, hour: int) -> bool:
    """True if the given hour (0-23 local) is within best_hours (fixes #6)."""
    slots = platform_cfg.get("best_hours", [])
    return any(int(s.split(":")[0]) == hour for s in slots)


def dedupe_check(conn, insight_key: str, window_days: int = 7) -> bool:
    """True if this insight was already posted within the window."""
    cutoff = (datetime.now() - timedelta(days=window_days)).isoformat()
    row = conn.execute(
        "SELECT 1 FROM posts WHERE body LIKE ? AND created_at > ? LIMIT 1",
        (f"%{insight_key[:40]}%", cutoff),
    ).fetchone()
    return row is not None