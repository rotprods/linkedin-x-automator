"""Load YAML config from config/ into dicts."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"


def load(name: str) -> dict:
    with open(CONFIG_DIR / name, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def topics() -> dict:
    return load("topics.yaml")


def platforms() -> dict:
    return load("platforms.yaml")


def cadence() -> dict:
    return load("cadence.yaml")