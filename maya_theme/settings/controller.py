"""Controller bridging PySide6 settings app to Maya config."""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import QObject, Property, Signal, Slot

from maya_theme.core import backup, compat, install
from maya_theme.core.config import load_config, save_config, DEFAULT_CONFIG


class SettingsController(QObject):
    configChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cfg = load_config()

    # ---- generic accessors ----
    def _g(self, *keys, default=None):
        d = self._cfg
        for k in keys:
            if isinstance(d, dict) and k in d:
                d = d[k]
            else:
                return default
        return d

    def _s(self, value, *keys):
        d = self._cfg
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
        save_config(self._cfg)
        self.configChanged.emit()

    # glass
    @Property(bool, notify=configChanged)
    def glassEnabled(self):
        return self._g("glass", "enabled", default=True)

    @glassEnabled.setter
    def glassEnabled(self, v):
        self._s(bool(v), "glass", "enabled")

    @Property(int, notify=configChanged)
    def glassBlur(self):
        return int(self._g("glass", "blur", default=28))

    @glassBlur.setter
    def glassBlur(self, v):
        self._s(int(v), "glass", "blur")

    @Property(float, notify=configChanged)
    def transpDark(self):
        return float(self._g("glass", "transparency_dark", default=0.72))

    @transpDark.setter
    def transpDark(self, v):
        self._s(float(v), "glass", "transparency_dark")

    @Property(float, notify=configChanged)
    def transpLight(self):
        return float(self._g("glass", "transparency_light", default=0.5))

    @transpLight.setter
    def transpLight(self, v):
        self._s(float(v), "glass", "transparency_light")

    # theme
    @Property(str, notify=configChanged)
    def themeMode(self):
        return str(self._g("theme", "mode", default="dark"))

    @themeMode.setter
    def themeMode(self, v):
        self._s(str(v), "theme", "mode")

    @Property(str, notify=configChanged)
    def accentStart(self):
        return str(self._g("theme", "accent_start", default="#FF7AB8"))

    @accentStart.setter
    def accentStart(self, v):
        self._s(str(v), "theme", "accent_start")

    @Property(str, notify=configChanged)
    def accentEnd(self):
        return str(self._g("theme", "accent_end", default="#A855F7"))

    @accentEnd.setter
    def accentEnd(self, v):
        self._s(str(v), "theme", "accent_end")

    # scope
    def _scope(self, key):
        return bool(self._g("scope", key, default=True))

    def _set_scope(self, key, v):
        self._s(bool(v), "scope", key)

    @Property(bool, notify=configChanged)
    def scopeKwin(self):
        return self._scope("kwin")

    @scopeKwin.setter
    def scopeKwin(self, v):
        self._set_scope("kwin", v)

    @Property(bool, notify=configChanged)
    def scopeQt(self):
        return self._scope("qt_apps")

    @scopeQt.setter
    def scopeQt(self, v):
        self._set_scope("qt_apps", v)

    @Property(bool, notify=configChanged)
    def scopeGtk(self):
        return self._scope("gtk_apps")

    @scopeGtk.setter
    def scopeGtk(self, v):
        self._set_scope("gtk_apps", v)

    @Property(bool, notify=configChanged)
    def scopePanels(self):
        return self._scope("panels")

    @scopePanels.setter
    def scopePanels(self, v):
        self._set_scope("panels", v)

    @Property(bool, notify=configChanged)
    def scopeNotifs(self):
        return self._scope("notifications")

    @scopeNotifs.setter
    def scopeNotifs(self, v):
        self._set_scope("notifications", v)

    # performance
    @Property(str, notify=configChanged)
    def perfPreset(self):
        return str(self._g("performance", "preset", default="balanced"))

    @perfPreset.setter
    def perfPreset(self, v):
        self._s(str(v), "performance", "preset")

    @Property(bool, notify=configChanged)
    def autoReduceBlur(self):
        return bool(self._g("performance", "auto_reduce_blur", default=True))

    @autoReduceBlur.setter
    def autoReduceBlur(self, v):
        self._s(bool(v), "performance", "auto_reduce_blur")

    # monitor
    @Property(bool, notify=configChanged)
    def monitorEnabled(self):
        return bool(self._g("monitor", "enabled", default=True))

    @monitorEnabled.setter
    def monitorEnabled(self, v):
        self._s(bool(v), "monitor", "enabled")

    @Property(int, notify=configChanged)
    def monitorInterval(self):
        return int(self._g("monitor", "interval", default=2))

    @monitorInterval.setter
    def monitorInterval(self, v):
        self._s(int(v), "monitor", "interval")

    # privacy
    @Property(bool, notify=configChanged)
    def updateChecks(self):
        return bool(self._g("privacy", "update_checks", default=False))

    @updateChecks.setter
    def updateChecks(self, v):
        self._s(bool(v), "privacy", "update_checks")

    # slots
    @Slot()
    def applyTheme(self):
        install.apply_config(self._cfg)

    @Slot()
    def createBackup(self):
        backup.create_backup("manual")

    @Slot(result=str)
    def compatReport(self):
        rep = compat.detect()
        return json.dumps(
            {
                "os": f"{rep.os_name} {rep.os_version}",
                "plasma": rep.plasma_version,
                "qt": rep.qt_version,
                "session": rep.session_type,
                "mode": rep.mode,
                "supported": rep.supported,
                "warnings": rep.warnings,
            }
        )

    @Slot(result=str)
    def exportConfig(self):
        p = backup.export_bundle(Path.home() / "Documents" / "maya-theme.json")
        return str(p)

    @Slot(str, result=bool)
    def importConfig(self, path):
        try:
            backup.import_bundle(Path(path))
            self._cfg = load_config()
            self.configChanged.emit()
            return True
        except Exception:
            return False

    @Slot()
    def resetDefaults(self):
        self._cfg = json.loads(json.dumps(DEFAULT_CONFIG))
        save_config(self._cfg)
        self.configChanged.emit()