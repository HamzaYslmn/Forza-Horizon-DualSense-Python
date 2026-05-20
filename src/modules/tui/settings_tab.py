"""Settings tab: numeric tuning inputs with live-save."""
import logging

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Input, Label, Switch

from lang import t
from modules import preferences

log = logging.getLogger("fhds")

SETTING_SECTIONS = [
    ("Pedals / deadzones", [
        ("accel_deadzone", "Accel deadzone", 0, 255),
        ("brake_deadzone", "Brake deadzone", 0, 255),
    ]),
    ("Brake (left trigger)", [
        ("brake_baseline_force", "Baseline force", 0, 255),
        ("brake_max_force",      "Max force",     0, 255),
        ("brake_curve",          "Curve",         0.1, 20.0),
        ("brake_static_wall_at",    "Static wall at",    0, 255),
        ("brake_static_wall_force", "Static wall force", 0, 255),
        ("handbrake_bonus",         "Handbrake bonus",   0, 255),
    ]),
    ("Throttle (right trigger)", [
        ("throttle_baseline_force", "Baseline force", 0, 255),
        ("throttle_max_force",      "Max force",     0, 255),
        ("throttle_curve",          "Curve",         0.1, 20.0),
    ]),
    ("ABS", [
        ("abs_brake_threshold",         "Brake threshold",         0, 255),
        ("abs_min_speed_kmh",           "Min speed (km/h)",        0.0, 500.0),
        ("abs_slip_ratio_threshold",    "Slip ratio threshold",    0.0, 10.0),
        ("abs_combined_slip_threshold", "Combined slip threshold", 0.0, 10.0),
        ("abs_freq",                    "Frequency (Hz)",          0, 255),
        ("abs_amp",                     "Amplitude",               0, 255),
    ]),
    ("Rev limiter", [
        ("rev_limit_ratio",   "Trigger at RPM ratio", 0.0, 1.0),
        ("rev_limit_freq",    "Frequency (Hz)",       0, 255),
        ("rev_limit_amp",     "Amplitude",            0, 255),
        ("rev_limit_hold_ms", "Hold (ms)",            0.0, 1000.0),
    ]),
    ("Wheelspin pulse", [
        ("wheelspin_min_throttle",    "Min throttle",          0, 255),
        ("wheelspin_slip_threshold",  "Slip threshold",        0.0, 10.0),
        ("wheelspin_slip_full_scale", "Slip full-scale range", 0.1, 10.0),
        ("wheelspin_freq",            "Frequency (Hz)",        0, 255),
    ]),
    ("Gear shift thump", [
        ("gear_shift_freq",        "Frequency (Hz)", 0, 255),
        ("gear_shift_amp",         "Amplitude",      0, 255),
        ("gear_shift_duration_ms", "Duration (ms)",  0.0, 2000.0),
    ]),
]

SYSTEM_SECTIONS = [
    ("Telemetry (applies on next launch)", [
        ("udp_port", "UDP port", 1, 65535),
    ]),
    ("Startup pulse", [
        ("startup_pulse_force", "Startup pulse force", 0, 255),
    ]),
    ("Reconnect", [
        ("enable_reconnect",     "Auto-reconnect controller (disable for HidHide)", None, None),
        ("reconnect_interval_s", "Reconnect interval (s)", 0.1, 60.0),
    ]),
    ("Game detection", [
        ("exit_on_game_close",   "Detect game (auto-exit when it closes)", None, None),
        ("game_poll_interval_s", "Poll interval (s)", 0.1, 60.0),
    ]),
]

SETTING_RANGES = {a: (lo, hi)
                  for sections in (SETTING_SECTIONS, SYSTEM_SECTIONS)
                  for _, fields in sections
                  for a, _, lo, hi in fields if lo is not None and hi is not None}


def _fmt_range(lo, hi):
    if isinstance(lo, int) and isinstance(hi, int):
        return f"{lo}-{hi}"
    return f"{lo:g}-{hi:g}"


