
from maya_theme.core.config import (
    DEFAULT_CONFIG,
    GlassSpec,
    load_config,
    save_config,
)


def test_default_config_has_glass():
    assert DEFAULT_CONFIG["glass"]["enabled"] is True
    assert "blur" in DEFAULT_CONFIG["glass"]


def test_glass_spec_css():
    g = GlassSpec(blur=20, transparency_dark=0.7)
    css = g.to_css(dark=True)
    assert "blur(20px)" in css
    assert "rgba(11,15,25,0.7)" in css


def test_config_roundtrip(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    monkeypatch.setattr(c, "MAYA_HOME", tmp_path)
    monkeypatch.setattr(c, "CONFIG_FILE", tmp_path / "config.json")
    monkeypatch.setattr(c, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(c, "BACKUP_DIR", tmp_path / "backups")
    cfg = load_config()
    assert cfg["version"] == DEFAULT_CONFIG["version"]
    cfg["glass"]["blur"] = 33
    save_config(cfg)
    cfg2 = load_config()
    assert cfg2["glass"]["blur"] == 33


def test_deep_merge_defaults():
    import maya_theme.core.config as c

    base = {"a": {"b": 1, "c": 2}, "d": 3}
    c._deep_merge(base, {"a": {"b": 9}})
    assert base["a"]["b"] == 9
    assert base["a"]["c"] == 2
    assert base["d"] == 3