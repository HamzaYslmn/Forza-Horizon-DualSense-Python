"""System tab: global / launch-time settings, with the ZUV update toggle at
the top.

The ZUV loader runs *before* this app starts, so toggling the update check here
only affects the next launch. The mechanism is a sentinel file
(.zuv-update-disabled) the loader checks in its cache_root; when present, the
update check is skipped. ZUV exports cache_root via the ZUV_CACHE_ROOT env var.
"""
import asyncio
import logging
import os
import threading
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, RadioButton, RadioSet, Switch

from lang import t
from modules.config import preferences
from modules.dualsense.main import _enumerate_dualsenses, _is_bluetooth, identify_pulse

from .settings_tab import SYSTEM_SECTIONS, SettingsTab

log = logging.getLogger("fhds")

SENTINEL = ".zuv-update-disabled"


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
    SystemTab #controller-hid-section { height: auto; }
    SystemTab #controller-hid-section > Label { padding: 0 1; }
    """

    def compose(self) -> ComposeResult:
        yield Label(t("Controller"), classes="section")
        with Vertical(id="controller-hid-section"):
            yield Label(t("Lock to controller"))
            self._devices = []
            yield RadioSet(*self._build_controller_buttons(), id="controller-radio")
            with Horizontal(id="controller-buttons"):
                yield Button(t("Rescan"), id="controller-rescan")
        yield Label(
            t("DSX is active - controller managed by DSX. "
              "Disable DSX to select a controller here."),
            id="dsx-controller-note",
            classes="hint",
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
        if sentinel_path() is not None:
            apply_sentinel(self.settings.check_for_updates)
        self._sync_controller_visibility()

    def _sync_controller_visibility(self) -> None:
        try:
            hid = self.query_one("#controller-hid-section")
            note = self.query_one("#dsx-controller-note")
            hid.display = not self.settings.use_dsx
            note.display = bool(self.settings.use_dsx)
        except Exception:
            pass

    async def on_show(self) -> None:
        if not self.settings.use_dsx:
            await self._rerender_controller()

    def _attached_serial(self) -> str:
        ds = getattr(self.app, "_ds", None)
        if ds is None or not ds.connected:
            return ""
        return getattr(ds, "dev_serial", "") or ""

    def _build_controller_buttons(self) -> list[RadioButton]:
        attached_serial = self._attached_serial()
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
                    f"\\[{transport}] {sn}{marker}",
                    id=f"ctrl-{sn}",
                    value=(sn == current_lock),
                ))
            else:
                no_serial = t("(no serial - not selectable)")
                buttons.append(RadioButton(
                    f"\\[{transport}] {no_serial}",
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
        # Enumerate off-thread; blocking HID I/O would freeze the event loop.
        self._devices = await asyncio.to_thread(_enumerate_dualsenses)
        # await remove_children() before mount() to avoid a DuplicateIds collision.
        radio = self.query_one("#controller-radio", RadioSet)
        await radio.remove_children()
        for b in self._build_controller_buttons():
            await radio.mount(b)

    async def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.radio_set.id != "controller-radio":
            return
        # Force visual sync: clear stale value=True on all but the pressed button.
        pressed = event.pressed
        for rb in event.radio_set.query(RadioButton):
            if rb is not pressed and rb.value:
                rb.value = False
        new = self._selected_lock()
        if new is None:
            return
        if pressed is not None and pressed.id is not None and pressed.id.startswith("ctrl-") \
                and pressed.id != "ctrl-auto" and not pressed.id.startswith("ctrl-noserial-"):
            serial = pressed.id[len("ctrl-"):]
            info = next((d for d in self._devices
                         if (d.get("serial_number") or "") == serial), None)
            if info is not None:
                threading.Thread(target=identify_pulse, args=(info,),
                                 kwargs={"force": self.settings.startup_pulse_force},
                                 daemon=True).start()
        current = self.settings.controller_lock_serial
        if new != current:
            self.settings.controller_lock_serial = new
            preferences.save(self.settings)
            log.info("controller_lock_serial = %r", new)
        ds = getattr(self.app, "_ds", None)
        if ds is not None and hasattr(ds, "set_selection"):
            ds.set_selection(new)
            if new and new != self._attached_serial():
                ds.force_reconnect()
        await self._rerender_controller()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "controller-rescan":
            await self._rerender_controller()

    def on_switch_changed(self, event: Switch.Changed) -> None:
        super().on_switch_changed(event)
        if event.switch.id == "check_for_updates":
            apply_sentinel(event.value)
        if event.switch.id == "use_dsx":
            self._sync_controller_visibility()
            log.info("DSX %s", "enabled" if event.value else "disabled")
