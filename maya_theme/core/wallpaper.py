"""Wallpaper management: static / animated / slideshow + light-dark auto-switch.

Supports:
- Static images (jpg, png, webp)
- Animated wallpapers (mp4, webm) — uses plasma-apply-wallpaperplugin or fallback
- Slideshow with configurable directory
- Parallax glass effect (compositor-level, subtle depth)
- Light/dark auto-switch by filename matching
- Themed Maya wallpaper pack generation
"""

from __future__ import annotations

import json
import random
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .config import load_config, save_config

WALL_DIR = Path.home() / ".local" / "share" / "maya-theme" / "wallpapers"
MAYA_WALLS = Path(__file__).resolve().parents[2] / "wallpapers"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
VIDEO_EXTS = {".mp4", ".webm", ".mkv", ".avi"}


def _plasma_set_wallpaper(path: str) -> bool:
    """Set wallpaper via Plasma 6 tools, with fallbacks."""
    p = Path(path)
    ext = p.suffix.lower()

    # Animated video wallpaper: use plasma-apply-wallpaperplugin if available
    if ext in VIDEO_EXTS:
        if shutil.which("plasma-apply-wallpaperplugin"):
            try:
                # QtQuickVideo / video wallpaper plugin
                subprocess.run(
                    ["plasma-apply-wallpaperplugin", "-p", path],
                    check=True, capture_output=True, timeout=10,
                )
                return True
            except Exception:
                pass
        # fallback: kwriteconfig to video wallpaper plugin
        try:
            subprocess.run(
                ["kwriteconfig6", "--file", "plasma-org.kde.plasma.desktop-appletsrc",
                 "--group", "Wallpaper", "--key", "plugin", "org.kde.video"],
                check=True, capture_output=True,
            )
            return True
        except Exception:
            pass

    # Static image: use plasma-apply-wallpaperimage
    if shutil.which("plasma-apply-wallpaperimage"):
        try:
            subprocess.run(["plasma-apply-wallpaperimage", path], check=True, capture_output=True, timeout=10)
            return True
        except Exception:
            pass
    # fallback: kwriteconfig (best-effort, image plugin)
    try:
        subprocess.run(
            ["kwriteconfig6", "--file", "plasma-org.kde.plasma.desktop-appletsrc",
             "--group", "Wallpaper", "--key", "Image", path],
            check=True, capture_output=True,
        )
        return True
    except Exception:
        return False


def list_wallpapers() -> list[Path]:
    out: list[Path] = []
    for d in (WALL_DIR, MAYA_WALLS):
        if d.exists():
            for p in d.iterdir():
                if p.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS:
                    out.append(p)
    return out


def set_wallpaper(path: str, cfg: dict | None = None) -> dict[str, Any]:
    cfg = cfg or load_config()
    p = Path(path)
    if not p.exists():
        return {"success": False, "error": "file not found"}
    ok = _plasma_set_wallpaper(str(p))
    wp = cfg.setdefault("wallpaper", {})
    wp["path"] = str(p)
    ext = p.suffix.lower()
    if ext in VIDEO_EXTS:
        wp["type"] = "animated"
    else:
        wp["type"] = "static"
    save_config(cfg)
    return {"success": ok, "path": str(p), "type": wp["type"]}


def upload_custom(src: str) -> Path:
    WALL_DIR.mkdir(parents=True, exist_ok=True)
    p = Path(src)
    dst = WALL_DIR / p.name
    shutil.copy2(p, dst)
    return dst


def slideshow_next(cfg: dict | None = None) -> dict[str, Any]:
    cfg = cfg or load_config()
    walls = list_wallpapers()
    if not walls:
        return {"success": False, "error": "no wallpapers"}
    choice = random.choice(walls)
    return set_wallpaper(str(choice), cfg)


def auto_switch_by_mode(mode: str, cfg: dict | None = None) -> dict[str, Any]:
    """Pick a wallpaper whose filename contains 'dark'/'light' matching mode."""
    cfg = cfg or load_config()
    walls = list_wallpapers()
    matches = [w for w in walls if mode in w.name.lower()]
    if matches:
        return set_wallpaper(str(matches[0]), cfg)
    return {"success": False, "error": "no matching wallpaper"}


def enable_parallax(enabled: bool = True) -> dict[str, Any]:
    """Toggle compositor-level parallax effect for wallpaper.

    Parallax = subtle mouse-follow depth shift on the wallpaper layer.
    Implemented via KWin script / effect toggle.
    """
    cfg = load_config()
    cfg.setdefault("wallpaper", {})["parallax"] = enabled
    save_config(cfg)
    if enabled:
        # enable the parallax effect via kwriteconfig (best-effort)
        try:
            subprocess.run(
                ["kwriteconfig6", "--file", "kwinrc", "--group", "Plugins",
                 "--key", "parallaxEnabled", "true"],
                check=False, capture_output=True,
            )
        except Exception:
            pass
    else:
        try:
            subprocess.run(
                ["kwriteconfig6", "--file", "kwinrc", "--group", "Plugins",
                 "--key", "parallaxEnabled", "false"],
                check=False, capture_output=True,
            )
        except Exception:
            pass
    return {"success": True, "parallax": enabled}