class SettingsTab(VerticalScroll):
    DEFAULT_CSS = """
    SettingsTab, SystemTab { width: 1fr; height: 1fr; padding: 1 2; }
    SettingsTab Label.section, SystemTab Label.section { text-style: bold; color: $accent; padding: 1 0 0 1; }
    SettingsTab .row, SystemTab .row { height: 3; width: 1fr; align-vertical: middle; padding: 0 1; }
    SettingsTab .row Label, SystemTab .row Label { width: 1fr; height: 3; content-align: left middle; }
    SettingsTab .row Input, SystemTab .row Input { width: 16; min-width: 10; max-width: 20; height: 3; }
    SettingsTab .row Switch, SystemTab .row Switch { margin-right: 2; }
    SettingsTab #reset-settings { width: 1fr; margin: 2 0 1 0; }
    SystemTab Label.hint { width: 1fr; height: auto; color: $text-muted; padding: 0 1 1 1; }
    SystemTab Label.error { width: 1fr; height: auto; color: $error; padding: 1; text-style: bold; }
    """

    SECTIONS = SETTING_SECTIONS
    SHOW_RESET = True

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def compose(self) -> ComposeResult:
        for section, fields in self.SECTIONS:
            yield Label(t(section), classes="section")
            for attr, label, lo, hi in fields:
                value = getattr(self.settings, attr, None)
                if value is None:
                    continue
                if isinstance(value, bool):
                    with Horizontal(classes="row"):
                        yield Switch(value=value, id=attr)
                        yield Label(t(label))
                    continue
                input_type = "integer" if isinstance(value, int) else "number"
                with Horizontal(classes="row"):
                    yield Label(f"{t(label)} ({_fmt_range(lo, hi)})")
                    yield Input(value=str(value), id=f"set-{attr}", type=input_type)
        if self.SHOW_RESET:
            yield Button(t("Reset to defaults"), id="reset-settings", variant="error")

    def on_switch_changed(self, event: Switch.Changed):
        attr = event.switch.id
        if not attr or not hasattr(self.settings, attr):
            return
        if getattr(self.settings, attr) != event.value:
            setattr(self.settings, attr, event.value)
            preferences.save(self.settings)
            log.info("%s = %s", attr, event.value)
        # Push live every time — profile-load/reset flow sets widget values
        # after the settings object is already mutated, so we'd otherwise miss
        # propagating to the running DualSense instance.
        self._push_live(attr, event.value)

    def _push_live(self, attr: str, value) -> None:
        """Push settings that DualSense captures at construction to the running
        instance so the toggle takes effect without restarting the backend."""
        ds = getattr(self.app, "_ds", None)
        if ds is None:
            return
        if attr == "enable_reconnect":
            ds.set_reconnect_enabled(value)
        elif attr == "reconnect_interval_s":
            ds.set_reconnect_interval(value)

    def on_input_submitted(self, event: Input.Submitted):
        self._commit(event.input, strict=True)

    def on_input_changed(self, event: Input.Changed):
        # Live-save on every keystroke that parses cleanly; partial input is ignored.
        self._commit(event.input, strict=False)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "reset-settings":
            preferences.reset(self.settings)
            self.app.refresh_setting_widgets()
            log.info("Settings reset to defaults.")

    def _commit(self, widget: Input, strict: bool) -> None:
        if not widget.id or not widget.id.startswith("set-"):
            return
        attr = widget.id[4:]
        if not hasattr(self.settings, attr):
            return
        current = getattr(self.settings, attr)
        raw = widget.value.strip()
        if not raw:
            return
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
                widget.value = str(current)
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
                    widget.value = str(new)
                else:
                    return
        if new != current:
            setattr(self.settings, attr, new)
            preferences.save(self.settings)
            log.info("%s = %s", attr, new)
        # Always push live (see on_switch_changed for the profile-load reason).
        self._push_live(attr, new)
