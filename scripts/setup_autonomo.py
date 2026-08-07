#!/usr/bin/env python3
"""Provisión autónoma idempotente del Social Growth Engine.

Ejecuta el agente (o el alumno) tras pegar PROMPT-0. Verifica la estructura,
crea configs runtime desde los .example si faltan, siembra la DB y comprueba
que el motor importa. Es seguro repetirlo: no rompe configs existentes.

Uso:  python3 scripts/setup_autonomo.py [--seed-db]
"""
from __future__ import annotations

import argparse
import importlib
import os
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
STATE_DIR = ROOT / "state"

# placeholders que deben quedar resueltos antes de correr
PLACEHOLDERS = ["{TU_", "{IDIOMA_", "{TEMA_", "{TU_HANDLE", "{TU_NOMBRE",
                "{TU_TIMEZONE", "{TUS_BEST_HOURS", "{TU_CHAT_ID", "{TU_CANAL",
                "{TU_SLACK_CHANNEL_ID", "{VOICE_ID}", "{ENGINE}", "{"]

CONFIG_PAIRS = [
    ("platforms.example.yaml", "platforms.yaml"),
    ("cadence.example.yaml", "cadence.yaml"),
    ("topics.example.yaml", "topics.yaml"),
]


def check_structure() -> list[str]:
    missing = []
    for d in ["signal_pipeline", "content_engine", "publisher", "learning_loop",
              "state", "scripts", "config", "data", "skills", "agents", "onboarding"]:
        if not (ROOT / d).is_dir():
            missing.append(f"carpeta faltante: {d}")
    for f in ["contentdb_client.py", "data/schema.sql", "PROMPT-0-ARRANQUE.md",
              "signal_pipeline/config.py", "publisher/publisher.py"]:
        if not (ROOT / f).is_file():
            missing.append(f"archivo faltante: {f}")
    return missing


def ensure_configs() -> list[str]:
    created = []
    for src, dst in CONFIG_PAIRS:
        s = CONFIG_DIR / src
        d = CONFIG_DIR / dst
        if not d.exists():
            if s.exists():
                shutil.copy(s, d)
                created.append(dst)
            else:
                created.append(f"FALTA {src}")
    # secrets.env (gitignored) — solo si no existe
    if not (CONFIG_DIR / "secrets.env").exists():
        if (CONFIG_DIR / "secrets.example.env").exists():
            shutil.copy(CONFIG_DIR / "secrets.example.env", CONFIG_DIR / "secrets.env")
    DATA_DIR.mkdir(exist_ok=True)
    STATE_DIR.mkdir(exist_ok=True)
    return created


def ensure_db() -> str:
    db = DATA_DIR / "signals.db"
    if not db.exists():
        con = sqlite3.connect(db)
        con.executescript((DATA_DIR / "schema.sql").read_text(encoding="utf-8"))
        con.commit()
        con.close()
        return f"creada {db.name}"
    return f"ya existe {db.name}"


def check_imports() -> list[str]:
    fails = []
    sys.path.insert(0, str(ROOT))
    mods = ["signal_pipeline.config", "signal_pipeline.store", "signal_pipeline.score",
            "signal_pipeline.sources", "content_engine.hooks", "content_engine.calendar",
            "content_engine.builders", "publisher.publisher", "learning_loop.metrics",
            "learning_loop.learn", "learning_loop.calibrate", "contentdb_client",
            "state.queue", "state.state_store"]
    for m in mods:
        try:
            importlib.import_module(m)
        except Exception as e:
            fails.append(f"{m}: {type(e).__name__}: {e}")
    return fails


def check_placeholders() -> list[str]:
    """Advierte si un config runtime aún tiene placeholders sin resolver."""
    warns = []
    for _src, dst in CONFIG_PAIRS:
        p = CONFIG_DIR / dst
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for ph in PLACEHOLDERS:
            if ph in text:
                warns.append(f"{dst} aún contiene '{ph}...' — rellenar con tus datos")
                break
    return warns


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-db", action="store_true", help="crear la DB si falta")
    args = parser.parse_args()

    ok = True
    missing = check_structure()
    if missing:
        ok = False
        print("❌ ESTRUCTURA:")
        for m in missing:
            print(f"   - {m}")
    else:
        print("✅ Estructura: OK")

    created = ensure_configs()
    bad = [c for c in created if c.startswith("FALTA")]
    if bad:
        ok = False
        print("❌ CONFIG:")
        for b in bad:
            print(f"   - {b}")
    else:
        print(f"✅ Config runtime: {'creados ' + ', '.join(created) if created else 'ya presentes'}")

    if args.seed_db:
        print(f"✅ DB: {ensure_db()}")

    fails = check_imports()
    if fails:
        ok = False
        print("❌ IMPORTS:")
        for f in fails:
            print(f"   - {f}")
    else:
        print("✅ Motor: todos los módulos importan")

    warns = check_placeholders()
    if warns:
        print("⚠️  PLACEHOLDERS PENDIENTES:")
        for w in warns:
            print(f"   - {w}")
        ok = False
    else:
        print("✅ Placeholders: configs resueltos")

    print("")
    print("RESULTADO:", "PROVISIÓN COMPLETA ✅" if ok else "REVISAR ❌")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())