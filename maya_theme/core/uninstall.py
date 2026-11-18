"""Uninstall Maya theme and restore defaults."""

from __future__ import annotations

import shutil
from pathlib import Path

from .backup import create_backup, restore_backup, latest_backup

MAYA_HOME = Path.home() / ".local" / "share" / "maya-theme"


def uninstall() -> dict:
    create_backup("pre-uninstall")
    lb = latest_backup()
    if lb:
        restore_backup(lb)
    # remove theme files
    theme_dir = MAYA_HOME / "theme"
    if theme_dir.exists():
        shutil.rmtree(theme_dir, ignore_errors=True)
    # remove installed desktop entry if present
    desktop = Path.home() / ".local" / "share" / "applications" / "maya-settings.desktop"
    if desktop.exists():
        desktop.unlink()
    return {"success": True}