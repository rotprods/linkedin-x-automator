#!/usr/bin/env python3
"""Ingest real X metrics + followers into the durable state (reactivates the loop).

The daily metrics tick was dead (metrics.csv stuck at 2026-08-06 06:01:30,
followers.csv had a single row). This script appends real numbers pulled from
the X connector into state/metrics.csv and state/followers.csv so the learning
loop and daily report have fresh data.

Usage (after the agent pulls list_x_user_tweets + get_x_profile):
    python3 scripts/metrics_ingest.py --metrics '{"<tweet_id>": [impressions,likes,replies,reposts], ...}'
    python3 scripts/metrics_ingest.py --followers X 54
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from state import state_store  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", default="", help='JSON dict {tweet_id: [imp,l,re,rt]}')
    ap.add_argument("--followers", nargs=2, metavar=("PLATFORM", "COUNT"), default=None)
    args = ap.parse_args()

    if args.metrics:
        data = json.loads(args.metrics)
        for tid, m in data.items():
            imp, likes, replies, reposts = (list(m) + [0, 0, 0, 0])[:4]
            state_store.log_metrics({
                "platform": "x", "post_external_id": tid,
                "impressions": imp, "likes": likes, "replies": replies, "reposts": reposts,
            })
            print(f"  metrics x/{tid}: {imp} imp, {likes} likes, {replies} re, {reposts} rt")

    if args.followers:
        plat, count = args.followers
        state_store.log_follower(plat, int(count))
        print(f"  followers {plat}: {count}")

    print("metrics.csv rows:", len(state_store.read_metrics()))
    print("followers.csv rows:", len(state_store.read_followers()))
    print("NEXT: commit + push (state/metrics.csv y state/followers.csv)")
    return 0


if __name__ == "__main__":
    sys.exit(main())