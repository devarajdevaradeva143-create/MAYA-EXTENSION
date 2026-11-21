"""Tests for install → rollback → uninstall cycle (integration-level).

These tests mock out the actual KWin/Plasma calls so they can run in CI
without a Plasma session.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from maya_theme.core import backup, install, rollback, uninstall


@pytest.fixture(autouse=True)
def _config(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    monkeypatch.setattr(c, "MAYA_HOME", tmp_path / "maya")
    monkeypatch.setattr(c, "CONFIG_FILE", tmp_path / "maya/config.json")
    monkeypatch.setattr(c, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(c, "BACKUP_DIR", tmp_path / "backups")
    (tmp_path / "maya").mkdir(parents=True)
    c.save_config(c.DEFAULT_CONFIG)
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path / "backups")
    monkeypatch.setattr(backup, "MAYA_HOME", tmp_path / "maya")
    monkeypatch.setattr(install, "MAYA_HOME", tmp_path / "maya")


def test_install_creates_backup():
    """Install should create a backup before applying."""
    with patch.object(install, "pre_check", return_value=(True, "ok")), \
         patch.object(install, "restart_plasma", return_value=True), \
         patch.object(install, "install_theme_files"):
        res = install.install()
    assert res["success"] is True
    assert "backup" in res
    assert Path(res["backup"]).exists()


def test_install_fails_on_unsupported():
    with patch.object(install, "pre_check", return_value=(False, "unsupported")):
        res = install.install()
    assert res["success"] is False
    assert "unsupported" in res["error"].lower()


def test_rollback_restores_backup(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    # create a backup first
    cfg = c.load_config()
    cfg["glass"]["blur"] = 10
    c.save_config(cfg)
    p = backup.create_backup("test-rollback")

    # change config
    cfg["glass"]["blur"] = 99
    c.save_config(cfg)
    assert c.load_config()["glass"]["blur"] == 99

    # rollback
    with patch("maya_theme.core.install.restart_plasma", return_value=True):
        r = rollback.rollback()
    assert r["success"] is True
    assert c.load_config()["glass"]["blur"] == 10


def test_uninstall_removes_theme_files(tmp_path, monkeypatch):
    theme_dir = tmp_path / "maya" / "theme"
    theme_dir.mkdir(parents=True)
    (theme_dir / "test.css").write_text("test")

    uninstall.MAYA_HOME = tmp_path / "maya"
    monkeypatch.setattr(uninstall, "MAYA_HOME", tmp_path / "maya")

    r = uninstall.uninstall()
    assert r["success"] is True
    assert not theme_dir.exists()


def test_install_uninstall_rollback_cycle():
    """Full cycle: install → rollback → uninstall, all should succeed."""
    with patch.object(install, "pre_check", return_value=(True, "ok")), \
         patch.object(install, "restart_plasma", return_value=True), \
         patch.object(install, "install_theme_files"):
        res_install = install.install()
        assert res_install["success"] is True

    with patch("maya_theme.core.install.restart_plasma", return_value=True):
        res_rollback = rollback.rollback()
        assert res_rollback["success"] is True

    res_uninstall = uninstall.uninstall()
    assert res_uninstall["success"] is True


def test_config_preserved_through_cycle(tmp_path, monkeypatch):
    """Config should be restorable after install/rollback."""
    import maya_theme.core.config as c

    # set a known config
    cfg = c.load_config()
    cfg["theme"]["mode"] = "light"
    cfg["glass"]["blur"] = 15
    c.save_config(cfg)

    # backup
    backup.create_backup("cycle-test")

    # change
    cfg["theme"]["mode"] = "dark"
    cfg["glass"]["blur"] = 35
    c.save_config(cfg)

    # rollback
    with patch("maya_theme.core.install.restart_plasma", return_value=True):
        rollback.rollback()

    restored = c.load_config()
    assert restored["theme"]["mode"] == "light"
    assert restored["glass"]["blur"] == 15