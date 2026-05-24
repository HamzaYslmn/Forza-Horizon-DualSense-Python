"""Settings tab: switches, sliders, entries with live save.

Each top-level section becomes a Card. Inside, rows use FieldRow for
label-control alignment.
"""
import logging

import customtkinter as ctk

from lang import t
from modules.config import preferences

from . import theme as T
from . import widgets as W

log = logging.getLogger("fhds")

# Mirrors src/modules/tui/settings_tab.py exactly.
SETTING_SECTIONS = [
    ("Pedal dead zones", [
        ("accel_deadzone", "Gas trigger dead zone", 0, 255, ""),
        ("brake_deadzone", "Brake trigger dead zone", 0, 255, ""),
    ]),
    ("Left trigger - Brake force", [
        ("brake_baseline_force", "Resting stiffness", 0, 255, ""),
        ("brake_max_force", "Hard-press stiffness", 0, 255, ""),
        ("brake_curve", "Stiffness curve shape", 0.1, 20.0, ""),
        ("handbrake_bonus", "Handbrake extra stiffness", 0, 255, ""),
    ]),
    ("Left trigger - Static wall (optional)", [
        ("brake_static_wall_at", "Wall position on the trigger", 0, 255, ""),
        ("brake_static_wall_force", "Wall hardness", 0, 255, ""),
    ]),
    ("Surface brake resistance", [
        ("enable_surface_brake", "Surface brake resistance", None, None,
         "Softer brake on loose surfaces, firmer on tarmac."),
        ("surface_brake_tarmac", "Tarmac multiplier", 0.0, 2.0,
         "1.0 = unchanged. Scales final resistance force."),
        ("surface_brake_dirt", "Dirt multiplier", 0.0, 2.0,
         "Lower = softer brake on dirt. Default 0.5."),
        ("surface_brake_gravel", "Gravel multiplier", 0.0, 2.0,
         "Lower = softer brake on gravel/water. Default 0.25."),
    ]),
    ("Right trigger - Gas force", [
        ("throttle_baseline_force", "Resting stiffness", 0, 255, ""),
        ("throttle_max_force", "Hard-press stiffness", 0, 255, ""),
        ("throttle_curve", "Stiffness curve shape", 0.1, 20.0, ""),
    ]),
    ("Speed-based throttle", [
        ("enable_speed_throttle", "Speed-based throttle", None, None,
         "Extra resistance at low speed for precise control, lighter at high speed."),
        ("speed_throttle_boost", "Extra force at standstill", 0, 255,
         "0 = off. Flat resistance added at 0 km/h, fading to normal."),
        ("speed_throttle_fade_km", "Fade-out speed (km/h)", 0.0, 500.0,
         "Speed where boost fully fades. Default 80."),
    ]),
    ("ABS (anti-lock brake) rumble", [
        ("abs_brake_threshold", "Only when braking harder than", 0, 255, ""),
        ("abs_min_speed_kmh", "Only when faster than (km/h)", 0.0, 500.0, ""),
        ("abs_slip_ratio_threshold", "Wheel slip sensitivity", 0.0, 10.0, ""),
        ("abs_combined_slip_threshold", "Tire grip sensitivity", 0.0, 10.0, ""),
        ("abs_freq", "Rumble speed (Hz)", 0, 255, ""),
        ("abs_amp", "Rumble strength", 0, 255, ""),
    ]),
    ("Redline (rev limiter) buzz", [
        ("rev_limit_ratio", "Fire near redline at", 0.0, 1.0, ""),
        ("rev_limit_freq", "Buzz speed (Hz)", 0, 255, ""),
        ("rev_limit_amp", "Buzz strength", 0, 255, ""),
        ("rev_limit_hold_ms", "Buzz hold time (ms)", 0.0, 1000.0, ""),
    ]),
    ("Wheelspin buzz", [
        ("wheelspin_amp", "Buzz strength", 0, 255, ""),
    ]),
    ("Idle buzz", [
        ("idle_amp_high", "Idle strength", 0, 255, ""),
    ]),
    ("Turbo lag", [
        ("enable_turbo_lag", "Turbo lag vibration", None, None,
         "Brief R2 rumble when boost pressure climbs."),
        ("turbo_lag_freq", "Rumble speed (Hz)", 0, 255,
         "Deep rumble frequency. Default 8."),
        ("turbo_lag_amp", "Rumble strength", 0, 255,
         "Max vibration amplitude. Default 40."),
        ("turbo_lag_threshold", "Boost change sensitivity", 0.0, 1.0,
         "Min boost delta per tick to trigger. Default 0.05."),
        ("turbo_lag_cooldown_ms", "Cooldown (ms)", 0.0, 2000.0,
         "Min gap between rumbles. Suppresses steady-state jitter. Default 300."),
    ]),
    ("Gear shift thump", [
        ("gear_shift_freq", "Thump speed (Hz)", 0, 255, ""),
        ("gear_shift_amp", "Thump strength", 0, 255, ""),
        ("gear_shift_duration_ms", "Thump length (ms)", 0.0, 2000.0, ""),
    ]),
]

