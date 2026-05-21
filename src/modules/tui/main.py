"""Textual TUI app: wires tabs together and owns the backend (DualSense + UDP loop)."""
import logging
import threading
import time
import webbrowser

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Header, Input, Static, Switch, TabbedContent, TabPane

from lang import set_language, t
from modules import dualsense, dsx as dsx_module, loop, preferences, profiles, udplistener
from modules.dualsense.triggers import off, vibration
from modules.preferences import _version

from .controls_tab import ControlsTab
from .lang_tab import LangTab
from .logs_tab import DEFAULT_LOG_LEVEL, LogsTab
from .profiles_tab import ProfilesTab
from .settings_tab import SettingsTab
from .system_tab import SystemTab
from .widgets import RangeSlider

log = logging.getLogger("fhds")

HAPTIC_FREQ_HZ = 40
HAPTIC_AMP_ON = 200
HAPTIC_AMP_OFF = 120
HAPTIC_DURATION_S = 0.10


class _LogHandler(logging.Handler):
    def __init__(self, app: "TriggerTUI"):
        super().__init__()
        self.app = app

    def emit(self, record):
        # MARK: drop records during teardown - call_from_thread on a stopped app raises
        if getattr(self.app, "_tearing_down", False):
            return
        msg = self.format(record)
        if threading.get_ident() == self.app._thread_id:
            self.app.write_log(msg)
        else:
            self.app.call_from_thread(self.app.write_log, msg)


