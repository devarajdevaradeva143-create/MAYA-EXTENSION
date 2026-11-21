"""Opt-in auto-update checker with GPG signature verification.

Privacy: no default cloud endpoint — user must configure a manifest URL.
Only version + OS/Plasma info is sent to the update server (never personal data).
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from .config import load_config

DEFAULT_MANIFEST = ""  # user must configure; no default cloud endpoint (privacy)
MAYA_HOME = Path.home() / ".local" / "share" / "maya-theme"


def _manifest_url() -> str:
    cfg = load_config()
    return cfg.get("privacy", {}).get("update_url", DEFAULT_MANIFEST)


def check_update() -> dict[str, Any]:
    """Check if a new version is available. Opt-in only."""
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

    if _version_gt(manifest.get("version", "0"), __version__):
        return {
            "available": True,
            "version": manifest["version"],
            "changelog": manifest.get("changelog", ""),
            "url": manifest.get("url"),
            "checksum": manifest.get("checksum"),
            "signature": manifest.get("signature"),
            "min_os": manifest.get("min_os"),
        }
    return {"available": False, "current": __version__}


def _version_gt(a: str, b: str) -> bool:
    """Return True if version a > b (simple semver tuple compare)."""

    def tup(v: str) -> tuple:
        parts = []
        for p in v.split("."):
            num = "".join(ch for ch in p if ch.isdigit())
            parts.append(int(num) if num else 0)
        return tuple(parts)

    try:
        return tup(a) > tup(b)
    except Exception:
        return a > b


def _verify_signature(data: bytes, sig_b64: str) -> bool:
    """Verify GPG signature of update data.

    Requires gpg binary. If gpg not present or no signature, skip (best-effort).
    Returns True if verified or no signature provided (caller decides policy).
    """
    if not sig_b64:
        return True  # no signature provided; caller may enforce
    if not shutil.which("gpg"):
        return False  # cannot verify without gpg
    try:
        import base64

        sig_bytes = base64.b64decode(sig_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sig") as sigf:
            sigf.write(sig_bytes)
            sig_path = sigf.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as datf:
            datf.write(data)
            data_path = datf.name
        r = subprocess.run(
            ["gpg", "--verify", sig_path, data_path],
            capture_output=True,
            timeout=30,
        )
        Path(sig_path).unlink(missing_ok=True)
        Path(data_path).unlink(missing_ok=True)
        return r.returncode == 0
    except Exception:
        return False


def _download(url: str, timeout: int = 120) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def _extract_archive(data: bytes, dest: Path) -> Path | None:
    """Extract downloaded update archive into dest. Returns theme dir if extracted."""
    import io

    # try zip
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            z.extractall(dest)
        # find theme dir
        for item in dest.rglob("theme"):
            if item.is_dir():
                return item
        return dest
    except Exception:
        pass
    # try tar
    try:
        with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tf:
            tf.write(data)
            tf.flush()
            with tarfile.open(tf.name, "r:*") as t:
                t.extractall(dest)
            tf_path = Path(tf.name)
            tf_path.unlink(missing_ok=True)
        for item in dest.rglob("theme"):
            if item.is_dir():
                return item
        return dest
    except Exception:
        pass
    return None


def apply_update() -> dict[str, Any]:
    """Download, verify, backup, install update with rollback safety."""
    info = check_update()
    if not info.get("available"):
        return {"success": False, "error": "no update available"}

    url = info.get("url")
    if not url:
        return {"success": False, "error": "no download url in manifest"}

    # privacy check: update checks must be enabled
    if not load_config().get("privacy", {}).get("update_checks", False):
        return {"success": False, "error": "update checks disabled in privacy settings"}

    # backup before update
    from .backup import create_backup

    backup_path = create_backup("pre-update")

    try:
        # download
        data = _download(url)

        # checksum verify
        expected = info.get("checksum")
        if expected:
            h = hashlib.sha256(data).hexdigest()
            if h != expected:
                return {"success": False, "error": "checksum mismatch — update rejected"}

        # GPG signature verify (if provided and gpg available)
        sig = info.get("signature")
        if sig:
            if not _verify_signature(data, sig):
                return {"success": False, "error": "GPG signature verification failed"}

        # extract into temp
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            extracted = _extract_archive(data, tmp)
            if extracted is None or not extracted.exists():
                return {"success": False, "error": "could not extract update archive"}

            # install extracted theme files

            # copy extracted theme over MAYA_HOME/theme
            dst_theme = MAYA_HOME / "theme"
            if dst_theme.exists():
                shutil.rmtree(dst_theme, ignore_errors=True)
            dst_theme.mkdir(parents=True, exist_ok=True)
            for item in extracted.iterdir():
                if item.is_dir():
                    shutil.copytree(item, dst_theme / item.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dst_theme / item.name)

            # apply config
            from .install import apply_config

            cfg = load_config()
            apply_config(cfg)

            # update version in config
            cfg["version"] = info.get("version", cfg.get("version"))
            from .config import save_config

            save_config(cfg)

    except Exception as e:
        from .backup import restore_backup

        restore_backup(backup_path)
        return {"success": False, "error": f"update failed: {e}", "rolled_back": True}

    return {
        "success": True,
        "version": info.get("version"),
        "backup": str(backup_path),
        "note": "restart plasmashell to apply: plasmashell --replace",
    }