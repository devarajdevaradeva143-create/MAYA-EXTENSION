#!/usr/bin/env bash
# Best-effort GNOME support (Phase 6)
set -euo pipefail

# Apply glass-ish GTK theme via gsettings (GNOME)
if command -v gsettings >/dev/null 2>&1; then
  gsettings set org.gnome.desktop.interface gtk-theme "MayaGlass" 2>/dev/null || true
  gsettings set org.gnome.desktop.interface color-scheme "prefer-dark" 2>/dev/null || true
  echo "GNOME settings applied (best-effort)."
else
  echo "gsettings not found — skipping."
fi