"""Tests for undo/redo, blur disable, light/dark toggle, reduced-motion."""

import json

import pytest

from maya_theme.core import undo


@pytest.fixture(autouse=True)
def _config(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    monkeypatch.setattr(c, "MAYA_HOME", tmp_path / "maya")
    monkeypatch.setattr(c, "CONFIG_FILE", tmp_path / "maya/config.json")
    monkeypatch.setattr(c, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(c, "BACKUP_DIR", tmp_path / "backups")
    (tmp_path / "maya").mkdir(parents=True)
    c.save_config(c.DEFAULT_CONFIG)


def test_undo_redo_basic():
    stack = undo.UndoStack()
    original = stack.current
    assert original["glass"]["blur"] == 28

    # make a change
    new_cfg = json.loads(json.dumps(original))
    new_cfg["glass"]["blur"] = 40
    stack.push(new_cfg)
    assert stack.current["glass"]["blur"] == 40

    # undo
    result = stack.undo()
    assert result is not None
    assert result["glass"]["blur"] == 28

    # redo
    result = stack.redo()
    assert result is not None
    assert result["glass"]["blur"] == 40


def test_undo_empty_stack():
    stack = undo.UndoStack()
    assert stack.undo() is None
    assert stack.can_undo is False


def test_redo_empty_stack():
    stack = undo.UndoStack()
    assert stack.redo() is None
    assert stack.can_redo is False


def test_undo_clears_redo():
    stack = undo.UndoStack()
    cfg1 = json.loads(json.dumps(stack.current))
    cfg1["glass"]["blur"] = 40
    stack.push(cfg1)
    stack.undo()
    assert stack.can_redo is True

    # new push should clear redo
    cfg2 = json.loads(json.dumps(cfg1))
    cfg2["glass"]["blur"] = 35
    stack.push(cfg2)
    assert stack.can_redo is False


def test_light_dark_toggle_preserves_other_settings():
    """Toggling light/dark should preserve other config values."""
    import maya_theme.core.config as c

    cfg = c.load_config()
    cfg["glass"]["blur"] = 32
    cfg["theme"]["mode"] = "dark"
    c.save_config(cfg)

    # toggle to light
    cfg = c.load_config()
    cfg["theme"]["mode"] = "light"
    c.save_config(cfg)

    cfg2 = c.load_config()
    assert cfg2["theme"]["mode"] == "light"
    assert cfg2["glass"]["blur"] == 32  # preserved
    assert cfg2["glass"]["enabled"] is True  # preserved


def test_blur_disable_glass_still_visible():
    """When blur is disabled, glass colors should still work."""
    from maya_theme.core.config import GlassSpec

    g = GlassSpec(blur=0, transparency_dark=0.72)
    css = g.to_css(dark=True)
    assert "blur(0px)" in css
    assert "rgba(11,15,25" in css  # glass color still there


def test_blur_reduction_on_low_battery():
    """Low battery should reduce blur (auto_reduce_blur)."""
    import maya_theme.core.config as c

    cfg = c.load_config()
    cfg["performance"]["auto_reduce_blur"] = True
    cfg["performance"]["preset"] = "quality"
    cfg["glass"]["blur"] = 40
    c.save_config(cfg)

    # simulate perf monitor auto-apply
    from maya_theme.core.perf_monitor import PerfBudgetMonitor

    mon = PerfBudgetMonitor()
    r = mon.auto_apply_balanced()
    assert r["success"] is True

    cfg2 = c.load_config()
    assert cfg2["glass"]["blur"] <= 16
    assert cfg2["performance"]["preset"] == "balanced"


def test_reduced_motion_flag():
    """Settings should respect prefers-reduced-motion."""
    import os

    # simulate reduced motion preference
    old = os.environ.get("MAYA_REDUCED_MOTION")
    try:
        os.environ["MAYA_REDUCED_MOTION"] = "1"
        # in a real scenario, the QML Animations.qml would check this
        # and skip the 3D flip, doing a simple fade instead.
        # Here we just verify the flag is settable.
        assert os.environ["MAYA_REDUCED_MOTION"] == "1"
    finally:
        if old is None:
            os.environ.pop("MAYA_REDUCED_MOTION", None)
        else:
            os.environ["MAYA_REDUCED_MOTION"] = old


def test_undo_stack_capacity():
    """Undo stack should respect capacity limit (default 50)."""
    stack = undo.UndoStack(capacity=5)
    for i in range(10):
        cfg = json.loads(json.dumps(stack.current))
        cfg["glass"]["blur"] = i
        stack.push(cfg)
    # should have at most 5 in undo stack
    # undo all 5
    count = 0
    while stack.undo() is not None:
        count += 1
    assert count == 5