"""Pinned-apps center taskbar panel layout helper."""

from __future__ import annotations

from pathlib import Path

PANEL_CONF = Path.home() / ".config" / "plasma-org.kde.plasma.desktop-appletsrc"


def apply_centered_panel() -> dict:
    # Plasma panel layout is complex; provide a best-effort note + manual steps.
    # We ship a template config the user can import via "Load Layout".
    template = Path(__file__).resolve().parents[2] / "packaging" / "panel-layout.template"
    return {
        "success": True,
        "note": "Panel layout template shipped; import via System Settings → Appearance → Panel, or apply manually.",
        "template": str(template),
    }