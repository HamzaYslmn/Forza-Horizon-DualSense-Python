"""Logs tab: level cycler, pause toggle, clear, scrolling log view."""
import logging
import tkinter as tk

import customtkinter as ctk

from lang import t

from . import theme as T
from . import widgets as W

log = logging.getLogger("fhds")

LOG_LEVELS = ("WARNING", "INFO", "DEBUG")
DEFAULT_LOG_LEVEL = "INFO"
MAX_LINES = 2000

# fg_color, hover_color, text_color per level
LEVEL_STYLES = {
    "DEBUG":   (T.BG_HOVER,  T.BG_ACTIVE,    T.TEXT_FAINT),
    "INFO":    (T.ACCENT,    T.ACCENT_HOVER,  "white"),
    "WARNING": (T.YELLOW,    "#b45309",       "white"),
}


class LogsTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._level_idx = LOG_LEVELS.index(DEFAULT_LOG_LEVEL)
        self._paused = False
        self._line_count = 0
        self._build()

    def _build(self):
        W.PageHeader(self, t("Logs"),
                     t("Live application output. Increase verbosity for debugging.")
                     ).pack(fill="x", pady=(0, T.PAD_MD))

        # Toolbar card
        toolbar = W.Card(self)
        toolbar.pack(fill="x", pady=(0, T.PAD_SM))
        tb = ctk.CTkFrame(toolbar, fg_color="transparent")
        tb.pack(fill="x", padx=T.PAD_MD, pady=T.PAD_SM)

        ctk.CTkLabel(tb, text=t("Level"),
                     text_color=T.TEXT_MUTED,
                     font=ctk.CTkFont(size=T.FS_SMALL)
                     ).pack(side="left", padx=(0, T.PAD_SM))
        self.btn_level = W.SecondaryButton(tb, self.level_name.lower(),
                                           command=self.cycle_level, width=90)
        self.btn_level.pack(side="left", padx=(0, T.PAD_SM))
        self._apply_level_style()
        self.btn_pause = W.SecondaryButton(tb, f"{T.ICON['pause']}  {t('pause')}",
                                           command=self.toggle_pause, width=110)
        self.btn_pause.pack(side="left", padx=(0, T.PAD_SM))
        W.SecondaryButton(tb, f"{T.ICON['clear']}  {t('clear')}",
                          command=self.clear, width=110
                          ).pack(side="left")

        # Log surface card
        surface = W.Card(self)
        surface.pack(fill="both", expand=True)
        holder = ctk.CTkFrame(surface, fg_color=T.BG_INPUT, corner_radius=6)
        holder.pack(fill="both", expand=True, padx=T.PAD_MD, pady=T.PAD_MD)
        self.text = tk.Text(
            holder, bg="#1e1f22", fg="#d4d4d4",
            insertbackground="#d4d4d4", borderwidth=0, highlightthickness=0,
            wrap="none", font=("Consolas", self.app.font_size(10)),
            state="disabled",
        )
        self.text.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)
        self.text.tag_configure("DEBUG", foreground=T.TEXT_FAINT)
        self.text.tag_configure("INFO", foreground="#d4d4d4")
        self.text.tag_configure("WARNING", foreground=T.YELLOW)
        self.text.tag_configure("ERROR", foreground=T.RED)
        self.text.tag_configure("CRITICAL", foreground="#ffffff", background=T.RED)
        scroll = tk.Scrollbar(holder, command=self.text.yview,
                              bg="#2b2d31", troughcolor="#1e1f22",
                              activebackground=T.ACCENT, borderwidth=0,
                              highlightthickness=0)
        scroll.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self.text.configure(yscrollcommand=scroll.set)

    @property
    def level_name(self) -> str:
        return LOG_LEVELS[self._level_idx]

    @property
    def level(self) -> int:
        return getattr(logging, self.level_name)

    def write(self, level: str, msg: str) -> None:
        self.text.configure(state="normal")
        tag = level if level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL") else "INFO"
        self.text.insert("end", msg + "\n", tag)
        self._line_count += 1
        if self._line_count > MAX_LINES:
            drop = self._line_count - (MAX_LINES - 200)
            self.text.delete("1.0", f"{drop + 1}.0")
            self._line_count = MAX_LINES - 200
        if not self._paused:
            self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self._line_count = 0
        self.text.configure(state="disabled")

    def toggle_pause(self) -> None:
        self._paused = not self._paused
        if self._paused:
            self.btn_pause.configure(text=f"{T.ICON['play']}  {t('resume')}",
                                     fg_color=T.ACCENT,
                                     hover_color=T.ACCENT_HOVER,
                                     text_color="white")
        else:
            self.btn_pause.configure(text=f"{T.ICON['pause']}  {t('pause')}",
                                     fg_color=T.BG_HOVER,
                                     hover_color=T.BG_ACTIVE,
                                     text_color=T.TEXT)

    def cycle_level(self) -> None:
        self._level_idx = (self._level_idx + 1) % len(LOG_LEVELS)
        logging.getLogger().setLevel(self.level)
        self.btn_level.configure(text=self.level_name.lower())
        self._apply_level_style()

    def _apply_level_style(self) -> None:
        fg, hover, txt = LEVEL_STYLES[self.level_name]
        self.btn_level.configure(fg_color=fg, hover_color=hover, text_color=txt)
        log.info("Log level: %s", self.level_name)
