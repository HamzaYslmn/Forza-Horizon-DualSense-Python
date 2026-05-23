#!/usr/bin/env bash
# FH DualSense - macOS launcher (zuv).
# Bundle lives in app/. Auto-downloads from GitHub Releases if missing.
# Set PRERELEASE=true to track rolling test builds (v999.0.0 tag).
#
# NOTE: Forza Horizon runs on Windows — this machine only runs the trigger
# effect app and must receive Forza's UDP telemetry over the network.
# In Forza's HUD & Gameplay -> Data Out settings, set the IP to this Mac's
# local IP and the port to 5300. Then launch with --host 0.0.0.0:
#
#   ./mac_start.sh --host 0.0.0.0
#
# Bluetooth DualSense: macOS will ask for Bluetooth permission on first run.
# USB DualSense: plug in and the app should detect it automatically.
set -e

PRERELEASE=false

ROOT="$(cd "$(dirname "$0")" && pwd)"
APP="$ROOT/app"
BUNDLE="$APP/fhds.zuv.py"
REPO="HamzaYslmn/Forza-Horizon-DualSense-Python"

if [ "$PRERELEASE" = "true" ]; then
    URL="https://github.com/$REPO/releases/download/v999.0.0/fhds.zuv.py"
    FLAGS=(--prerelease)
else
    URL="https://github.com/$REPO/releases/latest/download/fhds.zuv.py"
    FLAGS=()
fi

# Args starting with -- forward to bundle; rest = ignored on Mac (no Steam wrapper).
for a in "$@"; do
    case "$a" in
        --*) FLAGS+=("$a") ;;
    esac
done

trap 'c=$?; echo; echo "[fhds exited with code $c]"; read -r -p "Press Enter to close..." _; exit $c' EXIT

mkdir -p "$APP"

if [ ! -f "$BUNDLE" ]; then
    echo "Downloading fhds.zuv.py..."
    curl -LsSf --fail "$URL" -o "$BUNDLE" || {
        echo "Download failed. Get it manually from https://github.com/$REPO/releases"
        exit 1
    }
fi

if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    command -v uv >/dev/null 2>&1 || { echo "uv not on PATH - restart terminal and try again."; exit 1; }
fi

# Don't let host Python env leak into the bundled venv.
unset PYTHONHOME PYTHONPATH
export PYTHONNOUSERSITE=1

exec uv run "$BUNDLE" "${FLAGS[@]}"
