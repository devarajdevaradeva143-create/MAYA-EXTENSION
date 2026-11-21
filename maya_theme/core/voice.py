"""Voice/AI-driven theme switching (Phase 6).

Parses natural commands like 'Maya, change to dark glass', 'blur increase',
'set accent pink', 'performance battery' and maps them to config changes.
Replies in Maya's friendly Thanglish tone.
"""

from __future__ import annotations

import re
from typing import Any

from .config import load_config, save_config

# ---------------------------------------------------------------------------
# Maya personality — friendly Thanglish responses
# ---------------------------------------------------------------------------

GREETINGS = [
    "Vanakkam! Naan Maya, un theme assistant. Enna maathanum?",
    "Hey! Maya pesraen. Theme maathurama?",
    "Hi there! Glass theme la irukka, enna venum?",
]

FALLBACK_REPLY = (
    "Sorry da, puriyala. Try pannu: 'dark mode', 'light mode', "
    "'blur 30', 'accent purple', 'glass off', 'battery mode'."
)

SUCCESS_REPLY = "Done da! {summary} ✅"


def _tone_reply(msg: str) -> str:
    return msg


# ---------------------------------------------------------------------------
# Intent parsing
# ---------------------------------------------------------------------------

_THEME_ALIASES = {
    "dark": "dark",
    "night": "dark",
    "iravu": "dark",
    "light": "light",
    "day": "light",
    "white": "light",
    "auto": "auto",
}

_ACCENT_WORDS = {
    "pink": "#FF7AB8",
    "purple": "#A855F7",
    "blue": "#3B82F6",
    "green": "#4ADE80",
    "red": "#F87171",
    "orange": "#FBBF24",
    "cyan": "#06B6D4",
    "teal": "#14B8A6",
    "rose": "#F43F5E",
    "violet": "#8B5CF6",
}

_PERF_WORDS = {
    "quality": "quality",
    "high": "quality",
    "battery": "battery",
    "saver": "battery",
    "power saver": "battery",
    "balanced": "balanced",
    "normal": "balanced",
    "default": "balanced",
}

_SCOPE_WORDS = {
    "kwin": "kwin",
    "compositor": "kwin",
    "blur effect": "kwin",
    "qt": "qt_apps",
    "qt apps": "qt_apps",
    "gtk": "gtk_apps",
    "gtk apps": "gtk_apps",
    "panel": "panels",
    "panels": "panels",
    "taskbar": "panels",
    "notification": "notifications",
    "notifications": "notifications",
    "icon": "icons",
    "icons": "icons",
    "cursor": "cursors",
    "cursors": "cursors",
}


def _parse_theme_mode(text: str) -> str | None:
    low = text.lower()
    for alias, mode in _THEME_ALIASES.items():
        if re.search(rf"\b{alias}\b", low):
            return mode
    return None


def _parse_blur(text: str) -> int | None:
    m = re.search(r"blur\s*(?:to\s*|at\s*|=\s*)?(\d+)", text, re.IGNORECASE)
    if m:
        return max(0, min(40, int(m.group(1))))
    return None


def _parse_blur_delta(text: str) -> int:
    low = text.lower()
    if re.search(r"(increase|more|up|add|increase|kammi|extra)", low) or "more" in low:
        return +4
    if re.search(r"(decrease|less|down|reduce|kurai|reduce)", low) or "less" in low:
        return -4
    return 0


def _parse_accent(text: str) -> str | None:
    low = text.lower()
    # hex directly
    m = re.search(r"#[0-9a-fA-F]{6}", text)
    if m:
        return m.group(0)
    for word, color in _ACCENT_WORDS.items():
        if re.search(rf"\b{word}\b", low):
            return color
    return None


def _parse_perf(text: str) -> str | None:
    low = text.lower()
    for phrase, preset in _PERF_WORDS.items():
        if phrase in low:
            return preset
    return None


