#!/usr/bin/env bash
# Maya Extension — user-level install script (no root)
set -euo pipefail

PREFIX="${HOME}/.local"
SHARE="${PREFIX}/share/maya-theme"
BIN="${PREFIX}/bin"

echo "✦ Maya Extension installer"

# pre-check
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found"; exit 1
fi
if ! command -v kwriteconfig6 >/dev/null 2>&1; then
  echo "kwriteconfig6 not found — install Plasma 6 tools"; exit 1
fi

# install python package
python3 -m pip install --user --upgrade . 2>/dev/null || python3 -m pip install --user .

# copy theme assets
mkdir -p "${SHARE}"
cp -r theme/* "${SHARE}/" 2>/dev/null || true

# install color schemes
if [ -d "${SHARE}/colors" ]; then
  mkdir -p "${PREFIX}/share/color-schemes"
  cp "${SHARE}/colors/"*.colors "${PREFIX}/share/color-schemes/" 2>/dev/null || true
fi

# desktop entry
mkdir -p "${PREFIX}/share/applications"
cat > "${PREFIX}/share/applications/maya-settings.desktop" <<EOF
[Desktop Entry]
Name=Maya Settings
Comment=Maya Extension theme settings
Exec=maya-theme settings
Icon=preferences-desktop-theme
Type=Application
Categories=Settings;DesktopSettings;
EOF

# initial backup
maya-theme backup || true

echo "Installed. Run 'maya-theme install' to apply."