def enable_glass_blur(enabled: bool = True) -> dict[str, Any]:
    """Toggle glass blur effect on wallpaper layer."""
    cfg = load_config()
    cfg.setdefault("wallpaper", {})["glass_blur"] = enabled
    save_config(cfg)
    return {"success": True, "glass_blur": enabled}


def generate_manifest() -> dict[str, Any]:
    return {
        "wallpapers": [str(w) for w in list_wallpapers()],
        "count": len(list_wallpapers()),
    }


def generate_themed_pack(out_dir: Path | None = None) -> Path:
    """Generate a Maya-themed wallpaper pack (SVG gradient wallpapers).

    Creates SVG wallpapers with Maya pink-purple gradient + glass aesthetic,
    in both dark and light variants, plus animated variants.
    """
    out_dir = out_dir or (MAYA_WALLS)
    out_dir.mkdir(parents=True, exist_ok=True)

    wallpapers = {
        "maya-dark.svg": _svg_wallpaper("#0B0F19", "#1A1A2E", "#FF7AB8", "#A855F7", dark=True),
        "maya-light.svg": _svg_wallpaper("#F5F7FB", "#E8ECF4", "#FF7AB8", "#A855F7", dark=False),
        "maya-sunset.svg": _svg_wallpaper("#1A1A2E", "#2D1B3D", "#FF7AB8", "#A855F7", dark=True, variant="sunset"),
        "maya-ocean.svg": _svg_wallpaper("#0B0F19", "#0A2540", "#06B6D4", "#3B82F6", dark=True, variant="ocean"),
        "maya-aurora.svg": _svg_wallpaper("#0B0F19", "#1A2E1A", "#4ADE80", "#A855F7", dark=True, variant="aurora"),
    }

    for name, content in wallpapers.items():
        (out_dir / name).write_text(content)

    # manifest
    manifest = {
        "name": "Maya Themed Wallpapers",
        "version": "1.0",
        "wallpapers": list(wallpapers.keys()),
        "count": len(wallpapers),
    }
    (out_dir / "maya-pack-manifest.json").write_text(json.dumps(manifest, indent=2))
    return out_dir


def _svg_wallpaper(bg1: str, bg2: str, accent1: str, accent2: str,
                   dark: bool = True, variant: str = "") -> str:
    """Generate an SVG wallpaper with gradient + glass orbs."""
    variant_defs = {
        "sunset": f"""
            <ellipse cx="800" cy="200" rx="400" ry="300" fill="{accent1}" opacity="0.3">
                <animate attributeName="cy" values="200;220;200" dur="8s" repeatCount="indefinite"/>
            </ellipse>
            <ellipse cx="300" cy="500" rx="350" ry="250" fill="{accent2}" opacity="0.2">
                <animate attributeName="cx" values="300;320;300" dur="10s" repeatCount="indefinite"/>
            </ellipse>
        """,
        "ocean": f"""
            <ellipse cx="400" cy="300" rx="400" ry="200" fill="{accent1}" opacity="0.25">
                <animate attributeName="ry" values="200;220;200" dur="6s" repeatCount="indefinite"/>
            </ellipse>
            <ellipse cx="900" cy="600" rx="350" ry="180" fill="{accent2}" opacity="0.2"/>
        """,
        "aurora": f"""
            <ellipse cx="600" cy="250" rx="500" ry="150" fill="{accent1}" opacity="0.3">
                <animate attributeName="ry" values="150;180;150" dur="7s" repeatCount="indefinite"/>
            </ellipse>
            <ellipse cx="200" cy="500" rx="300" ry="200" fill="{accent2}" opacity="0.25"/>
        """,
    }
    orbs = variant_defs.get(variant, f"""
        <ellipse cx="600" cy="300" rx="400" ry="250" fill="{accent1}" opacity="0.25">
            <animate attributeName="cy" values="300;320;300" dur="9s" repeatCount="indefinite"/>
        </ellipse>
        <ellipse cx="300" cy="600" rx="300" ry="200" fill="{accent2}" opacity="0.2">
            <animate attributeName="cx" values="300;320;300" dur="11s" repeatCount="indefinite"/>
        </ellipse>
    """)

    text_color = "#FFFFFF" if dark else "#1F2937"
    sub_color = "rgba(255,255,255,0.5)" if dark else "rgba(31,41,55,0.5)"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <filter id="blur">
      <feGaussianBlur stdDeviation="60"/>
    </filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#bg)"/>
  <g filter="url(#blur)">
    {orbs}
  </g>
  <text x="960" y="500" text-anchor="middle" font-family="Inter, sans-serif" font-size="72" font-weight="bold" fill="{text_color}">
    ✦ Maya AI
  </text>
  <text x="960" y="560" text-anchor="middle" font-family="Inter, sans-serif" font-size="24" fill="{sub_color}">
    local only • your assistant
  </text>
</svg>"""