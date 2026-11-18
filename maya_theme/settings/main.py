"""Entry point for the Maya settings application."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

QML_DIR = Path(__file__).parent / "ui"


def run_settings() -> int:
    app = QGuiApplication(sys.argv)
    app.setApplicationName("Maya Settings")
    app.setOrganizationName("Maya")

    from .controller import SettingsController

    controller = SettingsController()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("settings", controller)
    qml_file = QML_DIR / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        print("Failed to load QML:", qml_file)
        return 1
    return app.exec()


if __name__ == "__main__":
    sys.exit(run_settings())