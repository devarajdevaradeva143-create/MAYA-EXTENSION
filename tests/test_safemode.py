"""Tests for safe mode (§8.3)."""

from pathlib import Path

from maya_theme.core import safemode


def test_safe_mode_flag_file(tmp_path, monkeypatch):
    flag = tmp_path / "safe-mode"
    monkeypatch.setattr(safemode, "MAYA_HOME", tmp_path)
    monkeypatch.setattr(safemode, "SAFE_MODE_FLAG", flag)

    assert safemode.is_safe_mode() is False
    safemode.enable_safe_mode()
    assert flag.exists()
    assert safemode.is_safe_mode() is True
    safemode.disable_safe_mode()
    assert safemode.is_safe_mode() is False


def test_safe_mode_env_var(monkeypatch):
    monkeypatch.setattr(safemode, "MAYA_HOME", Path("/tmp/test_maya"))
    monkeypatch.setattr(safemode, "SAFE_MODE_FLAG", Path("/tmp/test_maya/safe-mode"))
    monkeypatch.setenv("MAYA_SAFE_MODE", "1")
    assert safemode.is_safe_mode() is True
    monkeypatch.delenv("MAYA_SAFE_MODE", raising=False)
    assert safemode.is_safe_mode() is False


def test_safe_mode_status(monkeypatch):
    monkeypatch.setattr(safemode, "MAYA_HOME", Path("/tmp/test_maya2"))
    monkeypatch.setattr(safemode, "SAFE_MODE_FLAG", Path("/tmp/test_maya2/safe-mode"))
    s = safemode.safe_mode_status()
    assert "active" in s
    assert "flag_file" in s
    assert "env_var" in s


def test_safe_mode_entrypoint_returns_1_when_active(tmp_path, monkeypatch):
    flag = tmp_path / "safe-mode"
    monkeypatch.setattr(safemode, "MAYA_HOME", tmp_path)
    monkeypatch.setattr(safemode, "SAFE_MODE_FLAG", flag)
    flag.touch()
    assert safemode.safe_mode_entrypoint() == 1
    # one-shot: flag should be removed
    assert not flag.exists()


def test_safe_mode_entrypoint_returns_0_when_inactive(tmp_path, monkeypatch):
    flag = tmp_path / "safe-mode"
    monkeypatch.setattr(safemode, "MAYA_HOME", tmp_path)
    monkeypatch.setattr(safemode, "SAFE_MODE_FLAG", flag)
    assert safemode.safe_mode_entrypoint() == 0


def test_install_autostart(tmp_path, monkeypatch):
    autostart = tmp_path / "autostart"
    monkeypatch.setattr(safemode.Path, "home", classmethod(lambda cls: tmp_path))
    # patch the home() call inside install_autostart
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    p = safemode.install_autostart()
    assert p.exists()
    assert "Maya Safe Mode" in p.read_text()