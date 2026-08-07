"""Cliente de conexión a la BD central de contenido (higgsfield-hardness/content-db).

El growth engine escribe TODAS las señales, posts y métricas a la BD durable
trackeada en hardness. Nunca se pierde nada.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ruta a la BD central (actualizable)
HARDNESS_DB = Path("/home/user/higgsfield-hardness/content-db")


def _db():
    if HARDNESS_DB.exists():
        sys.path.insert(0, str(HARDNESS_DB))
        import db
        return db
    return None


def add_signal(sig: dict) -> bool:
    db = _db()
    if db is None:
        return False
    return db.add_signal(sig)


def add_post(post: dict) -> bool:
    db = _db()
    if db is None:
        return False
    db.add_post(post)
    return True


def add_metrics(m: dict) -> bool:
    db = _db()
    if db is None:
        return False
    db.add_metrics(m)
    return True


def add_campaign(c_id, name, signal_id, plan) -> bool:
    db = _db()
    if db is None:
        return False
    db.add_campaign(c_id, name, signal_id, plan)
    return True