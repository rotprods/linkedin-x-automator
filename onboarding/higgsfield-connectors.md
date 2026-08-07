# Conectar tus redes en Higgsfield (OAuth)

> Para que el motor publique por ti, primero tiene que acceder a tus cuentas. El agente te guía; tú haces los clics.

---

## X (Twitter)
1. En tu Supercomputer de Higgsfield, ve a **Connectors** (o "Social Media & Publishing").
2. Busca **X** y pulsa **Conectar**.
3. Se abre la autorización de X en una pestaña nueva → pulsa **"Authorize app"**.
4. Vuelve a Higgsfield → el conector debe mostrar **check verde** ✓.

## LinkedIn
1. En **Connectors** → busca **LinkedIn** → **Conectar**.
2. Autoriza con tu cuenta de LinkedIn → **Permitir**.
3. Vuelve → **check verde** ✓.

## (Opcional) TikTok / YouTube
1. Repite el mismo proceso si quieres activar TikTok o YouTube.
2. **Nota:** TikTok requiere un paso extra de consentimiento humano en cada publicación.

## Si no aparece la ventana de autorización
- Pulsa **"Reopen it"** para volver a abrirla.
- Si sigue sin aparecer, revisa que no tengas bloqueado el pop-up en el navegador.

## Verificación
- Confirma al agente que X y LinkedIn tienen **check verde**.
- El agente NO publicará nada hasta que estén conectados y con `auto_publish: false`.

---

> ⚠️ Conectar la cuenta autoriza al motor a publicar en tu nombre. Por eso el kill-switch viene en `false` por defecto: tú das el GO cuando confíes.