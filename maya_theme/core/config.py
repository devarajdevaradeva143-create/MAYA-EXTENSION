"""Configuration management for Maya theme.

Wraps kwriteconfig6 / kreadconfig6 (Plasma 6) with a Python-friendly API and
keeps a local JSON mirror under ~/.local/share/maya-theme/config.json so the
settings app can read/write without shelling out on every change.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MAYA_HOME = Path.home() / ".local" / "share" / "maya-theme"
CONFIG_FILE = MAYA_HOME / "config.json"
STATE_DIR = Path.home() / ".local" / "state" / "maya-theme"
BACKUP_DIR = MAYA_HOME / "backups"

DEFAULT_CONFIG: dict[str, Any] = {
    "version": "0.1.0",
    "glass": {
        "enabled": True,
        "blur": 28,
        "transparency_dark": 0.72,
        "transparency_light": 0.5,
        "border": 1.0,
        "noise": 0.02,
    },
    "theme": {
        "mode": "dark",  # dark | light | auto
        "accent_start": "#FF7AB8",
        "accent_end": "#A855F7",
    },
    "scope": {
        "kwin": True,
        "qt_apps": True,
        "gtk_apps": True,
        "panels": True,
        "notifications": True,
        "icons": True,
        "cursors": True,
    },
    "performance": {
        "preset": "balanced",  # quality | balanced | battery
        "auto_reduce_blur": True,
    },
    "wallpaper": {
        "type": "static",  # static | animated | slideshow
        "path": "",
        "glass_blur": True,
        "parallax": False,
        "auto_switch": False,
    },
    "monitor": {
        "enabled": True,
        "interval": 2,  # seconds
        "style": "cards",  # cards | graphs | rings | bars
        "metrics": ["cpu", "ram", "gpu", "battery", "disk", "network", "temp"],
        "alerts": True,
    },
    "privacy": {
        "update_checks": False,
        "diagnostics": False,
    },
}


def _ensure_dirs() -> None:
    for d in (MAYA_HOME, STATE_DIR, BACKUP_DIR):
        d.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    _ensure_dirs()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return json.loads(json.dumps(DEFAULT_CONFIG))
    try:
        with CONFIG_FILE.open() as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = {}
    # merge defaults for missing keys
    merged = json.loads(json.dumps(DEFAULT_CONFIG))
    _deep_merge(merged, data)
    return merged


def save_config(cfg: dict[str, Any]) -> None:
    _ensure_dirs()
    with CONFIG_FILE.open("w") as f:
        json.dump(cfg, f, indent=2)


def _deep_merge(base: dict, override: dict) -> None:
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def has_binary(name: str) -> bool:
    return shutil.which(name) is not None


def kwrite(key: str, value: str, file: str = "kwinrc") -> bool:
    """Write a KWin/Plasma config key via kwriteconfig6."""
    if not has_binary("kwriteconfig6"):
        return False
    try:
        subprocess.run(
            ["kwriteconfig6", "--file", file, "--group", _group_of(key), "--key", _key_of(key), str(value)],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def kread(key: str, file: str = "kwinrc") -> str | None:
    if not has_binary("kreadconfig6"):
        return None
    try:
        r = subprocess.run(
            ["kreadconfig6", "--file", file, "--group", _group_of(key), "--key", _key_of(key)],
            check=True,
            capture_output=True,
            text=True,
        )
        return r.stdout.strip() or None
    except subprocess.CalledProcessError:
        return None


def _group_of(key: str) -> str:
    # "Compositing/Blur" -> group "Compositing", key "Blur"
    if "/" in key:
        return key.split("/", 1)[0]
    return "General"


def _key_of(key: str) -> str:
    if "/" in key:
        return key.split("/", 1)[1]
    return key


@dataclass
class GlassSpec:
    enabled: bool = True
    blur: int = 28
    transparency_dark: float = 0.72
    transparency_light: float = 0.5
    border: float = 1.0
    noise: float = 0.02

    def to_css(self, dark: bool = True) -> str:
        alpha = self.transparency_dark if dark else self.transparency_light
        bg = f"rgba(11,15,25,{alpha})" if dark else f"rgba(245,247,251,{alpha})"
        return (
            f"background: {bg};\n"
            f"backdrop-filter: blur({self.blur}px);\n"
            f"border: {self.border}px solid rgba(255,255,255,0.18);\n"
            f"border-radius: 18px;\n"
            f"box-shadow: 0 8px 32px rgba(0,0,0,0.35);\n"
        )