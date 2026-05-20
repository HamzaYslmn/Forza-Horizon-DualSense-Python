"""System tab: global / launch-time settings, with the ZUV update toggle at
the top.

The ZUV loader runs *before* this app starts, so toggling the update check here
only affects the next launch. The mechanism is a sentinel file
(.zuv-update-disabled) the loader checks in its cache_root; when present, the
update check is skipped. ZUV exports cache_root via the ZUV_CACHE_ROOT env var.
"""
import logging
import os
import threading
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Label, RadioButton, RadioSet, Select, Switch

from lang import t
from modules import preferences
from modules.dualsense.main import _enumerate_dualsenses, _is_bluetooth, identify_pulse

from .settings_tab import SYSTEM_SECTIONS, SettingsTab

log = logging.getLogger("fhds")

SENTINEL = ".zuv-update-disabled"

TRANSPORT_CHOICES = [
    ("auto", "Auto"),
    ("bt",   "Prefer BT"),
    ("usb",  "Prefer USB"),
]


def sentinel_path() -> Path | None:
    """Path to the sentinel file, or None when not running inside a ZUV bundle."""
    root = os.environ.get("ZUV_CACHE_ROOT")
    return Path(root) / SENTINEL if root else None


def apply_sentinel(enabled: bool) -> None:
    """Reconcile the on-disk sentinel with the desired setting.
    enabled=True  -> updates wanted -> remove sentinel.
    enabled=False -> updates off    -> create sentinel.
    No-op when running outside a ZUV bundle (no ZUV_CACHE_ROOT)."""
    path = sentinel_path()
    if path is None:
        return
    try:
        if enabled:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
    except OSError as e:
        log.warning("Could not update %s: %s", SENTINEL, e)


