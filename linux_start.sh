#!/usr/bin/env bash
# FH DualSense - Linux/macOS launcher (zuv).
# Bundle lives in app/. Auto-downloads from GitHub Releases if missing.
# Set PRERELEASE=true to track rolling test builds (v999.0.0 tag).
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

# Args starting with -- forward to bundle; rest = Steam wrapper game cmd.
GAME=()
for a in "$@"; do
    case "$a" in
        --*) FLAGS+=("$a") ;;
        *) GAME+=("$a") ;;
    esac
done

trap 'c=$?; echo; echo "[fhds exited with code $c]"; [ ${#GAME[@]} -eq 0 ] && read -r -p "Press Enter to close..." _ || true; exit $c' EXIT

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
    command -v uv >/dev/null 2>&1 || { echo "uv not on PATH - restart shell."; exit 1; }
fi

# Linux only: install DualSense udev rule once (needs sudo). Pulled from repo
# because /etc/udev is system-wide and can't live in the bundle.
RULE_DST="/etc/udev/rules.d/70-dualsense.rules"
RULE_URL="https://raw.githubusercontent.com/$REPO/main/packaging/linux/70-dualsense.rules"
if [ "$(uname -s)" = "Linux" ] && [ ! -f "$RULE_DST" ]; then
    read -r -p "Install DualSense udev rule (sudo)? [Y/n] " ans
    case "${ans:-Y}" in [Nn]*) ;; *)
        TMP="$(mktemp)" && curl -LsSf "$RULE_URL" -o "$TMP" \
            && sudo install -m 0644 "$TMP" "$RULE_DST" \
            && sudo udevadm control --reload-rules && sudo udevadm trigger \
            && rm -f "$TMP" \
            && echo "Installed udev rule. Re-plug controller." ;;
    esac
fi

[ ${#GAME[@]} -gt 0 ] && "${GAME[@]}" &

# Don't let host Python env leak into the bundled venv.
unset PYTHONHOME PYTHONPATH
export PYTHONNOUSERSITE=1

exec uv run "$BUNDLE" "${FLAGS[@]}"
