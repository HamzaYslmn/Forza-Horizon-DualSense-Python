"""HidHide detection (Windows only).

We do NOT call HidHideCLI. We only check whether HidHide is installed so
the I/O loop can latch into persistent mode after the first successful
connect (HidHide can cloak the device mid-session; persistent mode keeps
the handle open and skips reconnect/watchdog churn).
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def _detect() -> bool:
    if sys.platform != "win32":
        return False
    env = os.environ.get("HIDHIDE_CLI")
    if env and Path(env).is_file():
        return True
    if shutil.which("HidHideCLI.exe"):
        return True
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    return (Path(pf) / "Nefarius Software Solutions" / "HidHide" / "x64"
            / "HidHideCLI.exe").is_file()


_detected: bool | None = None


def is_detected() -> bool:
    global _detected
    if _detected is None:
        _detected = _detect()
    return _detected
