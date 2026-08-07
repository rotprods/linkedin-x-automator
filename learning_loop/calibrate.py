"""Conecta el growth engine al calibrador central (gradient descent en higgsfield-hardness).

Cada post publicado con métricas reales se convierte en un datapoint
(componentes del score predictivo + rendimiento real) que alimenta el gradient
descent central. Los pesos resultantes viven en higgsfield-hardness y se usan
en todos los chats.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from state import state_store  # noqa: E402
except ImportError:
    # copia de seguridad si state_store no es importable
    state_store = None

# Ruta al calibrador central (actualizable)
HARDNESS_CALIB = Path("/home/user/higgsfield-hardness/content-pipeline/calibration")


def _load_calibrator():
    if HARDNESS_CALIB.exists():
        sys.path.insert(0, str(HARDNESS_CALIB))
        import calibrate  # noqa: F401
        return calibrate
    return None


def _components_from_body(body: str) -> dict:
    """Proxy de componentes desde el texto (sin llamar al scorer completo)."""
    import re
    t = (body or "").lower()
    has_num = bool(re.search(r"\d", t))
    return {
        "arousal": 0.5 if any(w in t for w in ["engañ", "malicioso", "atac", "pérdida", "crash", "record", "récord", "hack"]) else 0.3,
        "data": 1.0 if has_num else 0.3,
        "curiosity_gap": 0.5 if any(w in t for w in ["nadie", "lo que nadie", "secret", "por qué", "why"]) else 0.35,
        "novelty_timing": 0.6,
        "authority": 0.6,
        "preference": 0.7,
    }


def sync_to_calibrator(min_engagement: float = 0.0) -> dict:
    """Lee published+metrics del state, genera datapoints y corre calibrate()."""
    cal = _load_calibrator()
    if cal is None:
        return {"status": "calibrator_not_found"}
    if state_store is None:
        return {"status": "no_state_store"}

    published = state_store.read_published()
    metrics = state_store.read_metrics()
    by_id = {m.get("post_external_id"): m for m in metrics}

    added = 0
    for p in published:
        eid = p.get("post_external_id")
        m = by_id.get(eid)
        if not m:
            continue
        impressions = int(m.get("impressions", 0) or 0)
        if impressions <= 0:
            continue
        eng = (int(m.get("likes", 0) or 0) + int(m.get("replies", 0) or 0) + int(m.get("reposts", 0) or 0)) / impressions
        actual = max(0.0, min(1.0, eng * 20))  # normalize engagement → 0-1
        if actual < min_engagement:
            continue
        comps = _components_from_body(p.get("body", ""))
        cal.add_datapoint(comps, actual, {"topic": p.get("topic"), "platform": p.get("platform")})
        added += 1

    res = cal.calibrate(steps=25)
    return {"status": "ok", "added_datapoints": added, "calibration": res}


if __name__ == "__main__":
    import json
    print(json.dumps(sync_to_calibrator(), ensure_ascii=False, indent=2))