SYSTEM_SECTIONS = [
    ("Telemetry (applies on next launch)", [
        ("udp_port", "UDP port", 1, 65535,
         "In Forza HUD: host 127.0.0.1 (try ::1 if it fails)."),
    ]),
    ("Startup pulse", [
        ("startup_pulse_force", "Startup buzz strength", 0, 255, ""),
    ]),
    ("Reconnect", [
        ("enable_reconnect", "Auto-reconnect when controller drops", None, None, ""),
        ("reconnect_interval_s", "Reconnect check interval (s)", 0.1, 60.0, ""),
    ]),
    ("Game detection", [
        ("exit_on_game_close", "Auto-exit when the game closes", None, None, ""),
        ("game_poll_interval_s", "Game-watch check interval (s)", 0.1, 60.0, ""),
    ]),
]

SETTING_RANGES = {a: (lo, hi)
                  for sections in (SETTING_SECTIONS, SYSTEM_SECTIONS)
                  for _, fields in sections
                  for a, _lbl, lo, hi, *_rest in fields
                  if lo is not None and hi is not None}


def _format_value(v) -> str:
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


class SettingsTab(ctk.CTkFrame):
    """Header + scrollable sectioned list. System tab subclasses this."""
    SECTIONS = SETTING_SECTIONS
    SHOW_RESET = True
    PAGE_TITLE = "Settings"
    PAGE_SUBTITLE = "All changes save instantly."

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.settings = app.settings
        self._switches: dict[str, ctk.CTkSwitch] = {}
        self._sliders: dict[str, ctk.CTkSlider] = {}
        self._entries: dict[str, ctk.CTkEntry] = {}
        self._reset_armed = False
        self._reset_btn: ctk.CTkButton | None = None

        W.PageHeader(self, t(self.PAGE_TITLE), t(self.PAGE_SUBTITLE)
                     ).pack(fill="x", pady=(0, T.PAD_MD))
        self._scroll = W.FastScroll(self)
        self._scroll.pack(fill="both", expand=True)

        self._build()
        app.register_refresh(self._refresh_widgets)

    # MARK: build -----------------------------------------------------------

    def _build(self):
        for section, fields in self.SECTIONS:
            self._build_section_card(section, fields)
        if self.SHOW_RESET:
            self._reset_btn = W.DangerButton(self._scroll, t("Reset to defaults"),
                                             command=self._on_reset)
            self._reset_btn.pack(fill="x", pady=(T.PAD_MD, T.PAD_SM))

    def _build_section_card(self, section_title: str, fields: list):
        card = W.Card(self._scroll)
        card.pack(fill="x", pady=(0, T.PAD_MD))
        W.H2(card, t(section_title)).pack(anchor="w",
                                          padx=T.PAD_MD,
                                          pady=(T.PAD_MD, T.PAD_SM))
        for entry in fields:
            attr, label, lo, hi, *rest = entry
            hint = rest[0] if rest else ""
            value = getattr(self.settings, attr, None)
            if value is None:
                continue
            if isinstance(value, bool):
                self._add_switch_row(card, attr, label, hint)
            elif isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
                if attr == "udp_port":
                    self._add_entry_only_row(card, attr, label, value, hint)
                else:
                    self._add_slider_row(card, attr, label, value, lo, hi, hint)
            else:
                self._add_entry_only_row(card, attr, label, value, hint)
        ctk.CTkFrame(card, fg_color="transparent", height=T.PAD_SM).pack()

    # MARK: row helpers -----------------------------------------------------

    def _add_switch_row(self, parent, attr: str, label: str, hint: str):
        row = W.FieldRow(parent, t(label), hint=t(hint) if hint else "")
        row.pack(fill="x", padx=T.PAD_MD, pady=T.PAD_XS)
        sw = ctk.CTkSwitch(row.controls, text="",
                           command=lambda a=attr: self._on_switch(a))
        if getattr(self.settings, attr):
            sw.select()
        sw.pack(side="left", anchor="w")
        self._switches[attr] = sw

    def _add_entry_only_row(self, parent, attr: str, label: str, value, hint: str):
        row = W.FieldRow(parent, t(label), hint=t(hint) if hint else "")
        row.pack(fill="x", padx=T.PAD_MD, pady=T.PAD_XS)
        entry = ctk.CTkEntry(row.controls, width=120)
        entry.insert(0, _format_value(value))
        entry.pack(side="right")
        self._bind_entry(entry, attr)
        self._entries[attr] = entry

    def _add_slider_row(self, parent, attr: str, label: str, value, lo, hi, hint: str):
        row = W.FieldRow(parent, t(label), hint=t(hint) if hint else "")
        row.pack(fill="x", padx=T.PAD_MD, pady=T.PAD_XS)
        if isinstance(value, int):
            steps = max(1, int(hi - lo))
        else:
            steps = 200
        sld = ctk.CTkSlider(row.controls, from_=float(lo), to=float(hi),
                            number_of_steps=steps,
                            command=lambda v, a=attr: self._on_slider(a, v))
        sld.set(float(value))
        sld.pack(side="left", fill="x", expand=True, padx=(0, T.PAD_SM))
        entry = ctk.CTkEntry(row.controls, width=80)
        entry.insert(0, _format_value(value))
        entry.pack(side="right")
        self._bind_entry(entry, attr)
        self._sliders[attr] = sld
        self._entries[attr] = entry

    def _bind_entry(self, entry: ctk.CTkEntry, attr: str):
        entry.bind("<KeyRelease>", lambda _e, a=attr: self._on_entry_change(a, strict=False))
        entry.bind("<Return>", lambda _e, a=attr: self._on_entry_change(a, strict=True))
        entry.bind("<FocusOut>", lambda _e, a=attr: self._on_entry_change(a, strict=True))

    # MARK: handlers --------------------------------------------------------

    def _on_switch(self, attr: str):
        if self.app._refreshing:
            return
        if not hasattr(self.settings, attr):
            return
        value = bool(self._switches[attr].get())
        if getattr(self.settings, attr) != value:
            setattr(self.settings, attr, value)
            preferences.save(self.settings)
            log.info("%s = %s", attr, value)
        self._push_live(attr, value)

    def _on_slider(self, attr: str, raw: float):
        if self.app._refreshing:
            return
        if not hasattr(self.settings, attr):
            return
        current = getattr(self.settings, attr)
        new = int(round(raw)) if isinstance(current, int) else float(raw)
        if new != current:
            setattr(self.settings, attr, new)
            preferences.save(self.settings)
            log.info("%s = %s", attr, new)
        entry = self._entries.get(attr)
        if entry is not None:
            text = _format_value(new)
            if entry.get() != text:
                entry.delete(0, "end")
                entry.insert(0, text)
        self._push_live(attr, new)

    def _on_entry_change(self, attr: str, strict: bool):
        if self.app._refreshing:
            return
        if not hasattr(self.settings, attr):
            return
        entry = self._entries[attr]
        raw = entry.get().strip()
        if not raw:
            return
        current = getattr(self.settings, attr)
        try:
            if isinstance(current, bool):
                new = raw.lower() in ("1", "true", "yes", "on")
            elif isinstance(current, int):
                new = int(float(raw))
            elif isinstance(current, float):
                new = float(raw)
            else:
                new = raw
        except ValueError:
            if strict:
                entry.delete(0, "end")
                entry.insert(0, _format_value(current))
            return
        rng = SETTING_RANGES.get(attr)
        if rng and isinstance(new, (int, float)) and not isinstance(new, bool):
            lo, hi = rng
            clamped = max(lo, min(hi, new))
            if isinstance(current, int):
                clamped = int(clamped)
            if clamped != new:
                if strict:
                    new = clamped
                    entry.delete(0, "end")
                    entry.insert(0, _format_value(new))
                else:
                    return
        if new != current:
            setattr(self.settings, attr, new)
            preferences.save(self.settings)
            log.info("%s = %s", attr, new)
            sld = self._sliders.get(attr)
            if sld is not None and abs(float(sld.get()) - float(new)) > 1e-9:
                sld.set(float(new))
        self._push_live(attr, new)

    def _on_reset(self):
        if not self._reset_armed:
            self._reset_armed = True
            if self._reset_btn:
                self._reset_btn.configure(text=t("Click again to confirm reset"))
            return
        self._reset_armed = False
        if self._reset_btn:
            self._reset_btn.configure(text=t("Reset to defaults"))
        preferences.reset(self.settings)
        self.app.refresh_setting_widgets()
        log.info("Settings reset to defaults.")

    def _push_live(self, attr: str, value):
        ds = getattr(self.app, "_ds", None)
        if ds is None:
            return
        if attr == "enable_reconnect":
            ds.set_reconnect_enabled(value)
        elif attr == "reconnect_interval_s":
            ds.set_reconnect_interval(value)

    # MARK: refresh ---------------------------------------------------------

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
        for attr, sld in self._sliders.items():
            if not hasattr(self.settings, attr):
                continue
            want = float(getattr(self.settings, attr))
            if abs(float(sld.get()) - want) > 1e-9:
                sld.set(want)
        for attr, entry in self._entries.items():
            if not hasattr(self.settings, attr):
                continue
            text = _format_value(getattr(self.settings, attr))
            if entry.get() != text:
                entry.delete(0, "end")
                entry.insert(0, text)
