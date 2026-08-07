# PROMPTS DE REFUERZO (1–9)

> Usa estos prompts si quieres recalibrar o arreglar una parte del sistema sin rehacer el onboarding. Pégalos en Supercomputer cuando el caso lo pida. `{corchetes}` = tus datos.

---

## PROMPT 0b — Autoprovisionamiento del motor
Ejecuta `scripts/setup_autonomo.py --seed-db` en mi repo de alumno y verifica que: estructura OK, config runtime creada, motor importa, DB sembrada. Si hay placeholders sin resolver, dime cuáles y ayúdame a rellenarlos con mi configuración. Luego confirma que el motor arranca con `python3 signal_pipeline/run_every_4h.py --dry-run`.

## PROMPT 1 — Configurar mis plataformas e idiomas
Con mi configuración del onboarding, configura ahora mis plataformas:
- Conecta `{plataformas}` y verifica que los conectores están activos (check verde).
- `{X}`: idioma `{idioma_X}`, copy ≤280 caracteres, sin URL en el body (la fuente va en el primer reply).
- `{LinkedIn}`: idioma `{idioma_LI}`, tono narrativo, pregunta final, enlace al final del body, imagen 16:9 obligatoria.
Guarda todo en `config/platforms.yaml` y haz commit + push.

## PROMPT 2 — Definir mis temas + keywords
Crea `config/topics.yaml` con mis temas y sus keywords: `{temas}`.
Usa peso inicial uniforme. El learning loop re-ponderará cada tema según el engagement real. Cada señal debe llevar URL y fuente veraz (nada inventado).

## PROMPT 3 — Cadencia y best-hours
Crea `config/cadence.yaml`:
- best-hours: `{horarios}` (ventana OBLIGATORIA, NO publicar fuera).
- cadencia diaria: `{X: 9, LinkedIn: 3}`.
- señal-prioridad: 1 post/hora dentro de la ventana.
Guárdalo y haz commit + push.

## PROMPT 4 — Kill-switch y control de calidad
Activa el control de calidad:
- `auto_publish: {true|false}` (kill-switch global; en false solo encola, nunca publica).
- QA por post: imagen 16:9, copy ≤280 en X, fuente real, sin AI-slop, dedupe a 7 días.
Guárdalo en `config/platforms.yaml`.

## PROMPT 5 — Crear los skills
Crea los skills del motor desde las plantillas de `skills/`:
1. `social-growth-engine` (runbook completo)
2. `social-growth-engine-cycle` (ciclo de research + tick horario)
3. `sge-publish-one-post` (publica 1 post respetando kill-switch y best-hours)
4. `social-short-pipeline` (reels verticales con avatar y voz)
Usa las plantillas descargables de `skills/`.

## PROMPT 6 — Crear los subagentes
Crea los subagentes del equipo desde `agents/`:
growth-engine-operator (orquestador), content-creator, trend-scout, social-media-strategist, campaign-launch-pad, youtube-specialist. Sustituye los `{placeholders}` con mi configuración.

## PROMPT 7 — Programar los crons
Programa en Scheduled:
- Research: cada 4 horas → `python3 signal_pipeline/run_every_4h.py`.
- Publish: cada 1 hora (dentro de best-hours) → `python3 scripts/hourly_tick.py`.
- Reporte diario: 1 vez al día → `python3 scripts/daily_report.py`.
Verifica que cada runner arranca sin errores (dry-run) antes de dejarlo programado. Tras cada cambio, haz commit + push a git.

## PROMPT 8 — Configurar los avisos
Configura los avisos:
- Slack: canal `{canal}`, avisa de cada publicación y del reporte diario.
- Telegram: chatId `{chatId}` vía HTTP API.
Formato de cada aviso: `[SGE] Qué → URL · coste · fecha`.

## PROMPT 9 — Verificación final (GO / no-GO)
Verificación final:
- Revisa que conectores, config, skills y crons están listos.
- Cola vacía y configuración validada.
- Ejecuta un TEST con `auto_publish: false` y muéstrame el primer draft completo (copy + imagen).
- Espera mi OK. Solo cuando yo confirme, pon `auto_publish` en true.