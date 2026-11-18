"""Manual rollback command."""

from __future__ import annotations

from .backup import latest_backup, restore_backup


def rollback() -> dict:
    lb = latest_backup()
    if lb is None:
        return {"success": False, "error": "No backup found."}
    ok = restore_backup(lb)
    if ok:
        from .install import restart_plasma

        restart_plasma()
    return {"success": ok, "backup": str(lb)}