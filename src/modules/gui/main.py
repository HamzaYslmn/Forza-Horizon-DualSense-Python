"""CustomTkinter GUI app.

Layout:
  +-----------------------------------------------------------+
  |  header  [* status]  [Profile: name]            v1.2.3   |
  +---------+-------------------------------------------------+
  | sidebar |  main content (active tab frame)                |
  |  nav    |                                                 |
  | items   |                                                 |
  |         |                                                 |
  | footer  |                                                 |
  | links   |                                                 |
  +---------+-------------------------------------------------+

Threading: backend runs in a worker thread; logs are queued and drained on
the Tk main thread via root.after. Tk widgets are never touched off-thread.
"""
import logging
import os
import queue
import sys
import threading
import time
import tkinter as tk
import webbrowser

import customtkinter as ctk

from lang import set_language, t
from modules import dualsense, forzahorizon, loop
from modules.config import preferences, profiles
from modules.config.preferences import _version
from modules.dualsense.adaptive_trigger import off, vibrate

from . import theme as T
from . import widgets as W
from .tray import TrayController
from .controls_tab import ControlsTab
from .lang_tab import LangTab
from .logs_tab import DEFAULT_LOG_LEVEL, LogsTab
from .profiles_tab import ProfilesTab
from .settings_tab import SettingsTab
from .system_tab import SystemTab

log = logging.getLogger("fhds")

HAPTIC_FREQ_HZ = 40
HAPTIC_AMP_ON = 200
HAPTIC_AMP_OFF = 120
HAPTIC_DURATION_S = 0.10

SPONSOR_URL = "https://github.com/sponsors/HamzaYslmn"
CHANGELOG_URL = "https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python/releases/latest"

NAV_ITEMS = ("Controls", "Profiles", "Settings", "System", "Language", "Logs")


class _QueueLogHandler(logging.Handler):
    """Worker threads push records here; the Tk loop drains them."""

    def __init__(self, q: queue.Queue):
        super().__init__()
        self._q = q

    def emit(self, record):
        try:
            self._q.put_nowait((record.levelname, self.format(record)))
        except queue.Full:
            pass


