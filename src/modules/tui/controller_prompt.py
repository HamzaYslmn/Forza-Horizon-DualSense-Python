"""Modal prompt shown when multiple DualSenses are visible and no rule
resolves the tie. Clicking a row fires a haptic pulse on that controller
so the user can identify it by feel; Confirm commits a session-scoped
pick (the persistent lock is set only from the System tab)."""

import logging

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, RadioButton, RadioSet

from lang import t
from modules.dualsense.main import _is_bluetooth, identify_pulse

log = logging.getLogger("fhds")


class ControllerPrompt(ModalScreen[str]):
    """Returns the picked serial via dismiss(serial) or None on cancel."""

    DEFAULT_CSS = """
    ControllerPrompt { align: center middle; }
    ControllerPrompt Vertical#prompt-box {
        width: 60; height: auto; padding: 1 2;
        background: $panel; border: thick $accent;
    }
    ControllerPrompt Label.title { text-style: bold; color: $accent; padding-bottom: 1; }
    ControllerPrompt Label.hint { color: $text-muted; padding-bottom: 1; }
    ControllerPrompt RadioSet { height: auto; margin-bottom: 1; }
    ControllerPrompt #prompt-buttons { height: 3; }
    ControllerPrompt #prompt-buttons Button { margin-right: 2; }
    """

    def __init__(self, candidates: list[dict], pulse_force: int = 150):
        super().__init__()
        self._candidates = list(candidates)
        self._pulse_force = pulse_force
        self._selected_serial: str | None = None

    def compose(self) -> ComposeResult:
        with Vertical(id="prompt-box"):
            yield Label(t("Select a DualSense"), classes="title")
            yield Label(
                t("Multiple DualSenses are connected. Click one to feel a pulse on it, then confirm."),
                classes="hint",
            )
            yield RadioSet(*self._build_buttons(), id="prompt-radio")
            with Vertical(id="prompt-buttons"):
                yield Button(t("Confirm"), id="prompt-confirm", disabled=True)
                yield Button(t("Rescan"), id="prompt-rescan")

    def _build_buttons(self) -> list[RadioButton]:
        buttons = []
        for d in self._candidates:
            sn = d.get("serial_number") or ""
            transport = "BT" if _is_bluetooth(d) else "USB"
            if sn:
                label = f"[{transport}] {sn}"
                buttons.append(RadioButton(label, id=f"cand-{sn}"))
            else:
                buttons.append(RadioButton(
                    f"[{transport}] {t('(no serial - not selectable)')}",
                    id=f"cand-noserial-{id(d)}",
                    disabled=True,
                ))
        return buttons

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        button = event.pressed
        if button is None or button.id is None or not button.id.startswith("cand-"):
            return
        if button.id.startswith("cand-noserial-"):
            self._selected_serial = None
            self.query_one("#prompt-confirm", Button).disabled = True
            return
        serial = button.id[len("cand-"):]
        self._selected_serial = serial
        self.query_one("#prompt-confirm", Button).disabled = False
        info = next((d for d in self._candidates
                     if (d.get("serial_number") or "") == serial), None)
        if info is not None:
            self.run_worker(self._pulse_worker(info), exclusive=True, thread=True)

    async def _pulse_worker(self, info: dict) -> None:
        identify_pulse(info, force=self._pulse_force)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "prompt-confirm":
            if self._selected_serial:
                self.dismiss(self._selected_serial)
        elif event.button.id == "prompt-rescan":
            self.dismiss(None)
