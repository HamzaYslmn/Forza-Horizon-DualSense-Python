"""HidHide integration (Windows only).

Detects whether HidHide is installed and manages the application whitelist:
- register_app()   — add this process to the HidHide whitelist on startup
- unregister_app() — remove it on exit

The whitelist lets us read cloaked DualSense devices even when Steam Input or
another tool has hidden them. Cloaking state itself is never touched; we only
manage whether *our* process can see through it.

Latch mode: when HidHide is detected the I/O loop holds the HID handle silently
after the first connect, avoiding churn from mid-session cloak toggles.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

log = logging.getLogger("fhds.hidhide")


# ---------------------------------------------------------------------------
# CLI discovery
# ---------------------------------------------------------------------------

def _cli_path() -> Path | None:
    """Return the path to HidHideCLI.exe, or None if not found."""
    if sys.platform != "win32":
        return None
    env = os.environ.get("HIDHIDE_CLI")
    if env:
        p = Path(env)
        if p.is_file():
            return p
    which = shutil.which("HidHideCLI.exe")
    if which:
        return Path(which)
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    default = (Path(pf) / "Nefarius Software Solutions" / "HidHide"
               / "x64" / "HidHideCLI.exe")
    return default if default.is_file() else None


def _run(*args) -> tuple[bool, str]:
    """Run HidHideCLI with *args. Returns (success, combined output)."""
    cli = _cli_path()
    if cli is None:
        return False, "HidHideCLI.exe not found"
    try:
        r = subprocess.run(
            [str(cli), *args],
            capture_output=True, text=True, timeout=5,
        )
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Detection (cached)
# ---------------------------------------------------------------------------

_detected: bool | None = None


def _detect() -> bool:
    return _cli_path() is not None


def is_detected() -> bool:
    global _detected
    if _detected is None:
        _detected = _detect()
    return _detected


# ---------------------------------------------------------------------------
# Whitelist management
# ---------------------------------------------------------------------------

def _norm(exe_path: str | Path) -> str:
    return str(Path(exe_path).resolve())


def is_registered(exe_path: str | Path) -> bool:
    """Return True if exe_path is already in the HidHide whitelist."""
    ok, out = _run("--app-list")
    if not ok:
        return False
    needle = _norm(exe_path).lower()
    return any(needle == line.strip().lower() for line in out.splitlines())


def register_app(exe_path: str | Path) -> bool:
    """Add exe_path to the HidHide application whitelist.

    Safe to call when already registered — HidHide ignores duplicates.
    Returns True on success."""
    path = _norm(exe_path)
    if not is_detected():
        return False
    ok, out = _run("--app-reg", path)
    if ok:
        log.info("HidHide: whitelisted %s", path)
    else:
        log.warning("HidHide: --app-reg failed: %s", out)
    return ok


def unregister_app(exe_path: str | Path) -> bool:
    """Remove exe_path from the HidHide application whitelist.

    Returns True on success."""
    path = _norm(exe_path)
    if not is_detected():
        return False
    ok, out = _run("--app-unreg", path)
    if ok:
        log.info("HidHide: removed %s from whitelist", path)
    else:
        log.warning("HidHide: --app-unreg failed: %s", out)
    return ok
