"""Ingest performance metrics.

X: the connector `list_x_user_tweets` returns organic public_metrics per post
   (impressions, likes, replies, reposts, quote_count, profile_visits via expansions).
LinkedIn: no organic analytics API — track externally (post URLs + Google Sheets),
   ingested here as manual/CSV rows.
"""
from __future__ import annotations

from signal_pipeline import store


def ingest_x_metrics(conn, tweets: list[dict]) -> int:
    """tweets = list_x_user_tweets response items (each with id + public_metrics)."""
    n = 0
    for tw in tweets:
        pm = (tw.get("public_metrics") or {}) | (tw.get("non_public_metrics") or {})
        m = {
            "platform": "x",
            "post_external_id": tw.get("id"),
            "impressions": pm.get("impression_count", 0),
            "likes": pm.get("like_count", 0),
            "replies": pm.get("reply_count", 0),
            "reposts": pm.get("retweet_count", 0),
            "profile_visits": pm.get("user_profile_clicks", 0),
        }
        total = m["impressions"] or 1
        m["engagement_rate"] = round((m["likes"] + m["replies"] + m["reposts"]) / total, 4)
        store.add_metrics(conn, m)
        n += 1
    return n


def ingest_linkedin_metrics(conn, rows: list[dict]) -> int:
    """rows = [{post_external_id, impressions, likes, comments, ...}] from external tracking."""
    n = 0
    for r in rows:
        m = {
            "platform": "linkedin",
            "post_external_id": r.get("post_external_id"),
            "impressions": r.get("impressions", 0),
            "likes": r.get("likes", 0),
            "replies": r.get("comments", 0),
            "reposts": r.get("reposts", 0),
            "profile_visits": r.get("profile_visits", 0),
        }
        total = m["impressions"] or 1
        m["engagement_rate"] = round((m["likes"] + m["replies"] + m["reposts"]) / total, 4)
        store.add_metrics(conn, m)
        n += 1
    return n