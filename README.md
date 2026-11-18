# ✦ Maya Extension — Liquid Glass Theme for Fedora KDE

> Local-first, premium liquid glass morphism theme for **Fedora 40+ / KDE Plasma 6.x**.
> Tagline: *local only • your assistant*

## Features
- Liquid glass morphism across the whole desktop (KWin blur, Qt/GTK apps, panels, notifications)
- User-selectable blur/transparency, light/dark, accent color, scope toggles
- Windows 11-style pinned apps center taskbar, right-side quick settings shade
- Visual system monitoring widgets (CPU/RAM/GPU/NPU/battery/disk/network/temp)
- Safe install with backup + auto-rollback (10s timeout)
- Export/import theme bundles, opt-in auto-update

## Quick Start
```bash
# install (user-level, no root)
python -m pip install -e .
maya-theme install
```

## Commands
| Command | Purpose |
|---|---|
| `maya-theme install` | Install + apply |
| `maya-theme uninstall` | Remove + restore |
| `maya-theme rollback` | Restore last backup |
| `maya-theme status` | Current state + version |
| `maya-theme backup` | Manual backup |
| `maya-theme settings` | Open settings app |
| `maya-theme update check` | Check available version |

## Requirements
- Fedora 40+ (KDE Plasma spin)
- Plasma 6.x (5.x best-effort)
- Python 3.12+, PySide6 6.6+
- Wayland (primary) / X11 (fallback)

## Privacy
Local-first. No telemetry. No cloud calls by default. See `docs/privacy.md`.

## License
MIT