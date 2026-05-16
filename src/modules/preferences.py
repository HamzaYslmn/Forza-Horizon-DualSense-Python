"""Persist Settings to a JSON file next to main.py.

Saves simple-typed fields (bool/int/float/str). On version change the file
is wiped so users start each update with fresh defaults — the launcher
already asks before pulling a new version, so accepting the update is the
opt-in for the reset. Manual reset is also available via the TUI button.
"""
import json
import logging
import re
from pathlib import Path

log = logging.getLogger("fhds")

PATH = Path(__file__).resolve().parent.parent / "user_preferences.json"
PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"

_SIMPLE = (bool, int, float, str)


def _version() -> str:
    try:
        m = re.search(r'(?m)^\s*version\s*=\s*"([^"]+)"', PYPROJECT.read_text(encoding="utf-8"))
        return m.group(1) if m else ""
    except OSError:
        return ""


def _fields(s) -> dict:
    return {k: v for k, v in vars(s).items() if isinstance(v, _SIMPLE)}


def load(s) -> None:
    if not PATH.exists():
        return
    try:
        data = json.loads(PATH.read_text(encoding="utf-8"))
    except Exception as e:
        log.warning("Could not load preferences: %s", e)
        return
    if data.get("version") != _version():
        log.info("Resetting preferences: version changed (%s -> %s).",
                 data.get("version") or "unknown", _version() or "unknown")
        PATH.unlink(missing_ok=True)
        return
    for k, current in _fields(s).items():
        if k in data:
            try:
                setattr(s, k, type(current)(data[k]))
            except (TypeError, ValueError):
                pass


def save(s) -> None:
    data = _fields(s) | {"version": _version()}
    try:
        PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as e:
        log.warning("Could not save preferences: %s", e)


def reset(s) -> None:
    """Restore every persisted field on `s` to its class default and wipe the
    preferences file. Mutates `s` in place so the running loop picks up the
    new values on its next frame — no restart needed."""
    PATH.unlink(missing_ok=True)
    defaults = type(s)()
    for k in _fields(s):
        if hasattr(defaults, k):
            setattr(s, k, getattr(defaults, k))
