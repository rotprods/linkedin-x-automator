# Guía para rellenar todos los placeholders

> Esta guía te dice cómo sustituir **cada** `{placeholder}` del repo con TUS datos. Hubo un orden: primero prepara tus valores, luego rellena los configs, luego los skills y agentes. Al final ejecuta la verificación.

---

## 0. Prepara ANTES de empezar (tabla maestra)

Rellena esta tabla con tus datos. La usarás para todo.

| Tu dato | Dónde lo consigues | Ejemplo |
|---|---|---|
| **Handle de X** | Tu perfil de X (Twitter) | `@tuusuario` |
| **Nombre** | Tu nombre real / marca | `María García` |
| **Zona horaria** | [time.is](https://time.is) o tu país | `Europe/Madrid` |
| **Horas buenas X** | Las horas donde tu audiencia está activa | `08:00, 12:00, 18:00` |
| **Horas buenas LinkedIn** | Ídem para LinkedIn | `09:00, 13:00, 17:00` |
| **Idioma X** | El idioma de tus posts en X | `english` (X suele ir en inglés) |
| **Idioma LinkedIn** | El idioma de tus posts en LinkedIn | `spanish` |
| **Objetivo seguidores** | Tu meta | `100000` |
| **ChatId Telegram** | `onboarding/telegram-setup.md` paso 2 | `123456789` |
| **Canal Slack / ID** | `onboarding/slack-setup.md` pasos 2-3 | `#sge-notif` / `C0123ABCD` |
| **Voz clonada (`VOICE_ID`)** | Tu voz en Higgsfield (elemento de voz del canal) | el id UUID del elemento |
| **Motor de voz (`ENGINE`)** | Qué motor TTS usas | `elevenlabs` |
| **Max chars LinkedIn** | Límite de caracteres | `3000` |
| **Max créditos short** | Presupuesto por short | `50` |
| **Créditos por clip** | Coste real de un clip talking-head | `7.5` |
| **Idiomas extra (YT/TikTok)** | Si vas a usar esas redes | `spanish` |

> ⚠️ `VOICE_ID` y todos tus datos van solo en TU config/secrets.env local — **nunca en el repo público**.

---

## 1. Configs runtime (`config/`)

Estos archivos ya existen (los creó `setup_autonomo.py` o vienen con el repo). Edítalos y sustituye cada placeholder.

### 1.1 `config/platforms.yaml`

| Placeholder | Sustituye por |
|---|---|
| `{IDIOMA_X}` | Tu idioma de X (ej. `english`) |
| `{TU_HANDLE_X}` | Tu handle de X (ej. `@tuusuario`) |
| `{TU_TIMEZONE}` | Tu zona horaria (ej. `Europe/Madrid`) |
| `{TUS_BEST_HOURS}` | Horas buenas de X, lista (ej. `08:00, 12:00, 18:00`) |
| `{IDIOMA_LI}` | Tu idioma de LinkedIn (ej. `spanish`) |
| `{TU_NOMBRE}` | Tu nombre/marca |
| `{TUS_BEST_HOURS_LI}` | Horas buenas de LinkedIn |
| `{IDIOMA_YT}` | Idioma de YouTube (si activo) |
| `{IDIOMA_TK}` | Idioma de TikTok (si activo) |
| `{TU_ACCOUNT_TK}` | Tu cuenta de TikTok (si activo) |

### 1.2 `config/cadence.yaml`

| Placeholder | Sustituye por |
|---|---|
| `{TU_TIMEZONE}` | Tu zona horaria |
| `{TU_CHAT_ID_TELEGRAM}` | Tu chatId de Telegram |
| `{TU_CANAL_SLACK}` | Nombre de tu canal Slack (ej. `sge-notif`) |
| `{TU_SLACK_CHANNEL_ID}` | El ID de tu canal Slack |

### 1.3 `config/topics.yaml`

| Placeholder | Sustituye por |
|---|---|
| `{TEMA_1}`, `{TEMA_2}`, `{TEMA_3}` | Tus temas (ej. `ai`, `business`, `crypto`) |
| `keyword1`... | Las keywords reales de cada tema |
| `angle1`... | Los ángulos o enfoques de cada tema |

---

## 2. Skills y agentes (`skills/`, `agents/`)

Al crear las skills desde `skills/` (FASE 3 del PROMPT-0), el agente sustituye estos placeholders:

| Placeholder | Sustituye por | Dónde aparece |
|---|---|---|
| `{IDIOMA_X}` | Idioma de X | skills, agents |
| `{IDIOMA_LI}` | Idioma de LinkedIn | skills, agents |
| `{TONO}` | Tono de tu marca (narrativo, directo...) | skills de LinkedIn |
| `{MAX_CHARS_LI}` | Máx caracteres LinkedIn (3000) | skills de LinkedIn |
| `{BEST_HOURS}` | Tus horas buenas | agents |
| `{OBJETIVO_SEGUIDORES}` | Tu meta de seguidores | agents |
| `{VOICE_ID}` | Tu voz clonada (elemento de voz) | skills de voz |
| `{ENGINE}` | Motor TTS (`elevenlabs`, etc.) | skill nativa en español |
| `{MAX_CREDITOS_SHORT}` | Presupuesto por short | skills de shorts |
| `{CREDITOS_CLIP}` | Coste real por clip talking-head | skill avatar-video |

---

## 3. Verificar que quedó bien

Tras rellenar todo, ejecuta la verificación automática:

```bash
python3 scripts/setup_autonomo.py
```

- Si dice **"Placeholders: configs resueltos"** → todo listo.
- Si dice **"PLACEHOLDERS PENDIENTES"** → te dice exactamente qué placeholder sigue sin rellenar y en qué archivo. Búscalo en esta guía y complétalo.

Después, el test del repo:
```bash
python3 tests/e2e/test_repo.py
```

---

## 4. Cheat-sheet rápido

```text
1. Prepara tu tabla maestra (sección 0).
2. Edita config/platforms.yaml, cadence.yaml, topics.yaml.
3. Crea skills y agentes con tus placeholders.
4. python3 scripts/setup_autonomo.py  → confirma "configs resueltos".
5. python3 tests/e2e/test_repo.py     → confirma "TODOS LOS TESTS PASAN".
```

> **Regla de oro:** tus datos de identidad y credenciales (`VOICE_ID`, `TU_HANDLE_X`, chatId, webhooks) solo viven en tu config local / `secrets.env` (gitignored). El repo público del curso queda sin datos tuyos.