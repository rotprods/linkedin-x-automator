# FAQ — Preguntas frecuentes del Social Growth Engine

> Las dudas más comunes al instalar y usar el `linkedin-x-automator`. Si no encuentras tu respuesta, consulta `checklist-final.md` o repite el `PROMPT-0`.

---

## 💸 Costes y créditos

**¿Cuánto cuesta montar esto?**
El software es gratis (MIT). Los costes son los **créditos de Higgsfield** por generación de imágenes (nano_banana_pro) y por los reels verticales del short-pipeline (~33 créditos/reel). El flujo de textos (investigar, escribir) no gasta créditos de media.

**¿Puedo probarlo sin gastar créditos?**
Sí. Con `auto_publish: false` el motor solo ENCOLA drafts: no genera imagen de pago ni publica. Puedes ver el copy antes de gastar nada.

## 🛡️ Seguridad y control

**¿El motor publica solo desde el primer día?**
No. Viene con `auto_publish: false`. Hasta que tú no lo pongas en `true` (tras revisar un test en falso), **nunca publica nada**.

**¿Qué pasa si quiero pararlo?**
Pon `auto_publish: false` en `config/platforms.yaml`. Al instante, el motor deja de publicar y solo encola. Es el kill-switch.

**¿Mis credenciales están seguras?**
Sí, si las pones en `config/secrets.env` (que está en `.gitignore`). Nunca van en el repo público. El repo oficial ya viene **100% sanitizado** (verificado por test).

**¿Puede inventarse fuentes?**
No. Cada señal debe llevar una URL real verificable. Si no hay fuente, no se publica.

## 🧠 Funcionamiento

**¿Qué pasa si un tema no funciona?**
El **learning loop** lo detecta por las métricas y **reduce su peso** en la balanza. Los temas que rinden ganan peso. El motor se recalibra solo cada ciclo de aprendizaje (7 días).

**¿Cuántos posts hace al día?**
Depende de tu `cadence.yaml`. Por defecto: X 9 + LinkedIn 3, dentro de tus best-hours. Puedes cambiarlo.

**¿Publica a cualquier hora?**
No. Solo dentro de tus **best-hours** (ventana obligatoria). Nunca publica fuera de esa ventana.

**¿Qué es el "test en falso"?**
Con `auto_publish: false` el motor prepara el primer borrador (copy X + LinkedIn + imagen) y te lo muestra. Tú lo revisas y, si está bien, das el GO. Es el paso de confianza antes de la publicación real.

## 🔌 Conexiones

**¿Necesito saber programar?**
No. El `PROMPT-0` lo configura todo. Solo respondes 9 preguntas y haces los clics de conectar (OAuth) y Slack.

**¿Qué necesito para los avisos de Slack?**
Crea un workspace gratis, un canal (ej. `#sge-notif`), copia el **Channel ID** y crea un **Incoming Webhook** (ver `slack-setup.md`). Todo gratis.

**¿Puedo añadir TikTok o YouTube después?**
Sí. Conecta la plataforma en Higgsfield y activa el `enabled: true` en `config/platforms.yaml`. El motor lo soporta.

## 🐛 Problemas comunes

**El conector no muestra check verde.**
Reabre la ventana de autorización ("Reopen it") y revisa que el navegador no bloquee pop-ups.

**No llegan avisos a Slack.**
Verifica que pusiste la **Webhook URL** en `config/secrets.env` y que el canal ID es correcto. Haz un envío de prueba con el agente.

**El motor encola pero no publica.**
Comprueba que estás dentro de best-hours y que `auto_publish: true`. Si está fuera de la ventana, espera al siguiente slot.

## 📚 Más ayuda
- `cuestionario-9-preguntas.md` — qué te preguntará el agente
- `slack-setup.md` — configuración de Slack paso a paso
- `higgsfield-connectors.md` — conectar X y LinkedIn
- `checklist-final.md` — verificación antes del GO