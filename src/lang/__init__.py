"""Tiny file-based i18n.

Each language is a sibling module in this package exposing two names:
    NAME    -> the language's display name (str)
    STRINGS -> dict[english_source -> translated string]

English is the *source* language: the lookup key is the English string itself,
so any string a catalog omits falls back to English automatically. To add a
language, drop a `<code>.py` file in this folder (e.g. `de.py`); it is
auto-discovered on startup and appears in the LANG tab. No registry to edit.

Restart-to-apply: the active language is chosen once at startup (from the saved
setting) and the whole UI is composed against it. Changing it persists the
choice; the new language renders on the next launch.
"""
import importlib
import logging
from pathlib import Path

log = logging.getLogger("fhds")

DEFAULT_LANG = "en"

_catalogs: dict[str, dict] = {}   # code -> STRINGS (also the loaded-yet? flag)
_names: dict[str, str] = {}
_active: str = DEFAULT_LANG


def _discover() -> None:
    """Glob `<code>.py` files in this package and load each catalog.
    Works in source, in the zuv-extracted bundle, and in PyInstaller when the
    `lang/` folder is shipped as data (so __file__ resolves next to the .py
    catalogs)."""
    _catalogs.clear()
    _names.clear()
    folder = Path(__file__).resolve().parent
    for f in sorted(folder.glob("*.py")):
        code = f.stem
        if code.startswith("_"):
            continue
        try:
            m = importlib.import_module(f"{__name__}.{code}")
        except Exception as e:  # a broken catalog must not crash the app
            log.warning("Skipping language '%s': %s", code, e)
            continue
        _catalogs[code] = dict(getattr(m, "STRINGS", {}))
        _names[code] = str(getattr(m, "NAME", code))
    # English is the source language; guarantee it exists even if en.py is gone.
    _catalogs.setdefault(DEFAULT_LANG, {})
    _names.setdefault(DEFAULT_LANG, "English")


def _ensure() -> None:
    if not _catalogs:  # _discover always leaves at least English, so this is the loaded flag
        _discover()


def available() -> list[tuple[str, str]]:
    """(code, display_name) pairs. English first, then by display name."""
    _ensure()
    return sorted(_names.items(), key=lambda kv: (kv[0] != DEFAULT_LANG, kv[1].lower()))


def set_language(code: str) -> None:
    """Select the active language, falling back to English for unknown codes."""
    global _active
    _ensure()
    _active = code if code in _catalogs else DEFAULT_LANG


def current() -> str:
    return _active


def t(key: str) -> str:
    """Translate `key` into the active language, or return it unchanged.

    `key` is the English source string; pass it through `str.format(...)` after
    translating when it carries `{placeholders}`."""
    _ensure()
    cat = _catalogs.get(_active)
    return cat.get(key, key) if cat else key
