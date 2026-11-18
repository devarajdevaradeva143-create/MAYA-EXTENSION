"""Backup / restore of KDE + Maya theme state."""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any

from .config import BACKUP_DIR, MAYA_HOME, load_config, save_config

KDE_CONFIG_FILES = [
    "kwinrc",
    "plasmarc",
    "plasmashellrc",
    "kglobalshortcutsrc",
    "kdeglobals",
]


def _timestamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def create_backup(label: str = "auto") -> Path:
    """Snapshot current KDE config + Maya config into a timestamped dir."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    dest = BACKUP_DIR / f"{_timestamp()}-{label}"
    dest.mkdir(parents=True, exist_ok=True)

    kde_dir = Path.home() / ".config"
    for name in KDE_CONFIG_FILES:
        src = kde_dir / name
        if src.exists():
            shutil.copy2(src, dest / name)

    # Maya own config
    if (MAYA_HOME / "config.json").exists():
        shutil.copy2(MAYA_HOME / "config.json", dest / "maya-config.json")

    meta = {
        "label": label,
        "created": time.time(),
        "files": [n for n in KDE_CONFIG_FILES if (kde_dir / n).exists()],
    }
    (dest / "meta.json").write_text(json.dumps(meta, indent=2))
    _rotate_backups(keep=5)
    return dest


def restore_backup(backup_dir: Path) -> bool:
    kde_dir = Path.home() / ".config"
    if not backup_dir.exists():
        return False
    for name in KDE_CONFIG_FILES:
        src = backup_dir / name
        if src.exists():
            shutil.copy2(src, kde_dir / name)
    maya_cfg = backup_dir / "maya-config.json"
    if maya_cfg.exists():
        shutil.copy2(maya_cfg, MAYA_HOME / "config.json")
    return True


def latest_backup() -> Path | None:
    if not BACKUP_DIR.exists():
        return None
    dirs = sorted(BACKUP_DIR.iterdir(), key=lambda p: p.name, reverse=True)
    return dirs[0] if dirs else None


def list_backups() -> list[Path]:
    if not BACKUP_DIR.exists():
        return []
    return sorted(BACKUP_DIR.iterdir(), key=lambda p: p.name, reverse=True)


def _rotate_backups(keep: int = 5) -> None:
    dirs = sorted(BACKUP_DIR.iterdir(), key=lambda p: p.name)
    while len(dirs) > keep:
        oldest = dirs.pop(0)
        shutil.rmtree(oldest, ignore_errors=True)


def export_bundle(out_path: Path, include_wallpaper: bool = False) -> Path:
    """Export current theme config to a JSON file (or zip if wallpaper included)."""
    cfg = load_config()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if include_wallpaper:
        import zipfile

        wp = cfg.get("wallpaper", {}).get("path", "")
        with zipfile.ZipFile(out_path, "w") as z:
            z.writestr("maya-config.json", json.dumps(cfg, indent=2))
            if wp and Path(wp).exists():
                z.write(wp, f"wallpaper/{Path(wp).name}")
    else:
        out_path.write_text(json.dumps(cfg, indent=2))
    return out_path


def import_bundle(in_path: Path) -> dict[str, Any]:
    import zipfile

    if in_path.suffix == ".zip":
        with zipfile.ZipFile(in_path) as z:
            cfg = json.loads(z.read("maya-config.json"))
    else:
        cfg = json.loads(in_path.read_text())
    # validate minimal schema
    if "version" not in cfg:
        raise ValueError("Invalid bundle: missing version")
    save_config(cfg)
    return cfg