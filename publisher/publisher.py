"""Publishing layer with kill-switch guard + dedupe + char-count validation.

The Python layer validates and logs posts; the orchestrating agent executes the
actual API calls through the platform connectors (X, LinkedIn). Durable record
goes to the tracked state store (survives clones).

The hourly tick MUST call ``check_publishable`` before any API call so the
guards here are actually enforced (previously the cron bypassed this module).
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from signal_pipeline import config as cfg  # noqa: E402
from state import queue  # noqa: E402
from state import state_store  # noqa: E402

X_MAX_CHARS = 280
MAD = ZoneInfo("Europe/Madrid")

# Detects URLs with or without a protocol (bare domains like siliconangle.com/...).
_URL_RE = re.compile(
    r"(?:https?://|www\.|(?<![@\w])[a-z0-9-]+\.(?:com|co|news|io|ai|org|net|eu|dev|blog|media|gov|uk|kr|cn|es|me|xyz|app|site|link|ly|it|to)/)\S+",
    re.IGNORECASE,
)


def _guard() -> bool:
    return bool(cfg.platforms().get("auto_publish", False))


def _count_x_chars(text: str) -> int:
    """X counts any URL as 23 chars, whether or not it carries a protocol."""
    return len(_URL_RE.sub("X" * 23, text))


def validate_x(text: str) -> list[str]:
    """Char-count validation for X (fixes #9)."""
    # X counts URLs as 23 chars; detect bare domains too (no https:// prefix),
    # which the previous regex missed and let 5 posts >280 chars slip through.
    n = _count_x_chars(text)
    if n > X_MAX_CHARS:
        return [f"X post is {n} chars (max {X_MAX_CHARS})"]
    return []


def dedupe_check(platform: str, source_url: str | None = None, topic: str = "") -> bool:
    """True if this platform already published the same source/topic (fixes #7).

    Dedupes by source_url (the real insight identity) first, falling back to
    topic only when no source is present. Topic-only dedupe was too broad and
    blocked legitimately distinct posts (7x ai_agents, 3x crypto, ...).
    """
    if source_url:
        return state_store.already_published(platform, source_url=source_url)
    if topic:
        return state_store.already_published(platform, topic=topic)
    return False


def record_published(platform: str, external_id: str, topic: str, body: str, source_url: str = "") -> None:
    """Persist a published post to the durable state store."""
    state_store.log_published({
        "platform": platform, "post_external_id": external_id,
        "topic": topic, "body": body, "source_url": source_url,
    })


def is_optimal_hour(platform: str) -> bool:
    """True if the current Madrid hour is inside this platform's best_hours.

    best_hours are HOUR WINDOWS (1 post/hora cadence): a slot like "16:00"
    covers the whole 16:xx hour, and "12:30"/"21:30" mark the hour 12/21.
    Matches by hour, consistent with content_engine/calendar.is_optimal_hour.
    """
    plat = cfg.platforms().get("platforms", {}).get(platform, {})
    slots = plat.get("best_hours", [])
    if not slots:
        return True
    cur_hour = datetime.now(MAD).strftime("%H")
    return any(int(s.split(":")[0]) == int(cur_hour) for s in slots)


def can_publish(platform: str, source_url: str = "", topic: str = "", image_url: str | None = None) -> tuple[bool, list[str]]:
    """Pre-publish gate: kill-switch + dedupe (image is a warning, not a blocker)."""
    errors: list[str] = []
    if not _guard():
        errors.append("auto_publish is false (kill-switch)")
    if dedupe_check(platform, source_url=source_url, topic=topic):
        errors.append(f"duplicate: {platform}/{topic} already published")
    return (len(errors) == 0, errors)


def check_publishable(platform: str, source_url: str = "", topic: str = "",
                      body: str = "", image_url: str | None = None) -> tuple[bool, list[str]]:
    """Full guard the hourly tick MUST run before publishing.

    Combines: kill-switch + dedupe + best_hours (HARD window) + X 280-char
    validation. Image is only a warning (returned but non-blocking). Returns
    (ok, errors).
    """
    errors: list[str] = []
    warnings: list[str] = []
    ok, gate_errors = can_publish(platform, source_url=source_url, topic=topic, image_url=image_url)
    errors += gate_errors
    if not image_url and platform in ("x", "linkedin"):
        warnings.append(f"{platform}: sin imagen (recomendado 16:9, no bloqueante)")
    if not is_optimal_hour(platform):
        errors.append(f"{platform}: fuera de la ventana óptima (best_hours)")
    if platform == "x" and body:
        errors += validate_x(body)
    return (not errors, errors + warnings)


def require_image16x9(platform: str) -> bool:
    return platform in ("x", "linkedin")


def published_in_current_hour(platform: str) -> bool:
    """True if a post was already published on this platform in the current hour.

    Enforces the 1 post/hour cadence in code (the obraje once fired a burst of
    posts in a few minutes). published_at strings are stored as Madrid wall-clock
    (naive or +02:00 aware), so comparing the first 13 chars against the current
    Madrid 'YYYY-MM-DDTHH' is correct for both forms.
    """
    cur_hh = datetime.now(MAD).strftime("%Y-%m-%dT%H")
    for it in queue.list_published():
        if it.get("platform") != platform:
            continue
        pa = it.get("published_at", "")
        if pa and pa[:13] == cur_hh:
            return True
    return False