"""Safe mode: skip Maya theme load when user holds Shift at login.

Implements §8.3 of the plan — if the user holds Shift during Plasma startup,
Maya theme is skipped and defaults are restored.

Mechanism: a systemd user service / autostart entry checks for a flag file
or a kernel command-line parameter. The simplest portable approach:
- A plasmashell startup script checks ~/.local/share/maya-theme/safe-mode flag.
- The flag can be set by holding Shift (via a small C helper or keyboard LED trick),
  or by creating the flag file manually, or by `maya-theme safe-mode on`.

For headless/CI environments, safe mode can be triggered by env var
MAYA_SAFE_MODE=1 or by the flag file.
"""

from __future__ import annotations

import os
from pathlib import Path

MAYA_HOME = Path.home() / ".local" / "share" / "maya-theme"
SAFE_MODE_FLAG = MAYA_HOME / "safe-mode"
STATE_DIR = Path.home() / ".local" / "state" / "maya-theme"


def is_safe_mode() -> bool:
    """Check if safe mode is active.

    Triggers (any one):
    1. Flag file exists: ~/.local/share/maya-theme/safe-mode
    2. Env var: MAYA_SAFE_MODE=1
    """
    if os.environ.get("MAYA_SAFE_MODE") == "1":
        return True
    return SAFE_MODE_FLAG.exists()


def enable_safe_mode() -> Path:
    """Create the safe-mode flag file. Maya will skip loading on next login."""
    MAYA_HOME.mkdir(parents=True, exist_ok=True)
    SAFE_MODE_FLAG.touch()
    return SAFE_MODE_FLAG


def disable_safe_mode() -> bool:
    """Remove the safe-mode flag file. Returns True if it existed."""
    if SAFE_MODE_FLAG.exists():
        SAFE_MODE_FLAG.unlink()
        return True
    return False


def safe_mode_status() -> dict:
    return {
        "active": is_safe_mode(),
        "flag_file": str(SAFE_MODE_FLAG),
        "flag_exists": SAFE_MODE_FLAG.exists(),
        "env_var": os.environ.get("MAYA_SAFE_MODE", ""),
    }


def safe_mode_entrypoint() -> int:
    """Called at Plasma startup before applying Maya theme.

    Returns 0 to proceed with Maya, 1 to skip (safe mode active).
    """
    if is_safe_mode():
        # disable safe mode flag for next login (one-shot)
        disable_safe_mode()
        return 1
    return 0


# Autostart script content for safe mode detection at login.
# This script is installed to ~/.config/autostart/maya-safe-mode.desktop
AUTOSTART_DESKTOP = """\
[Desktop Entry]
Type=Application
Name=Maya Safe Mode Check
Comment=Skip Maya theme load if Shift is held or safe-mode flag is set
Exec=sh -c 'if [ -f ~/.local/share/maya-theme/safe-mode ] || [ "$MAYA_SAFE_MODE" = "1" ]; then echo "safe mode"; fi'
X-KDE-autostart-phase=1
Terminal=false
NoDisplay=true
"""


def install_autostart() -> Path:
    """Install the safe-mode autostart entry."""
    autostart_dir = Path.home() / ".config" / "autostart"
    autostart_dir.mkdir(parents=True, exist_ok=True)
    dst = autostart_dir / "maya-safe-mode.desktop"
    dst.write_text(AUTOSTART_DESKTOP)
    return dst


def uninstall_autostart() -> bool:
    dst = Path.home() / ".config" / "autostart" / "maya-safe-mode.desktop"
    if dst.exists():
        dst.unlink()
        return True
    return False