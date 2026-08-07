"""Build platform-native posts from a signal.

X (EN): tight, opinionated, hook-driven, 280 chars, punchy.
LinkedIn (ES): narrative, value-first, 800-1500 chars, question to drive comments.
Same insight, different angle — never a verbatim copy.
"""
from __future__ import annotations

import uuid

from content_engine import hooks


def _x_post(sig: dict, pattern: str, fields: dict) -> str:
    hook = hooks.render(pattern, fields)
    insight = sig.get("summary") or sig.get("title", "")
    url = sig.get("url", "")

    body = f"{hook}\n\n{insight}"
    if url:
        body += f"\n\n{url}"

    # Trim to 280 chars, keeping the hook and url if possible.
    if len(body) > 280:
        body = body[:270].rsplit(" ", 1)[0] + "…"
    return body


def _linkedin_post(sig: dict, pattern: str, fields: dict) -> str:
    hook = hooks.render(pattern, fields)
    insight = sig.get("summary") or sig.get("title", "")
    url = sig.get("url", "")

    lines = [
        hook,
        "",
        insight,
        "",
        "Lo más interesante no es el dato en sí, sino lo que implica para quien construye con IA.",
        "Tres implicaciones rápidas:",
        "1. ",
        "2. ",
        "3. ",
        "",
        "¿Qué lectura le das tú? Dejadme vuestra opinión en los comentarios.",
    ]
    if url:
        lines.insert(2, f"Fuente: {url}")
    return "\n".join(lines)


def build_x(sig: dict, pattern: str | None = None) -> dict:
    pattern = pattern or hooks.pick_pattern()
    fields = {"topic": sig.get("topic", "AI"), "consensus": "the obvious narrative",
              "prediction": "this accelerates", "horizon": "12 months",
              "thing": sig.get("topic", "it"), "story": sig.get("title", "this"),
              "situation": sig.get("topic", "the market"), "task": "the workflow",
              "actor": "builder", "industry": "AI"}
    return {"id": str(uuid.uuid4()), "language": "english", "hook": hooks.render(pattern, fields),
            "body": _x_post(sig, pattern, fields)}


def build_linkedin(sig: dict, pattern: str | None = None) -> dict:
    pattern = pattern or hooks.pick_pattern()
    fields = {"topic": sig.get("topic", "IA"), "consensus": "la narrativa obvia",
              "prediction": "esto se acelera", "horizon": "12 meses",
              "thing": sig.get("topic", "esto"), "story": sig.get("title", "esto"),
              "situation": sig.get("topic", "el sector"), "task": "el flujo",
              "actor": "creador", "industry": "IA"}
    return {"id": str(uuid.uuid4()), "language": "spanish", "hook": hooks.render(pattern, fields),
            "body": _linkedin_post(sig, pattern, fields)}