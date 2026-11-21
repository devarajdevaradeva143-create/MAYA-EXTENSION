"""System metrics collection for Maya monitor widget."""

from __future__ import annotations

import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None


@dataclass
class Metrics:
    cpu_percent: float = 0.0
    ram_percent: float = 0.0
    ram_used_mb: float = 0.0
    gpu_percent: float | None = None
    gpu_temp: float | None = None
    npu_percent: float | None = None
    battery_percent: float | None = None
    battery_charging: bool | None = None
    disk_percent: float = 0.0
    net_up_kbps: float = 0.0
    net_down_kbps: float = 0.0
    cpu_temp: float | None = None


_prev_net = {"sent": 0, "recv": 0, "t": 0.0}


def _gpu_info() -> tuple[float | None, float | None]:
    # try nvidia-smi
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,temperature.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3,
        )
        if r.returncode == 0 and r.stdout.strip():
            parts = r.stdout.strip().split(",")
            return float(parts[0]), float(parts[1])
    except Exception:
        pass
    # AMD iGPU via sysfs
    try:
        for card in Path("/sys/class/drm").glob("card*"):
            busy = card / "device" / "gpu_busy_percent"
            if busy.exists():
                pct = float(busy.read_text().strip())
                # temperature from hwmon
                temp = None
                for hw in (card / "device" / "hwmon").glob("hwmon*") if (card / "device" / "hwmon").exists() else []:
                    tf = hw / "temp1_input"
                    if tf.exists():
                        temp = int(tf.read_text().strip()) / 1000.0
                return pct, temp
    except Exception:
        pass
    return None, None


def _cpu_temp() -> float | None:
    try:
        temps = psutil.sensors_temperatures() if psutil else {}
    except Exception:
        temps = {}
    for name, entries in temps.items():
        for e in entries:
            if e.current and e.current > 0:
                return float(e.current)
    # fallback: thermal zone
    try:
        p = Path("/sys/class/thermal/thermal_zone0/temp")
        if p.exists():
            return int(p.read_text()) / 1000.0
    except Exception:
        pass
    return None


def collect() -> Metrics:
    m = Metrics()
    if psutil is None:
        return m
    m.cpu_percent = psutil.cpu_percent(interval=None)
    vm = psutil.virtual_memory()
    m.ram_percent = vm.percent
    m.ram_used_mb = vm.used / (1024 * 1024)
    du = psutil.disk_usage("/")
    m.disk_percent = du.percent

    # network deltas
    import time

    io = psutil.net_io_counters()
    now = time.time()
    dt = now - _prev_net["t"] if _prev_net["t"] else 1.0
    if dt <= 0:
        dt = 1.0
    if _prev_net["t"]:
        up = (io.bytes_sent - _prev_net["sent"]) / 1024.0 / dt
        down = (io.bytes_recv - _prev_net["recv"]) / 1024.0 / dt
        m.net_up_kbps = max(0.0, up)
        m.net_down_kbps = max(0.0, down)
    _prev_net["sent"] = io.bytes_sent
    _prev_net["recv"] = io.bytes_recv
    _prev_net["t"] = now

    # battery
    try:
        bat = psutil.sensors_battery()
        if bat is not None:
            m.battery_percent = bat.percent
            m.battery_charging = bat.power_plugged
    except Exception:
        pass

    g, gt = _gpu_info()
    m.gpu_percent = g
    m.gpu_temp = gt
    m.cpu_temp = _cpu_temp()
    return m


def to_dict(m: Metrics) -> dict[str, Any]:
    return asdict(m)