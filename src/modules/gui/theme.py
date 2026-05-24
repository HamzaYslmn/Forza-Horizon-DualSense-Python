"""Design tokens for the GUI: colors, spacing, icon glyphs, font sizes.

Discord-dark inspired palette. Single source of truth - never hardcode
colors elsewhere; import from here.
"""

# Background tiers ---------------------------------------------------------
BG_DEEP   = ("#fafafa", "#1e1f22")  # sidebar
BG_MAIN   = ("#ffffff", "#313338")  # content area
BG_PANEL  = ("#f2f3f5", "#2b2d31")  # cards
BG_INPUT  = ("#ffffff", "#1e1f22")  # inputs / lists / log box
BG_HOVER  = ("#e5e7eb", "#35373c")
BG_ACTIVE = ("#d1d5db", "#404249")

# Borders
BORDER = ("#e5e7eb", "#1e1f22")

# Text
TEXT       = ("#060607", "#f2f3f5")
TEXT_MUTED = ("#4e5058", "#b5bac1")
TEXT_FAINT = ("#6d6f78", "#80848e")

# Accent (Discord blurple)
ACCENT       = "#5865f2"
ACCENT_HOVER = "#4752c4"
ACCENT_SOFT  = ("#5865f2", "#7983f5")

# Semantic
GREEN  = ("#1f8a3a", "#23a55a")
YELLOW = ("#b45309", "#f0b132")
RED    = ("#b91c1c", "#f23f43")
PINK   = "#ff5fa2"
BLUE   = ("#1e90ff", "#1e90ff")  # dodgerblue - DSX status

# Spacing tokens
PAD_XS = 4
PAD_SM = 8
PAD_MD = 16
PAD_LG = 24

# Sizes
SIDEBAR_W = 188
HEADER_H  = 44

# Font sizes
FS_H1 = 18
FS_H2 = 13
FS_BODY = 12
FS_SMALL = 11
FS_TINY = 10

# Icon glyphs
ICON = {
    "Controls": "\U0001F3AE",  # gamepad
    "Profiles": "\U0001F4CB",  # clipboard
    "Settings": "\u2699",        # gear
    "System":   "\U0001F5A5",  # computer
    "Language": "\U0001F310",  # globe
    "Logs":     "\U0001F4DC",  # scroll
    "pause":    "\u23F8",
    "play":     "\u25B6",
    "clear":    "\U0001F5D1",
    "reload":   "\u21BB",
    "heart":    "\u2665",
    "dot":      "\u25CF",
    "x":        "\u2715",
    "warn":     "\u26A0",
}
