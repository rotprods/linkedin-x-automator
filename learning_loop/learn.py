"""Learning loop: reweight topics/hook-patterns from real performance.

Run weekly (config: learning.cadence_days). Reads aggregated metrics per topic
and writes weights back to topic_performance so the content engine biases
toward what actually works.
"""
from __future__ import annotations

from signal_pipeline import config as cfg
from signal_pipeline import store


def compute_topic_weights(conn, min_data_points: int = 5) -> dict[str, float]:
    """Returns {topic: weight} rebased so the best topic = 1.0."""
    rows = conn.execute(
        """
        SELECT p.topic,
               COUNT(*)                                   AS n,
               SUM(m.impressions)                          AS imp,
               AVG(m.engagement_rate)                      AS er
        FROM posts p
        JOIN metrics m ON m.post_external_id = p.post_external_id
        WHERE m.impressions > 0
        GROUP BY p.topic
        """
    ).fetchall()

    agg = {r["topic"]: {"n": r["n"], "impressions": r["imp"] or 0, "er": r["er"] or 0.0}
           for r in rows if r["n"] >= min_data_points}
    if not agg:
        return {}

    # Score topic = impressions-share * engagement-rate, normalized.
    total_imp = sum(v["impressions"] for v in agg.values()) or 1
    scored = {t: (v["impressions"] / total_imp) * (1 + v["er"] * 10) for t, v in agg.items()}
    best = max(scored.values()) or 1.0
    return {t: round(s / best, 2) for t, s in scored.items()}


def apply_weights(conn) -> dict[str, float]:
    weights = compute_topic_weights(conn)
    for topic, w in weights.items():
        store.upsert_topic_performance(conn, topic, {"weight": w, "posts": 0,
                                                     "impressions": 0, "engagement_rate": 0.0})
    return weights


def report(conn) -> str:
    lines = ["# Learning report", f"(min_data_points={cfg.cadence()['learning']['min_data_points']})", ""]
    for topic, perf in store.load_topic_performance(conn).items():
        lines.append(f"- {topic}: weight={perf['weight']} posts={perf['posts']} imp={perf['impressions']}")
    return "\n".join(lines) or "No topic performance yet."