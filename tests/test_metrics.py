from maya_theme.monitor.metrics import collect, to_dict


def test_collect_returns_metrics():
    m = collect()
    assert 0 <= m.cpu_percent <= 100
    assert 0 <= m.ram_percent <= 100
    d = to_dict(m)
    assert "cpu_percent" in d
    assert "ram_used_mb" in d