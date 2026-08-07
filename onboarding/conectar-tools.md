# Conectar las tools del motor

> Qué herramientas usa el Social Growth Engine y cómo las conecta el agente del alumno. El alumno hace los clics de autorización; el agente verifica que todo quedó activo.

---

## 1. Tools de publicación (imprescindibles)

### X (Twitter)
- **Dónde:** Higgsfield → "Social Media & Publishing" → X.
- **Cómo:** conectar (OAuth) → autorizar en la pestaña que se abre → check verde.
- **Qué permite:** leer timeline/menciones y publicar posts (con imagen/vídeo).

### LinkedIn
- **Dónde:** Higgsfield → "Social Media & Publishing" → LinkedIn.
- **Cómo:** conectar (OAuth) → autorizar → check verde.
- **Qué permite:** publicar texto, imagen, carrusel, vídeo.

## 2. Tools de avisos

### Slack
- Crea un workspace + canal (ej. `#sge-notif`).
- Obtén el **Channel ID** y crea un **Incoming Webhook** (ver `slack-setup.md`).
- El webhook va en `config/secrets.env` (`SLACK_WEBHOOK_URL`).

### Telegram
- Crea un bot con **@BotFather** → obtén el token.
- Obtén tu `chat_id` (ver `telegram-setup.md`).
- Token → `config/secrets.env` (`TELEGRAM_BOT_TOKEN`); chat_id → `config/cadence.yaml`.

## 3. Tools de investigación (opcionales pero recomendadas)

- **web_search** — buscar señales y fuentes reales.
- **trend research / trend_scout** (AI employee) — detectar qué está de moda.
- **Ad libraries** (Meta/TikTok) — si el trend-scout los usa.

## 4. Cómo verifica el agente que todo está conectado

1. Listar las tools disponibles del conector (por ejemplo, ver que X tiene `publish_x_tweet` y `list_user_tweets`).
2. Hacer una llamada de **solo lectura** a cada conector (ej. leer el perfil/timeline) para confirmar el check.
3. Reportar al alumno el estado: ✅ conectado / ❌ pendiente.
4. Si una conexión falla, guiar al alumno a reautorizarla (botón "Reopen it" si el pop-up no aparece).

## 5. Kill-switch y buenas prácticas

- Hasta que el alumno dé el **GO**, el motor va con `auto_publish: false` (solo encola).
- El agente **no gasta créditos sin permiso** (regla #1): si un paso cuesta créditos, dice el coste exacto y espera el OK.
- Las credenciales del alumno (tokens, webhooks, chatId) van en `config/secrets.env` (gitignored) — nunca en el repo.

---

> Resumen: X + LinkedIn (publicación) + Slack/Telegram (avisos) + web_search (investigación). Con eso, el motor tiene todo lo que necesita.