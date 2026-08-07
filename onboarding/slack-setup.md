# Configurar Slack para los avisos del SGE

> Guía paso a paso para que el alumno configure Slack por su cuenta. El agente le guía, pero el alumno hace los clics (es su cuenta y sus credenciales).

---

## 1. Crea tu cuenta / workspace de Slack
1. Ve a [slack.com](https://slack.com) y pulsa **"Try Slack"** (o "Crear un workspace").
2. Introduce tu email y pulsa **Continuar**.
3. Revisa tu correo y pulsa el **enlace de verificación** que te envía Slack.
4. Inventa un nombre para tu workspace (ej. `mi-sge`).
5. Pulsa **Crear workspace**.
6. Invita a las personas que quieras (puedes saltártelo → "Hacer esto más tarde"). Tu workspace está listo.

## 2. Crea un canal para los avisos
1. En la barra lateral izquierda, pulsa el **+** junto a "Canales" (o "Channel").
2. Pulsa **Crear un canal** (Create channel).
3. Ponle un nombre, p. ej. `#sge-notif`.
4. Pulsa **Crear** → **Listo**.

## 3. Obten el ID del canal (Channel ID)
1. Haz clic con el botón derecho (o clic en el nombre) sobre tu canal `#sge-notif`.
2. Pulsa **Copiar enlace** o selecciona **"Ver detalles del canal"** (View channel details).
3. Abajo, en **Detalles**, verás el **Channel ID** (una cadena, ej. `C0XXXXXXXX`).
4. Cópialo: es el valor que corresponde a `{TU_SLACK_CHANNEL_ID}` en `config/cadence.yaml`.

## 4. Crea un Incoming Webhook (para que el motor pueda escribir)
1. Entra en [api.slack.com/apps](https://api.slack.com/apps) (con la misma cuenta).
2. Pulsa **Create New App** → **From scratch**.
3. Ponle nombre (ej. `sge-motor`) y elige tu workspace.
4. Pulsa **Create App**.
5. En el menú izquierdo → **Incoming Webhooks** → pulsa **Activate Incoming Webhooks** (interruptor ON).
6. Pulsa **Add New Webhook to Workspace**.
7. Elige el canal `#sge-notif` → **Allow**.
8. Copia la **Webhook URL** (empieza por `https://hooks.slack.com/services/...`).
9. Esa URL va en `SLACK_WEBHOOK_URL` dentro de `config/secrets.env` (¡no en el repo!).

## 5. Verifica con el agente
- Confirma al agente que ya tienes el **Channel ID** y la **Webhook URL**.
- El agente los guardará en la configuración local (no en el repo público) y hará un test de envío.

---

> ⚠️ **Seguridad:** el Channel ID y la Webhook URL son tuyos. Nunca los subas al repo público `linkedin-x-automator`. Van en `config/secrets.env` (gitignored).