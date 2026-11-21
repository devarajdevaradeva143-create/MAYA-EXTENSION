"""Maya theme CLI entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from maya_theme import __version__
from maya_theme.core import backup, compat, install, rollback, uninstall
from maya_theme.core.config import MAYA_HOME, load_config, save_config


def _print(obj) -> None:
    print(json.dumps(obj, indent=2, default=str))


def cmd_install(args) -> int:
    cfg = load_config()
    res = install.install(cfg)
    _print(res)
    return 0 if res.get("success") else 1


def cmd_uninstall(args) -> int:
    _print(uninstall.uninstall())
    return 0


def cmd_rollback(args) -> int:
    _print(rollback.rollback())
    return 0


def cmd_status(args) -> int:
    rep = compat.detect()
    print(f"Maya Extension v{__version__}")
    print(f"OS: {rep.os_name} {rep.os_version}")
    print(f"Plasma: {rep.plasma_version}")
    print(f"Qt: {rep.qt_version}")
    print(f"Python: {rep.python_version}")
    print(f"Session: {rep.session_type}")
    print(f"GPU: {rep.gpu}")
    print(f"Mode: {rep.mode}  supported={rep.supported}")
    for w in rep.warnings:
        print(f"  warn: {w}")
    cfg = load_config()
    print(f"Config: {MAYA_HOME / 'config.json'}")
    print(f"Glass enabled: {cfg['glass']['enabled']}  blur={cfg['glass']['blur']}")
    print(f"Theme mode: {cfg['theme']['mode']}")
    return 0


def cmd_backup(args) -> int:
    p = backup.create_backup("manual")
    print(f"Backup created: {p}")
    return 0


def cmd_settings(args) -> int:
    try:
        from maya_theme.settings.main import run_settings
    except Exception as e:
        print(f"Settings app unavailable: {e}")
        return 1
    run_settings()
    return 0


def cmd_monitor(args) -> int:
    import json

    from maya_theme.monitor.metrics import collect, to_dict

    print(json.dumps(to_dict(collect()), indent=2))
    return 0


def cmd_wallpaper(args) -> int:
    from maya_theme.core import wallpaper

    if args.wpcmd == "list":
        for w in wallpaper.list_wallpapers():
            print(w)
        return 0
    if args.wpcmd == "set":
        if not args.path:
            print("path required")
            return 1
        print(wallpaper.set_wallpaper(args.path))
        return 0
    if args.wpcmd == "next":
        print(wallpaper.slideshow_next())
        return 0
    if args.wpcmd == "upload":
        if not args.path:
            print("path required")
            return 1
        print(wallpaper.upload_custom(args.path))
        return 0
    if args.wpcmd == "parallax":
        if args.flag is None:
            print("specify 'on' or 'off'")
            return 1
        print(wallpaper.enable_parallax(args.flag == "on"))
        return 0
    if args.wpcmd == "pack":
        out = wallpaper.generate_themed_pack()
        print(f"Themed wallpaper pack generated: {out}")
        return 0
    return 0


def cmd_voice(args) -> int:
    from maya_theme.core import voice

    if args.text:
        text = " ".join(args.text)
        result = voice.handle_command(text)
        print(result.get("reply", result.get("error", "done")))
        if not result.get("success"):
            return 1
        return 0
    else:
        print(voice.greet())
        return 0


def cmd_panel(args) -> int:
    from maya_theme.core import panel

    print(panel.apply_centered_panel())
    return 0


def cmd_safe_mode(args) -> int:
    from maya_theme.core import safemode

    if args.smcmd == "on":
        p = safemode.enable_safe_mode()
        print(f"Safe mode enabled. Flag: {p}")
        return 0
    if args.smcmd == "off":
        existed = safemode.disable_safe_mode()
        print(f"Safe mode disabled. Flag {'removed' if existed else 'was not set'}.")
        return 0
    if args.smcmd == "status":
        _print(safemode.safe_mode_status())
        return 0
    if args.smcmd == "install-autostart":
        p = safemode.install_autostart()
        print(f"Autostart entry installed: {p}")
        return 0
    return 0


def cmd_perf(args) -> int:
    from maya_theme.core.perf_monitor import get_monitor

    mon = get_monitor()
    if args.perf_cmd == "check":
        _print(mon.check())
        return 0
    if args.perf_cmd == "usage":
        print(mon.format_usage())
        return 0
    if args.perf_cmd == "auto":
        _print(mon.auto_apply_balanced())
        return 0
    return 0


def cmd_update(args) -> int:
    sub = args.update_cmd
    if sub == "check":
        from maya_theme.core.update import check_update

        _print(check_update())
    elif sub == "apply":
        from maya_theme.core.update import apply_update

        _print(apply_update())
    elif sub == "configure":
        cfg = load_config()
        if args.url:
            cfg.setdefault("privacy", {})["update_url"] = args.url
        cfg["privacy"]["update_checks"] = True
        save_config(cfg)
        print("Update checks configured.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="maya-theme", description="Maya Extension theme CLI")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("install", help="Install + apply theme")
    sub.add_parser("uninstall", help="Remove + restore defaults")
    sub.add_parser("rollback", help="Restore last backup")
    sub.add_parser("status", help="Show state + version")
    sub.add_parser("backup", help="Manual backup")
    sub.add_parser("settings", help="Open settings app")
    sub.add_parser("monitor", help="Print live system metrics")

    wp = sub.add_parser("wallpaper", help="Wallpaper management")
    wp.add_argument("wpcmd", choices=["set", "next", "upload", "list", "parallax", "pack"])
    wp.add_argument("path", nargs="?", help="Wallpaper path (for 'set'/'upload')")
    wp.add_argument("--flag", choices=["on", "off"], help="Enable/disable parallax")

    sh = sub.add_parser("voice", help="Voice/AI command")
    sh.add_argument("text", nargs="*", help="Command text, e.g. 'dark mode'")

    sub.add_parser("panel", help="Apply centered panel layout")

    sm = sub.add_parser("safe-mode", help="Safe mode management")
    sm.add_argument("smcmd", choices=["on", "off", "status", "install-autostart"])

    pf = sub.add_parser("perf", help="Performance budget monitor")
    pf.add_argument("perf_cmd", choices=["check", "usage", "auto"])

    up = sub.add_parser("update", help="Update management")
    up.add_argument("update_cmd", choices=["check", "apply", "configure"])
    up.add_argument("--url", default=None, help="Manifest URL for configure")

    ex = sub.add_parser("export", help="Export theme bundle")
    ex.add_argument("path", help="Output path (.json or .zip)")
    ex.add_argument("--wallpaper", action="store_true")
    im = sub.add_parser("import", help="Import theme bundle")
    im.add_argument("path", help="Input bundle path")

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "export":
        out = Path(args.path)
        p = backup.export_bundle(out, include_wallpaper=args.wallpaper)
        print(f"Exported: {p}")
        return 0
    if args.command == "import":
        cfg = backup.import_bundle(Path(args.path))
        print(f"Imported config version {cfg.get('version')}")
        return 0

    handlers = {
        "install": cmd_install,
        "uninstall": cmd_uninstall,
        "rollback": cmd_rollback,
        "status": cmd_status,
        "backup": cmd_backup,
        "settings": cmd_settings,
        "update": cmd_update,
        "monitor": cmd_monitor,
        "wallpaper": cmd_wallpaper,
        "voice": cmd_voice,
        "panel": cmd_panel,
        "safe-mode": cmd_safe_mode,
        "perf": cmd_perf,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())