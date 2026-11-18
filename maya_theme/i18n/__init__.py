"""i18n helpers."""

from __future__ import annotations

import json
from pathlib import Path

I18N_DIR = Path(__file__).parent


def load(lang: str = "en") -> dict:
    p = I18N_DIR / f"{lang}.json"
    if not p.exists():
        p = I18N_DIR / "en.json"
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def t(key: str, lang: str = "en", default: str = "") -> str:
    data = load(lang)
    cur = data
    for part in key.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default or key
    return cur if isinstance(cur, str) else (default or key)