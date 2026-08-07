# PROMPT 0 — ARRANQUE AUTÓNOMO DEL SOCIAL GROWTH ENGINE

> **Pégalo tal cual en tu chat de Higgsfield Supercomputer.** Es el ÚNICO prompt que necesitas. Tu agente hace TODO el resto: onboarding, conectar herramientas, instalar skills y agentes, provisionar el motor, programar crons y configurar avisos — paso a paso, guiándote.

---

## Contexto inmediato
Recién he subido/clonado el repo `linkedin-x-automator` a mi Supercomputer. Antes de empezar:
1. **Localiza el repo** en mi workspace (búscalo; si no está, dime exactamente cómo lo subo o clóno).
2. Lee `GOAL-STATE.md` y `README.es.md` para conocer el sistema.
3. Arranca el **onboarding** (abajo) — UNA pregunta a la vez.

Quiero que conviertas este repo en **mi motor de crecimiento autónomo** para X y LinkedIn, y que lo hagas TODO tú. No publiques nada hasta el GO final.

---

## FASE 1 — Onboarding (9 preguntas, UNA a la vez)
Hazme estas preguntas de una en una, esperando mi respuesta antes de la siguiente:

1. **Plataformas** — ¿Qué redes quiero activar? (recomendado: X + LinkedIn; opcional TikTok/YouTube)
2. **Idioma** — ¿En qué idioma publico en cada red? (p. ej. X en inglés, LinkedIn en español)
3. **Objetivo** — ¿Cuántos seguidores quiero? (p. ej. 100.000)
4. **Temas / nichos** — ¿Sobre qué quiero publicar? (lista + keywords)
5. **Best-hours** — ¿En qué horas está mi audiencia? (ventana obligatoria)
6. **Cadencia** — ¿Cuántos posts al día y por red? (p. ej. X 9, LinkedIn 3)
7. **Tono de voz** — ¿Cómo suena mi marca? (directo, narrativo, educativo, humor…)
8. **Kill-switch** — ¿Publico solo, o me enseñas antes el borrador? (auto_publish true/false)
9. **Avisos** — ¿Dónde te aviso? (Slack, Telegram, ambos)

NO hagas nada más hasta responder las 9.

---

## FASE 2 — Conectar herramientas y herramientas (tools/connectors)
Guíame y verifíca cada conexión (lee `onboarding/conectar-tools.md`):

1. **X** — conectar en "Social Media & Publishing" (OAuth) → check verde.
2. **LinkedIn** — conectar (OAuth) → check verde.
3. **(Opcional)** TikTok / YouTube.
4. **Avisos**:
   - Si Slack: abre y sigue `onboarding/slack-setup.md` (crear workspace, canal, webhook, channel ID). No avances hasta que yo confirme que lo tengo.
   - Si Telegram: sigue `onboarding/telegram-setup.md` (BotFather, token, chat_id).
5. **Verifica que tus tools de investigación** (web_search / trend research) están disponibles. Si falta algo, dímelo.

## FASE 3 — Instalar skills y configurar AI employees
1. **Skills** → crea los **10 skills** leyendo `skills/` (social-growth-engine, social-growth-engine-cycle, sge-publish-one-post, social-short-pipeline, linkedin-post-quality-checklist, linkedin-prepublish-qa, shorts-production-qa, native-spanish-short-production, avatar-talking-head-shorts, higgsfield-avatar-video), sustituyendo los `{placeholders}` con mis respuestas. Sigue `onboarding/skills-produccion-setup.md` para las de calidad/producción.
2. **AI employees (subagentes)** → configura los **6** desde `agents/` (growth-engine-operator, content-creator, trend-scout, social-media-strategist, campaign-launch-pad, youtube-specialist), adaptando los placeholders.
3. **Config** → rellena `config/platforms.example.yaml`, `config/cadence.example.yaml`, `config/topics.example.yaml` con mis respuestas → guarda como `config/platforms.yaml`, `config/cadence.yaml`, `config/topics.yaml`.
4. **Secrets** → copia `config/secrets.example.env` a `config/secrets.env` y dime exactamente qué credenciales me toca poner a mí (sin que aparezcan en el repo).

## FASE 4 — Provisionar mi motor (repo, .py, DB)
1. **Crea/clona MI repo de alumno** (lee `onboarding/autoprovisionamiento.md`): si no tengo repo propio aún, ayúdame a clonar `linkedin-x-automator` como base y a inicializar git en mi cuenta.
2. **Instala el motor**: verifica que los `.py` (signal_pipeline/, content_engine/, publisher/, learning_loop/, state/, scripts/, contentdb_client.py) están en su sitio y que importan (Python 3.11 + `pyyaml`).
3. **Sembra la DB**: ejecuta `data/schema.sql` → `data/signals.db` (o usa `scripts/setup_autonomo.py` si lo incluí).
4. Verifica con `scripts/seed_first_run.py` o un dry-run que el motor arranca.

## FASE 5 — Programar crons
En Higgsfield **Scheduled**, programa:
- Research: cada 4 horas.
- Publish: cada 1 hora (SOLO dentro de mis best-hours).
- Reporte diario: 1 vez al día (a Slack/Telegram según mi elección).

## FASE 6 — Test en falso ANTES de publicar
- Pon `auto_publish: false`.
- Ejecuta un ciclo de prueba y muéstrame el **primer borrador completo** (copy X + LinkedIn + imagen).
- Espera mi OK explícito. Solo entonces pones `auto_publish: true`.

## Reglas de oro
- **Git es la verdad**: haz commit + push en MI repo de alumno tras cada cambio.
- **Nunca inventes** fuentes: cada señal lleva URL real verificable.
- **QA obligatorio por post**: imagen 16:9 (X) / formato correcto (LinkedIn), copy ≤280 en X con URL en el primer reply, sin AI-slop, dedupe a 7 días.
- **Respeta el kill-switch y los best-hours**.
- **Mis credenciales** (tokens, chatId, webhooks) van en `config/secrets.env` (gitignored) — nunca en el repo.
- Si algo requiere gastar créditos, **dímelo primero con el coste exacto y espera mi OK** (regla #1).

Empieza con el onboarding: pregúntame la primera de las 9.