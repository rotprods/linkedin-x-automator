#!/usr/bin/env python3
"""Hourly publish tick — deterministic gate for the Social Growth Engine.

SINGLE entry point for the scheduled publish job. The operator (or cron) runs
this and follows its output verbatim — it removes the manual rule-implementation
that let the old "regla 8 / best-hour ampliado" logic through.

Modes:
  python3 scripts/hourly_tick.py               # gate: prints PUBLISH manifest or BLOCKED
  python3 scripts/hourly_tick.py --pub ID      # show the exact item to publish (id)
  python3 scripts/hourly_tick.py --mark ID EXT_ID   # mark published + record + suggest commit

The GATE never publishes by itself (connectors are agent-side). It returns the
exact item + platform to publish and where the source URL goes. Correctness is
enforced here, not in the agent prompt.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from publisher import publisher  # noqa: E402
from state import queue  # noqa: E402
from state import state_store  # noqa: E402


def _gate() -> dict:
    """Return the first publishable item, or a BLOCKED descriptor.

    Scans ALL pending items in queue order and returns the first one whose
    platform is in window and passes the full guard. A blocked item does NOT
    wedge its platform: the gate skips it and tries the next pending item,
    both across platforms AND within the same platform (fixes the "first item
    blocks the whole queue" bug — previously only the first pending item per
    platform was considered, so a single bad X body/duplicate at the head of
    the queue stalled every later X post).
    """
    blocked = {"blocked": True, "reason": None, "item": None}

    # 1. Kill-switch
    if not publisher._guard():
        blocked["reason"] = "kill-switch (auto_publish=false)"
        return blocked

    # 2. Scan every pending item in order; publish the first eligible one.
    for item in queue.list_pending():
        plat = item.get("platform")
        if plat not in ("x", "linkedin"):
            continue
        if publisher.published_in_current_hour(plat):
            # 1 post/hour cadence (hard): skip this platform for the rest of the hour.
            blocked["reason"] = f"{plat}: ya se publicó un post en esta hora (cadencia 1/h)"
            continue
        if not publisher.is_optimal_hour(plat):
            blocked["reason"] = f"{plat}: fuera de ventana óptima (best_hours)"
            continue
        ok, errs = publisher.check_publishable(
            plat,
            source_url=item.get("source_url", ""),
            topic=item.get("topic", ""),
            body=item.get("body", ""),
            image_url=item.get("image_url"),
        )
        if not ok:
            blocked["reason"] = f"{plat}: " + "; ".join(errs)
            continue
        return {"blocked": False, "item": item, "platform": plat}

    blocked["reason"] = blocked.get("reason") or "no quedan ítems pendientes"
    return blocked


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pub", metavar="ID", help="mostrar el ítem pendiente dado")
    ap.add_argument("--mark", nargs=2, metavar=("ID", "EXTERNAL_ID"), help="marcar publicado + registrar")
    args = ap.parse_args()

    if args.mark:
        item_id, ext = args.mark
        item = next((i for i in queue.list_pending() if i["id"] == item_id), None)
        if not item:
            print(f"ERROR: ítem {item_id} no está pendiente en state/queue.json")
            return 1
        ok = queue.mark_published(item_id, ext)
        publisher.record_published(item["platform"], ext, item.get("topic", ""),
                                   item.get("body", ""), item.get("source_url", ""))
        print(f"MARKED platform={item['platform']} id={item_id} external_id={ext} ok={ok}")
        print("NEXT: commit + push (state/queue.json y state/published.csv)")
        return 0

    if args.pub:
        item = next((i for i in queue.list_pending() if i["id"] == args.pub), None)
        if not item:
            print(f"ERROR: ítem {args.pub} no encontrado")
            return 1
        print(f"PUBLISH platform={item['platform']} id={item['id']}")
        print(f"BODY: {item['body']}")
        print(f"SOURCE_URL: {item.get('source_url','')}")
        print(f"URL_WAY: {'reply' if item['platform']=='x' else 'end_of_body'}")
        return 0

    g = _gate()
    if g["blocked"]:
        print(f"BLOCKED: {g['reason']}")
        return 0
    it = g["item"]
    print(f"PUBLISH platform={g['platform']} id={it['id']} topic={it['topic']}")
    print(f"BODY: {it['body']}")
    print(f"SOURCE_URL: {it.get('source_url','')}")
    print(f"URL_WAY: {'reply (primer comment en X)' if g['platform']=='x' else 'al final del body'}")
    print("NEXT: publica vía conector y luego: python3 scripts/hourly_tick.py --mark <id> <external_id>")
    return 0


if __name__ == "__main__":
    sys.exit(main())