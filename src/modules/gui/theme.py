"""Design tokens — glass-morphism dark palette.

All colors, spacing, and type scale live here. Never hardcode elsewhere.
"""

# ── Background tiers ──────────────────────────────────────────────────────────
# These sit *over* the blurred background image.
BG_ROOT   = "#08090f"          # window fill (fallback when no image)
BG_DEEP   = "#0c0d16"          # sidebar panel
BG_MAIN   = "#0f1019"          # content area
BG_PANEL  = "#13151f"          # glass cards
BG_INPUT  = "#0c0d16"          # entries / list boxes / log
BG_HOVER  = "#1c1e2d"          # hover state
BG_ACTIVE = "#252840"          # selected nav item

# ── Glass card surface ─────────────────────────────────────────────────────────
GLASS_BORDER        = "#2d2f4a"   # subtle card border
GLASS_BORDER_LIGHT  = "#3d3f60"   # hover / highlight border
GLASS_RADIUS        = 14          # corner radius for all cards

# ── Borders & dividers ────────────────────────────────────────────────────────
BORDER        = "#1a1c2a"
BORDER_SUBTLE = "#12131e"

# ── Text ──────────────────────────────────────────────────────────────────────
TEXT       = "#e8eaf6"
TEXT_MUTED = "#8b8fa8"
TEXT_FAINT = "#555870"

# ── Accent (electric indigo) ──────────────────────────────────────────────────
ACCENT       = "#6366f1"
ACCENT_HOVER = "#4f52d4"
ACCENT_SOFT  = "#6366f1"

# ── Semantic ──────────────────────────────────────────────────────────────────
GREEN        = "#22c55e"
GREEN_HOVER  = "#16a34a"
GREEN_DIM    = "#14532d"
YELLOW       = "#eab308"
RED          = "#ef4444"
RED_HOVER    = "#dc2626"
RED_DIM      = "#450a0a"
PINK         = "#ec4899"

# ── Spacing ───────────────────────────────────────────────────────────────────
PAD_XS = 4
PAD_SM = 8
PAD_MD = 16
PAD_LG = 24
PAD_XL = 32

# ── Sizes ─────────────────────────────────────────────────────────────────────
SIDEBAR_W = 200
HEADER_H  = 52

# ── Font sizes ────────────────────────────────────────────────────────────────
FS_H1    = 20
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
