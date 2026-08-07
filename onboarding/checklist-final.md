# Checklist final — antes del GO

> Revisa esto con tu agente ANTES de activar la publicación automática. Todo debe estar en orden.

## ✅ Conectores
- [ ] X conectado (check verde)
- [ ] LinkedIn conectado (check verde)
- [ ] (Opcional) TikTok / YouTube conectados

## ⚙️ Configuración
- [ ] `config/platforms.yaml` creado con tus plataformas, idiomas y best-hours
- [ ] `config/cadence.yaml` creado con tu cadencia
- [ ] `config/topics.yaml` con tus temas y keywords
- [ ] `config/secrets.env` rellenado (webhook Slack, etc.) — **no en el repo**
- [ ] `auto_publish` en **false** (aún)

## 🧠 Skills y agentes
- [ ] Skills creados desde `skills/` (los 4)
- [ ] Agentes creados desde `agents/` (el equipo)
- [ ] `PROMPTS-1-9.md` disponible por si hay que recalibrar

## 🤖 Automatización
- [ ] Cron Research: cada 4h
- [ ] Cron Publish: cada 1h (dentro de best-hours)
- [ ] Cron Reporte diario (Slack/Telegram)

## 🧪 Test en falso (obligatorio)
- [ ] `auto_publish: false`
- [ ] Ejecutado 1 ciclo de prueba
- [ ] Revisado el primer borrador (copy X + LinkedIn + imagen)
- [ ] Mi OK explícito

## 🚀 GO
- [ ] `auto_publish: true`
- [ ] Primer post publicado correctamente
- [ ] Aviso recibido en Slack/Telegram

---

> Cuando todo esté marcado, el motor funciona solo. Tú solo supervisas el reporte diario.