# Autoprovisionamiento — el agente provisiona tu motor

> Guía técnica para que el agente del alumno (en Supercomputer) monte el motor completo: repo, código, DB, subagentes y tools. El alumno solo hace los clics de conexión; el agente hace el resto.

---

## 1. Repo del alumno

El alumno necesita un repo propio (el motor vive ahí). Dos vías:

### A) Clonar la base (recomendado para empezar)
```bash
git clone https://github.com/rotprods/linkedin-x-automator.git mi-motor
cd mi-motor
git remote set-url origin https://github.com/{TU_USUARIO}/mi-motor.git   # apunta a TU repo
git push -u origin main
```
→ El alumno hereda plantillas, skills, motor y config. Después lo personaliza.

### B) Start desde cero
1. Crear un repo vacío en la cuenta del alumno (GitHub).
2. Copiar el contenido de `linkedin-x-automator` (los archivos, no `.git`).
3. `git init` → commit → push.

## 2. Instalar el motor (.py)

El motor es Python 3.11 + SQLite. Verifica que está en su sitio y que importa:

```bash
# dependencias
pip install pyyaml

# verificar que los módulos importan (desde la raíz del repo)
python3 -c "import signal_pipeline.config, signal_pipeline.store, content_engine.builders, publisher.publisher, learning_loop.metrics, contentdb_client, state.queue; print('motor OK')"
```

Estructura esperada:
```
signal_pipeline/   # investigación de señales cada 4h
content_engine/    # señales → posts + imágenes
publisher/         # publicación X/LinkedIn
learning_loop/     # métricas + aprendizaje
state/             # cola + estado (queue, state_store)
scripts/           # seed, reportes, ticks
contentdb_client.py
```

## 3. Sembrar la DB

```bash
mkdir -p data state
sqlite3 data/signals.db < data/schema.sql   # crea tablas signals, queue, metrics, topics
# o desde Python:
python3 -c "import sqlite3; con=sqlite3.connect('data/signals.db'); con.executescript(open('data/schema.sql').read()); print('DB OK')"
```

## 4. Config (rellenar placeholders antes de correr)

El agente debe crear los configs runtime desde los `.example`:
```bash
cp config/platforms.example.yaml config/platforms.yaml
cp config/cadence.example.yaml  config/cadence.yaml
cp config/topics.example.yaml   config/topics.yaml
cp config/secrets.example.env   config/secrets.env
```
Y reemplazar `{placeholders}` con las respuestas del onboarding del alumno.

> ⚠️ `config/secrets.env` está gitignored: ahí van las credenciales del alumno, nunca en el repo.

## 5. Configurar subagentes (AI employees)

Desde `agents/` el agente crea los 6 AI employees (growth-engine-operator, content-creator, trend-scout, social-media-strategist, campaign-launch-pad, youtube-specialist), sustituyendo `{placeholders}`. Cada employee se registra en el sistema de Supercomputer (agentes) con su prompt de rol.

## 6. Conectar tools / connectors

El agente verifica que las tools del motor están disponibles:
- **X y LinkedIn** → conectores OAuth (ver `conectar-tools.md`).
- **Slack / Telegram** → avisos (ver `slack-setup.md` / `telegram-setup.md`).
- **web_search / trend research** → investigación de señales.

## 7. Verificación final

```bash
python3 scripts/seed_first_run.py      # seed + audit
python3 signal_pipeline/run_every_4h.py --dry-run   # un ciclo sin publicar
python3 tests/e2e/test_repo.py         # QA del repo
```
Todo debe arrancar sin errores. Después se programa cron (FASE 5 de PROMPT-0) y se hace el test en falso antes del GO.

---

> **Regla de oro:** el agente NO publica nada con `auto_publish: false`. Y si algo requiere gastar créditos, dicme el coste exacto y espera mi OK.