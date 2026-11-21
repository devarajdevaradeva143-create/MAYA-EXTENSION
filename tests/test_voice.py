"""Tests for voice/AI command parsing."""


import pytest

from maya_theme.core import voice


@pytest.fixture(autouse=True)
def _config(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    monkeypatch.setattr(c, "MAYA_HOME", tmp_path / "maya")
    monkeypatch.setattr(c, "CONFIG_FILE", tmp_path / "maya/config.json")
    monkeypatch.setattr(c, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(c, "BACKUP_DIR", tmp_path / "backups")
    (tmp_path / "maya").mkdir(parents=True)
    c.save_config(c.DEFAULT_CONFIG)


def test_dark_mode():
    r = voice.handle_command("maya change to dark")
    assert r["success"] is True
    assert "theme" in str(r["applied"])
    assert r["config"]["theme"]["mode"] == "dark"


def test_light_mode():
    r = voice.handle_command("switch to light")
    assert r["success"] is True
    assert r["config"]["theme"]["mode"] == "light"


def test_blur_value():
    r = voice.handle_command("set blur to 30")
    assert r["success"] is True
    assert r["config"]["glass"]["blur"] == 30


def test_blur_increase():
    r = voice.handle_command("blur increase")
    assert r["success"] is True
    # default 28 + 4 = 32
    assert r["config"]["glass"]["blur"] == 32


def test_blur_decrease():
    r = voice.handle_command("blur decrease")
    assert r["success"] is True
    # default 28 - 4 = 24
    assert r["config"]["glass"]["blur"] == 24


def test_accent_color():
    r = voice.handle_command("make it purple")
    assert r["success"] is True
    assert r["config"]["theme"]["accent_start"] == "#A855F7"


def test_accent_hex():
    r = voice.handle_command("accent #3B82F6")
    assert r["success"] is True
    assert r["config"]["theme"]["accent_start"] == "#3B82F6"


def test_performance_preset():
    r = voice.handle_command("performance battery saver")
    assert r["success"] is True
    assert r["config"]["performance"]["preset"] == "battery"


def test_glass_off():
    r = voice.handle_command("glass off")
    assert r["success"] is True
    assert r["config"]["glass"]["enabled"] is False


def test_glass_on():
    # first turn off
    voice.handle_command("glass off")
    # then on
    r = voice.handle_command("glass on")
    assert r["success"] is True
    assert r["config"]["glass"]["enabled"] is True


def test_scope_toggle():
    r = voice.handle_command("disable gtk apps")
    assert r["success"] is True
    assert r["config"]["scope"]["gtk_apps"] is False


def test_scope_enable():
    # first disable
    voice.handle_command("disable gtk")
    # then enable
    r = voice.handle_command("enable gtk apps")
    assert r["success"] is True
    assert r["config"]["scope"]["gtk_apps"] is True


def test_transparency_percentage():
    r = voice.handle_command("transparency dark 60%")
    assert r["success"] is True
    assert abs(r["config"]["glass"]["transparency_dark"] - 0.6) < 0.01


def test_monitor_toggle():
    r = voice.handle_command("monitor off")
    assert r["success"] is True
    assert r["config"]["monitor"]["enabled"] is False


def test_status_command():
    r = voice.handle_command("what is the current status")
    assert r["success"] is True
    assert "reply" in r
    assert "dark" in r["reply"].lower() or "mode" in r["reply"].lower()


def test_unknown_command():
    r = voice.handle_command("make me a sandwich")
    assert r["success"] is False
    assert "reply" in r


def test_empty_command():
    r = voice.handle_command("")
    assert r["success"] is False


def test_greet():
    g = voice.greet()
    assert isinstance(g, str)
    assert len(g) > 0


def test_reply_has_maya_tone():
    r = voice.handle_command("dark mode")
    assert r["success"] is True
    # Maya tone: friendly Thanglish
    reply = r["reply"].lower()
    assert "da" in reply or "done" in reply or "maya" in reply