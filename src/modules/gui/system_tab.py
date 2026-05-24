"""System tab: extends SettingsTab with controller selection + update toggle."""
import logging
import os
import threading
from pathlib import Path

import customtkinter as ctk

from lang import t
from modules.config import preferences
from modules.dualsense.main import _enumerate_dualsenses, _is_bluetooth, identify_pulse

from . import theme as T
from . import widgets as W
from .settings_tab import SYSTEM_SECTIONS, SettingsTab

log = logging.getLogger("fhds")

SENTINEL = ".zuv-update-disabled"


def sentinel_path() -> Path | None:
    root = os.environ.get("ZUV_CACHE_ROOT")
    return Path(root) / SENTINEL if root else None


def apply_sentinel(enabled: bool) -> None:
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
    PAGE_TITLE = "System"
    PAGE_SUBTITLE = "Controller, background, updates, and app-level options."

    def __init__(self, parent, app):
        self._devices: list[dict] = []
        self._lock_var: ctk.StringVar | None = None
        self._radio_holder: "W.FastScroll | None" = None
        self._radio_buttons: list[ctk.CTkRadioButton] = []
        self._update_switch: ctk.CTkSwitch | None = None
        self._bg_path_var: ctk.StringVar | None = None
        self._bg_path_lbl: ctk.CTkLabel | None = None
        super().__init__(parent, app)
        if sentinel_path() is not None:
            apply_sentinel(self.settings.check_for_updates)
        threading.Thread(target=self._enumerate_async, daemon=True).start()

    def _build(self):
        self._build_controller_card()
        self._build_background_card()
        self._build_updates_card()
        # Standard sections from SYSTEM_SECTIONS
        super()._build()

    # MARK: controller card -------------------------------------------------

    def _build_controller_card(self):
        card = W.Card(self._scroll)
        card.pack(fill="x", pady=(0, T.PAD_MD))
        W.H2(card, t("Controller")).pack(anchor="w", padx=T.PAD_MD,
                                         pady=(T.PAD_MD, T.PAD_XS))
        W.Hint(card, t("Lock the app to a specific DualSense, or let it pick the first one.")
               ).pack(anchor="w", padx=T.PAD_MD, pady=(0, T.PAD_SM))

        self._lock_var = ctk.StringVar(value=self.settings.controller_lock_serial or "")
        self._radio_holder = W.FastScroll(card, height=140,
                                                    fg_color=T.BG_INPUT,
                                                    corner_radius=6)
        self._radio_holder.pack(fill="x", padx=T.PAD_MD, pady=(0, T.PAD_SM))
        self._render_radio_buttons()

        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill="x", padx=T.PAD_MD, pady=(0, T.PAD_MD))
        W.SecondaryButton(actions, t("Rescan"), self._on_rescan, width=120
                          ).pack(side="left")

    def _build_background_card(self):
        card = W.Card(self._scroll)
        card.pack(fill="x", pady=(0, T.PAD_MD))
        W.H2(card, t("Background Image")).pack(anchor="w", padx=T.PAD_MD,
                                               pady=(T.PAD_MD, T.PAD_XS))
        W.Hint(
            card,
            t("Choose any image file. It will be blurred and darkened automatically."),
            wrap=self.app.px(600),
        ).pack(fill="x", padx=T.PAD_MD, pady=(0, T.PAD_SM))

        path = self.settings.background_image_path or ""
        label_text = os.path.basename(path) if path else t("Default gradient (no image set)")

        self._bg_path_lbl = ctk.CTkLabel(
            card, text=label_text,
            anchor="w",
            text_color=T.TEXT_MUTED,
            font=ctk.CTkFont(size=T.FS_SMALL),
        )
        self._bg_path_lbl.pack(fill="x", padx=T.PAD_MD, pady=(0, T.PAD_XS))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=T.PAD_MD, pady=(0, T.PAD_MD))

        W.SecondaryButton(btn_row, t("Browse…"), self._on_browse_bg, width=110
                          ).pack(side="left", padx=(0, T.PAD_SM))
        W.DangerButton(btn_row, t("Clear"), self._on_clear_bg, width=80
                       ).pack(side="left")

    def _on_browse_bg(self):
        import tkinter.filedialog as fd
        path = fd.askopenfilename(
            title=t("Choose a background image"),
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tiff"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        self.settings.background_image_path = path
        preferences.save(self.settings)
        if self._bg_path_lbl:
            self._bg_path_lbl.configure(text=os.path.basename(path))
        gui = self.app
        if hasattr(gui, "reload_background"):
            gui.reload_background()
        log.info("background_image_path = %r", path)

    def _on_clear_bg(self):
        self.settings.background_image_path = ""
        preferences.save(self.settings)
        if self._bg_path_lbl:
            self._bg_path_lbl.configure(text=t("Default gradient (no image set)"))
        gui = self.app
        if hasattr(gui, "reload_background"):
            gui.reload_background()
        log.info("background_image_path cleared")

    def _build_updates_card(self):
        card = W.Card(self._scroll)
        card.pack(fill="x", pady=(0, T.PAD_MD))
        W.H2(card, t("Updates")).pack(anchor="w", padx=T.PAD_MD,
                                      pady=(T.PAD_MD, T.PAD_SM))
        if sentinel_path() is None:
            W.Danger(
                card,
                t("ZUV not found: this build is not running inside a ZUV bundle "
                  "(ZUV_CACHE_ROOT env var is missing), so the update toggle has "
                  "nothing to control. Run the bundled .zuv.py to manage updates."),
                wrap=self.app.px(640),
            ).pack(fill="x", padx=T.PAD_MD, pady=(0, T.PAD_MD))
            return
        self._update_switch = ctk.CTkSwitch(card,
                                            text=t("Check for updates at launch"),
                                            command=self._on_update_toggle)
        if self.settings.check_for_updates:
            self._update_switch.select()
        self._update_switch.pack(anchor="w", padx=T.PAD_MD, pady=(0, T.PAD_XS))
        W.Hint(
            card,
            t("When off, ZUV will not prompt for updates on startup. "
              "Toggle on and restart the app to check for a new release."),
            wrap=self.app.px(640),
        ).pack(fill="x", padx=T.PAD_MD, pady=(0, T.PAD_MD))

    # MARK: controller list -------------------------------------------------

    def _attached_serial(self) -> str:
        ds = getattr(self.app, "_ds", None)
        if ds is None or not ds.connected:
            return ""
        return getattr(ds, "dev_serial", "") or ""

    def _render_radio_buttons(self):
        if self._radio_holder is None or self._lock_var is None:
            return
        for rb in self._radio_buttons:
            rb.destroy()
        self._radio_buttons.clear()
        attached = self._attached_serial()

        rb = ctk.CTkRadioButton(self._radio_holder, text=t("Auto (first found)"),
                                variable=self._lock_var, value="",
                                command=self._on_lock_changed)
        rb.pack(anchor="w", padx=T.PAD_SM, pady=2)
        self._radio_buttons.append(rb)

        for d in self._devices:
            sn = d.get("serial_number") or ""
            transport = "BT" if _is_bluetooth(d) else "USB"
            if sn:
                marker = f"  < {t('attached now')}" if sn == attached else ""
                rb = ctk.CTkRadioButton(self._radio_holder,
                                        text=f"[{transport}] {sn}{marker}",
                                        variable=self._lock_var, value=sn,
                                        command=self._on_lock_changed)
            else:
                rb = ctk.CTkRadioButton(self._radio_holder,
                                        text=f"[{transport}] {t('(no serial - not selectable)')}",
                                        variable=self._lock_var,
                                        value=f"__noserial_{id(d)}__",
                                        state="disabled")
            rb.pack(anchor="w", padx=T.PAD_SM, pady=2)
            self._radio_buttons.append(rb)

    def _on_rescan(self):
        threading.Thread(target=self._enumerate_async, daemon=True).start()

    def _enumerate_async(self):
        try:
            devs = _enumerate_dualsenses()
        except Exception:
            log.exception("controller enumeration failed")
            devs = []
        try:
            self.app.root.after(0, lambda: self._apply_devices(devs))
        except Exception:
            pass

    def _apply_devices(self, devices: list[dict]):
        self._devices = devices
        if self._lock_var is not None:
            self._lock_var.set(self.settings.controller_lock_serial or "")
        self._render_radio_buttons()

    def _on_lock_changed(self):
        if self._lock_var is None:
            return
        new = self._lock_var.get()
        if new.startswith("__noserial_"):
            return
        if new:
            info = next((d for d in self._devices
                         if (d.get("serial_number") or "") == new), None)
            if info is not None:
                threading.Thread(
                    target=identify_pulse, args=(info,),
                    kwargs={"force": self.settings.startup_pulse_force},
                    daemon=True,
                ).start()
        if self.settings.controller_lock_serial != new:
            self.settings.controller_lock_serial = new
            preferences.save(self.settings)
            log.info("controller_lock_serial = %r", new)
        ds = getattr(self.app, "_ds", None)
        if ds is not None:
            ds.set_selection(new)
            if new and new != self._attached_serial():
                ds.force_reconnect()
        threading.Thread(target=self._enumerate_async, daemon=True).start()

    # MARK: updates ---------------------------------------------------------

    def _on_update_toggle(self):
        if self._update_switch is None or self.app._refreshing:
            return
        value = bool(self._update_switch.get())
        if self.settings.check_for_updates != value:
            self.settings.check_for_updates = value
            preferences.save(self.settings)
            log.info("check_for_updates = %s", value)
        apply_sentinel(value)

    def _refresh_widgets(self):
        super()._refresh_widgets()
        if self._update_switch is not None:
            want = bool(self.settings.check_for_updates)
            if bool(self._update_switch.get()) != want:
                if want:
                    self._update_switch.select()
                else:
                    self._update_switch.deselect()
        if self._lock_var is not None:
            self._lock_var.set(self.settings.controller_lock_serial or "")
            self._render_radio_buttons()
