"""KCM wrapper: launches Maya settings inside System Settings context."""

from __future__ import annotations

import sys

from maya_theme.settings.main import run_settings


def main() -> int:
    # When invoked by System Settings, embed via external process.
    return run_settings()


if __name__ == "__main__":
    sys.exit(main())