def _parse_bool_toggle(text: str, section: str, key: str) -> bool | None:
    """Return True to enable, False to disable, None if no match."""
    low = text.lower()
    # check for scope keyword
    words_in = section in low or any(
        k in low for k in _SCOPE_WORDS if _SCOPE_WORDS[k] == key
    )
    if not words_in:
        return None
    if re.search(r"(off|disable|remove|neekku|ama|poo|kill|stop|no glass)", low):
        return False
    if re.search(r"(on|enable|add|um|yes|start|put|va|on pannu)", low):
        return True
    return None


def _parse_transparency(text: str) -> tuple[str, float] | None:
    """Parse 'transparency dark 0.6' or 'transparency 60%'."""
    low = text.lower()
    if "transparency" not in low and "transparent" not in low:
        return None
    # percentage
    m = re.search(r"(\d{1,3})\s*%", text)
    if m:
        val = int(m.group(1))
        val = min(val, 100)
        alpha = val / 100.0
        target = "transparency_light" if "light" in low else "transparency_dark"
        return (target, max(0.0, min(1.0, alpha)))
    m = re.search(r"0?\.\d+", text)
    if m:
        alpha = float(m.group(0))
        target = "transparency_light" if "light" in low else "transparency_dark"
        return (target, max(0.0, min(1.0, alpha)))
    return None


# ---------------------------------------------------------------------------
# Main handler
# ---------------------------------------------------------------------------

