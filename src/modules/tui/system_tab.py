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
from textual.containers import Horizontal
from textual.widgets import Button, Label, RadioButton, RadioSet, Static, Switch

from lang import t
from modules import preferences
from modules.dualsense.main import _enumerate_dualsenses, _is_bluetooth, identify_pulse

from modules import dsx as dsx_module
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
    SystemTab #dsx-status-row { height: 3; padding: 0 1; align-vertical: middle; }
    SystemTab #dsx-status { width: 1fr; height: 1; color: $text-muted; }
    SystemTab #dsx-status.running { color: $success; text-style: bold; }
    SystemTab #dsx-status.stopped { color: $error; text-style: bold; }
    SystemTab #dsx-check {
        height: 1; min-height: 1; width: auto;
        padding: 0 2; margin: 0;
        border: none; background: $boost; color: $text-muted;
    }
    SystemTab #dsx-check:hover { background: $accent 30%; color: $text; }
    """

    def compose(self) -> ComposeResult:
        yield Label(t("Controller"), classes="section")
        yield Label(t("Lock to controller"))
        # Skip blocking HID enumeration here; on_show() scans off-thread.
        self._devices = []
        yield RadioSet(*self._build_controller_buttons(), id="controller-radio")
        with Horizontal(id="controller-buttons"):
            yield Button(t("Rescan"), id="controller-rescan")

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

        for section, fields in self.SECTIONS:
            yield Label(t(section), classes="section")
            if section == "DSX output":
                with Horizontal(id="dsx-status-row"):
                    yield Static(t("DSX: checking..."), id="dsx-status")
                    yield Button(t("Refresh"), id="dsx-check")
            yield from self._compose_fields(fields)

    def on_mount(self) -> None:
        if sentinel_path() is not None:
            apply_sentinel(self.settings.check_for_updates)

    def _update_dsx_status(self, running: bool) -> None:
        try:
            widget = self.query_one("#dsx-status", Static)
        except Exception:
            return
        if running:
            widget.update(t("DSX: running"))
            widget.set_classes("running")
            if not self.settings.enable_dsx:
                self.settings.enable_dsx = True
                preferences.save(self.settings)
                try:
                    self.query_one("#enable_dsx", Switch).value = True
                except Exception:
                    pass
                log.info("DSX detected — enable_dsx auto-enabled")
        else:
            widget.update(t("DSX: not detected"))
            widget.set_classes("stopped")

    async def _check_dsx(self) -> None:
        running = await asyncio.to_thread(dsx_module.is_dsx_running)
        self._update_dsx_status(running)

    async def on_show(self) -> None:
        await self._rerender_controller()
        await self._check_dsx()

    def _attached_serial(self) -> str:
        ds = getattr(self.app, "_ds", None)
        if ds is None or not ds.connected:
            return ""
        path = ds.dev_path
        for d in self._devices:
            if d.get("path") == path:
                return d.get("serial_number") or ""
        return ""

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
        if ds is not None:
            ds.set_selection(new)
            if new and new != self._attached_serial():
                ds.force_reconnect()
        await self._rerender_controller()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "controller-rescan":
            await self._rerender_controller()
        elif event.button.id == "dsx-check":
            w = self.query_one("#dsx-status", Static)
            w.update(t("DSX: checking..."))
            w.set_classes("")
            await self._check_dsx()

    def on_switch_changed(self, event: Switch.Changed) -> None:
        super().on_switch_changed(event)
        if event.switch.id == "check_for_updates":
            apply_sentinel(event.value)
