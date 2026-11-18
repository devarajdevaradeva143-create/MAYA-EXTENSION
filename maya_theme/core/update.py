"""Opt-in auto-update checker."""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

from .config import load_config

DEFAULT_MANIFEST = ""  # user must configure; no default cloud endpoint (privacy)


def _manifest_url() -> str:
    cfg = load_config()
    return cfg.get("privacy", {}).get("update_url", DEFAULT_MANIFEST)


def check_update() -> dict:
    url = _manifest_url()
    if not url:
        return {"available": False, "reason": "no update source configured (opt-in)"}
    if not load_config().get("privacy", {}).get("update_checks", False):
        return {"available": False, "reason": "update checks disabled"}
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            manifest = json.loads(r.read())
    except Exception as e:
        return {"available": False, "error": str(e)}
    from maya_theme import __version__

    if manifest.get("version", "0") > __version__:
        return {
            "available": True,
            "version": manifest["version"],
            "changelog": manifest.get("changelog", ""),
            "url": manifest.get("url"),
            "checksum": manifest.get("checksum"),
        }
    return {"available": False, "current": __version__}


def apply_update() -> dict:
    info = check_update()
    if not info.get("available"):
        return {"success": False, "error": "no update available"}
    # download + verify + backup + install (placeholder pipeline)
    url = info.get("url")
    if not url:
        return {"success": False, "error": "no download url"}
    try:
        from .backup import create_backup

        create_backup("pre-update")
        # download
        data = urllib.request.urlopen(url, timeout=60).read()
        if info.get("checksum"):
            h = hashlib.sha256(data).hexdigest()
            if h != info["checksum"]:
                return {"success": False, "error": "checksum mismatch"}
        # write to temp; real install would extract + apply
        tmp = Path("/tmp/opencode") / "maya-update.bin"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_bytes(data)
        return {"success": True, "downloaded": str(tmp), "note": "manual apply required"}
    except Exception as e:
        from .backup import rollback

        rollback.rollback()
        return {"success": False, "error": str(e)}