class TriggerTUI(App):
    CSS = """
    Screen { background: $surface; }

    #topbar { dock: top; height: 1; background: $boost; }
    #profile { width: auto; height: 1; padding: 0 2; color: $accent; text-style: bold; }
    #status { width: 1fr; height: 1; padding: 0 2; text-align: center; }
    #version { width: auto; height: 1; padding: 0 2; text-align: right; color: $text-muted; }
    #version:hover { color: $accent; text-style: underline; }

    TabbedContent { height: 1fr; }
    Tabs { align-horizontal: center; }
    TabPane { padding: 0; }
    #tab-logs { padding: 0; align-horizontal: left; }

    #bottombar { dock: bottom; height: 1; background: $boost; padding: 0; }
    #bb-spacer { width: 1fr; height: 1; background: transparent; }
    .bb-btn {
        height: 1; min-height: 1; width: auto; min-width: 0;
        padding: 0 2; margin: 0;
        border: none; background: transparent; color: $text-muted;
    }
    .bb-btn:hover { background: $accent 30%; color: $text; }
    #bb-sponsor { background: hotpink; color: white; text-style: bold; }
    #bb-sponsor:hover { background: deeppink; color: white; }
    #bb-changelog { color: $accent; text-style: bold; }
    #bb-changelog:hover { background: $accent 30%; color: $text; }
    """
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "sponsor", "♥ Sponsor"),
    ]
    HORIZONTAL_BREAKPOINTS = [(0, "-narrow"), (80, "-normal"), (120, "-wide")]
    SPONSOR_URL = "https://github.com/sponsors/HamzaYslmn"
    CHANGELOG_URL = "https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python/releases/latest"

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        set_language(settings.language)
        self._stop = threading.Event()
        self._thread = None
        self._ds = None
        self._dsx = None
        self._listener_cm = None
        self._listener = None
        self._status_timer = None
        self._tearing_down = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="topbar"):
            yield Static("", id="profile")
            yield Static("", id="status")
            yield Static(f"v{_version() or '?'}", id="version")
        with TabbedContent(initial="tab-controls"):
            with TabPane(t("Controls"), id="tab-controls"):
                yield ControlsTab(self.settings)
            with TabPane(t("Profiles"), id="tab-profiles"):
                yield ProfilesTab(self.settings)
            with TabPane(t("Settings"), id="tab-settings"):
                yield SettingsTab(self.settings)
            with TabPane(t("System"), id="tab-system"):
                yield SystemTab(self.settings)
            with TabPane(t("Language"), id="tab-lang"):
                yield LangTab(self.settings)
            with TabPane(t("Logs"), id="tab-logs"):
                yield LogsTab()
        with Horizontal(id="bottombar"):
            yield Button(f"q  {t('Quit')}", id="bb-quit", classes="bb-btn")
            yield Static(id="bb-spacer")
            yield Button(t("Changelog"), id="bb-changelog", classes="bb-btn")
            yield Button(t("♥ Sponsor"), id="bb-sponsor", classes="bb-btn")

    # --- lifecycle ----------------------------------------------------------

    def on_mount(self):
        self.title = "FH DualSense"
        self.sub_title = f"UDP {self.settings.udp_host}:{self.settings.udp_port}"

        root = logging.getLogger()
        root.handlers.clear()
        handler = _LogHandler(self)
        handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt="%H:%M:%S"))
        root.addHandler(handler)
        root.setLevel(getattr(logging, DEFAULT_LOG_LEVEL))

        self.refresh_status()
        self.refresh_profile()
        # MARK: keep handle so on_unmount can stop the poller before backend teardown
        self._status_timer = self.set_interval(1.0, self.refresh_status)
        log.info("Starting controller and telemetry listener...")
        self.call_after_refresh(self._start_backend)

    def on_unmount(self):
        # Detach our log handler before tearing down: backend shutdown emits
        # log records, and routing those into the unmounted widgets raises.
        self._tearing_down = True
        if self._status_timer is not None:
            self._status_timer.stop()
            self._status_timer = None
        root = logging.getLogger()
        for h in list(root.handlers):
            if isinstance(h, _LogHandler):
                root.removeHandler(h)
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        if self._listener_cm:
            self._listener_cm.__exit__(None, None, None)
        if self._ds:
            self._ds.close()

    def _start_backend(self):
        s = self.settings
        try:
            # MARK: resync prefs - user may have switched profile before this deferred call ran
            preferences.load(s)
            dsx_running = dsx_module.is_dsx_running()
            use_dsx = dsx_running or s.enable_dsx
            self._ds = dualsense.DualSense(
                startup_pulse_force=s.startup_pulse_force,
                enable_startup_pulse=s.enable_startup_pulse and not use_dsx,
                reconnect_interval_s=s.reconnect_interval_s,
                enable_reconnect=s.enable_reconnect,
                controller_lock_serial=s.controller_lock_serial,
            )
            if use_dsx:
                if dsx_running:
                    log.info("DSX auto-detected as running")
                port = dsx_module.autodetect_port() if s.dsx_autodetect_port else s.dsx_port
                sender = dsx_module.DSXSender(s.dsx_host, port, s.dsx_controller_index)
                if sender.open():
                    self._dsx = sender
                else:
                    log.error("DSX sender could not open — falling back to HID output")
                    self.query_one("#status", Static).update(
                        t("[bold red]DSX open failed — HID fallback[/]")
                    )
            if not self._dsx:
                self._ds.open()
            self._listener_cm = udplistener.UDPListener(s.udp_host, s.udp_port, s.udp_timeout)
            self._listener = self._listener_cm.__enter__()
            log.info("Listening on %s:%d", s.udp_host, s.udp_port)
            log.info("In game: HUD & Gameplay -> Data Out: ON, IP %s, Port %d", s.udp_host, s.udp_port)
            if self._dsx:
                log.info("DSX mode active — sending triggers to %s:%d", self._dsx.host, self._dsx.port)
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
        except OSError as exc:
            # MARK: friendly UDP bind error - usually port in use
            log.exception("UDP bind failed on %s:%d", s.udp_host, s.udp_port)
            msg = t("UDP port {port} is in use. Close the other listener or change the port in the System tab.").format(port=s.udp_port)
            self.query_one("#status", Static).update(msg)
        except Exception as exc:
            log.exception("Backend startup failed")
            self.query_one("#status", Static).update(t("Backend failed: {error}").format(error=exc))

    def _run_loop(self):
        try:
            loop.run(self._ds, self._listener, self.settings, stop_event=self._stop, dsx=self._dsx)
        except Exception:
            # An unexpected error here would otherwise kill the backend thread
            log.exception("Telemetry loop crashed")
        finally:
            if self._dsx:
                self._dsx.close()
                self._dsx = None
            if not self._stop.is_set():
                self.call_from_thread(self.exit)

    @staticmethod
    def _open_url(url: str) -> None:
        # webbrowser.open() can block while a browser cold-starts
        threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()

    def on_click(self, event) -> None:
        widget = getattr(event, "widget", None)
        if widget is not None and widget.id == "version":
            self._open_url(self.CHANGELOG_URL)

    # --- topbar / logs bridge -----------------------------------------------

    def refresh_status(self):
        if self._dsx is not None:
            state = f"[bold green]{t('active')}[/] (DSX)"
        else:
            connected = bool(self._ds and self._ds.connected)
            state = f"[bold green]{t('connected')}[/]" if connected else f"[bold red]{t('waiting')}[/]"
        self.query_one("#status", Static).update(f"DualSense: {state}")

    def refresh_profile(self):
        """Update the active profile label. Cheap path is called only on profile
        mutations / app mount — avoids hitting disk on the per-second timer."""
        try:
            active = profiles.load_store().get("active") or t("(none)")
        except Exception:
            active = t("(none)")
        self.query_one("#profile", Static).update(t("Profile: {name}").format(name=active))

    def _logs_tab(self) -> LogsTab | None:
        try:
            return self.query_one(LogsTab)
        except Exception:
            return None

    def write_log(self, msg: str) -> None:
        tab = self._logs_tab()
        if tab:
            tab.write(msg)

    # --- shared helpers used by tabs ----------------------------------------

    def refresh_setting_widgets(self) -> None:
        """Called by tabs after profile load / settings reset."""
        # MARK: guard programmatic Switch/Input writes so tab handlers skip save churn
        self._refreshing = True
        try:
            for sw in self.query(Switch):
                if sw.id and hasattr(self.settings, sw.id):
                    sw.value = getattr(self.settings, sw.id)
            for inp in self.query(Input):
                if inp.id and inp.id.startswith("set-"):
                    attr = inp.id[4:]
                    if hasattr(self.settings, attr):
                        inp.value = str(getattr(self.settings, attr))
            for sld in self.query(RangeSlider):
                if sld.id and sld.id.startswith("slider-"):
                    attr = sld.id[len("slider-"):]
                    if hasattr(self.settings, attr):
                        sld.value = float(getattr(self.settings, attr))
        finally:
            self._refreshing = False

    def haptic(self, on: bool) -> None:
        if self._ds and self._ds.connected:
            threading.Thread(target=self._do_haptic, args=(on,), daemon=True).start()

    def _do_haptic(self, on: bool) -> None:
        amp = HAPTIC_AMP_ON if on else HAPTIC_AMP_OFF
        v = vibration(HAPTIC_FREQ_HZ, amp)
        self._ds.set(v, v)
        time.sleep(HAPTIC_DURATION_S)
        self._ds.set(off(), off())

    # --- bottombar / bindings -----------------------------------------------

    def action_sponsor(self):
        self._open_url(self.SPONSOR_URL)
        log.info("Opened sponsor page: %s", self.SPONSOR_URL)

    def action_changelog(self):
        self._open_url(self.CHANGELOG_URL)
        log.info("Opened changelog: %s", self.CHANGELOG_URL)

    def on_button_pressed(self, event: Button.Pressed):
        bid = event.button.id
        if bid == "bb-quit":
            self.exit()
        elif bid == "bb-sponsor":
            self.action_sponsor()
        elif bid == "bb-changelog":
            self.action_changelog()
