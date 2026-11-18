"""Install flow for Maya theme (user-level, no root)."""

from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path

from .backup import create_backup
from .compat import detect

MAYA_HOME = Path.home() / ".local" / "share" / "maya-theme"
THEME_SRC = Path(__file__).resolve().parents[2] / "theme"


def pre_check() -> tuple[bool, str]:
    rep = detect()
    if not rep.supported:
        return False, "Unsupported OS/Plasma. See compat report."
    if not shutil.which("kwriteconfig6"):
        return False, "kwriteconfig6 not found (Plasma 6 tools missing)."
    return True, "ok"


def install_theme_files() -> None:
    """Copy theme assets into ~/.local/share/."""
    MAYA_HOME.mkdir(parents=True, exist_ok=True)
    for sub in ("colors", "kwin", "plasma", "gtk", "icons"):
        src = THEME_SRC / sub
        dst = MAYA_HOME / "theme" / sub
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
    # color schemes into KDE color-schemes dir
    cs_dir = Path.home() / ".local" / "share" / "color-schemes"
    cs_dir.mkdir(parents=True, exist_ok=True)
    for cs in (THEME_SRC / "colors").glob("*.colors"):
        shutil.copy2(cs, cs_dir / cs.name)
    # KCM desktop entry
    kcm_src = Path(__file__).resolve().parents[1] / "kcm" / "maya-settings.desktop"
    if kcm_src.exists():
        dst_dir = Path.home() / ".local" / "share" / "kservices6"
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(kcm_src, dst_dir / "maya-settings.desktop")


def apply_config(cfg: dict) -> None:
    from .config import kwrite

    glass = cfg.get("glass", {})
    if glass.get("enabled"):
        kwrite("Compositing/OpenGLIsUnsafe", "false", "kwinrc")
        kwrite("Plugins/blurEnabled", "true", "kwinrc")
        kwrite("Plugins/backgroundcontrastEnabled", "true", "kwinrc")
    else:
        kwrite("Plugins/blurEnabled", "false", "kwinrc")
    kwrite("Effect-Blur/BlurStrength", str(glass.get("blur", 28)), "kwinrc")
    kwrite("Effect-Blur/NoiseStrength", str(int(glass.get("noise", 0.02) * 100)), "kwinrc")
    mode = cfg.get("theme", {}).get("mode", "dark")
    kwrite("General/ColorScheme", "MayaDark" if mode == "dark" else "MayaLight", "kdeglobals")
    # panel opacity hint
    if cfg.get("scope", {}).get("panels", True):
        kwrite("General/panelOpacity", "0.72", "plasmashellrc")


def restart_plasma(timeout: int = 5) -> bool:
    """Restart plasmashell with a confirm timeout; auto-rollback if it doesn't return."""
    if not shutil.which("plasmashell"):
        return False
    try:
        subprocess.Popen(["plasmashell", "--replace"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(timeout)
        # check it's alive
        r = subprocess.run(["pgrep", "-x", "plasmashell"], capture_output=True)
        return r.returncode == 0
    except Exception:
        return False


def install(cfg: dict | None = None) -> dict:
    ok, msg = pre_check()
    if not ok:
        return {"success": False, "error": msg}
    from .config import load_config, save_config

    if cfg is None:
        cfg = load_config()
    backup_path = create_backup("pre-install")
    try:
        install_theme_files()
        apply_config(cfg)
        save_config(cfg)
        shell_ok = restart_plasma()
        if not shell_ok:
            # auto rollback
            from .backup import restore_backup

            restore_backup(backup_path)
            restart_plasma()
            return {"success": False, "error": "Plasma shell did not return; rolled back."}
    except Exception as e:
        from .backup import restore_backup

        restore_backup(backup_path)
        return {"success": False, "error": str(e)}
    return {"success": True, "backup": str(backup_path)}