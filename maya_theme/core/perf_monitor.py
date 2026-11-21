"""AI performance budget monitor — suggests 'Balanced' mode when budget exceeded 30s.

Implements §10.3 of the plan:
- Built-in perf counter in settings page (own CPU/RAM usage)
- If budget exceeded for 30s → auto-suggest 'Balanced mode'
- Logs: no personal data, only metrics
"""

from __future__ import annotations

import os
import time
from typing import Any

from .config import load_config, save_config

# Performance budget (§10.1)
BUDGET = {
    "cpu_percent": 2.0,       # extra CPU idle
    "ram_mb": 150.0,          # extra RAM
    "gpu_percent": 5.0,       # blur GPU cost
    "fps": 60,                # frame rate
}

# Thresholds for triggering suggestion
SUSTAINED_SECONDS = 30.0     # budget exceeded for 30s → suggest
MEMORY_HIGH_MB = 120.0      # own RAM high → warn


class PerfBudgetMonitor:
    """Tracks Maya's own resource usage and suggests balanced mode if over budget."""

    def __init__(self):
        self._start_time = time.time()
        self._start_cpu = self._cpu_time()
        self._start_mem = self._mem_mb()
        self._over_budget_since: float | None = None
        self._last_suggestion: float | None = None

    def _cpu_time(self) -> float:
        try:
            import psutil
            return psutil.Process(os.getpid()).cpu_times().user
        except Exception:
            return 0.0

    def _mem_mb(self) -> float:
        try:
            import psutil
            return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        except Exception:
            return 0.0

    def _cpu_percent(self) -> float:
        """Maya's own CPU% since last call."""
        now = time.time()
        elapsed = now - self._start_time
        if elapsed <= 0:
            return 0.0
        cpu_now = self._cpu_time()
        cpu_delta = cpu_now - self._start_cpu
        pct = (cpu_delta / elapsed) * 100.0
        self._start_time = now
        self._start_cpu = cpu_now
        return min(100.0, pct)

    def check(self) -> dict[str, Any]:
        """Check budget and return suggestion if needed.

        Returns dict with: over_budget, suggest_balanced, metrics, message.
        """
        cpu = self._cpu_percent()
        mem = self._mem_mb()
        now = time.time()

        over = False
        reasons = []
        if cpu > BUDGET["cpu_percent"]:
            over = True
            reasons.append(f"CPU {cpu:.1f}% > {BUDGET['cpu_percent']}%")
        if mem > BUDGET["ram_mb"]:
            over = True
            reasons.append(f"RAM {mem:.0f}MB > {BUDGET['ram_mb']}MB")

        if over:
            if self._over_budget_since is None:
                self._over_budget_since = now
        else:
            self._over_budget_since = None

        suggest = False
        message = ""
        if self._over_budget_since is not None:
            duration = now - self._over_budget_since
            if duration >= SUSTAINED_SECONDS:
                # don't spam suggestions — only every 5 minutes
                if self._last_suggestion is None or (now - self._last_suggestion) > 300:
                    suggest = True
                    self._last_suggestion = now
                    current_preset = load_config().get("performance", {}).get("preset", "balanced")
                    if current_preset == "quality":
                        message = (
                            f"Maya perf budget exceeded for {duration:.0f}s "
                            f"({', '.join(reasons)}). Switch to 'balanced' preset."
                        )
                    else:
                        message = (
                            f"Maya perf budget exceeded for {duration:.0f}s "
                            f"({', '.join(reasons)}). Consider 'balanced' preset."
                        )

        return {
            "over_budget": over,
            "suggest_balanced": suggest,
            "duration_over": (now - self._over_budget_since) if self._over_budget_since else 0,
            "metrics": {"cpu_percent": cpu, "ram_mb": mem},
            "budget": BUDGET,
            "message": message,
        }

    def auto_apply_balanced(self) -> dict[str, Any]:
        """If user has auto_reduce_blur and is in quality mode, switch to balanced."""
        cfg = load_config()
        if cfg.get("performance", {}).get("auto_reduce_blur", True) and \
           cfg.get("performance", {}).get("preset") == "quality":
            cfg.setdefault("performance", {})["preset"] = "balanced"
            # also reduce blur if high
            glass = cfg.get("glass", {})
            if glass.get("blur", 28) > 16:
                glass["blur"] = 16
                cfg["glass"] = glass
            save_config(cfg)
            return {"success": True, "switched_to": "balanced", "blur_reduced": glass.get("blur", 28)}
        return {"success": False, "reason": "not in quality mode or auto-reduce disabled"}

    def format_usage(self) -> str:
        """Format own usage for display in settings."""
        cpu = self._cpu_percent()
        mem = self._mem_mb()
        return f"Maya: CPU {cpu:.1f}% · RAM {mem:.0f}MB / {BUDGET['ram_mb']:.0f}MB budget"


def get_monitor() -> PerfBudgetMonitor:
    """Singleton accessor for the settings controller."""
    global _monitor
    if _monitor is None:
        _monitor = PerfBudgetMonitor()
    return _monitor

_monitor: PerfBudgetMonitor | None = None