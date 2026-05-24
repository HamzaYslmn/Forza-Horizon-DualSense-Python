"""Reusable widget primitives — glass-morphism edition.

Build screens by composing these; never re-implement colors/spacing locally.
"""
import customtkinter as ctk

from . import theme as T


# ── Typography ────────────────────────────────────────────────────────────────

class H1(ctk.CTkLabel):
    def __init__(self, parent, text: str, **kw):
        super().__init__(parent, text=text, anchor="w",
                         font=ctk.CTkFont(size=T.FS_H1, weight="bold"),
                         text_color=T.TEXT, **kw)


class H2(ctk.CTkLabel):
    def __init__(self, parent, text: str, **kw):
        super().__init__(parent, text=text, anchor="w",
                         font=ctk.CTkFont(size=T.FS_H2, weight="bold"),
                         text_color=T.TEXT, **kw)


class Body(ctk.CTkLabel):
    def __init__(self, parent, text: str, **kw):
        super().__init__(parent, text=text, anchor="w", justify="left",
                         font=ctk.CTkFont(size=T.FS_BODY),
                         text_color=T.TEXT, **kw)


class Hint(ctk.CTkLabel):
    def __init__(self, parent, text: str, wrap: int = 0, **kw):
        super().__init__(parent, text=text, anchor="w", justify="left",
                         font=ctk.CTkFont(size=T.FS_SMALL),
                         text_color=T.TEXT_MUTED, **kw)
        if wrap:
            self.configure(wraplength=wrap)


class Warning(ctk.CTkLabel):
    def __init__(self, parent, text: str, wrap: int = 0, **kw):
        super().__init__(parent, text=text, anchor="w", justify="left",
                         font=ctk.CTkFont(size=T.FS_SMALL),
                         text_color=T.YELLOW, **kw)
        if wrap:
            self.configure(wraplength=wrap)


class Danger(ctk.CTkLabel):
    def __init__(self, parent, text: str, wrap: int = 0, **kw):
        super().__init__(parent, text=text, anchor="w", justify="left",
                         font=ctk.CTkFont(size=T.FS_SMALL),
                         text_color=T.RED, **kw)
        if wrap:
            self.configure(wraplength=wrap)


# ── Surfaces ──────────────────────────────────────────────────────────────────

class Card(ctk.CTkFrame):
    """Glass-morphism card: dark background, subtle glowing border."""
    def __init__(self, parent, **kw):
        kw.setdefault("fg_color", T.BG_PANEL)
        kw.setdefault("corner_radius", T.GLASS_RADIUS)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", T.GLASS_BORDER)
        super().__init__(parent, **kw)


class GlassCard(ctk.CTkFrame):
    """Slightly elevated card for hero/status sections."""
    def __init__(self, parent, **kw):
        kw.setdefault("fg_color", T.BG_HOVER)
        kw.setdefault("corner_radius", T.GLASS_RADIUS)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", T.GLASS_BORDER_LIGHT)
        super().__init__(parent, **kw)


class Section(ctk.CTkFrame):
    def __init__(self, parent, title: str, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        H2(self, title).pack(anchor="w", padx=T.PAD_MD, pady=(T.PAD_MD, T.PAD_SM))
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=T.PAD_MD, pady=(0, T.PAD_MD))


# ── Chips / pills ─────────────────────────────────────────────────────────────

class Pill(ctk.CTkFrame):
    """Rounded chip: optional colored dot + prefix label + main label."""
    def __init__(self, parent, label: str = "", prefix: str = "",
                 dot_color=None, **kw):
        kw.setdefault("fg_color", T.BG_HOVER)
        kw.setdefault("corner_radius", 14)
        kw.setdefault("height", 28)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", T.GLASS_BORDER)
        super().__init__(parent, **kw)
        self._dot = None
        self._prefix = None
        if dot_color is not None:
            self._dot = ctk.CTkLabel(self, text=T.ICON["dot"], width=8,
                                     text_color=dot_color,
                                     font=ctk.CTkFont(size=9))
            self._dot.pack(side="left", padx=(12, 4), pady=0)
        if prefix:
            self._prefix = ctk.CTkLabel(self, text=prefix.upper(),
                                        text_color=T.TEXT_FAINT,
                                        font=ctk.CTkFont(size=T.FS_TINY, weight="bold"))
            self._prefix.pack(side="left",
                              padx=(12 if dot_color is None else 0, 4), pady=0)
        self._label = ctk.CTkLabel(self, text=label, text_color=T.TEXT,
                                   font=ctk.CTkFont(size=T.FS_SMALL, weight="bold"))
        self._label.pack(side="left", padx=(0, 14), pady=0)

    def set_label(self, text: str):
        self._label.configure(text=text)

    def set_dot_color(self, color):
        if self._dot is not None:
            self._dot.configure(text_color=color)


# ── Buttons ───────────────────────────────────────────────────────────────────

class PrimaryButton(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None, **kw):
        kw.setdefault("height", 34)
        kw.setdefault("fg_color", T.ACCENT)
        kw.setdefault("hover_color", T.ACCENT_HOVER)
        kw.setdefault("text_color", "white")
        kw.setdefault("corner_radius", 8)
        kw.setdefault("font", ctk.CTkFont(size=T.FS_BODY, weight="bold"))
        super().__init__(parent, text=text, command=command, **kw)


