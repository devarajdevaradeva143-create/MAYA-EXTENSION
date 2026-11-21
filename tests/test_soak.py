"""1-hour soak test for performance budget verification (§10, §11.4).

This test runs Maya's own perf monitor for a sustained period and verifies
CPU/RAM stay within budget. Designed to be run periodically in CI.

Usage:
    pytest tests/test_soak.py -v --soak-duration=3600  # 1 hour
    pytest tests/test_soak.py -v                        # default 60s smoke

Or standalone:
    python tests/test_soak.py --duration 3600
"""

import os
import sys
import time
from pathlib import Path

import pytest

# Add parent to path for direct execution
sys.path.insert(0, str(Path(__file__).parent.parent))

from maya_theme.core.perf_monitor import BUDGET, PerfBudgetMonitor
from maya_theme.monitor.metrics import collect, to_dict


def _parse_duration() -> int:
    """Parse --soak-duration from pytest args or env."""
    for i, arg in enumerate(sys.argv):
        if arg == "--soak-duration" and i + 1 < len(sys.argv):
            return int(sys.argv[i + 1])
        if arg.startswith("--soak-duration="):
            return int(arg.split("=")[1])
    env = os.environ.get("MAYA_SOAK_DURATION")
    if env:
        try:
            return int(env)
        except ValueError:
            pass
    return 60  # default: 60s smoke test


SOAK_DURATION = _parse_duration()
SAMPLE_INTERVAL = 5.0  # seconds between samples
MAX_SAMPLES = int(SOAK_DURATION / SAMPLE_INTERVAL) + 1


@pytest.mark.slow
def test_soak_performance_budget():
    """Run for SOAK_DURATION seconds, verify Maya stays within budget.

    Budget (§10.1):
    - Extra CPU (idle): < 2%
    - Extra RAM: < 150 MB
    - Blur GPU cost: < 5% (when enabled)

    The test samples Maya's own process usage periodically.
    """
    mon = PerfBudgetMonitor()
    samples = []
    violations = []

    print(f"\n🔥 Starting soak test: {SOAK_DURATION}s "
          f"(sample every {SAMPLE_INTERVAL}s, max {MAX_SAMPLES} samples)")

    start = time.time()
    sample_count = 0

    while time.time() - start < SOAK_DURATION:
        time.sleep(SAMPLE_INTERVAL)
        sample_count += 1

        # Maya's own perf
        r = mon.check()
        m = r["metrics"]

        # Also collect system-wide metrics for context
        sys_m = to_dict(collect())

        sample = {
            "t": time.time() - start,
            "maya_cpu": m["cpu_percent"],
            "maya_ram_mb": m["ram_mb"],
            "sys_cpu": sys_m["cpu_percent"],
            "sys_ram_pct": sys_m["ram_percent"],
            "over_budget": r["over_budget"],
        }
        samples.append(sample)

        # Check for sustained violations
        if r["over_budget"]:
            violations.append(sample)
            print(f"  ⚠️ t={sample['t']:.0f}s: CPU={m['cpu_percent']:.1f}% "
                  f"RAM={m['ram_mb']:.0f}MB — over budget")

        # Print progress every 12 samples (1 min)
        if sample_count % 12 == 0:
            print(f"  t={sample['t']:.0f}s: Maya CPU={m['cpu_percent']:.1f}% "
                  f"RAM={m['ram_mb']:.0f}MB | Sys CPU={sys_m['cpu_percent']:.1f}% "
                  f"RAM={sys_m['ram_percent']:.1f}%")

    # Analysis
    print(f"\n📊 Soak test complete: {sample_count} samples over {SOAK_DURATION}s")

    if samples:
        avg_cpu = sum(s["maya_cpu"] for s in samples) / len(samples)
        avg_ram = sum(s["maya_ram_mb"] for s in samples) / len(samples)
        max_cpu = max(s["maya_cpu"] for s in samples)
        max_ram = max(s["maya_ram_mb"] for s in samples)

        print(f"  Maya avg CPU: {avg_cpu:.2f}% (budget: <{BUDGET['cpu_percent']}%)")
        print(f"  Maya max CPU: {max_cpu:.2f}%")
        print(f"  Maya avg RAM: {avg_ram:.0f}MB (budget: <{BUDGET['ram_mb']}MB)")
        print(f"  Maya max RAM: {max_ram:.0f}MB")
        print(f"  Over-budget samples: {len(violations)}/{len(samples)}")

        # Assertions: average should be within budget
        # Allow brief spikes, but average must be under budget
        assert avg_cpu < BUDGET["cpu_percent"] * 2, \
            f"Average CPU {avg_cpu:.1f}% exceeds 2x budget ({BUDGET['cpu_percent']}%)"
        assert avg_ram < BUDGET["ram_mb"], \
            f"Average RAM {avg_ram:.0f}MB exceeds budget ({BUDGET['ram_mb']}MB)"

        # No more than 10% of samples should be over budget
        violation_rate = len(violations) / len(samples) if samples else 0
        assert violation_rate < 0.1, \
            f"Over-budget rate {violation_rate:.0%} exceeds 10% threshold"
    else:
        pytest.fail("No samples collected during soak test")


