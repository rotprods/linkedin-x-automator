"""Signal scoring: freshness, novelty, virality potential, confidence.

Score = weighted sum fed into the content engine. The learning loop later
reweights topics based on real performance.
"""
from __future__ import annotations

from datetime import datetime, timezone


def _parse_dt(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def freshness(published_at: str | None, half_life_hours: float = 12.0) -> float:
    """Decay to 0.5 after half_life_hours. Fresh news scores high."""
    dt = _parse_dt(published_at)
    if not dt:
        return 0.5
    age_h = (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0
    return 1.0 / (1.0 + age_h / half_life_hours)


def narrative_score(sig: dict) -> float:
    """Reward signals that fit the brand's narrative (AI/business/finance)."""
    topics = {"ai", "business", "stocks", "crypto", "bretton_woods", "ai_tools",
              "ai_agents", "ai_engineering", "vibecoding_marketing_branding"}
    return 1.0 if sig.get("topic") in topics else 0.3


def score_signal(sig: dict, weights: dict | None = None) -> dict:
    w = weights or {"freshness": 0.30, "novelty": 0.25, "virality": 0.25, "narrative": 0.20}

    fresh = freshness(sig.get("published_at"))
    novelty = float(sig.get("novelty", 0.5))          # 0..1 (set by researcher)
    virality = float(sig.get("virality_potential", 0.5))  # 0..1 (researcher estimate)
    narr = narrative_score(sig)

    score = (w["freshness"] * fresh + w["novelty"] * novelty
             + w["virality"] * virality + w["narrative"] * narr)

    return {
        **sig,
        "freshness": round(fresh, 3),
        "novelty": round(novelty, 3),
        "virality_potential": round(virality, 3),
        "score": round(score, 3),
        "confidence": round(float(sig.get("confidence", 0.5)), 3),
    }