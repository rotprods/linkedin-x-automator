# Configurar Telegram para los avisos del SGE

> Guía paso a paso para que el alumno configure los avisos de Telegram por su cuenta. El agente le guía, pero el alumno hace los clics (es su cuenta y su token).

---

## 1. Crea tu bot con BotFather
1. Abre Telegram y busca **@BotFather** (cuenta oficial).
2. Pulsa **Start** (o escribe `/start`).
3. Escribe `/newbot`.
4. Ponle un nombre al bot (ej. `mi-sge-avisos`).
5. Ponle un **username** que termine en `bot` (ej. `mi_sge_avisos_bot`).
6. BotFather te devuelve un **token** (ej. `123456789:AAF...`). **Guárdalo** — es la clave de tu bot.

## 2. Obten tu chat_id (el número al que te avisa)
1. Abre un chat con tu bot recién creado y envíale cualquier mensaje (ej. `hola`).
2. Abre en el navegador: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
   (sustituye `<TU_TOKEN>` por el token del paso 1).
3. Verás un JSON con tus mensajes. Busca el campo `"chat":{"id":<numero>}`.
   Ese **número** es tu `chat_id` (puede ser positivo o negativo).
4. Cópialo: es el valor para `{TU_CHAT_ID_TELEGRAM}` en `config/cadence.yaml`.

## 3. Dónde poner el token
- El **token** del bot va en `config/secrets.env` (campo `TELEGRAM_BOT_TOKEN`).
- El **chat_id** va en `config/cadence.yaml` (campo `telegram_chat_id`).
- **Nunca en el repo público** — van en tu configuración local (gitignored).

## 4. Verifica con el agente
- Confirma al agente que ya tienes el **token** y el **chat_id**.
- El agente hará un **envío de prueba** a tu Telegram para confirmar que llega.

---

> ⚠️ **Seguridad:** el token de tu bot y tu chat_id son tuyos. Nunca los subas al repo público `linkedin-x-automator`.