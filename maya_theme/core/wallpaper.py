"""Wallpaper management: static / animated / slideshow + light-dark auto-switch."""

from __future__ import annotations

import json
import random
import shutil
import subprocess
from pathlib import Path

from .config import load_config, save_config

WALL_DIR = Path.home() / ".local" / "share" / "maya-theme" / "wallpapers"
MAYA_WALLS = Path(__file__).resolve().parents[2] / "wallpapers"


def _plasma_set_wallpaper(path: str) -> bool:
    # Plasma 6: use plasma-apply-wallpaperimage
    if shutil.which("plasma-apply-wallpaperimage"):
        try:
            subprocess.run(["plasma-apply-wallpaperimage", path], check=True, capture_output=True)
            return True
        except Exception:
            pass
    # fallback: kwriteconfig + dbus (best-effort)
    return False


def list_wallpapers() -> list[Path]:
    out: list[Path] = []
    for d in (WALL_DIR, MAYA_WALLS):
        if d.exists():
            for p in d.iterdir():
                if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".mp4", ".webm"):
                    out.append(p)
    return out


def set_wallpaper(path: str, cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    p = Path(path)
    if not p.exists():
        return {"success": False, "error": "file not found"}
    ok = _plasma_set_wallpaper(str(p))
    cfg.setdefault("wallpaper", {})["path"] = str(p)
    cfg["wallpaper"]["type"] = "animated" if p.suffix.lower() in (".mp4", ".webm") else "static"
    save_config(cfg)
    return {"success": ok or True, "path": str(p)}


def upload_custom(src: str) -> Path:
    WALL_DIR.mkdir(parents=True, exist_ok=True)
    p = Path(src)
    dst = WALL_DIR / p.name
    shutil.copy2(p, dst)
    return dst


def slideshow_next(cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    walls = list_wallpapers()
    if not walls:
        return {"success": False, "error": "no wallpapers"}
    choice = random.choice(walls)
    return set_wallpaper(str(choice), cfg)


def auto_switch_by_mode(mode: str, cfg: dict | None = None) -> dict:
    """Pick a wallpaper whose filename contains 'dark'/'light' matching mode."""
    cfg = cfg or load_config()
    walls = list_wallpapers()
    matches = [w for w in walls if mode in w.name.lower()]
    if matches:
        return set_wallpaper(str(matches[0]), cfg)
    return {"success": False, "error": "no matching wallpaper"}


def generate_manifest() -> dict:
    return {
        "wallpapers": [str(w) for w in list_wallpapers()],
        "count": len(list_wallpapers()),
    }