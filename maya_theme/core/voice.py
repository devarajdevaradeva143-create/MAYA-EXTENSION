"""Voice/AI-driven theme switching (Phase 6 placeholder).

Parses simple commands like 'Maya, change to dark glass' and maps to config changes.
"""

from __future__ import annotations

import re

from .config import load_config, save_config

PATTERNS = [
    (re.compile(r"dark", re.I), {"theme": {"mode": "dark"}}),
    (re.compile(r"light", re.I), {"theme": {"mode": "light"}}),
    (re.compile(r"glass (on|enable)", re.I), {"glass": {"enabled": True}}),
    (re.compile(r"glass (off|disable)", re.I), {"glass": {"enabled": False}}),
    (re.compile(r"blur (up|increase|more)", re.I), None),  # handled specially
]


def handle_command(text: str) -> dict:
    text = text.strip()
    cfg = load_config()
    applied = []
    for pat, changes in PATTERNS:
        if pat.search(text):
            if changes:
                for section, vals in changes.items():
                    cfg.setdefault(section, {}).update(vals)
                applied.append(pat.pattern)
    # blur intensity
    m = re.search(r"blur\s+(\d+)", text, re.I)
    if m:
        cfg.setdefault("glass", {})["blur"] = int(m.group(1))
        applied.append("blur value")
    if "more" in text.lower() or "increase" in text.lower():
        cfg.setdefault("glass", {})["blur"] = min(40, cfg["glass"].get("blur", 28) + 4)
        applied.append("blur+")
    if "less" in text.lower() or "decrease" in text.lower():
        cfg.setdefault("glass", {})["blur"] = max(0, cfg["glass"].get("blur", 28) - 4)
        applied.append("blur-")
    if applied:
        save_config(cfg)
        from .install import apply_config

        apply_config(cfg)
        return {"success": True, "applied": applied}
    return {"success": False, "error": "command not recognized"}