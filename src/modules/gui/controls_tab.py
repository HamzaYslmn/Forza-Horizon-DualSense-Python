"""Controls tab: per-trigger effect on/off switches."""
import logging

import customtkinter as ctk

from lang import t
from modules.config import preferences

from . import theme as T
from . import widgets as W

log = logging.getLogger("fhds")

TRIGGER_CONTROLS = [
    ("L2 - Brake", [
        ("enable_gear_shift_brake",  "Shift thump"),
        ("enable_abs",               "ABS rumble"),
        ("enable_brake_static_wall", "Static brake wall"),
        ("enable_brake_resistance",  "Brake stiffness"),
        ("enable_handbrake_bonus",   "Handbrake stiffness bonus"),
    ]),
    ("R2 - Throttle", [
        ("enable_gear_shift",          "Shift thump"),
        ("enable_rev_limiter",         "Redline buzz"),
        ("enable_wheelspin_buzz",      "Wheelspin buzz"),
        ("enable_idle_buzz",           "Idle buzz"),
        ("enable_throttle_resistance", "Throttle stiffness"),
    ]),
    ("LED Lighting", [
        ("enable_lighting",     "LED Lighting"),
        ("enable_lightbar",     "LightBar"),
        ("enable_player_led",   "Player LED"),
        ("enable_mic_led",      "ABS Light"),
    ]),
]


class ControlsTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.settings = app.settings
        self._switches: dict[str, ctk.CTkSwitch] = {}
        self._build()
        app.register_refresh(self._refresh_widgets)

    def _build(self):
        W.PageHeader(self, t("Controls"),
                     t("Toggle individual trigger effects. Changes save instantly.")
                     ).pack(fill="x", pady=(0, T.PAD_MD))

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=1, uniform="cols")
        grid.grid_columnconfigure(1, weight=1, uniform="cols")
        grid.grid_columnconfigure(2, weight=1, uniform="cols")
        grid.grid_rowconfigure(0, weight=1)

        for col, (title, toggles) in enumerate(TRIGGER_CONTROLS):
            card = W.Card(grid)
            card.grid(row=0, column=col,
                      padx=(0 if col == 0 else T.PAD_MD // 2, 0 if col else T.PAD_MD // 2),
                      sticky="nsew")
            W.H2(card, t(title)).pack(anchor="w", padx=T.PAD_MD,
                                      pady=(T.PAD_MD, T.PAD_SM))
            for attr, label in toggles:
                sw = ctk.CTkSwitch(card, text=t(label),
                                   command=lambda a=attr: self._on_toggle(a))
                if getattr(self.settings, attr):
                    sw.select()
                sw.pack(anchor="w", padx=T.PAD_MD, pady=T.PAD_XS)
                self._switches[attr] = sw
            ctk.CTkFrame(card, fg_color="transparent", height=T.PAD_SM
                         ).pack()  # bottom breathing room

    def _on_toggle(self, attr: str):
        if self.app._refreshing:
            return
        sw = self._switches[attr]
        value = bool(sw.get())
        if hasattr(self.settings, attr) and getattr(self.settings, attr) != value:
            setattr(self.settings, attr, value)
            preferences.save(self.settings)
            log.info("%s = %s", attr, value)
        self.app.haptic(value)

    def _refresh_widgets(self):
        for attr, sw in self._switches.items():
            if not hasattr(self.settings, attr):
                continue
            want = bool(getattr(self.settings, attr))
            if bool(sw.get()) != want:
                if want:
                    sw.select()
                else:
                    sw.deselect()