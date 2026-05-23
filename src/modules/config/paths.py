"""Single source of truth for filesystem paths.

All modules read paths from here, never recompute them. The same constants
work across three execution modes:

    dev          : `python main.py` from src/         ROOT = src/
    zuv bundle   : extracted at runtime               ROOT = extracted folder
    PyInstaller  : one-file frozen EXE                ROOT = MEIPASS (auto-wiped)

Writable user data (DATA) lives next to the EXE when frozen so settings
persist across launches; in dev/zuv it sits under ROOT.
"""
import sys
from pathlib import Path

# ROOT: package root containing main.py + bundled assets (icons, lang, pyproject).
ROOT = Path(__file__).resolve().parent.parent.parent

# DATA: writable user data dir (user_preferences.json, crash.log, ...).
# Frozen EXE -> next to executable (MEIPASS would be wiped on exit).
# Dev / zuv  -> data/ under ROOT.
if getattr(sys, "frozen", False):
    DATA = Path(sys.executable).resolve().parent / "data"
else:
    DATA = ROOT / "data"

# Read-only bundled assets.
PYPROJECT = ROOT / "pyproject.toml"
LANG = ROOT / "lang"
ICON_ICO = ROOT / "data" / "icon.ico"
ICON_PNG = ROOT / "data" / "icon.png"
