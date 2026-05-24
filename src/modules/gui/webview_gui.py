"""pywebview GUI — true glassmorphism via macOS WKWebView (WebKit).

Python-JS bridge: JS calls window.pywebview.api.*  →  API class methods.
Python pushes updates: window.evaluate_js('__fhds.onXxx({...})')
"""
import base64
import dataclasses
import json
import logging
import os
import queue
import sys
import threading
import time
import webbrowser
from pathlib import Path

from lang import set_language, t
from modules import dualsense, forzahorizon, loop
from modules.config import paths, preferences, profiles
from modules.config.preferences import _version
from modules.config.settings import Settings
from modules.dualsense.main import _enumerate_dualsenses, _is_bluetooth, identify_pulse

log = logging.getLogger("fhds")

SPONSOR_URL   = "https://github.com/sponsors/HamzaYslmn"
CHANGELOG_URL = "https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python/releases/latest"
SOURCE_URL    = "https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python"

# ── Settings schema ────────────────────────────────────────────────────────────

SETTINGS_SCHEMA = [
    {"section": "Pedal dead zones", "fields": [
        {"key": "accel_deadzone",  "label": "Gas trigger dead zone",  "type": "int", "min": 0, "max": 255},
        {"key": "brake_deadzone",  "label": "Brake trigger dead zone", "type": "int", "min": 0, "max": 255},
    ]},
    {"section": "Left trigger — Brake force", "fields": [
        {"key": "brake_baseline_force", "label": "Resting stiffness",       "type": "int",   "min": 0,   "max": 255},
        {"key": "brake_max_force",      "label": "Hard-press stiffness",    "type": "int",   "min": 0,   "max": 255},
        {"key": "brake_curve",          "label": "Stiffness curve shape",   "type": "float", "min": 0.1, "max": 20.0},
        {"key": "handbrake_bonus",      "label": "Handbrake extra stiffness","type": "int",   "min": 0,   "max": 255},
    ]},
    {"section": "Left trigger — Static wall", "fields": [
        {"key": "brake_static_wall_at",    "label": "Wall position", "type": "int", "min": 0, "max": 255},
        {"key": "brake_static_wall_force", "label": "Wall hardness", "type": "int", "min": 0, "max": 255},
    ]},
    {"section": "Right trigger — Gas force", "fields": [
        {"key": "throttle_baseline_force", "label": "Resting stiffness",    "type": "int",   "min": 0,   "max": 255},
        {"key": "throttle_max_force",      "label": "Hard-press stiffness", "type": "int",   "min": 0,   "max": 255},
        {"key": "throttle_curve",          "label": "Curve shape",          "type": "float", "min": 0.1, "max": 20.0},
    ]},
    {"section": "ABS (anti-lock brake) rumble", "fields": [
        {"key": "abs_brake_threshold",        "label": "Min brake pressure",  "type": "int",   "min": 0,   "max": 255},
        {"key": "abs_min_speed_kmh",          "label": "Min speed (km/h)",    "type": "float", "min": 0,   "max": 500},
        {"key": "abs_slip_ratio_threshold",   "label": "Wheel slip sensitivity","type": "float","min": 0,  "max": 10},
        {"key": "abs_combined_slip_threshold","label": "Tyre grip sensitivity","type": "float","min": 0,   "max": 10},
        {"key": "abs_freq",                   "label": "Rumble speed (Hz)",   "type": "int",   "min": 0,   "max": 255},
        {"key": "abs_amp",                    "label": "Rumble strength",     "type": "int",   "min": 0,   "max": 255},
    ]},
    {"section": "Redline (rev limiter) buzz", "fields": [
        {"key": "rev_limit_ratio",   "label": "Trigger near redline at", "type": "float", "min": 0,   "max": 1},
        {"key": "rev_limit_freq",    "label": "Buzz speed (Hz)",         "type": "int",   "min": 0,   "max": 255},
        {"key": "rev_limit_amp",     "label": "Buzz strength",           "type": "int",   "min": 0,   "max": 255},
        {"key": "rev_limit_hold_ms", "label": "Hold time (ms)",          "type": "float", "min": 0,   "max": 1000},
    ]},
    {"section": "Wheelspin buzz", "fields": [
        {"key": "wheelspin_amp", "label": "Buzz strength", "type": "int", "min": 0, "max": 255},
    ]},
    {"section": "Idle buzz", "fields": [
        {"key": "idle_amp_high", "label": "Idle strength", "type": "int", "min": 0, "max": 255},
    ]},
    {"section": "Gear shift thump", "fields": [
        {"key": "gear_shift_freq",        "label": "Thump speed (Hz)", "type": "int",   "min": 0, "max": 255},
        {"key": "gear_shift_amp",         "label": "Thump strength",   "type": "int",   "min": 0, "max": 255},
        {"key": "gear_shift_duration_ms", "label": "Thump length (ms)","type": "float", "min": 0, "max": 2000},
    ]},
]

