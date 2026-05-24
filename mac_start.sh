#!/usr/bin/env bash
# FH DualSense - macOS launcher (zuv).
# Bundle lives in app/. Auto-downloads from GitHub Releases if missing.
# Set PRERELEASE=true to track rolling test builds (v999.0.0 tag).
#
# Forza Horizon runs on your Windows PC; this app runs on your Mac and
# receives the UDP telemetry over the network (LAN or Moonlight stream).
#
# Setup:
#   1. Find your Mac's local IP:  System Settings → Wi-Fi → Details
#   2. In Forza on your Windows PC:
#        HUD & Gameplay → Data Out → ON
#        IP address = <your Mac's IP>
#        Port = 5300
#   3. Run this script — it binds to 0.0.0.0 automatically so it accepts
#      packets from any network interface.
#
# Bluetooth DualSense: macOS will ask for Bluetooth permission on first run.
# USB DualSense: plug in — the app detects it automatically.
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

# macOS defaults: GUI mode + listen on all interfaces (Forza runs on a remote PC).
# The user can override either with explicit flags, e.g. --tui or --host 127.0.0.1
_has_gui=false _has_tui=false _has_host=false
for a in "$@"; do
    case "$a" in
        --gui)    _has_gui=true ;;
        --tui)    _has_tui=true ;;
        --host*)  _has_host=true ;;
    esac
done
$_has_gui  || $_has_tui  || FLAGS+=(--gui)
$_has_host               || FLAGS+=(--host 0.0.0.0)

# Args starting with -- forward to bundle; rest = ignored on Mac (no Steam wrapper).
for a in "$@"; do
    case "$a" in
        --*) FLAGS+=("$a") ;;
    esac
done

trap 'c=$?; echo; echo "[fhds exited with code $c]"; read -r -p "Press Enter to close..." _; exit $c' EXIT

if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    command -v uv >/dev/null 2>&1 || { echo "uv not on PATH - restart terminal and try again."; exit 1; }
fi

# Don't let host Python env leak into the bundled venv.
unset PYTHONHOME PYTHONPATH
export PYTHONNOUSERSITE=1
# Use uv's own managed Python (includes Tk); avoids pyenv builds that lack it.
export UV_PYTHON_PREFERENCE=only-managed

# Prefer local source (dev / git clone) over the downloaded bundle.
SRC="$ROOT/src/main.py"
if [ -f "$SRC" ]; then
    export FHDS_DEV=1
    exec uv run --python cpython-3.13 --project "$ROOT/src" "$SRC" "${FLAGS[@]}"
fi

mkdir -p "$APP"

if [ ! -f "$BUNDLE" ]; then
    echo "Downloading fhds.zuv.py..."
    curl -LsSf --fail "$URL" -o "$BUNDLE" || {
        echo "Download failed. Get it manually from https://github.com/$REPO/releases"
        exit 1
    }
fi

exec uv run "$BUNDLE" "${FLAGS[@]}"
