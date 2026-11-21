"""Compatibility checks for Fedora / Plasma / Qt versions."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class CompatReport:
    os_name: str = ""
    os_version: str = ""
    plasma_version: str = ""
    qt_version: str = ""
    python_version: str = ""
    session_type: str = ""  # wayland | x11
    gpu: str = ""
    supported: bool = True
    mode: str = "full"  # full | basic
    warnings: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.warnings is None:
            self.warnings = []


def _run(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return (r.stdout or r.stderr or "").strip()
    except Exception:
        return ""


def detect() -> CompatReport:
    rep = CompatReport()
    # OS
    import pathlib

    osr = pathlib.Path("/etc/os-release")
    if osr.exists():
        for line in osr.read_text().splitlines():
            if line.startswith("NAME="):
                rep.os_name = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("VERSION_ID="):
                rep.os_version = line.split("=", 1)[1].strip().strip('"')

    # Plasma
    rep.plasma_version = _run(["plasmashell", "--version"])
    # Qt (from PySide6 since qmake may be absent)
    try:
        from PySide6.QtCore import qVersion

        rep.qt_version = qVersion()
    except Exception:
        rep.qt_version = _run(["qmake6", "-query", "QT_VERSION"]) or _run(["qmake", "-query", "QT_VERSION"])
    # Python
    import sys

    rep.python_version = sys.version.split()[0]
    # Session
    import os

    rep.session_type = os.environ.get("XDG_SESSION_TYPE", "unknown")
    # GPU
    rep.gpu = _run(["bash", "-c", "lspci | grep -iE 'vga|display|3d' | head -1"])

    # Support decision
    if "Fedora" not in rep.os_name:
        rep.warnings.append("Not Fedora — best-effort only")
    try:
        fv = int(rep.os_version.split(".")[0]) if rep.os_version else 0
    except ValueError:
        fv = 0
    if fv and fv < 40:
        rep.supported = False
        rep.mode = "basic"
        rep.warnings.append(f"Fedora {fv} < 40 — not supported")
    if "5." in rep.plasma_version or "Plasma 5" in rep.plasma_version:
        rep.mode = "basic" if rep.mode == "full" else rep.mode
        rep.warnings.append("Plasma 5.x — best-effort fallback (no KWin blur API v2)")
    if rep.session_type not in ("wayland", "x11"):
        rep.warnings.append(f"Unknown session type: {rep.session_type}")
    return rep


def has_kwin_blur() -> bool:
    return shutil.which("kwriteconfig6") is not None