def handle_command(text: str) -> dict[str, Any]:
    """Parse a natural command and apply to Maya config.

    Returns dict with: success, applied (list of change descriptions),
    reply (Maya-tone message), config (the new config).
    """
    text = text.strip()
    if not text:
        return {
            "success": False,
            "error": "empty command",
            "reply": FALLBACK_REPLY,
        }

    cfg = load_config()
    applied: list[str] = []

    # --- theme mode ---
    mode = _parse_theme_mode(text)
    if mode:
        cfg.setdefault("theme", {})["mode"] = mode
        applied.append(f"theme → {mode}")

    # --- glass on/off ---
    low = text.lower()
    if "glass" in low:
        if re.search(r"(off|disable|remove|no glass|neekku|poo)", low):
            if cfg.get("glass", {}).get("enabled", True):
                cfg.setdefault("glass", {})["enabled"] = False
                applied.append("glass disabled")
        elif re.search(r"(on|enable|add|um|yes|va|on pannu)", low):
            if not cfg.get("glass", {}).get("enabled", True):
                cfg.setdefault("glass", {})["enabled"] = True
                applied.append("glass enabled")

    # --- blur value / delta ---
    blur_val = _parse_blur(text)
    if blur_val is not None:
        cfg.setdefault("glass", {})["blur"] = blur_val
        applied.append(f"blur → {blur_val}px")

    blur_delta = _parse_blur_delta(text)
    if blur_delta != 0 and "blur" in low:
        current = cfg.get("glass", {}).get("blur", 28)
        new_val = max(0, min(40, current + blur_delta))
        cfg.setdefault("glass", {})["blur"] = new_val
        applied.append(f"blur {blur_delta:+d} → {new_val}px")

    # --- accent color ---
    accent = _parse_accent(text)
    if accent:
        cfg.setdefault("theme", {})["accent_start"] = accent
        # derive a complementary end from Maya palette
        if accent.upper() == "#FF7AB8":
            cfg["theme"]["accent_end"] = "#A855F7"
        elif accent.upper() == "#A855F7":
            cfg["theme"]["accent_end"] = "#FF7AB8"
        else:
            cfg["theme"]["accent_end"] = "#A855F7"
        applied.append(f"accent → {accent}")

    # --- performance preset ---
    perf = _parse_perf(text)
    if perf:
        cfg.setdefault("performance", {})["preset"] = perf
        applied.append(f"performance → {perf}")

    # --- scope toggles ---
    for keyword, scope_key in _SCOPE_WORDS.items():
        if re.search(rf"\b{keyword}\b", low):
            val = _parse_bool_toggle(text, keyword, scope_key)
            if val is not None and val != cfg.get("scope", {}).get(scope_key, True):
                cfg.setdefault("scope", {})[scope_key] = val
                applied.append(f"{scope_key} → {'on' if val else 'off'}")
            break  # only first scope match

    # --- transparency ---
    transp = _parse_transparency(text)
    if transp:
        target, alpha = transp
        cfg.setdefault("glass", {})[target] = alpha
        label = "dark" if "dark" in target else "light"
        applied.append(f"transparency {label} → {int(alpha*100)}%")

    # --- auto reduce blur toggle ---
    if re.search(r"(auto.?reduce|auto.?blur|battery.?blur)", low):
        if re.search(r"(off|disable|no)", low):
            cfg.setdefault("performance", {})["auto_reduce_blur"] = False
            applied.append("auto-reduce blur → off")
        elif re.search(r"(on|enable|yes)", low):
            cfg.setdefault("performance", {})["auto_reduce_blur"] = True
            applied.append("auto-reduce blur → on")

    # --- monitor ---
    if re.search(r"(monitor|widget)", low):
        if re.search(r"(off|disable|no|hide)", low):
            cfg.setdefault("monitor", {})["enabled"] = False
            applied.append("monitor → off")
        elif re.search(r"(on|enable|show|yes)", low):
            cfg.setdefault("monitor", {})["enabled"] = True
            applied.append("monitor → on")

    # --- wallpaper ---
    if re.search(r"wallpaper", low):
        if re.search(r"(dark|night)", low):
            from . import wallpaper as _wp

            r = _wp.auto_switch_by_mode("dark", cfg)
            if r.get("success"):
                applied.append("wallpaper → dark")
        elif re.search(r"(light|day)", low):
            from . import wallpaper as _wp

            r = _wp.auto_switch_by_mode("light", cfg)
            if r.get("success"):
                applied.append("wallpaper → light")
        elif re.search(r"(next|change|random|shuffle)", low):
            from . import wallpaper as _wp

            r = _wp.slideshow_next(cfg)
            if r.get("success"):
                applied.append("wallpaper → next")

    # --- status / info commands (don't modify) ---
    if re.search(r"(status|what|show|ennoda|epdi|current)", low) and not applied:
        cfg = load_config()
        return {
            "success": True,
            "applied": [],
            "reply": (
                f"Current setup da: {cfg['theme']['mode']} mode, "
                f"blur {cfg['glass']['blur']}px, "
                f"glass {'ON' if cfg['glass']['enabled'] else 'OFF'}, "
                f"accent {cfg['theme']['accent_start']}."
            ),
            "config": cfg,
        }

    if not applied:
        return {
            "success": False,
            "error": "command not recognized",
            "reply": FALLBACK_REPLY,
        }

    # save + apply
    save_config(cfg)
    try:
        from .install import apply_config

        apply_config(cfg)
    except Exception:
        pass  # apply best-effort; config saved regardless

    summary = ", ".join(applied)
    reply = SUCCESS_REPLY.format(summary=summary)
    return {
        "success": True,
        "applied": applied,
        "reply": reply,
        "config": cfg,
    }


def handle_voice_input(audio_path: str) -> dict[str, Any]:
    """Placeholder for voice input — converts audio to text then handles.

    Currently expects text via stdin/env; real STT would use a local model.
    """
    return {
        "success": False,
        "error": "voice STT not available — type your command instead",
        "reply": "Naan mic support illa ippo. Type pannu da: 'dark mode', 'blur 30', etc.",
    }


def greet() -> str:
    import random

    return random.choice(GREETINGS)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(greet())
        print("Usage: python -m maya_theme.core.voice 'dark mode'")
        sys.exit(0)
    cmd = " ".join(sys.argv[1:])
    result = handle_command(cmd)
    print(result.get("reply", result.get("error", "done")))