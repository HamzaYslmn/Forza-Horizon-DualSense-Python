"""Design tokens — glass-morphism dark palette.

All colors, spacing, and type scale live here. Never hardcode elsewhere.
"""

# ── Background tiers ──────────────────────────────────────────────────────────
BG_ROOT   = "#07080e"          # window fill (behind everything)
BG_DEEP   = "#0a0b14"          # sidebar / header panels
BG_MAIN   = "#0d0e18"          # content area base
BG_PANEL  = "#12141f"          # glass cards
BG_INPUT  = "#0a0c18"          # entries / list boxes / log
BG_HOVER  = "#1e2035"          # hover state
BG_ACTIVE = "#252a45"          # selected nav item

# ── Glass surface tokens ───────────────────────────────────────────────────────
GLASS_BORDER        = "#3b3e62"   # card border (visible glow line)
GLASS_BORDER_LIGHT  = "#5558a0"   # hover / highlight border
GLASS_RADIUS        = 16          # corner radius for cards
GLASS_HEADER        = "#0e1020"   # header / sidebar tinted glass colour

# ── Borders & dividers ────────────────────────────────────────────────────────
BORDER        = "#181a2c"
BORDER_SUBTLE = "#101220"

# ── Text ──────────────────────────────────────────────────────────────────────
TEXT       = "#eceef8"
TEXT_MUTED = "#7e82a0"
TEXT_FAINT = "#4a4d68"

# ── Accent (electric indigo) ──────────────────────────────────────────────────
ACCENT       = "#6366f1"
ACCENT_HOVER = "#4f52d4"
ACCENT_SOFT  = "#818cf8"
ACCENT_GLOW  = "#6366f133"   # used for box-shadow approximation (border trick)

# ── Semantic ──────────────────────────────────────────────────────────────────
GREEN        = "#22c55e"
GREEN_HOVER  = "#16a34a"
GREEN_DIM    = "#14532d"
GREEN_GLOW   = "#22c55e55"
YELLOW       = "#eab308"
RED          = "#ef4444"
RED_HOVER    = "#dc2626"
RED_DIM      = "#3d0c0c"
RED_GLOW     = "#ef444455"
PINK         = "#ec4899"

# ── Spacing ───────────────────────────────────────────────────────────────────
PAD_XS = 4
PAD_SM = 8
PAD_MD = 16
PAD_LG = 24
PAD_XL = 32

# ── Sizes ─────────────────────────────────────────────────────────────────────
SIDEBAR_W = 210
HEADER_H  = 56

# ── Font sizes ────────────────────────────────────────────────────────────────
FS_H1    = 18
FS_H2    = 13
FS_BODY  = 12
FS_SMALL = 11
FS_TINY  = 10

# ── Icon glyphs ───────────────────────────────────────────────────────────────
ICON = {
    "Controls": "\U0001F3AE",
    "Profiles": "\U0001F4CB",
    "Settings": "⚙",
    "System":   "\U0001F5A5",
    "Language": "\U0001F310",
    "Logs":     "\U0001F4DC",
    "pause":    "⏸",
    "play":     "▶",
    "stop":     "■",
    "clear":    "\U0001F5D1",
    "reload":   "↻",
    "heart":    "♥",
    "dot":      "●",
    "x":        "✕",
    "warn":     "⚠",
    "image":    "\U0001F5BC",
}
