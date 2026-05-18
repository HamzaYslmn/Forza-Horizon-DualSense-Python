#!/usr/bin/env bash
# FH DualSense — Linux/macOS launcher. Downloads the latest release into ./app and runs it.
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="HamzaYslmn/Forza-Horizon-DualSense-Python"
RELEASES="https://github.com/$REPO/releases/latest"
APP="$ROOT/app"
PYPROJECT="$APP/src/pyproject.toml"

trap 'c=$?; echo; echo "App exited with code $c."; [ $# -eq 0 ] && read -r -p "Press Enter to close this window..." _ || true; exit $c' EXIT

need() { command -v "$1" >/dev/null 2>&1; }
fetch() { if need curl; then curl -fsSL "$1"; elif need wget; then wget -qO- "$1"; fi; }

# --- Resolve latest release tag (fall back to 'main' branch) ---
LATEST=$(fetch "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null \
    | grep -E '"tag_name"' | head -n1 | sed -E 's/.*"tag_name":\s*"([^"]+)".*/\1/')
SOURCE="tags"
if [ -z "$LATEST" ]; then
    echo "No release found. Using 'main' branch."
    LATEST="main"
    SOURCE="heads"
fi

# --- Read currently-installed version from pyproject.toml ---
CURRENT=""
if [ -f "$PYPROJECT" ]; then
    v=$(grep -E '^version\s*=' "$PYPROJECT" | head -n1 | sed -E 's/version\s*=\s*"([^"]+)".*/\1/')
    [ -n "$v" ] && CURRENT="v$v"
fi

install_release() {
    local tag="$1" kind="$2"
    local zip="$ROOT/fhds.zip" extract="$ROOT/_extract"
    echo "Downloading $tag..."
    if ! fetch "https://github.com/$REPO/archive/refs/$kind/$tag.zip" > "$zip"; then
        echo
        echo "Download failed. Download the latest release manually from:"
        echo "   $RELEASES"
        echo "and extract its contents into the 'app' folder next to this script."
        echo
        rm -f "$zip"
        return 1
    fi
    rm -rf "$extract"; mkdir -p "$extract"
    if need unzip; then unzip -q "$zip" -d "$extract"
    else python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$zip" "$extract"
    fi
    rm -rf "$APP"
    mv "$extract"/*/ "$APP"
    rm -rf "$extract" "$zip"
    echo "Installed $tag."
}

try_install() { install_release "$1" "$2" || [ -f "$APP/src/main.py" ] || exit 1; }

if [ "$SOURCE" = "heads" ]; then
    echo "Refreshing 'main' branch (installed: $CURRENT)..."
    try_install "$LATEST" "$SOURCE"
elif [ -z "$CURRENT" ]; then
    echo "Installing $LATEST..."
    try_install "$LATEST" "$SOURCE"
elif [ "$CURRENT" = "$LATEST" ]; then
    echo "Up to date ($CURRENT)."
else
    echo "Update available: $CURRENT -> $LATEST"
    echo "If the automatic update doesn't work, download manually start script from:"
    echo "   $RELEASES"
    read -r -p "Update now? [Y/n] " ans
    case "${ans:-Y}" in
        [Nn]*) ;;
        *) try_install "$LATEST" "$SOURCE" ;;
    esac
fi

if ! need uv; then
    echo "uv was not found. Installing from https://astral.sh/uv/ ..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    need uv || { echo "uv installed but not on PATH. Restart your shell or add ~/.local/bin to PATH."; exit 1; }
fi

# Linux: install the DualSense udev rule if missing (else hidapi reports "open failed").
RULE_DST="/etc/udev/rules.d/70-dualsense.rules"
if [ "$(uname -s)" = "Linux" ] && [ ! -f "$RULE_DST" ] && [ -f "$APP/packaging/linux/70-dualsense.rules" ]; then
    read -r -p "Install DualSense udev rule (sudo)? [Y/n] " ans
    case "${ans:-Y}" in [Nn]*) ;; *)
        sudo cp "$APP/packaging/linux/70-dualsense.rules" "$RULE_DST" \
            && sudo udevadm control --reload-rules && sudo udevadm trigger \
            && echo "Installed. Unplug/replug (USB) or re-pair (Bluetooth)." ;;
    esac
fi

cd "$APP/src"
if [ "$#" -gt 0 ]; then
    echo "Launching game: $*"
    "$@" &
fi
uv run main.py