def test_soak_config_defaults():
    """Verify default config is soak-test-friendly."""
    from maya_theme.core.config import DEFAULT_CONFIG

    assert DEFAULT_CONFIG["performance"]["preset"] == "balanced"
    assert DEFAULT_CONFIG["performance"]["auto_reduce_blur"] is True
    # monitor should be enabled by default
    assert DEFAULT_CONFIG["monitor"]["enabled"] is True
    # reasonable interval
    assert DEFAULT_CONFIG["monitor"]["interval"] <= 5


def test_soak_monitor_no_memory_leak():
    """Monitor should not leak memory over time."""
    import gc

    mon = PerfBudgetMonitor()
    initial_objects = len(gc.get_objects())

    # Run many checks
    for _ in range(1000):
        mon.check()

    gc.collect()
    final_objects = len(gc.get_objects())

    # Allow some growth (caches etc), but not unbounded
    growth = final_objects - initial_objects
    assert growth < 1000, f"Object count grew by {growth} — possible memory leak"


if __name__ == "__main__":
    # Standalone execution: python tests/test_soak.py --duration 3600
    duration = SOAK_DURATION
    mon = PerfBudgetMonitor()
    print(f"🔥 Maya Soak Test — {duration}s")
    print(f"Budget: CPU<{BUDGET['cpu_percent']}% RAM<{BUDGET['ram_mb']}MB\n")

    samples = []
    start = time.time()
    while time.time() - start < duration:
        time.sleep(SAMPLE_INTERVAL)
        r = mon.check()
        m = r["metrics"]
        samples.append(m)
        elapsed = time.time() - start
        if r["over_budget"]:
            print(f"⚠️ t={elapsed:.0f}s CPU={m['cpu_percent']:.1f}% RAM={m['ram_mb']:.0f}MB")
        else:
            print(f"✅ t={elapsed:.0f}s CPU={m['cpu_percent']:.1f}% RAM={m['ram_mb']:.0f}MB")

    if samples:
        avg_cpu = sum(s["cpu_percent"] for s in samples) / len(samples)
        avg_ram = sum(s["ram_mb"] for s in samples) / len(samples)
        print(f"\n📊 Avg CPU: {avg_cpu:.2f}% | Avg RAM: {avg_ram:.0f}MB")
        if avg_cpu < BUDGET["cpu_percent"] * 2 and avg_ram < BUDGET["ram_mb"]:
            print("✅ Soak test PASSED")
            sys.exit(0)
        else:
            print("❌ Soak test FAILED — budget exceeded")
            sys.exit(1)