SYSTEM_SCHEMA = [
    {"section": "Telemetry", "fields": [
        {"key": "udp_host", "label": "Bind address", "type": "str",
         "hint": "127.0.0.1 = local only · 0.0.0.0 = network / Moonlight"},
        {"key": "udp_port", "label": "UDP port", "type": "int", "min": 1, "max": 65535,
         "hint": "Match the port in Forza: HUD & Gameplay → Data Out"},
    ]},
    {"section": "Startup", "fields": [
        {"key": "enable_startup_pulse",  "label": "Startup vibration",  "type": "bool"},
        {"key": "startup_pulse_force",   "label": "Vibration strength", "type": "int", "min": 0, "max": 255},
    ]},
    {"section": "Auto-reconnect", "fields": [
        {"key": "enable_reconnect",       "label": "Auto-reconnect",          "type": "bool"},
        {"key": "reconnect_interval_s",   "label": "Reconnect interval (s)",  "type": "float", "min": 0.1, "max": 60},
    ]},
    {"section": "Game detection", "fields": [
        {"key": "exit_on_game_close",   "label": "Exit when game closes",     "type": "bool"},
        {"key": "game_poll_interval_s", "label": "Game-check interval (s)",   "type": "float", "min": 0.1, "max": 60},
    ]},
    {"section": "Moonlight / streaming mode", "fields": [
        {"key": "moonlight_mode", "label": "Moonlight mode (write-only)", "type": "bool",
         "hint": "Fixes controller conflict when streaming via Moonlight. Skips reading from the controller so FH DualSense does not compete with Moonlight for HID input reports."},
    ]},
]


# ── Log handler ────────────────────────────────────────────────────────────────

class _BufHandler(logging.Handler):
    def __init__(self, buf: list, lock: threading.Lock):
        super().__init__()
        self._buf = buf
        self._lock = lock

    def emit(self, record):
        try:
            msg = self.format(record)
            with self._lock:
                self._buf.append({"level": record.levelname, "msg": msg})
                if len(self._buf) > 3000:
                    del self._buf[:500]
        except Exception:
            pass


# ── JS API (exposed to JavaScript) ─────────────────────────────────────────────

