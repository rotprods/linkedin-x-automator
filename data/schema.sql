-- Esquema SQLite del Social Growth Engine (limpio, sin datos).
-- Ejecuta con: sqlite3 data/sge.db < data/schema.sql

-- Señales detectadas en cada ciclo de investigación
CREATE TABLE IF NOT EXISTS signals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source      TEXT NOT NULL,          -- web | x_timeline | x_mentions | trend_research
    url         TEXT NOT NULL,          -- fuente real verificable
    source_name TEXT,                   -- dominio / medio
    summary     TEXT,                   -- resumen de la señal
    score       REAL,                   -- puntuación 0-100 de potencial viral
    topic       TEXT,                   -- tema asignado (de topics.yaml)
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used        INTEGER DEFAULT 0       -- si ya se convirtió en post
);

-- Cola de publicación (señales → drafts listos)
CREATE TABLE IF NOT EXISTS queue (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_id   INTEGER REFERENCES signals(id),
    platform    TEXT NOT NULL,          -- x | linkedin
    body        TEXT NOT NULL,          -- copy del post
    image_url   TEXT,                   -- imagen 16:9 generada
    status      TEXT DEFAULT 'queued',  -- queued | published | skipped
    priority    INTEGER DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

-- Métricas post-publicación (para el learning loop)
CREATE TABLE IF NOT EXISTS metrics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    queue_id    INTEGER REFERENCES queue(id),
    platform    TEXT NOT NULL,
    external_id TEXT,                   -- id del post publicado
    impressions INTEGER DEFAULT 0,
    likes       INTEGER DEFAULT 0,
    replies     INTEGER DEFAULT 0,
    retweets    INTEGER DEFAULT 0,
    engagement_rate REAL,               -- engagement / impressions
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Temas y pesos (learning loop repondera según rendimiento)
CREATE TABLE IF NOT EXISTS topics (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT UNIQUE NOT NULL,
    weight    REAL DEFAULT 1.0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_signals_score ON signals(score);
CREATE INDEX IF NOT EXISTS idx_queue_status ON queue(status);
CREATE INDEX IF NOT EXISTS idx_metrics_queue ON metrics(queue_id);