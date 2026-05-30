"""System-tray helper: hide GUI to tray, restore on click, quit from menu.

Uses pystray + Pillow. The tray thread is daemon, lives for the app lifetime.
All Tk interactions are marshalled back to the main thread via root.after.
"""
from __future__ import annotations

import os
import sys
import threading
from typing import Callable, Optional

import tkinter as tk

from modules.config import paths

# On Wayland, XEmbed trays don't show; force the appindicator backend.
if (
    sys.platform == "linux"
    and not os.environ.get("PYSTRAY_BACKEND")
    and (os.environ.get("WAYLAND_DISPLAY") or os.environ.get("XDG_SESSION_TYPE") == "wayland")
):
    os.environ["PYSTRAY_BACKEND"] = "appindicator"


class TrayController:
    def __init__(self, root: tk.Tk, on_show: Callable[[], None], on_quit: Callable[[], None]):
        self._root = root
        self._on_show = on_show
        self._on_quit = on_quit
        self._icon = None
        self._thread: Optional[threading.Thread] = None
        self._started = False

    def start(self) -> bool:
        """Start the tray icon. Returns True if running, False if unavailable."""
        if self._started:
            return True
        try:
            import pystray
            from PIL import Image
        except Exception:
            return False
        png = paths.ICON_PNG
        try:
            image = Image.open(str(png))
        except Exception:
            image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

        def _show(_icon=None, _item=None):
            self._root.after(0, self._on_show)

        def _quit(_icon=None, _item=None):
            try:
                if self._icon is not None:
                    self._icon.stop()
            except Exception:
                pass
            self._root.after(0, self._on_quit)

        menu = pystray.Menu(
            pystray.MenuItem("Show", _show, default=True),
            pystray.MenuItem("Quit", _quit),
        )
        self._icon = pystray.Icon("fhds", image, "FH DualSense", menu)
        self._thread = threading.Thread(target=self._icon.run, name="fhds-tray", daemon=True)
        self._thread.start()
        self._started = True
        return True

    def stop(self) -> None:
        if self._icon is not None:
            try:
                self._icon.stop()
            except Exception:
                pass
        self._icon = None
        self._started = False