class StartButton(ctk.CTkButton):
    """Large green start button."""
    def __init__(self, parent, command=None, **kw):
        kw.setdefault("height", 40)
        kw.setdefault("fg_color", T.GREEN)
        kw.setdefault("hover_color", T.GREEN_HOVER)
        kw.setdefault("text_color", "white")
        kw.setdefault("corner_radius", 10)
        kw.setdefault("font", ctk.CTkFont(size=T.FS_BODY, weight="bold"))
        super().__init__(parent, text=f"  {T.ICON['play']}  Start", command=command, **kw)


class StopButton(ctk.CTkButton):
    """Large red stop button."""
    def __init__(self, parent, command=None, **kw):
        kw.setdefault("height", 40)
        kw.setdefault("fg_color", T.RED)
        kw.setdefault("hover_color", T.RED_HOVER)
        kw.setdefault("text_color", "white")
        kw.setdefault("corner_radius", 10)
        kw.setdefault("font", ctk.CTkFont(size=T.FS_BODY, weight="bold"))
        super().__init__(parent, text=f"  {T.ICON['stop']}  Stop", command=command, **kw)


class GhostButton(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None, **kw):
        kw.setdefault("height", 32)
        kw.setdefault("fg_color", "transparent")
        kw.setdefault("hover_color", T.BG_HOVER)
        kw.setdefault("text_color", T.TEXT)
        kw.setdefault("corner_radius", 8)
        kw.setdefault("font", ctk.CTkFont(size=T.FS_BODY))
        super().__init__(parent, text=text, command=command, **kw)


class SecondaryButton(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None, **kw):
        kw.setdefault("height", 32)
        kw.setdefault("fg_color", T.BG_HOVER)
        kw.setdefault("hover_color", T.BG_ACTIVE)
        kw.setdefault("text_color", T.TEXT)
        kw.setdefault("corner_radius", 8)
        kw.setdefault("font", ctk.CTkFont(size=T.FS_BODY))
        super().__init__(parent, text=text, command=command, **kw)


class DangerButton(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None, **kw):
        kw.setdefault("height", 32)
        kw.setdefault("fg_color", T.RED)
        kw.setdefault("hover_color", T.RED_HOVER)
        kw.setdefault("text_color", "white")
        kw.setdefault("corner_radius", 8)
        kw.setdefault("font", ctk.CTkFont(size=T.FS_BODY, weight="bold"))
        super().__init__(parent, text=text, command=command, **kw)


# ── Form layout helpers ───────────────────────────────────────────────────────

class FieldRow(ctk.CTkFrame):
    """Label column + flexible control column."""
    LABEL_W = 220

    def __init__(self, parent, label: str, hint: str = "", **kw):
        kw.setdefault("fg_color", "transparent")
        super().__init__(parent, **kw)
        self.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self, text=label, anchor="w", width=self.LABEL_W,
                     text_color=T.TEXT,
                     font=ctk.CTkFont(size=T.FS_BODY)
                     ).grid(row=0, column=0, padx=(0, T.PAD_MD), sticky="w")
        self.controls = ctk.CTkFrame(self, fg_color="transparent")
        self.controls.grid(row=0, column=1, sticky="ew")
        if hint:
            Hint(self, hint).grid(row=1, column=1, sticky="w", pady=(T.PAD_XS, 0))


class PageHeader(ctk.CTkFrame):
    def __init__(self, parent, title: str, subtitle: str = "", **kw):
        kw.setdefault("fg_color", "transparent")
        super().__init__(parent, **kw)
        H1(self, title).pack(anchor="w")
        if subtitle:
            Hint(self, subtitle).pack(anchor="w", pady=(T.PAD_XS, 0))


# ── Scrollable containers ─────────────────────────────────────────────────────

WHEEL_MULT = 5


class FastScroll(ctk.CTkScrollableFrame):
    """CTkScrollableFrame with faster mouse-wheel and accent scrollbar."""
    def __init__(self, parent, **kw):
        kw.setdefault("fg_color", "transparent")
        kw.setdefault("scrollbar_fg_color", T.BG_PANEL)
        kw.setdefault("scrollbar_button_color", T.BG_ACTIVE)
        kw.setdefault("scrollbar_button_hover_color", T.ACCENT)
        super().__init__(parent, **kw)

    def _mouse_wheel_all(self, event):
        import sys as _sys
        if not self.check_if_master_is_canvas(event.widget):
            return
        cv = self._parent_canvas
        if _sys.platform.startswith("win"):
            step = -int(event.delta / 6) * WHEEL_MULT
        else:
            step = -int(event.delta) * WHEEL_MULT
        if self._shift_pressed:
            if cv.xview() != (0.0, 1.0):
                cv.xview("scroll", step, "units")
        else:
            if cv.yview() != (0.0, 1.0):
                cv.yview("scroll", step, "units")
        cv.update_idletasks()


class ScrollCard(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kw):
        kw.setdefault("fg_color", T.BG_PANEL)
        kw.setdefault("corner_radius", T.GLASS_RADIUS)
        super().__init__(parent, **kw)
