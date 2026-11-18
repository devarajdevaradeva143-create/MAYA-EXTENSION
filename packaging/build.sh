#!/usr/bin/env bash
# Build Maya Extension distribution package
set -euo pipefail
cd "$(dirname "$0")/.."

VERSION=$(python3 -c "import maya_theme; print(maya_theme.__version__)")
OUT="dist/maya-extension-${VERSION}"
mkdir -p dist
rm -rf "$OUT"
mkdir -p "$OUT"

cp -r maya_theme theme plasmoids packaging docs README.md pyproject.toml "$OUT/"
tar -czf "dist/maya-extension-${VERSION}.tar.gz" -C dist "maya-extension-${VERSION}"
echo "Built: dist/maya-extension-${VERSION}.tar.gz"