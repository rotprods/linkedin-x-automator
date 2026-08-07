#!/usr/bin/env python3
"""End-to-end test del repo linkedin-x-automator.

Valida que el kit de instalación está completo, correcto y 100% sanitizado
(sin datos personales del autor). Ejecuta:

    python3 tests/e2e/test_repo.py

Sale con código 0 si todo pasa, 1 si algo falla.
"""
import os
import re
import sqlite3
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Datos personales del autor que NUNCA deben aparecer ---
FORBIDDEN = [
    "robertogort", "Roberto Ortega", "6314605296",
    "C0APPHK8GAE", "C0BNFTG1EEQ", "1A8Dmpwhh", "rot.prods",
]

# --- Archivos y carpetas obligatorios ---
REQUIRED_FILES = [
    "PROMPT-0-ARRANQUE.md", "PROMPTS-1-9.md", "README.md", "README.es.md",
    "README.en.md", "LICENSE", ".gitignore",
    "skills/social-growth-engine.md",
    "skills/social-growth-engine-cycle.md",
    "skills/sge-publish-one-post.md",
    "skills/social-short-pipeline.md",
    "agents/growth-engine-operator.md",
    "agents/content-creator.md",
    "agents/trend-scout.md",
    "agents/social-media-strategist.md",
    "agents/campaign-launch-pad.md",
    "agents/youtube-specialist.md",
    "config/platforms.example.yaml",
    "config/cadence.example.yaml",
    "config/topics.example.yaml",
    "config/secrets.example.env",
    "onboarding/cuestionario-9-preguntas.md",
    "onboarding/slack-setup.md",
    "onboarding/higgsfield-connectors.md",
    "onboarding/checklist-final.md",
    "onboarding/FAQ.md",
    "onboarding/telegram-setup.md",
    "data/schema.sql",
    # Motor (código real copiado)
    "signal_pipeline/config.py",
    "signal_pipeline/score.py",
    "signal_pipeline/sources.py",
    "signal_pipeline/store.py",
    "signal_pipeline/run_every_4h.py",
    "content_engine/builders.py",
    "content_engine/calendar.py",
    "content_engine/hooks.py",
    "publisher/publisher.py",
    "learning_loop/calibrate.py",
    "learning_loop/learn.py",
    "learning_loop/metrics.py",
    "contentdb_client.py",
    "scripts/seed_first_run.py",
    "scripts/daily_ingest.py",
    "scripts/daily_report.py",
    "scripts/hourly_tick.py",
    # Config runtime (con placeholders)
    "config/platforms.yaml",
    "config/cadence.yaml",
    "config/topics.yaml",
]

REQUIRED_DIRS = ["skills", "agents", "config", "onboarding", "data", "state",
                 "tests", "signal_pipeline", "content_engine", "publisher",
                 "learning_loop", "scripts"]


def walk_files(root):
    out = []
    for dirpath, _dirnames, filenames in os.walk(root):
        if ".git" in dirpath or "__pycache__" in dirpath:
            continue
        for f in filenames:
            out.append(os.path.join(dirpath, f))
    return out


def check_structure():
    errors = []
    for d in REQUIRED_DIRS:
        if not os.path.isdir(os.path.join(REPO, d)):
            errors.append(f"Falta carpeta: {d}")
    for f in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(REPO, f)):
            errors.append(f"Falta archivo: {f}")
    return errors


def check_sanitized():
    errors = []
    for absf in walk_files(REPO):
        rel = os.path.relpath(absf, REPO)
        # El propio test contiene los strings para detectarlos: se auto-excluye
        if rel == "tests/e2e/test_repo.py":
            continue
        try:
            text = open(absf, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for pid in FORBIDDEN:
            if pid in text:
                errors.append(f"Dato personal detectado ('{pid}') en {rel}")
        # Los secrets reales no deben estar commiteados
        if rel == "config/secrets.env":
            errors.append("config/secrets.env no debe estar commiteado")
    return errors


def check_placeholders():
    """Los archivos de config DEBEN tener placeholders {TU_...} o {IDIOMA_...}."""
    errors = []
    for f in ["config/platforms.example.yaml", "config/cadence.example.yaml",
              "config/topics.example.yaml"]:
        text = open(os.path.join(REPO, f), encoding="utf-8").read()
        if "{TU_" not in text and "{IDIOMA_" not in text and "{TEMA_" not in text:
            errors.append(f"{f} no contiene placeholders de tipo {{TU_...}}")
    return errors


def check_schema():
    """El schema.sql debe poder crear las tablas en una DB limpia."""
    errors = []
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        con = sqlite3.connect(db_path)
        con.executescript(open(os.path.join(REPO, "data/schema.sql"), encoding="utf-8").read())
        tables = {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        for t in ["signals", "queue", "metrics", "topics"]:
            if t not in tables:
                errors.append(f"Falta tabla {t} en el schema")
        con.close()
    except Exception as e:
        errors.append(f"Schema SQL inválido: {e}")
    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass
    return errors


def check_prompt0():
    """PROMPT-0 debe pedir onboarding de 9 preguntas y test con kill-switch."""
    errors = []
    text = open(os.path.join(REPO, "PROMPT-0-ARRANQUE.md"), encoding="utf-8").read()
    for needle in ["9 preguntas", "auto_publish", "onboarding", "kill-switch",
                   "Test en falso"]:
        if needle.lower() not in text.lower():
            errors.append(f"PROMPT-0 no menciona: {needle}")
    return errors


def main():
    all_errors = []
    checks = [
        ("Estructura", check_structure),
        ("Sanitización (sin datos personales)", check_sanitized),
        ("Placeholders en config", check_placeholders),
        ("Esquema SQLite", check_schema),
        ("PROMPT-0 completo", check_prompt0),
    ]
    failed = 0
    for name, fn in checks:
        errs = fn()
        if errs:
            failed += 1
            print(f"❌ {name}:")
            for e in errs:
                print(f"   - {e}")
        else:
            print(f"✅ {name}: OK")
    # Ver también que git está limpio de secrets
    out = subprocess.run(["git", "-C", REPO, "status", "--porcelain"],
                         capture_output=True, text=True).stdout.strip()
    print(f"ℹ️  git status: {'limpio' if not out else out}")
    print("")
    if failed:
        print(f"RESULTADO: {len(all_errors)} errores — FALLÓ")
        return 1
    print("RESULTADO: TODOS LOS TESTS PASAN ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())