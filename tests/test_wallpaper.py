"""Tests for wallpaper: parallax, glass blur, themed pack generation."""

import json

import pytest

from maya_theme.core import wallpaper


@pytest.fixture(autouse=True)
def _config(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    monkeypatch.setattr(c, "MAYA_HOME", tmp_path / "maya")
    monkeypatch.setattr(c, "CONFIG_FILE", tmp_path / "maya/config.json")
    monkeypatch.setattr(c, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(c, "BACKUP_DIR", tmp_path / "backups")
    (tmp_path / "maya").mkdir(parents=True)
    c.save_config(c.DEFAULT_CONFIG)
    monkeypatch.setattr(wallpaper, "WALL_DIR", tmp_path / "wallpapers")
    monkeypatch.setattr(wallpaper, "MAYA_WALLS", tmp_path / "maya_walls")


def test_enable_parallax_on():
    r = wallpaper.enable_parallax(True)
    assert r["success"] is True
    assert r["parallax"] is True


def test_enable_parallax_off():
    r = wallpaper.enable_parallax(False)
    assert r["success"] is True
    assert r["parallax"] is False


def test_enable_glass_blur():
    r = wallpaper.enable_glass_blur(True)
    assert r["success"] is True
    assert r["glass_blur"] is True


def test_generate_themed_pack(tmp_path):
    out = wallpaper.generate_themed_pack(tmp_path / "walls")
    assert out.exists()
    # should have SVG wallpapers
    svgs = list(out.glob("*.svg"))
    assert len(svgs) >= 3
    # manifest
    manifest_file = out / "maya-pack-manifest.json"
    assert manifest_file.exists()
    manifest = json.loads(manifest_file.read_text())
    assert "wallpapers" in manifest
    assert manifest["count"] >= 3


def test_themed_pack_has_dark_and_light():
    out = wallpaper.generate_themed_pack()
    names = [p.name for p in out.glob("*.svg")]
    assert any("dark" in n for n in names)
    assert any("light" in n for n in names)


def test_list_wallpapers_empty():
    walls = wallpaper.list_wallpapers()
    assert isinstance(walls, list)


def test_set_wallpaper_not_found():
    r = wallpaper.set_wallpaper("/nonexistent/file.jpg")
    assert r["success"] is False
    assert "not found" in r.get("error", "")


def test_slideshow_next_no_wallpapers():
    r = wallpaper.slideshow_next()
    assert r["success"] is False
    assert "no wallpapers" in r.get("error", "")


def test_svg_wallpaper_content():
    svg = wallpaper._svg_wallpaper("#0B0F19", "#1A1A2E", "#FF7AB8", "#A855F7", dark=True)
    assert "<svg" in svg
    assert "Maya" in svg
    assert "#FF7AB8" in svg or "#ff7ab8" in svg.lower()


def test_svg_wallpaper_light_mode():
    svg = wallpaper._svg_wallpaper("#F5F7FB", "#E8ECF4", "#FF7AB8", "#A855F7", dark=False)
    assert "1F2937" in svg or "#1f2937" in svg.lower()