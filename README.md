# ✦ Maya Extension — Liquid Glass Theme for Fedora KDE

> Local-first, premium liquid glass morphism theme for **Fedora 40+ / KDE Plasma 6.x**.
> Tagline: *local only • your assistant*

## Features
- Liquid glass morphism across the whole desktop (KWin blur, Qt/GTK apps, panels, notifications)
- User-selectable blur/transparency, light/dark, accent color, scope toggles
- Windows 11-style pinned apps center taskbar, right-side quick settings shade
- Visual system monitoring widgets (CPU/RAM/GPU/NPU/battery/disk/network/temp)
- Safe install with backup + auto-rollback (10s timeout)
- Export/import theme bundles, opt-in auto-update with GPG signature verification
- **AI voice command interface** — natural language theme control ("dark mode", "blur 30", "accent purple")
- **Performance budget monitor** — tracks Maya's own CPU/RAM, suggests "Balanced" mode if budget exceeded
- **Safe mode** — hold Shift at login to skip Maya theme load
- **Animated & parallax wallpapers** + Maya-themed SVG wallpaper pack generator
- **Responsive settings UI** — sidebar on desktop, bottom tabs on mobile (<768px)
- **Liquid glass spec** — noise grain, 0.5px inner highlight, 3D flip-in animations, success bounce

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
| `maya-theme monitor` | Print live system metrics |
| `maya-theme wallpaper list/set/next/upload/parallax/pack` | Wallpaper management |
| `maya-theme voice "dark mode"` | AI voice command |
| `maya-theme safe-mode on/off/status` | Safe mode control |
| `maya-theme perf check/usage/auto` | Performance budget monitor |
| `maya-theme update check/apply/configure` | Auto-update management |
| `maya-theme export/import` | Theme bundle export/import |

## AI Voice Commands
Natural language theme control with Maya's friendly Thanglish personality:
```
maya-theme voice "dark mode"          # → theme → dark
maya-theme voice "light mode"         # → theme → light
maya-theme voice "blur 30"            # → blur → 30px
maya-theme voice "blur increase"      # → blur +4
maya-theme voice "accent purple"      # → accent → #A855F7
maya-theme voice "performance battery" # → preset → battery
maya-theme voice "glass off"          # → glass disabled
maya-theme voice "status"             # → current setup summary
```

## Requirements
- Fedora 40+ (KDE Plasma spin)
- Plasma 6.x (5.x best-effort)
- Python 3.12+, PySide6 6.6+
- Wayland (primary) / X11 (fallback)

## Testing
```bash
# quick tests (skip slow soak)
pytest tests/ -m "not slow"

# full 1-hour soak test
pytest tests/ --soak-duration=3600

# update golden images for visual regression
UPDATE_GOLDEN=1 pytest tests/test_visual.py
```

## Privacy
Local-first. No telemetry. No cloud calls by default. See `docs/privacy.md`.

## License
MIT