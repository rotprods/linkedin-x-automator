# GOAL — Kit 100% autónomo instalable para el alumno (linkedin-x-automator)

- **Definición de completado** (DoD):
  - PROMPT-0 guía al agente del alumno a hacer TODO autónomamente: onboarding de 9 preguntas → conectar tools/connectors (X, LinkedIn, Slack, Telegram, web) → crear las 10 skills → configurar los 6 AI employees → clonar/crear su propio repo → instalar el motor (.py) → seed DB → programar crons → test en falso → GO.
  - Repo incluye: `autoprovisionamiento.md`, `conectar-tools.md`, `scripts/setup_autonomo.py`, PROMPT-0 reescrito con 6 fases, PROMPTS-1-9 actualizado con runners.
  - 100% sanitizado (0 datos personales), test e2e verde, motor verificado end-to-end (ciclo research local con auto_publish:false).
- **Estado actual**: COMPLETADO ✅ (2026-08-07)
- **Tarea actual**: ninguno (goal cerrado).
- **Próximas**: ninguna.
- **Bloqueos / cancelados**: g10 cancelado — "conectar tools reales del alumno y GH Actions" no aplica (repo plantilla público; cada alumno conecta sus propias tools en su cuenta).
- **Historial de logros**:
  - g02 GOAL-STATE.md con DoD.
  - g03 PROMPT-0-ARRANQUE.md reescrito: 6 fases autónomas (onboarding → tools → skills/agentes → provisión motor → crons → test/GO).
  - g04 onboarding/autoprovisionamiento.md (repo, .py, DB, subagentes).
  - g05 onboarding/conectar-tools.md (X, LinkedIn, Slack, Telegram, web).
  - g06 scripts/setup_autonomo.py (idempotente, verificado: estructura OK, motor importa, DB creada).
  - g07 PROMPTS-1-9 actualizado (PROMPT 0b + runners en crons).
  - g08 Motor verificado end-to-end (run_every_4h, auto-publish false), test e2e verde, 0 datos personales.
  - g09 Commit + push `4334381`.