class API:
    def __init__(self, gui: "WebViewGUI"):
        self._g = gui

    # -- settings --

    def get_settings(self):
        try:
            return dataclasses.asdict(self._g.settings)
        except Exception:
            s = self._g.settings
            return {f.name: getattr(s, f.name) for f in dataclasses.fields(s)}

    def get_schema(self):
        return {"settings": SETTINGS_SCHEMA, "system": SYSTEM_SCHEMA}

    def save_setting(self, key, value):
        s = self._g.settings
        if not hasattr(s, key):
            return {"ok": False, "error": "unknown key"}
        current = getattr(s, key)
        try:
            if isinstance(current, bool):
                value = bool(value)
            elif isinstance(current, int):
                value = int(float(value))
            elif isinstance(current, float):
                value = float(value)
            else:
                value = str(value)
        except (ValueError, TypeError) as e:
            return {"ok": False, "error": str(e)}
        setattr(s, key, value)
        preferences.save(s)
        self._g._push_live(key, value)
        return {"ok": True}

    def reset_settings(self):
        preferences.reset(self._g.settings)
        return self.get_settings()

    # -- session --

    def start_session(self):
        if self._g._session_running:
            return {"ok": False, "error": "already running"}
        threading.Thread(target=self._g._start_session, daemon=True).start()
        return {"ok": True}

    def stop_session(self):
        if not self._g._session_running:
            return {"ok": False, "error": "not running"}
        threading.Thread(target=self._g._stop_session, daemon=True).start()
        return {"ok": True}

    def get_status(self):
        return self._g._status_dict()

    # -- logs --

    def get_logs(self, count: int = 300):
        with self._g._log_lock:
            return self._g._log_buf[-int(count):]

    def clear_logs(self):
        with self._g._log_lock:
            self._g._log_buf.clear()
        return {"ok": True}

    # -- profiles --

    def get_profiles(self):
        try:
            store = profiles.load_store()
            return {"active": store.get("active", ""), "list": store.get("profiles", {})}
        except Exception as e:
            return {"active": "", "list": {}, "error": str(e)}

    def load_profile(self, name: str):
        try:
            profiles.apply(name, self._g.settings)
            preferences.save(self._g.settings)
            return {"ok": True, "settings": self.get_settings()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def save_profile(self, name: str):
        try:
            profiles.save_current(name, self._g.settings)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_profile(self, name: str):
        try:
            profiles.delete(name)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # -- controller --

    def get_controllers(self):
        try:
            devs = _enumerate_dualsenses()
            result = []
            for d in devs:
                result.append({
                    "serial": d.get("serial_number", ""),
                    "transport": "BT" if _is_bluetooth(d) else "USB",
                    "path": (d.get("path") or b"").decode(errors="replace"),
                })
            return result
        except Exception:
            return []

    def identify_controller(self, serial: str):
        try:
            devs = _enumerate_dualsenses()
            info = next((d for d in devs if d.get("serial_number") == serial), None)
            if info:
                threading.Thread(target=identify_pulse, args=(info,),
                                 kwargs={"force": self._g.settings.startup_pulse_force},
                                 daemon=True).start()
            return {"ok": bool(info)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_controller_lock(self, serial: str):
        self._g.settings.controller_lock_serial = serial
        preferences.save(self._g.settings)
        ds = self._g._ds
        if ds:
            ds.set_selection(serial)
            if serial and serial != getattr(ds, "dev_serial", ""):
                ds.force_reconnect()
        return {"ok": True}

    # -- background --

    def browse_background(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes("-topmost", True)
            path = filedialog.askopenfilename(
                title="Choose a background image",
                filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp"), ("All files", "*.*")],
            )
            root.destroy()
        except Exception:
            path = ""
        if path and os.path.isfile(path):
            self._g.settings.background_image_path = path
            preferences.save(self._g.settings)
            uri = _image_to_uri(path)
            return {"ok": True, "uri": uri, "path": path}
        return {"ok": False, "uri": ""}

    def clear_background(self):
        self._g.settings.background_image_path = ""
        preferences.save(self._g.settings)
        default_uri = _image_to_uri(str(paths.DEFAULT_BG))
        return {"ok": True, "uri": default_uri}

    def get_version(self):
        return _version() or "?"

    # -- external --

    def open_url(self, url: str):
        threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()
        return {"ok": True}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _image_to_uri(path: str) -> str:
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = Path(path).suffix.lower().lstrip(".")
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png",
                "webp": "webp", "bmp": "bmp"}.get(ext, "jpeg")
        return f"data:image/{mime};base64,{data}"
    except Exception:
        return ""


# ── Main GUI class ────────────────────────────────────────────────────────────

class WebViewGUI:
    def __init__(self, settings: Settings):
        self.settings = settings
        set_language(settings.language)

        self._session_running = False
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._ds: dualsense.DualSense | None = None
        self._listener_cm = None
        self._listener = None
        self._tearing_down = False

        self._log_buf: list = []
        self._log_lock = threading.Lock()
        self._window = None

        self._install_log_handler()

    def run(self):
        import webview

        bg_path = self.settings.background_image_path or str(paths.DEFAULT_BG)
        if not os.path.isfile(bg_path):
            bg_path = str(paths.DEFAULT_BG)
        bg_uri = _image_to_uri(bg_path)

        html_file = Path(__file__).parent / "web" / "index.html"
        with open(html_file, encoding="utf-8") as f:
            html = f.read()
        html = html.replace("__BG_URI__", bg_uri)
        html = html.replace("__VERSION__", _version() or "?")
        html = html.replace('"__SETTINGS_SCHEMA__"', json.dumps(SETTINGS_SCHEMA))
        html = html.replace('"__SYSTEM_SCHEMA__"', json.dumps(SYSTEM_SCHEMA))
        html = html.replace("__CHANGELOG__", CHANGELOG_URL)
        html = html.replace("__SPONSOR__", SPONSOR_URL)
        html = html.replace("__SOURCE__", SOURCE_URL)

        api = API(self)
        self._window = webview.create_window(
            "FH DualSense",
            html=html,
            js_api=api,
            width=1100,
            height=720,
            min_size=(820, 540),
            background_color="#07080e",
            frameless=False,
        )
        self._window.events.closed += self._on_closed

        webview.start(self._on_started, debug=False)

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def _on_started(self):
        time.sleep(0.3)   # let JS initialise
        self._start_session()
        threading.Thread(target=self._push_loop, daemon=True).start()

    def _on_closed(self):
        self._tearing_down = True
        self._stop_session()

    def _push_loop(self):
        """Push status + buffered logs to JS every 300 ms."""
        while not self._tearing_down:
            try:
                self._eval("__fhds.onStatus(" + json.dumps(self._status_dict()) + ")")
                with self._log_lock:
                    pending = self._log_buf[:]
                    self._log_buf.clear()
                if pending:
                    self._eval("__fhds.appendLogs(" + json.dumps(pending) + ")")
            except Exception:
                pass
            time.sleep(0.3)

    def _eval(self, js: str):
        if self._window:
            try:
                self._window.evaluate_js(js)
            except Exception:
                pass

    # ── Session ───────────────────────────────────────────────────────────────

    def _start_session(self):
        if self._session_running:
            return
        self._stop = threading.Event()
        s = self.settings
        try:
            preferences.load(s)
            self._ds = dualsense.DualSense(
                startup_pulse_force=s.startup_pulse_force,
                enable_startup_pulse=s.enable_startup_pulse,
                reconnect_interval_s=s.reconnect_interval_s,
                enable_reconnect=s.enable_reconnect,
                controller_lock_serial=s.controller_lock_serial,
                disable_input_watchdog=s.moonlight_mode,
            )
            self._ds.open()
            self._listener_cm = forzahorizon.UDPListener(s.udp_host, s.udp_port, s.udp_timeout)
            self._listener = self._listener_cm.__enter__()
            log.info("Listening on %s:%d | Start driving in Forza", s.udp_host, s.udp_port)
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
            self._session_running = True
        except OSError:
            log.exception("UDP bind failed on %s:%d", s.udp_host, s.udp_port)
        except Exception:
            log.exception("Session start failed")

    def _stop_session(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=3.0)
            self._thread = None
        if self._listener_cm:
            try:
                self._listener_cm.__exit__(None, None, None)
            except Exception:
                pass
            self._listener_cm = None
            self._listener = None
        if self._ds:
            try:
                self._ds.close()
            except Exception:
                pass
            self._ds = None
        self._session_running = False

    def _run_loop(self):
        try:
            loop.run(self._ds, self._listener, self.settings, stop_event=self._stop)
        except Exception:
            log.exception("Telemetry loop crashed")
        finally:
            if not self._stop.is_set() and not self._tearing_down:
                self._session_running = False
                log.info("Backend exited — press Start to restart.")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _status_dict(self) -> dict:
        ds = self._ds
        if ds and getattr(ds, "persistent", False):
            state, label = "connected", "connected · latched"
        elif ds and ds.connected:
            state, label = "connected", "connected"
        elif self._session_running:
            state, label = "waiting", "waiting for controller"
        else:
            state, label = "stopped", "stopped"
        return {
            "state": state,
            "label": label,
            "running": self._session_running,
            "serial": getattr(ds, "dev_serial", "") or "",
        }

    def _push_live(self, key: str, value):
        ds = self._ds
        if ds is None:
            return
        if key == "enable_reconnect":
            ds.set_reconnect_enabled(value)
        elif key == "reconnect_interval_s":
            ds.set_reconnect_interval(value)

    def _install_log_handler(self):
        root = logging.getLogger()
        root.handlers.clear()
        h = _BufHandler(self._log_buf, self._log_lock)
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                          datefmt="%H:%M:%S"))
        root.addHandler(h)
        root.setLevel(logging.DEBUG)
