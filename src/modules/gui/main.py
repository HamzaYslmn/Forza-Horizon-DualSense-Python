"""CustomTkinter GUI — glass-morphism redesign.

Layout:
  ┌──────────────────────────────────────────────────────────┐
  │  header  [logo + app name]    [status pill]   [version]  │
  ├────────────┬─────────────────────────────────────────────┤
  │  sidebar   │  content area (active tab)                  │
  │  nav items │                                             │
  │            │                                             │
  │  [▶ Start] │                                             │
  │  [■ Stop ] │                                             │
  │            │                                             │
  │  [♥ Spon.] │                                             │
  │  [credit]  │                                             │
  └────────────┴─────────────────────────────────────────────┘

Background: PIL-processed image (blurred + darkened) drawn behind all widgets.
Threading: backend runs in a worker thread; logs queued and drained on Tk thread.
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

HAPTIC_FREQ_HZ   = 40
HAPTIC_AMP_ON    = 200
HAPTIC_AMP_OFF   = 120
HAPTIC_DURATION_S = 0.10

SPONSOR_URL   = "https://github.com/sponsors/HamzaYslmn"
CHANGELOG_URL = "https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python/releases/latest"
SOURCE_URL    = "https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python"

NAV_ITEMS = ("Controls", "Profiles", "Settings", "System", "Language", "Logs")

# Background image blur / dim settings
BG_BLUR_RADIUS = 32
BG_BRIGHTNESS  = 0.28   # 0=black  1=original


class _QueueLogHandler(logging.Handler):
    def __init__(self, q: queue.Queue):
        super().__init__()
        self._q = q

    def emit(self, record):
        try:
            self._q.put_nowait((record.levelname, self.format(record)))
        except queue.Full:
            pass


# ── Background image helpers ──────────────────────────────────────────────────

def _make_gradient(w: int, h: int):
    """Generate a dark blue-purple gradient as the default background."""
    from PIL import Image
    img = Image.new("RGB", (max(w, 1), max(h, 1)))
    pixels = img.load()
    for y in range(h):
        t_val = y / max(h - 1, 1)
        r = int(8  + (15 - 8)  * t_val)
        g = int(9  + (10 - 9)  * t_val)
        b = int(20 + (35 - 20) * t_val)
        for x in range(w):
            # Add a subtle radial highlight at top-left
            dist = ((x / w) ** 2 + (y / h) ** 2) ** 0.5
            r2 = min(255, r + int(25 * max(0, 0.6 - dist)))
            b2 = min(255, b + int(40 * max(0, 0.6 - dist)))
            pixels[x, y] = (r2, g, b2)
    return img


def _process_background(path: str, w: int, h: int):
    """Load (or generate), resize, blur, and darken the background image.
    Returns a PIL Image ready to convert to PhotoImage."""
    from PIL import Image, ImageFilter, ImageEnhance
    from modules.config import paths as _paths
    w, h = max(w, 2), max(h, 2)
    # Priority: user custom path → bundled default → gradient
    candidates = [path, str(_paths.DEFAULT_BG)]
    img = None
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            try:
                img = Image.open(candidate).convert("RGB")
                break
            except Exception:
                continue
    if img is None:
        img = _make_gradient(w, h)
    img = img.resize((w, h), Image.LANCZOS)
    img = img.filter(ImageFilter.GaussianBlur(radius=BG_BLUR_RADIUS))
    img = ImageEnhance.Brightness(img).enhance(BG_BRIGHTNESS)
    return img


# ── Main app class ────────────────────────────────────────────────────────────

class TriggerGUI:
    def __init__(self, settings):
        self.settings = settings
        set_language(settings.language)

        # Session state
        self._session_running = False
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._ds: dualsense.DualSense | None = None
        self._listener_cm = None
        self._listener = None
        self._tearing_down = False
        self._refreshing = False
        self._refresh_callbacks: list = []
        self._log_queue: queue.Queue = queue.Queue(maxsize=4000)

        # Background image state
        self._bg_pil = None          # PIL Image (processed, full-size)
        self._bg_photo = None        # tk.PhotoImage reference (keep alive)
        self._bg_path_loaded = ""    # path that produced _bg_pil
        self._bg_resize_job = None   # pending after() call id for debounce

        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self._apply_theme()
        self._enable_process_dpi_awareness()
        self.scale = 1.0

        # Window
        self.root = ctk.CTk()
        self.root.title("FH DualSense")
        self.root.configure(fg_color=T.BG_ROOT)
        self._set_window_icon()
        self._center_window()
        self._tray = TrayController(self.root, on_show=self._show_window,
                                    on_quit=self._quit)
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
        self.root.bind("<Unmap>", self._on_unmap)

        # Background image label (created FIRST so it is behind all other widgets)
        self._bg_label = tk.Label(self.root, bd=0, highlightthickness=0,
                                  bg=T.BG_ROOT)
        self._bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Layout
        self._build_header()
        self._build_body()

        # Final wiring
        self._install_log_handler()
        self._refresh_status()
        self._refresh_profile()

        # Bind resize for background
        self.root.bind("<Configure>", self._on_configure)

    # ── Theme / DPI ───────────────────────────────────────────────────────────

    @staticmethod
    def _apply_theme():
        from customtkinter import ThemeManager
        th = ThemeManager.theme
        th["CTk"]["fg_color"]                             = [T.BG_ROOT, T.BG_ROOT]
        th["CTkToplevel"]["fg_color"]                     = [T.BG_ROOT, T.BG_ROOT]
        th["CTkFrame"]["fg_color"]                        = [T.BG_PANEL, T.BG_PANEL]
        th["CTkFrame"]["top_fg_color"]                    = [T.BG_HOVER, T.BG_HOVER]
        th["CTkFrame"]["border_color"]                    = [T.GLASS_BORDER, T.GLASS_BORDER]
        th["CTkButton"]["fg_color"]                       = [T.ACCENT, T.ACCENT]
        th["CTkButton"]["hover_color"]                    = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkSwitch"]["progress_color"]                 = [T.ACCENT, T.ACCENT]
        th["CTkSlider"]["progress_color"]                 = [T.ACCENT, T.ACCENT]
        th["CTkSlider"]["button_color"]                   = [T.ACCENT, T.ACCENT]
        th["CTkSlider"]["button_hover_color"]             = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkSegmentedButton"]["selected_color"]        = [T.ACCENT, T.ACCENT]
        th["CTkSegmentedButton"]["selected_hover_color"]  = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkProgressBar"]["progress_color"]            = [T.ACCENT, T.ACCENT]
        th["CTkCheckBox"]["fg_color"]                     = [T.ACCENT, T.ACCENT]
        th["CTkCheckBox"]["hover_color"]                  = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkRadioButton"]["fg_color"]                  = [T.ACCENT, T.ACCENT]
        th["CTkRadioButton"]["hover_color"]               = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkEntry"]["border_color"]                    = [T.GLASS_BORDER, T.GLASS_BORDER]
        th["CTkEntry"]["fg_color"]                        = [T.BG_INPUT, T.BG_INPUT]
        th["CTkOptionMenu"]["fg_color"]                   = [T.ACCENT, T.ACCENT]
        th["CTkOptionMenu"]["button_color"]               = [T.ACCENT_HOVER, T.ACCENT_HOVER]
        th["CTkOptionMenu"]["button_hover_color"]         = [T.ACCENT_HOVER, T.ACCENT_HOVER]

    @staticmethod
    def _enable_process_dpi_awareness():
        if not sys.platform.startswith("win"):
            return
        try:
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    def px(self, n: int) -> int:
        return max(1, int(round(n * self.scale)))

    def font_size(self, base: int) -> int:
        return max(8, int(round(base * self.scale)))

    def _set_window_icon(self):
        from modules.config import paths
        ico = paths.ICON_ICO
        png = paths.ICON_PNG
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
        try:
            from customtkinter import ScalingTracker
            dpi = float(ScalingTracker.get_window_dpi_scaling(self.root)) or 1.0
        except Exception:
            dpi = 1.0
        sw_u, sh_u = sw / dpi, sh / dpi
        base_w, base_h = 1060, 700
        w_u = int(min(base_w, sw_u * 0.88))
        h_u = int(min(base_h, sh_u * 0.88))
        w_phys = int(w_u * dpi)
        h_phys = int(h_u * dpi)
        x = max(0, (sw - w_phys) // 2)
        y = max(0, (sh - h_phys) // 2 - int(sh * 0.04))
        self.root.geometry(f"{w_u}x{h_u}+{x}+{y}")
        self.root.minsize(720, 480)

    # ── Background image ──────────────────────────────────────────────────────

    def _on_configure(self, event):
        if event.widget is not self.root:
            return
        # Debounce: wait 120 ms after last resize event before redrawing
        if self._bg_resize_job:
            self.root.after_cancel(self._bg_resize_job)
        self._bg_resize_job = self.root.after(120, self._redraw_background)

    def _redraw_background(self):
        self._bg_resize_job = None
        try:
            from PIL import ImageTk
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            if w < 10 or h < 10:
                return
            path = self.settings.background_image_path or ""
            # Re-process only when the source changed or first time
            if self._bg_pil is None or path != self._bg_path_loaded:
                self._bg_pil = _process_background(path, w, h)
                self._bg_path_loaded = path
            else:
                # Same source — just resize the already-processed image
                from PIL import Image, ImageFilter, ImageEnhance
                if path and os.path.isfile(path):
                    try:
                        raw = Image.open(path).convert("RGB")
                    except Exception:
                        raw = _make_gradient(w, h)
                else:
                    raw = _make_gradient(w, h)
                raw = raw.resize((w, h), Image.LANCZOS)
                raw = raw.filter(ImageFilter.GaussianBlur(radius=BG_BLUR_RADIUS))
                self._bg_pil = ImageEnhance.Brightness(raw).enhance(BG_BRIGHTNESS)
            self._bg_photo = ImageTk.PhotoImage(self._bg_pil)
            self._bg_label.configure(image=self._bg_photo)
            self._update_scroll_bg()
        except Exception as e:
            log.debug("Background render failed: %s", e)

    def reload_background(self):
        """Called by System tab when the user changes the image path."""
        self._bg_pil = None
        self._bg_path_loaded = ""
        self._redraw_background()

    def _update_scroll_bg(self):
        """Draw the full-window blurred image onto each tab's scroll canvas at the
        correct offset so the right background portion shows between cards."""
        if self._bg_photo is None:
            return
        if not hasattr(self, "controls_tab"):
            return
        tabs = [self.controls_tab, self.settings_tab, self.system_tab,
                self.profiles_tab, self.lang_tab, self.logs_tab]
        try:
            rx = self.root.winfo_rootx()
            ry = self.root.winfo_rooty()
        except Exception:
            return
        for tab in tabs:
            scroll = getattr(tab, "_scroll", None)
            if scroll is None:
                continue
            try:
                cv = scroll._parent_canvas
                cx = cv.winfo_rootx() - rx
                cy = cv.winfo_rooty() - ry
                if not getattr(cv, "_fhds_bg_set", False):
                    cv._fhds_bg = cv.create_image(-cx, -cy, anchor="nw", tags="fhds_bg")
                    cv.tag_lower("fhds_bg")
                    cv._fhds_bg_set = True
                else:
                    cv.coords(cv._fhds_bg, -cx, -cy)
                cv.itemconfigure(cv._fhds_bg, image=self._bg_photo)
            except Exception:
                pass

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_header(self):
        bar = ctk.CTkFrame(self.root, height=T.HEADER_H, corner_radius=0,
                           fg_color=T.GLASS_HEADER, border_width=0)
        bar.pack(side="top", fill="x")
        bar.grid_columnconfigure(0, weight=1, uniform="hdr")
        bar.grid_columnconfigure(1, weight=0)
        bar.grid_columnconfigure(2, weight=1, uniform="hdr")
        bar.grid_propagate(False)

        # Left: logo dot + app name
        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.grid(row=0, column=0, padx=(T.PAD_LG, 0), pady=0, sticky="w")
        ctk.CTkLabel(
            left, text="●",
            text_color=T.ACCENT,
            font=ctk.CTkFont(size=10),
        ).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            left, text="FH DualSense",
            text_color=T.TEXT,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left")

        # Centre: status pill
        self.status_pill = W.Pill(bar, label=t("waiting"),
                                  prefix="DualSense", dot_color=T.RED)
        self.status_pill.grid(row=0, column=1, padx=T.PAD_SM, pady=T.PAD_SM)

        # Right: version
        self.lbl_version = ctk.CTkLabel(
            bar, text=f"v{_version() or '?'}",
            text_color=T.TEXT_FAINT, cursor="hand2",
            font=ctk.CTkFont(size=T.FS_TINY),
        )
        self.lbl_version.grid(row=0, column=2, padx=(0, T.PAD_LG), pady=0, sticky="e")
        self.lbl_version.bind("<Button-1>", lambda _e: self._open_url(CHANGELOG_URL))

        # Glow separator
        ctk.CTkFrame(self.root, height=1, corner_radius=0,
                     fg_color=T.GLASS_BORDER).pack(side="top", fill="x")

    def _build_body(self):
        body = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        body.pack(side="top", fill="both", expand=True)

        # ── Sidebar ───────────────────────────────────────────────────────────
        sidebar = ctk.CTkFrame(body, width=T.SIDEBAR_W, corner_radius=0,
                               fg_color=T.GLASS_HEADER, border_width=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Nav glass card
        nav_card = ctk.CTkFrame(sidebar,
                                fg_color=T.BG_PANEL,
                                corner_radius=T.GLASS_RADIUS,
                                border_width=1,
                                border_color=T.GLASS_BORDER)
        nav_card.pack(fill="x", padx=T.PAD_SM, pady=(T.PAD_MD, 0))

        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        for key in NAV_ITEMS:
            btn = ctk.CTkButton(
                nav_card,
                text=f"  {T.ICON[key]}   {t(key)}", anchor="w",
                height=34, corner_radius=8,
                fg_color="transparent", hover_color=T.BG_HOVER,
                text_color=T.TEXT_MUTED,
                font=ctk.CTkFont(size=T.FS_BODY),
                command=lambda k=key: self._select_nav(k),
            )
            btn.pack(side="top", fill="x", padx=T.PAD_XS, pady=1)
            self._nav_buttons[key] = btn
        ctk.CTkFrame(nav_card, fg_color="transparent", height=T.PAD_XS).pack()

        # Start / Stop glass card
        ctrl_card = ctk.CTkFrame(sidebar,
                                 fg_color=T.BG_PANEL,
                                 corner_radius=T.GLASS_RADIUS,
                                 border_width=1,
                                 border_color=T.GLASS_BORDER)
        ctrl_card.pack(fill="x", padx=T.PAD_SM, pady=(T.PAD_SM, 0))
        ctk.CTkFrame(ctrl_card, fg_color="transparent", height=T.PAD_SM).pack()
        self._btn_start = W.StartButton(ctrl_card, command=self._on_start)
        self._btn_start.pack(fill="x", padx=T.PAD_SM, pady=(0, T.PAD_XS))
        self._btn_stop = W.StopButton(ctrl_card, command=self._on_stop)
        self._btn_stop.pack(fill="x", padx=T.PAD_SM, pady=(0, T.PAD_SM))

        # ── Sidebar footer ────────────────────────────────────────────────────
        sfooter = ctk.CTkFrame(sidebar, fg_color="transparent")
        sfooter.pack(side="bottom", fill="x", padx=T.PAD_SM, pady=(0, T.PAD_MD))

        changelog_btn = ctk.CTkButton(
            sfooter,
            text=t("Changelog"),
            height=26, corner_radius=8,
            fg_color="transparent", hover_color=T.BG_HOVER,
            text_color=T.TEXT_FAINT,
            border_width=1, border_color=T.BORDER,
            font=ctk.CTkFont(size=T.FS_SMALL),
            command=lambda: self._open_url(CHANGELOG_URL),
        )
        changelog_btn.pack(fill="x", pady=(0, T.PAD_XS))

        sponsor_btn = ctk.CTkButton(
            sfooter,
            text=f"{T.ICON['heart']}  {t('Sponsor')}",
            height=34, corner_radius=10,
            fg_color=T.PINK, hover_color="#d43882",
            text_color="#ffffff",
            font=ctk.CTkFont(size=T.FS_BODY, weight="bold"),
            command=lambda: self._open_url(SPONSOR_URL),
        )
        sponsor_btn.pack(fill="x", pady=(0, T.PAD_SM))

        # Attribution — required by AGPLv3 license
        credit_card = ctk.CTkFrame(sfooter,
                                   fg_color=T.BG_PANEL,
                                   corner_radius=10,
                                   border_width=1,
                                   border_color=T.GLASS_BORDER)
        credit_card.pack(fill="x")
        ctk.CTkLabel(
            credit_card,
            text="Originally created by",
            text_color=T.TEXT_FAINT,
            font=ctk.CTkFont(size=T.FS_TINY),
            anchor="center",
        ).pack(pady=(T.PAD_SM, 1))
        name_lbl = ctk.CTkLabel(
            credit_card,
            text="Hamza Yeşilmen",
            text_color=T.ACCENT_SOFT,
            font=ctk.CTkFont(size=T.FS_TINY, weight="bold"),
            cursor="hand2",
            anchor="center",
        )
        name_lbl.pack(pady=(0, T.PAD_SM))
        name_lbl.bind("<Button-1>", lambda _e: self._open_url(SOURCE_URL))

        # Glow vertical separator
        ctk.CTkFrame(body, width=1, corner_radius=0,
                     fg_color=T.GLASS_BORDER).pack(side="left", fill="y")

        # ── Content area ──────────────────────────────────────────────────────
        self._content = ctk.CTkFrame(body, corner_radius=0, fg_color="transparent")
        self._content.pack(side="left", fill="both", expand=True)

        self.controls_tab = ControlsTab(self._content, self)
        self.profiles_tab = ProfilesTab(self._content, self)
        self.settings_tab = SettingsTab(self._content, self)
        self.system_tab   = SystemTab(self._content, self)
        self.lang_tab     = LangTab(self._content, self)
        self.logs_tab     = LogsTab(self._content, self)

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
        self._update_session_buttons()

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
        # Refresh scroll canvas background positions after tab is shown
        self.root.after(50, self._update_scroll_bg)

    def _update_session_buttons(self):
        if not hasattr(self, "_btn_start"):
            return
        if self._session_running:
            self._btn_start.configure(state="disabled", fg_color=T.GREEN_DIM)
            self._btn_stop.configure(state="normal", fg_color=T.RED)
        else:
            self._btn_start.configure(state="normal", fg_color=T.GREEN)
            self._btn_stop.configure(state="disabled", fg_color=T.RED_DIM)

    # ── Session lifecycle ─────────────────────────────────────────────────────

    def _on_start(self):
        if self._session_running:
            return
        self._start_session()

    def _on_stop(self):
        if not self._session_running:
            return
        self._stop_session()
        log.info("Session stopped by user.")

    def _start_session(self):
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
            self._listener_cm = forzahorizon.UDPListener(s.udp_host, s.udp_port,
                                                          s.udp_timeout)
            self._listener = self._listener_cm.__enter__()
            log.info("Listening on %s:%d", s.udp_host, s.udp_port)
            log.info("In game: HUD & Gameplay -> Data Out: ON, IP %s, Port %d",
                     s.udp_host, s.udp_port)
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
            self._session_running = True
            self._update_session_buttons()
        except OSError:
            log.exception("UDP bind failed on %s:%d", s.udp_host, s.udp_port)
            self.status_pill.set_label(
                t("UDP port {port} in use").format(port=s.udp_port))
        except Exception as exc:
            log.exception("Backend startup failed")
            self.status_pill.set_label(
                t("Backend failed: {error}").format(error=exc))

    def _stop_session(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)
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
        self._update_session_buttons()
        self._refresh_status()

    def _run_loop(self):
        try:
            loop.run(self._ds, self._listener, self.settings,
                     stop_event=self._stop)
        except Exception:
            log.exception("Telemetry loop crashed")
        finally:
            if not self._stop.is_set() and not self._tearing_down:
                # Backend exited on its own (game closed) — update state
                self._session_running = False
                try:
                    self.root.after(0, self._on_backend_exit)
                except (RuntimeError, tk.TclError):
                    pass

    def _on_backend_exit(self):
        """Backend loop exited without user pressing Stop (e.g. game closed)."""
        self._session_running = False
        self._update_session_buttons()
        self._refresh_status()
        log.info("Backend exited — press Start to restart.")

    # ── App lifecycle ─────────────────────────────────────────────────────────

    def run(self):
        self.root.after(0, self._start_session)
        self.root.after(1000, self._tick_status)
        self.root.after(100, self._drain_logs)
        # Render background after window is shown
        self.root.after(200, self._redraw_background)
        try:
            self.root.mainloop()
        finally:
            self._full_teardown()

    def _on_unmap(self, event):
        if event.widget is not self.root:
            return
        try:
            if self.root.state() == "iconic":
                self._hide_to_tray()
        except tk.TclError:
            pass

    def _hide_to_tray(self):
        try:
            self.root.withdraw()
        except tk.TclError:
            return
        self._tray.start()

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
        self._full_teardown()
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def _full_teardown(self):
        if self._tearing_down:
            return
        self._tearing_down = True
        root = logging.getLogger()
        for h in list(root.handlers):
            if isinstance(h, _QueueLogHandler):
                root.removeHandler(h)
        self._stop_session()

    # ── Log handling ──────────────────────────────────────────────────────────

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

    # ── Status polling ────────────────────────────────────────────────────────

    def _tick_status(self):
        if self._tearing_down:
            return
        self._refresh_status()
        self.root.after(1000, self._tick_status)

    def _refresh_status(self):
        ds = self._ds
        if ds and getattr(ds, "persistent", False):
            color, label = T.GREEN, f"{t('connected')} — {t('latched')}"
        elif ds and ds.connected:
            color, label = T.GREEN, t("connected")
        elif self._session_running:
            color, label = T.YELLOW, t("waiting")
        else:
            color, label = T.RED, t("stopped")
        self.status_pill.set_dot_color(color)
        self.status_pill.set_label(label)

    def _refresh_profile(self):
        try:
            active = profiles.load_store().get("active") or t("(none)")
        except Exception:
            active = t("(none)")
        if hasattr(self, "profile_pill"):
            self.profile_pill.set_label(active)

    refresh_profile = _refresh_profile
    refresh_status  = _refresh_status

    # ── Shared helpers ────────────────────────────────────────────────────────

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
            threading.Thread(target=self._do_haptic, args=(on_state,),
                             daemon=True).start()

    def _do_haptic(self, on_state: bool):
        amp = HAPTIC_AMP_ON if on_state else HAPTIC_AMP_OFF
        v = vibrate(HAPTIC_FREQ_HZ, amp)
        self._ds.set(v, v)
        time.sleep(HAPTIC_DURATION_S)
        self._ds.set(off(), off())

    @staticmethod
    def _open_url(url: str):
        threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()
