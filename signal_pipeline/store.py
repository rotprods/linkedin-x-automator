"""SQLite store for signals, posts, and metrics. Standard library only."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "signals.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    kind TEXT NOT NULL,            -- news | viral_post | image | policy | market | prediction
    title TEXT NOT NULL,
    summary TEXT,
    url TEXT,
    confidence REAL DEFAULT 0.0,
    score REAL DEFAULT 0.0,
    freshness REAL DEFAULT 0.0,
    novelty REAL DEFAULT 0.0,
    virality_potential REAL DEFAULT 0.0,
    source TEXT,
    published_at TEXT,
    created_at TEXT,
    used INTEGER DEFAULT 0          -- 1 if already turned into a post
);

CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    signal_id TEXT,
    platform TEXT NOT NULL,        -- x | linkedin
    language TEXT NOT NULL,
    topic TEXT,
    hook TEXT,
    body TEXT,
    image_url TEXT,
    status TEXT DEFAULT 'draft',   -- draft | queued | published | failed
    post_external_id TEXT,
    metrics TEXT,                  -- JSON doc of performance
    created_at TEXT,
    published_at TEXT
);

CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    post_external_id TEXT,
    collected_at TEXT,
    impressions INTEGER,
    likes INTEGER,
    replies INTEGER,
    reposts INTEGER,
    profile_visits INTEGER,
    engagement_rate REAL
);

CREATE TABLE IF NOT EXISTS topic_performance (
    topic TEXT PRIMARY KEY,
    weight REAL DEFAULT 1.0,
    posts INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    engagement_rate REAL DEFAULT 0.0,
    updated_at TEXT
);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def add_signal(conn: sqlite3.Connection, sig: dict) -> bool:
    """Insert a signal if not already present (dedupe by id). Returns True if new."""
    sig.setdefault("created_at", utcnow())
    cur = conn.execute(
        "INSERT OR IGNORE INTO signals "
        "(id, topic, kind, title, summary, url, confidence, score, freshness, novelty, "
        " virality_potential, source, published_at, created_at) "
        "VALUES (:id, :topic, :kind, :title, :summary, :url, :confidence, :score, "
        ":freshness, :novelty, :virality_potential, :source, :published_at, :created_at)",
        sig,
    )
    return cur.rowcount > 0


def list_signals(conn: sqlite3.Connection, limit: int = 50, unused_only: bool = False) -> list:
    q = "SELECT * FROM signals"
    if unused_only:
        q += " WHERE used = 0"
    q += " ORDER BY score DESC LIMIT ?"
    return [dict(r) for r in conn.execute(q, (limit,))]


def mark_used(conn: sqlite3.Connection, signal_id: str) -> None:
    conn.execute("UPDATE signals SET used = 1 WHERE id = ?", (signal_id,))
    conn.commit()


def add_post(conn: sqlite3.Connection, post: dict) -> None:
    post.setdefault("created_at", utcnow())
    conn.execute(
        "INSERT OR REPLACE INTO posts "
        "(id, signal_id, platform, language, topic, hook, body, image_url, status, "
        " post_external_id, metrics, created_at, published_at) "
        "VALUES (:id, :signal_id, :platform, :language, :topic, :hook, :body, :image_url, "
        ":status, :post_external_id, :metrics, :created_at, :published_at)",
        post,
    )
    conn.commit()


def list_posts(conn: sqlite3.Connection, platform: str | None = None, status: str | None = None) -> list:
    q = "SELECT * FROM posts"
    where, args = [], []
    if platform:
        where.append("platform = ?")
        args.append(platform)
    if status:
        where.append("status = ?")
        args.append(status)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY created_at DESC"
    return [dict(r) for r in conn.execute(q, args)]


def add_metrics(conn: sqlite3.Connection, m: dict) -> None:
    m.setdefault("collected_at", utcnow())
    conn.execute(
        "INSERT INTO metrics (platform, post_external_id, collected_at, impressions, likes, "
        "replies, reposts, profile_visits, engagement_rate) "
        "VALUES (:platform, :post_external_id, :collected_at, :impressions, :likes, "
        ":replies, :reposts, :profile_visits, :engagement_rate)",
        m,
    )
    conn.commit()


def load_post_metrics(conn: sqlite3.Connection, post_external_id: str) -> dict | None:
    row = conn.execute(
        "SELECT * FROM metrics WHERE post_external_id = ? ORDER BY collected_at DESC LIMIT 1",
        (post_external_id,),
    ).fetchone()
    return dict(row) if row else None


def upsert_topic_performance(conn: sqlite3.Connection, topic: str, perf: dict) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO topic_performance "
        "(topic, weight, posts, impressions, engagement_rate, updated_at) "
        "VALUES (:topic, :weight, :posts, :impressions, :engagement_rate, :updated_at)",
        {**perf, "topic": topic, "updated_at": utcnow()},
    )
    conn.commit()


def load_topic_performance(conn: sqlite3.Connection) -> dict:
    return {r["topic"]: dict(r) for r in conn.execute("SELECT * FROM topic_performance")}