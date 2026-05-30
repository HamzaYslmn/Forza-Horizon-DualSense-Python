#!/usr/bin/env bash
# Build a standalone single-file ELF of FH-DualSense.
# Output: packaging/linux/dist/FH-DualSense-vX.Y.Z
# (no install, no traces - MEIPASS auto-cleans on exit)
# Requires: uv  (https://docs.astral.sh/uv/)
set -e

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
DIST="$HERE/dist"
WORK="$HERE/build"

# MARK: read version = "X.Y.Z" from src/pyproject.toml
VER="$(grep -m1 '^version' "$ROOT/src/pyproject.toml" | cut -d'"' -f2)"
if [ -z "$VER" ]; then
    echo "Could not read version from src/pyproject.toml"
    exit 1
fi
echo "Building FH-DualSense v$VER ..."

rm -rf "$WORK" "$DIST"

uvx --from "pyinstaller>=6.11.1" \
    --with customtkinter --with textual \
    --with hidapi --with psutil --with dotenv \
    --with pystray --with pillow \
    pyinstaller "$HERE/fhds.spec" \
    --distpath "$DIST" --workpath "$WORK" \
    --noconfirm --clean

# MARK: rename output to include version
mv -f "$DIST/FH-DualSense" "$DIST/FH-DualSense-v$VER"
chmod +x "$DIST/FH-DualSense-v$VER"

echo
echo "Build OK. Binary: $DIST/FH-DualSense-v$VER"
