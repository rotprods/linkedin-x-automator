# Skill: sge-publish-one-post

Publica UN post respetando kill-switch, best-hours y los límites de cada plataforma.

## Flujo
1. Sacar el post de mayor prioridad de la cola.
2. Validar best-hours (no publicar fuera de la ventana).
3. QA: imagen 16:9, copy ≤280 (X), fuente real, dedupe a 7 días.
4. Publicar vía conector OAuth; registrar el `external_id`.
5. Commit + push; avisar por Slack/Telegram.

## Kill-switch
- `auto_publish=false` → solo encolar, NUNCA publicar.

> Personalízalo: redes, límites de caracteres y ventana de publicación.