class TriggerGUI:
    def __init__(self, settings):
        self.settings = settings
        set_language(settings.language)

        # Runtime state
        self._stop = threading.Event()
        self._thread = None
        self._ds = None
        self._listener_cm = None
        self._listener = None
        self._tearing_down = False
        self._refreshing = False
        self._refresh_callbacks: list = []
        self._log_queue: queue.Queue = queue.Queue(maxsize=4000)

        # Theme + DPI
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self._apply_theme()
        # Make Windows treat us as Per-Monitor v2 BEFORE Tk is created so
        # CTk's auto-DPI reads the right monitor DPI.
        self._enable_process_dpi_awareness()
        self.scale = 1.0

        # Window
        self.root = ctk.CTk()
        self.root.title("FH DualSense")
        self._set_window_icon()
        self._center_window()
        self._tray = TrayController(self.root, on_show=self._show_window, on_quit=self._quit)
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
        self.root.bind("<Unmap>", self._on_unmap)

        # Layout
        self._build_header()
        self._build_body()

        # Final wiring
        self._install_log_handler()
        self._refresh_status()
        self._refresh_profile()

    # MARK: theme / dpi -----------------------------------------------------

    @staticmethod
    def _apply_theme():
        from customtkinter import ThemeManager
        th = ThemeManager.theme
        th["CTk"]["fg_color"] = list(T.BG_MAIN)
        th["CTkToplevel"]["fg_color"] = list(T.BG_MAIN)
        th["CTkFrame"]["fg_color"] = list(T.BG_PANEL)
        th["CTkFrame"]["top_fg_color"] = list(T.BG_HOVER)
        th["CTkFrame"]["border_color"] = list(T.BORDER)
        th["CTkButton"]["fg_color"] = [T.ACCENT, T.ACCENT]
        th["CTkButton"]["hover_color"] = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkSwitch"]["progress_color"] = [T.ACCENT, T.ACCENT]
        th["CTkSlider"]["progress_color"] = [T.ACCENT, T.ACCENT]
        th["CTkSlider"]["button_color"] = [T.ACCENT, T.ACCENT]
        th["CTkSlider"]["button_hover_color"] = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkSegmentedButton"]["selected_color"] = [T.ACCENT, T.ACCENT]
        th["CTkSegmentedButton"]["selected_hover_color"] = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkProgressBar"]["progress_color"] = [T.ACCENT, T.ACCENT]
        th["CTkCheckBox"]["fg_color"] = [T.ACCENT, T.ACCENT]
        th["CTkCheckBox"]["hover_color"] = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkRadioButton"]["fg_color"] = [T.ACCENT, T.ACCENT]
        th["CTkRadioButton"]["hover_color"] = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkEntry"]["border_color"] = list(T.BORDER)
        th["CTkEntry"]["fg_color"] = list(T.BG_INPUT)
        th["CTkOptionMenu"]["fg_color"] = [T.ACCENT, T.ACCENT]
        th["CTkOptionMenu"]["button_color"] = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkOptionMenu"]["button_hover_color"] = [T.ACCENT_HOVER, T.ACCENT_HOVER]

    @staticmethod
    def _enable_process_dpi_awareness():
        if not sys.platform.startswith("win"):
            return
        try:
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass
        except Exception:
            pass

    def px(self, n: int) -> int:
        return max(1, int(round(n * self.scale)))

    def font_size(self, base: int) -> int:
        return max(8, int(round(base * self.scale)))

    def toast(self, message: str, ms: int = 2500):
        """Show a transient banner at the top of the window. Cross-platform."""
        top = ctk.CTkToplevel(self.root)
        top.overrideredirect(True)
        try:
            top.attributes("-topmost", True)
            top.attributes("-alpha", 0.95)
        except tk.TclError:
            pass
        lbl = ctk.CTkLabel(
            top, text=message,
            fg_color=T.ACCENT, text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=T.FS_BODY, weight="bold"),
        )
        lbl.pack(ipadx=18, ipady=10)
        top.update_idletasks()
        rx = self.root.winfo_rootx()
        ry = self.root.winfo_rooty()
        rw = self.root.winfo_width()
        tw = top.winfo_width()
        top.geometry(f"+{rx + (rw - tw) // 2}+{ry + 24}")
        top.after(ms, top.destroy)

    def _set_window_icon(self):
        from modules.config import paths
        ico = paths.ICON_ICO
        png = paths.ICON_PNG
        # iconphoto with a large PNG gives Windows a high-DPI source it can
        # downscale crisply for the taskbar; iconbitmap alone tends to pick
        # the 32x32 entry of the .ico for the taskbar (Tk limitation).
        if png.exists():
            try:
                self._icon_img = tk.PhotoImage(file=str(png))
                self.root.iconphoto(True, self._icon_img)
            except Exception:
                pass
        if sys.platform.startswith("win") and ico.exists():
            try:
                self.root.iconbitmap(default=str(ico))
            except Exception:
                pass

    def _center_window(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        # CTk scales width/height in geometry strings by the monitor DPI, but
        # leaves +x+y position unscaled. So: w,h in logical units, x,y in
        # physical pixels.
        try:
            from customtkinter import ScalingTracker
            dpi = float(ScalingTracker.get_window_dpi_scaling(self.root)) or 1.0
        except Exception:
            dpi = 1.0
        sw_u = sw / dpi
        sh_u = sh / dpi
        base_w, base_h = 960, 660
        w_u = int(min(base_w, sw_u * 0.85))
        h_u = int(min(base_h, sh_u * 0.85))
        w_phys = int(w_u * dpi)
        h_phys = int(h_u * dpi)
        x = max(0, (sw - w_phys) // 2)
        y = max(0, (sh - h_phys) // 2 - int(sh * 0.04))
        self.root.geometry(f"{w_u}x{h_u}+{x}+{y}")
        self.root.minsize(640, 440)

    # MARK: layout ----------------------------------------------------------

    def _build_header(self):
        bar = ctk.CTkFrame(self.root, height=T.HEADER_H, corner_radius=0,
                           fg_color=T.BG_PANEL)
        bar.pack(side="top", fill="x")
        bar.grid_columnconfigure(0, weight=1, uniform="hdr")
        bar.grid_columnconfigure(1, weight=0)
        bar.grid_columnconfigure(2, weight=1, uniform="hdr")
        bar.grid_propagate(False)

        self.profile_pill = W.Pill(bar, label="-", prefix=t("Profile"))
        self.profile_pill.grid(row=0, column=0, padx=(T.PAD_MD, T.PAD_SM),
                               pady=T.PAD_SM, sticky="w")

        self.status_pill = W.Pill(bar, label=t("waiting"),
                                  prefix="DualSense", dot_color=T.RED)
        self.status_pill.grid(row=0, column=1, padx=T.PAD_SM, pady=T.PAD_SM)

        self.lbl_version = ctk.CTkLabel(
            bar, text=f"v{_version() or '?'}",
            text_color=T.TEXT_FAINT, cursor="hand2",
            font=ctk.CTkFont(size=T.FS_TINY),
        )
        self.lbl_version.grid(row=0, column=2, padx=(T.PAD_SM, T.PAD_MD),
                              pady=T.PAD_SM, sticky="e")
        self.lbl_version.bind("<Button-1>", lambda _e: self._open_url(CHANGELOG_URL))

        ctk.CTkFrame(self.root, height=1, corner_radius=0,
                     fg_color=T.BORDER).pack(side="top", fill="x")

    def _build_body(self):
        body = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        body.pack(side="top", fill="both", expand=True)

        sidebar = ctk.CTkFrame(body, width=T.SIDEBAR_W, corner_radius=0,
                               fg_color=T.BG_DEEP)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        nav_box = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_box.pack(side="top", fill="x", pady=(T.PAD_MD, 0))

        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        for key in NAV_ITEMS:
            btn = ctk.CTkButton(
                nav_box, text=f"  {T.ICON[key]}   {t(key)}", anchor="w",
                height=36, corner_radius=6,
                fg_color="transparent", hover_color=T.BG_HOVER,
                text_color=T.TEXT_MUTED,
                font=ctk.CTkFont(size=T.FS_BODY),
                command=lambda k=key: self._select_nav(k),
            )
            btn.pack(side="top", fill="x", padx=T.PAD_SM, pady=2)
            self._nav_buttons[key] = btn

        sfooter = ctk.CTkFrame(sidebar, fg_color="transparent")
        sfooter.pack(side="bottom", fill="x", padx=T.PAD_SM, pady=T.PAD_MD)

        sponsor_btn = ctk.CTkButton(
            sfooter,
            text=f"{T.ICON['heart']}  {t('Sponsor')}",
            height=34, corner_radius=8,
            fg_color=T.PINK, hover_color="#e94f8e",
            text_color="#ffffff",
            font=ctk.CTkFont(size=T.FS_BODY, weight="bold"),
            command=lambda: self._open_url(SPONSOR_URL),
        )
        sponsor_btn.pack(side="top", fill="x", pady=(0, T.PAD_SM))

        changelog_btn = ctk.CTkButton(
            sfooter,
            text=t("Changelog"),
            height=26, corner_radius=6,
            fg_color="transparent", hover_color=T.BG_HOVER,
            text_color=T.TEXT_FAINT,
            font=ctk.CTkFont(size=T.FS_SMALL),
            command=lambda: self._open_url(CHANGELOG_URL),
        )
        changelog_btn.pack(side="top", fill="x")

        self._content = ctk.CTkFrame(body, corner_radius=0, fg_color=T.BG_MAIN)
        self._content.pack(side="left", fill="both", expand=True)

        self.controls_tab = ControlsTab(self._content, self)
        self.profiles_tab = ProfilesTab(self._content, self)
        self.settings_tab = SettingsTab(self._content, self)
        self.system_tab = SystemTab(self._content, self)
        self.lang_tab = LangTab(self._content, self)
        self.logs_tab = LogsTab(self._content, self)
        self._tab_frames = {
            "Controls": self.controls_tab,
            "Profiles": self.profiles_tab,
            "Settings": self.settings_tab,
            "System":   self.system_tab,
            "Language": self.lang_tab,
            "Logs":     self.logs_tab,
        }
        self._active_nav: str | None = None
        self._select_nav("Controls")

    def _select_nav(self, key: str):
        if key == self._active_nav:
            return
        if self._active_nav:
            self._tab_frames[self._active_nav].pack_forget()
            prev = self._nav_buttons[self._active_nav]
            prev.configure(fg_color="transparent", text_color=T.TEXT_MUTED)
        self._tab_frames[key].pack(fill="both", expand=True,
                                   padx=T.PAD_LG, pady=T.PAD_LG)
        btn = self._nav_buttons[key]
        btn.configure(fg_color=T.BG_ACTIVE, text_color=T.TEXT)
        self._active_nav = key

    # MARK: lifecycle -------------------------------------------------------

    def run(self):
        self.root.after(0, self._start_backend)
        self.root.after(1000, self._tick_status)
        self.root.after(100, self._drain_logs)
        try:
            self.root.mainloop()
        finally:
            self._teardown()

    def _on_close(self):
        # Kept for backend-triggered shutdown (e.g. exit-detection).
        self._quit()

    def _hide_to_tray(self):
        if not self._tray.start():
            return
        try:
            self.root.withdraw()
        except tk.TclError:
            pass

    def _on_unmap(self, event):
        if event.widget is not self.root:
            return
        try:
            if self.root.state() == "iconic":
                self._hide_to_tray()
        except tk.TclError:
            pass

    def _show_window(self):
        try:
            self.root.deiconify()
            self.root.state("normal")
            self.root.lift()
            self.root.focus_force()
        except tk.TclError:
            pass

    def _quit(self):
        try:
            self._tray.stop()
        except Exception:
            pass
        self._teardown()
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def _teardown(self):
        if self._tearing_down:
            return
        self._tearing_down = True
        root = logging.getLogger()
        for h in list(root.handlers):
            if isinstance(h, _QueueLogHandler):
                root.removeHandler(h)
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        if self._listener_cm:
            try:
                self._listener_cm.__exit__(None, None, None)
            except Exception:
                pass
        if self._ds:
            try:
                self._ds.close()
            except Exception:
                pass

    def _install_log_handler(self):
        root = logging.getLogger()
        root.handlers.clear()
        h = _QueueLogHandler(self._log_queue)
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                          datefmt="%H:%M:%S"))
        root.addHandler(h)
        root.setLevel(getattr(logging, DEFAULT_LOG_LEVEL))

    def _drain_logs(self):
        if self._tearing_down:
            return
        for _ in range(200):
            try:
                level, msg = self._log_queue.get_nowait()
            except queue.Empty:
                break
            self.logs_tab.write(level, msg)
        self.root.after(100, self._drain_logs)

    def _start_backend(self):
        s = self.settings
        try:
            preferences.load(s)
            self._ds = dualsense.DualSense(
                startup_pulse_force=s.startup_pulse_force,
                enable_startup_pulse=s.enable_startup_pulse,
                reconnect_interval_s=s.reconnect_interval_s,
                enable_reconnect=s.enable_reconnect,
                controller_lock_serial=s.controller_lock_serial,
            )
            self._ds.open()
            self._listener_cm = forzahorizon.UDPListener(s.udp_host, s.udp_port, s.udp_timeout)
            self._listener = self._listener_cm.__enter__()
            log.info("Listening on %s:%d", s.udp_host, s.udp_port)
            log.info("In game: HUD & Gameplay -> Data Out: ON, IP %s, Port %d",
                     s.udp_host, s.udp_port)
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
        except OSError:
            log.exception("UDP bind failed on %s:%d", s.udp_host, s.udp_port)
            self.status_pill.set_label(t("UDP port {port} in use").format(port=s.udp_port))
        except Exception as exc:
            log.exception("Backend startup failed")
            self.status_pill.set_label(t("Backend failed: {error}").format(error=exc))

    def _run_loop(self):
        try:
            loop.run(self._ds, self._listener, self.settings, stop_event=self._stop)
        except Exception:
            log.exception("Telemetry loop crashed")
        finally:
            if not self._stop.is_set():
                try:
                    self.root.after(0, self._on_close)
                except (RuntimeError, tk.TclError):
                    pass

    # MARK: status / profile ------------------------------------------------

    def _tick_status(self):
        if self._tearing_down:
            return
        self._refresh_status()
        self.root.after(1000, self._tick_status)

    def _refresh_status(self):
        ds = self._ds
        if ds and getattr(ds, "persistent", False):
            color, label = T.GREEN, f"{t('connected')} - {t('latched')}"
        elif ds and ds.connected:
            color, label = T.GREEN, t("connected")
        else:
            color, label = T.RED, t("waiting")
        self.status_pill.set_dot_color(color)
        self.status_pill.set_label(label)

    def _refresh_profile(self):
        try:
            active = profiles.load_profiles().get("active") or t("(none)")
        except Exception:
            active = t("(none)")
        self.profile_pill.set_label(active)

    refresh_profile = _refresh_profile
    refresh_status = _refresh_status

    # MARK: shared helpers --------------------------------------------------

    def register_refresh(self, fn):
        self._refresh_callbacks.append(fn)

    def refresh_setting_widgets(self):
        self._refreshing = True
        try:
            for fn in self._refresh_callbacks:
                try:
                    fn()
                except Exception:
                    log.exception("refresh callback failed")
        finally:
            self._refreshing = False

    def haptic(self, on_state: bool):
        if self._ds and self._ds.connected:
            threading.Thread(target=self._do_haptic, args=(on_state,), daemon=True).start()

    def _do_haptic(self, on_state: bool):
        amp = HAPTIC_AMP_ON if on_state else HAPTIC_AMP_OFF
        v = vibrate(HAPTIC_FREQ_HZ, amp)
        self._ds.set(v, v)
        time.sleep(HAPTIC_DURATION_S)
        self._ds.set(off(), off())

    @staticmethod
    def _open_url(url: str):
        threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()
