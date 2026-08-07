# Guía de instalación y configuración — Skills de calidad y producción

> Esta guía explica cómo instalar y adaptar las **6 skills de calidad/producción** del repo con TUS propios datos. Sigue el orden: primero lee, luego sustituye los `{placeholders}`, luego instala, luego prueba.

**Archivos:** `skills/*.md` → `linkedin-post-quality-checklist`, `linkedin-prepublish-qa`, `shorts-production-qa`, `native-spanish-short-production`, `avatar-talking-head-shorts`, `higgsfield-avatar-video`.

---

## 1. Cómo se instalan (en Supercomputer)

Estas skills se crean en tu **Higgsfield Supercomputer** (Skills). El agente del `PROMPT-0` puede crearlas automáticamente leyendo los archivos de `skills/`. Para hacerlo manualmente:

1. Abre tu chat de **Supercomputer**.
2. Pide: *"Crea las skills leyendo los archivos de `skills/` en el repo `linkedin-x-automator`, sustituyendo los `{placeholders}` con mi configuración."*
3. El agente rellena tus datos y crea cada skill.

> Si prefieres crearlas tú a mano: copia el contenido de cada `.md`, reemplaza los `{placeholders}` y guárdala como skill.

---

## 2. Los placeholders que tienes que rellenar

Antes de instalar, define estos valores (los usarás en varias skills):

| Placeholder | Qué es | Ejemplo |
|---|---|---|
| `{IDIOMA_LI}` | Idioma de LinkedIn | `spanish` |
| `{TONO}` | Tono de tu marca en LinkedIn | `narrativo, profesional, educativo` |
| `{MAX_CHARS_LI}` | Máx caracteres LinkedIn | `3000` |
| `{VOICE_ID}` | Tu voz clonada (de la voz del canal) | el id de tu elemento de voz |
| `{ENGINE}` | Motor TTS (ElevenLabs/MiniMax/Seed Speech) | `elevenlabs` |
| `{MAX_CREDITOS_SHORT}` | Límite de créditos por short | `50` |
| `{CREDITOS_CLIP}` | Créditos por clip talking-head | `7.5` |

---

## 3. Skill por skill — qué configurar

### 3.1 `linkedin-post-quality-checklist` (gate de calidad de posts)
- **Sustituye:** `{IDIOMA_LI}`, `{TONO}`, `{MAX_CHARS_LI}`.
- **Ajusta los criterios** si tu sector lo exige (p. ej. añade "cumplimiento regulatorio" si es finanzas/salud).
- **Umbral:** el 7.5 por defecto; súbelo si quieres más exigencia (8-8.5) o bájalo si estás empezando.

### 3.2 `linkedin-prepublish-qa` (QA antes de publicar)
- **Sustituye:** `{IDIOMA_LI}`, `{TONO}`.
- Este es el **último gate** antes de publicar. No lo saltes.

### 3.3 `shorts-production-qa` (producción de shorts 9:16)
- **Sustituye:** `{MAX_CREDITOS_SHORT}`.
- **Ajusta los gates** de QA (G1-G5) a tu estándar visual.
- **Cámbiale los modelos** si quieres otros (p. ej. un modelo de avatar distinto).

### 3.4 `native-spanish-short-production` (voz nativa)
- **Sustituye:** `{VOICE_ID}`, `{ENGINE}`.
- **Pon TU voz clonada** en `{VOICE_ID}` (el elemento de voz del canal). Es la clave para que la narración suene nativa.

### 3.5 `avatar-talking-head-shorts` (short con tu avatar)
- **Sustituye:** `{VOICE_ID}`, `{MAX_CREDITOS_SHORT}`.
- Usa tu **imagen canónica** del avatar (plano medio, boca cerrada, mirando a cámara).

### 3.6 `higgsfield-avatar-video` (videos largos con tu avatar)
- **Sustituye:** `{VOICE_ID}`, `{CREDITOS_CLIP}`.
- **Nota de coste:** los videos largos se montan encadenando clips (~15s máx cada uno). Divide tu guion en bloques y genera clip a clip.

---

## 4. Verificación tras instalar

Después de instalar las 6, comprueba que funcionan:

1. **QA de LinkedIn:** pide al agente que evalúe un borrador con `linkedin-post-quality-checklist` → debe devolver un score 0-10 por sección.
2. **Prepublish:** pide evaluar un post listo con `linkedin-prepublish-qa` → debe bloquear o aprobar.
3. **Short con voz:** pide un short corto con `native-spanish-short-production` y tu voz → verifica que la voz suena nativa.
4. **Talking-head:** pide un clip con `avatar-talking-head-shorts` → verifica identidad y lip-sync.

> Si algo falla, revisa que rellenaste bien los placeholders y que la skill quedó creada con tu configuración, no con los ejemplos.

---

## 5. Cheat-sheet rápido

```text
1. Define tus datos (tabla de placeholders).
2. Pide crear las skills desde skills/ sustituyendo placeholders.
3. Verifica cada una con una prueba (sección 4).
4. Si un placeholder quedó sin rellenar, corrígelo y recréala.
```

> **Regla de oro:** nunca pongas tus IDs/credenciales reales en el repo público. Los `{placeholders}` se sustituyen en TU Supercomputer, no en el archivo del repo.