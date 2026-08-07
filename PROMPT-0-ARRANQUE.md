# PROMPT 0 — ARRANQUE DEL SOCIAL GROWTH ENGINE

> **Pégalo tal cual en tu chat de Higgsfield Supercomputer.** Este es el único prompt que necesitas. El agente hará el resto: onboarding, instalación y configuración paso a paso.

---

Antes de empezar, dime si en tu Supercomputer ya tienes el repo `linkedin-x-automator` disponible (clonado o subido). Si no, primero súbelo o clónalo y avísame cuando esté.

Cuando esté disponible, quiero que instales el **Social Growth Engine (SGE)** en mi cuenta, siguiendo exactamente estas reglas:

## 1. Onboarding primero — NUNCA publiques antes
Hazme un onboarding de **9 preguntas, UNA a la vez**, esperando mi respuesta a cada una antes de la siguiente:

1. **Plataformas** — ¿Qué redes quieres activar? (recomendado: X + LinkedIn; opcional TikTok/YouTube)
2. **Idioma** — ¿En qué idioma publico en cada red? (p. ej. X en inglés, LinkedIn en español)
3. **Objetivo** — ¿Cuántos seguidores quieres alcanzar? (p. ej. 100.000)
4. **Temas / nichos** — ¿Sobre qué quieres publicar? (lista de temas + keywords)
5. **Best-hours** — ¿En qué horas está tu audiencia? (ventana obligatoria de publicación)
6. **Cadencia** — ¿Cuántos posts al día y por red? (p. ej. X 9, LinkedIn 3)
7. **Tono de voz** — ¿Cómo suena tu marca? (directo, narrativo, educativo, humor…)
8. **Kill-switch** — ¿Publico solo o te enseño antes el borrador? (auto_publish: true o false)
9. **Avisos** — ¿Dónde te aviso de cada publicación? (Slack, Telegram, ambos)

NO publiques nada hasta que responda las 9 preguntas.

## 2. Instala leyendo el repo `linkedin-x-automator`
Cuando tenga las respuestas del onboarding, instala el sistema leyendo las plantillas del repo:

- **Skills** → crea los skills desde `skills/` (social-growth-engine, social-growth-engine-cycle, sge-publish-one-post, social-short-pipeline).
- **Agentes** → crea los subagentes desde `agents/` (growth-engine-operator, content-creator, trend-scout, social-media-strategist, campaign-launch-pad, youtube-specialist), adaptando los `{placeholders}` con mis respuestas.
- **Config** → rellena `config/platforms.example.yaml`, `config/cadence.example.yaml` y `config/topics.example.yaml` con mis respuestas del onboarding, guardándolos como `config/platforms.yaml`, `config/cadence.yaml` y `config/topics.yaml` (sin los `.example`).
- **Secrets** → copia `config/secrets.example.env` a `config/secrets.env` y dime EXACTAMENTE qué credenciales necesito darte (o qué debo configurar yo) para que funcione.

## 3. Configura MIS avisos (guíame, no hagas por mí)
Para Slack y Telegram necesito configurarlos yo. **Guíame paso a paso**:
- Si elegí Slack: abre y sigue `onboarding/slack-setup.md` — descargar la app, crear el workspace, generar el webhook, y darme el ID del canal. No avances hasta que yo confirme que lo tengo.
- Si elegí Telegram: dime qué bot/token necesito crear y cómo (usa `onboarding/telegram-setup.md` si existe) y dónde ponerlo.
- Recuerda: **mi chatId y mis credenciales NO van en el repo** — van en `config/secrets.env` (gitignored).

## 4. Conecta mis redes (guíame)
Guíame para conectar X y LinkedIn en "Social Media & Publishing" de Higgsfield (OAuth). No publiques hasta que tengan el check verde.

## 5. Programa los crons
Programa en Scheduled:
- **Research:** cada 4 horas.
- **Publish:** cada 1 hora (SOLO dentro de mis best-hours).
- **Reporte diario:** 1 vez al día (a Slack/Telegram según mi elección).

## 6. Test en falso ANTES de publicar
- Pon `auto_publish: false`.
- Ejecuta un ciclo de prueba y muéstrame el **primer borrador completo** (copy X + copy LinkedIn + imagen) para que lo revise.
- Espera mi OK explícito. Solo entonces pones `auto_publish: true`.

## 7. Reglas de oro
- **Git es la verdad**: si haces un cambio, haz commit + push en el repo de mi alumno (no en el tuyo).
- **Nunca inventes** fuentes: cada señal debe llevar URL real verificable.
- **QA obligatorio por post**: imagen 16:9 (X) / formato correcto (LinkedIn), copy ≤280 chars en X con la URL en el primer reply, sin AI-slop, dedupe a 7 días.
- **Respeto total del kill-switch** y de los best-hours.

Empieza con el onboarding. Pregúntame la primera de las 9.