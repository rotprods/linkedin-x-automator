# LinkedIn · X Automator

**Un motor de agentes de IA que publica por ti en X (Twitter) y LinkedIn, de forma autónoma.** Investiga cada 4 horas, puntúa señales virales, escribe el copy, genera la imagen, publica solo y aprende de los resultados. De **0 a 100.000 seguidores**.

> 🎓 **Para alumnos:** este repo es un **kit de instalación autónoma**. Solo necesitas pegar UN prompt en tu Supercomputer de Higgsfield y el agente hace el onboarding, la instalación y la configuración paso a paso.

---

## 🚀 Arranque en 3 pasos (para el alumno)

### 1. Crea tu cuenta en Higgsfield
Ve a [higgsfield.ai](https://higgsfield.ai) y entra en **Supercomputer** ("Automation, skills, apps and more").

### 2. Sube o clona este repo a tu Supercomputer
```
git clone https://github.com/rotprods/linkedin-x-automator.git
```
(O súbelo directamente desde tu Supercomputer si no usas git.)

### 3. Pega el PROMPT-0
Abre un chat en tu Supercomputer y pega el contenido de **[`PROMPT-0-ARRANQUE.md`](PROMPT-0-ARRANQUE.md)**.

El agente te hará un **onboarding de 9 preguntas**, instalará los skills y subagentes, te guiará a configurar Slack y conectar tus redes, programará los crons, hará un **test en falso** y solo publicará cuando tú des el **GO**.

---

## 📦 Qué incluye

| Ruta | Contenido |
|---|---|
| `PROMPT-0-ARRANQUE.md` | El prompt que pegas para instalarlo todo |
| `PROMPTS-1-9.md` | Prompts de refuerzo por fase |
| `skills/` | Los 10 skills del motor y de calidad/producción (plantillas) |
| `agents/` | El equipo de subagentes (plantillas) |
| `config/` | Configuración (platforms, cadence, topics, secrets) |
| `onboarding/` | Guías paso a paso (Slack, Telegram, conectores, checklist, cuestionario, FAQ, skills-produccion) |
| `signal_pipeline/` | **Motor**: investigación de señales cada 4h |
| `content_engine/` | **Motor**: señales → posts + imágenes |
| `publisher/` | **Motor**: publicación X/LinkedIn + anti-duplicados |
| `learning_loop/` | **Motor**: métricas + aprendizaje dinámico |
| `scripts/` | Seed inicial, reportes, ticks |
| `data/schema.sql` | Esquema SQLite (sin datos) |
| `tests/` | Test end-to-end del repo |

## 🧠 Cómo funciona (en simple)

1. **Investiga** cada 4h → señales virales con fuente real.
2. **Puntúa** 0-100 y elige las mejores.
3. **Genera** imagen 16:9 + copy (X en inglés, LinkedIn en español).
4. **Encola** → **publica** dentro de tus best-hours.
5. **Mide** y **aprende**: repondera temas según el engagement.

## 🧪 Test del repo
Puedes validar que el kit está completo y sin datos personales:
```bash
python3 tests/e2e/test_repo.py
```
Verifica: estructura, sanitización (0 datos personales), placeholders en config, esquema SQLite y que el PROMPT-0 esté completo.

## 🛡️ Seguridad
- **Kill-switch:** `auto_publish: false` por defecto → el motor solo encola, nunca publica hasta que TÚ des el GO.
- **Tus credenciales** (webhooks, chatId, tokens) van en `config/secrets.env` (gitignored) — **nunca en el repo público**.
- **Fuentes reales** con URL verificable. Nada inventado.

## ⚙️ Stack
- Python 3.11 + SQLite · Higgsfield Supercomputer (skills, agents, connectors, crons)
- Publicación vía OAuth (X + LinkedIn) · Avisos Slack/Telegram

## 📄 Licencia
MIT — libre para uso educativo y personal.

> **¿Dudas?** Consulta primero `onboarding/checklist-final.md` y `onboarding/cuestionario-9-preguntas.md`. El agente te guía en todo el proceso.