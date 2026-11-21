"""Tests for performance budget monitor (§10.3)."""


import pytest

from maya_theme.core import perf_monitor


@pytest.fixture(autouse=True)
def _config(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    monkeypatch.setattr(c, "MAYA_HOME", tmp_path / "maya")
    monkeypatch.setattr(c, "CONFIG_FILE", tmp_path / "maya/config.json")
    monkeypatch.setattr(c, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(c, "BACKUP_DIR", tmp_path / "backups")
    (tmp_path / "maya").mkdir(parents=True)
    c.save_config(c.DEFAULT_CONFIG)


def test_budget_constants():
    assert perf_monitor.BUDGET["cpu_percent"] == 2.0
    assert perf_monitor.BUDGET["ram_mb"] == 150.0
    assert perf_monitor.BUDGET["gpu_percent"] == 5.0


def test_monitor_check_returns_dict():
    mon = perf_monitor.PerfBudgetMonitor()
    r = mon.check()
    assert "over_budget" in r
    assert "suggest_balanced" in r
    assert "metrics" in r
    assert "message" in r


def test_monitor_usage_format():
    mon = perf_monitor.PerfBudgetMonitor()
    u = mon.format_usage()
    assert "Maya" in u
    assert "CPU" in u
    assert "RAM" in u


def test_monitor_no_suggestion_immediately():
    mon = perf_monitor.PerfBudgetMonitor()
    r = mon.check()
    # fresh monitor, not over budget long enough
    assert r["suggest_balanced"] is False


def test_auto_apply_balanced_in_quality():
    import maya_theme.core.config as c

    cfg = c.load_config()
    cfg["performance"]["preset"] = "quality"
    cfg["performance"]["auto_reduce_blur"] = True
    cfg["glass"]["blur"] = 36
    c.save_config(cfg)

    mon = perf_monitor.PerfBudgetMonitor()
    r = mon.auto_apply_balanced()
    assert r["success"] is True
    assert r["switched_to"] == "balanced"

    cfg2 = c.load_config()
    assert cfg2["performance"]["preset"] == "balanced"
    assert cfg2["glass"]["blur"] <= 16


def test_auto_apply_balanced_not_in_quality():
    import maya_theme.core.config as c

    cfg = c.load_config()
    cfg["performance"]["preset"] = "balanced"
    c.save_config(cfg)

    mon = perf_monitor.PerfBudgetMonitor()
    r = mon.auto_apply_balanced()
    assert r["success"] is False


def test_auto_apply_disabled():
    import maya_theme.core.config as c

    cfg = c.load_config()
    cfg["performance"]["preset"] = "quality"
    cfg["performance"]["auto_reduce_blur"] = False
    c.save_config(cfg)

    mon = perf_monitor.PerfBudgetMonitor()
    r = mon.auto_apply_balanced()
    assert r["success"] is False


def test_get_monitor_singleton():
    m1 = perf_monitor.get_monitor()
    m2 = perf_monitor.get_monitor()
    assert m1 is m2