class SystemTab(SettingsTab):
    SECTIONS = SYSTEM_SECTIONS
    SHOW_RESET = False

    DEFAULT_CSS = """
    SystemTab #controller-buttons { height: 3; padding: 0 1; }
    SystemTab #controller-buttons Button { margin-right: 2; }
    SystemTab #controller-radio { height: auto; padding: 0 1 1 1; }
    SystemTab #transport-row { height: 3; padding: 0 1; }
    SystemTab #transport-row Select { width: 24; }
    """

    def compose(self) -> ComposeResult:
        yield Label(t("Controller"), classes="section")
        yield Label(t("Lock to controller"))
        self._devices = _enumerate_dualsenses()
        yield RadioSet(*self._build_controller_buttons(), id="controller-radio")
        with Horizontal(id="controller-buttons"):
            yield Button(t("Apply"), id="controller-apply", disabled=True)
            yield Button(t("Rescan"), id="controller-rescan")
        with Horizontal(id="transport-row"):
            yield Label(t("Transport preference (when transports differ)"))
            yield Select(
                [(t(label), value) for value, label in TRANSPORT_CHOICES],
                value=self.settings.controller_transport_preference,
                allow_blank=False,
                id="transport-pref",
            )

        yield Label(t("Updates"), classes="section")
        if sentinel_path() is None:
            yield Label(
                t("ZUV not found: this build is not running inside a ZUV bundle "
                  "(ZUV_CACHE_ROOT env var is missing), so the update toggle has "
                  "nothing to control. Run the bundled .zuv.py to manage updates."),
                classes="error",
            )
        else:
            with Horizontal(classes="row"):
                yield Switch(value=self.settings.check_for_updates, id="check_for_updates")
                yield Label(t("Check for updates at launch"))
            yield Label(
                t("When off, ZUV will not prompt for updates on startup. "
                  "Toggle on and restart the app to check for a new release."),
                classes="hint",
            )

        yield from super().compose()

    def on_mount(self) -> None:
        # Reconcile sentinel with stored setting in case the cache was wiped or
        # the prefs file was edited externally.
        if sentinel_path() is not None:
            apply_sentinel(self.settings.check_for_updates)

    def _build_controller_buttons(self) -> list[RadioButton]:
        ds = getattr(self.app, "_ds", None)
        attached_serial = ""
        if ds is not None and ds.connected:
            path = ds.dev_path
            for d in self._devices:
                if d.get("path") == path:
                    attached_serial = d.get("serial_number") or ""
                    break

        current_lock = self.settings.controller_lock_serial
        buttons: list[RadioButton] = []
        buttons.append(RadioButton(
            t("Auto (first found)"),
            id="ctrl-auto",
            value=(current_lock == ""),
        ))
        for d in self._devices:
            sn = d.get("serial_number") or ""
            transport = "BT" if _is_bluetooth(d) else "USB"
            if sn:
                attached_now = t("attached now")
                marker = f"  < {attached_now}" if sn == attached_serial else ""
                buttons.append(RadioButton(
                    f"[{transport}] {sn}{marker}",
                    id=f"ctrl-{sn}",
                    value=(sn == current_lock),
                ))
            else:
                no_serial = t("(no serial - not selectable)")
                buttons.append(RadioButton(
                    f"[{transport}] {no_serial}",
                    id=f"ctrl-noserial-{id(d)}",
                    disabled=True,
                ))
        return buttons

    def _selected_lock(self) -> str | None:
        radio = self.query_one("#controller-radio", RadioSet)
        button = radio.pressed_button
        if button is None or button.id is None:
            return None
        if button.id == "ctrl-auto":
            return ""
        if button.id.startswith("ctrl-noserial-"):
            return None
        return button.id[len("ctrl-"):]

    async def _rerender_controller(self) -> None:
        # await remove_children() before mount() to avoid a DuplicateIds collision.
        self._devices = _enumerate_dualsenses()
        radio = self.query_one("#controller-radio", RadioSet)
        await radio.remove_children()
        for b in self._build_controller_buttons():
            await radio.mount(b)
        self.query_one("#controller-apply", Button).disabled = True

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.radio_set.id != "controller-radio":
            return
        new = self._selected_lock()
        current = self.settings.controller_lock_serial
        self.query_one("#controller-apply", Button).disabled = (new is None or new == current)
        button = event.pressed
        if button is None or button.id is None or not button.id.startswith("ctrl-"):
            return
        if button.id in ("ctrl-auto",) or button.id.startswith("ctrl-noserial-"):
            return
        serial = button.id[len("ctrl-"):]
        info = next((d for d in self._devices
                     if (d.get("serial_number") or "") == serial), None)
        if info is not None:
            threading.Thread(target=identify_pulse, args=(info,),
                             kwargs={"force": self.settings.startup_pulse_force},
                             daemon=True).start()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "controller-rescan":
            await self._rerender_controller()
            return
        if bid != "controller-apply":
            return
        new = self._selected_lock()
        if new is None:
            return
        current = self.settings.controller_lock_serial
        if new == current:
            self.query_one("#controller-apply", Button).disabled = True
            return
        self.settings.controller_lock_serial = new
        preferences.save(self.settings)
        log.info("controller_lock_serial = %r", new)
        ds = getattr(self.app, "_ds", None)
        if ds is not None:
            ds.set_selection(new, self.settings.controller_transport_preference)
            attached_serial = ""
            path = ds.dev_path
            for d in self._devices:
                if d.get("path") == path:
                    attached_serial = d.get("serial_number") or ""
                    break
            if new and new != attached_serial:
                ds.force_reconnect()
        await self._rerender_controller()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id != "transport-pref":
            return
        new = event.value
        if not isinstance(new, str) or new == self.settings.controller_transport_preference:
            return
        self.settings.controller_transport_preference = new
        preferences.save(self.settings)
        log.info("controller_transport_preference = %s", new)
        ds = getattr(self.app, "_ds", None)
        if ds is not None:
            ds.set_selection(self.settings.controller_lock_serial, new)

    def on_switch_changed(self, event: Switch.Changed) -> None:
        super().on_switch_changed(event)
        if event.switch.id == "check_for_updates":
            apply_sentinel(event.value)
