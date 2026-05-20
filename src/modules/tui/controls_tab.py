"""Controls tab: per-trigger effect on/off switches."""
import logging

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Label, Switch

from lang import t
from modules import preferences

log = logging.getLogger("fhds")

# Listed highest priority first, matching the Controller's effect precedence.
TRIGGER_CONTROLS = [
    ("L2", [
        ("enable_gear_shift_brake",  "Shift thump"),
        ("enable_abs",               "ABS rumble"),
        ("enable_brake_static_wall", "Static brake wall"),
        ("enable_brake_resistance",  "Brake stiffness"),
        ("enable_handbrake_bonus",   "Handbrake stiffness bonus"),
    ]),
    ("R2", [
        ("enable_gear_shift",          "Shift thump"),
        ("enable_wheelspin_pulse",     "Wheelspin pulse"),
        ("enable_rev_limiter",         "Redline buzz"),
        ("enable_throttle_resistance", "Throttle stiffness"),
    ]),
]


class ControlsTab(VerticalScroll):
    DEFAULT_CSS = """
    ControlsTab { width: 1fr; height: 1fr; padding: 1 2; }
    ControlsTab .grid { width: 1fr; height: auto; }
    ControlsTab .column { width: 1fr; height: auto; padding: 0 1; }
    ControlsTab Label.section { text-style: bold; color: $accent; padding: 1 0 0 3; }
    ControlsTab .row { height: 3; width: 1fr; align-vertical: middle; padding: 0 1; }
    ControlsTab .row Switch { margin-right: 2; }
    ControlsTab .row Label { width: 1fr; height: 3; content-align: left middle; }
    App.-narrow ControlsTab .grid { layout: vertical; }
    App.-narrow ControlsTab .column { width: 1fr; }
    """

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def compose(self) -> ComposeResult:
        with Horizontal(classes="grid"):
            for trigger, toggles in TRIGGER_CONTROLS:
                with Vertical(classes="column"):
                    yield Label(trigger, classes="section")
                    for attr, label in toggles:
                        with Horizontal(classes="row"):
                            yield Switch(value=getattr(self.settings, attr), id=attr)
                            yield Label(t(label))

    def on_switch_changed(self, event: Switch.Changed):
        attr = event.switch.id
        if attr and hasattr(self.settings, attr):
            setattr(self.settings, attr, event.value)
            preferences.save(self.settings)
            self.app.haptic(event.value)
