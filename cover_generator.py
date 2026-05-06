"""
From the Kitchen of Debby Kobrosly — Lulu Hardcover Case Wrap Cover
=====================================================================
Lulu 6.25×9.5 Hardcover | 250 pages | Premium Color 80# Coated
Wrap area 0.625" all sides (wraps around board — no separate bleed)

Spread layout (left → right):
  [0.625" wrap] [6.25" back] [0.813" spine] [6.25" front] [0.625" wrap]
  Total = 14.563" × 10.75"
"""

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ── Fonts ─────────────────────────────────────────────────────────────────────
FD = "/home/roni/.local/share/fonts"

pdfmetrics.registerFont(TTFont("Raleway",         f"{FD}/Raleway-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Raleway-Bold",    f"{FD}/Raleway-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Raleway-Light",    f"{FD}/Raleway-Light.ttf"))
pdfmetrics.registerFont(TTFont("Raleway-Italic",    f"{FD}/Raleway-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Lato",            f"{FD}/Lato-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lato-Italic",     f"{FD}/Lato-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans",      "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

# ── Palette (same as interior) ────────────────────────────────────────────────
C_BLACK  = colors.HexColor("#1A1A1A")
C_ACCENT = colors.HexColor("#8B6F47")
C_MID    = colors.HexColor("#5A5A5A")
C_LIGHT  = colors.HexColor("#D4C5A9")
C_CREAM  = colors.HexColor("#FAF7F2")   # warm off-white background
C_DARK   = colors.HexColor("#2C2419")   # deep warm brown for spine/back

# ── Page / spread dimensions ──────────────────────────────────────────────────
BLEED     = 0.625 * inch   # case wrap area (folds around board)
PAGE_W    = 6.25  * inch   # trim width
PAGE_H    = 9.5   * inch   # trim height
SPINE_W   = 0.813 * inch   # 250 pages, per Lulu template

TOTAL_W   = BLEED + PAGE_W + SPINE_W + PAGE_W + BLEED
TOTAL_H   = BLEED + PAGE_H + BLEED

# Key X positions (from left edge of spread)
X_BACK_START  = 0             # bleed starts
X_BACK_LIVE   = BLEED         # back cover live area
X_SPINE_START = BLEED + PAGE_W
X_SPINE_CX    = X_SPINE_START + SPINE_W / 2
X_FRONT_START = X_SPINE_START + SPINE_W
X_FRONT_LIVE  = X_FRONT_START  # front cover live area start
X_FRONT_END   = X_FRONT_START + PAGE_W
X_BLEED_END   = TOTAL_W

# Vertical: bleed starts at y=0, live area at y=BLEED
Y_BOTTOM_LIVE = BLEED
Y_TOP_LIVE    = BLEED + PAGE_H

# Front cover centre — centred in the live/trim area (X_FRONT_LIVE → X_FRONT_END)
FC_CX = X_FRONT_LIVE + PAGE_W / 2
FC_CY = Y_BOTTOM_LIVE + PAGE_H / 2

# Back cover centre — centred in the live/trim area (X_BACK_LIVE → X_SPINE_START)
BC_CX = X_BACK_LIVE + PAGE_W / 2
BC_CY = Y_BOTTOM_LIVE + PAGE_H / 2

# ── Drawing helpers ───────────────────────────────────────────────────────────

def hline(c, x1, x2, y, color=C_LIGHT, width=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)

def vline(c, x, y1, y2, color=C_LIGHT, width=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x, y1, x, y2)

def centred_text(c, text, x, y, font, size, color=C_BLACK, char_space=0):
    c.setFont(font, size)
    c.setFillColor(color)
    if char_space:
        # Manually space characters for letter-spaced text
        total_w = c.stringWidth(text, font, size) + char_space * (len(text) - 1)
        cx = x - total_w / 2
        for i, ch in enumerate(text):
            c.drawString(cx, y, ch)
            cx += c.stringWidth(ch, font, size) + char_space
    else:
        c.drawCentredString(x, y, text)

def left_text(c, text, x, y, font, size, color=C_BLACK):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)

# ── Front cover ───────────────────────────────────────────────────────────────

def draw_front(c):
    """Draw the front cover panel."""
    # Warm cream background
    c.setFillColor(C_CREAM)
    c.rect(X_FRONT_LIVE, 0, PAGE_W + BLEED, TOTAL_H, fill=1, stroke=0)

    # Subtle textured border lines — outer frame inset from trim, scaled to 90%
    INSET = 0.35 * inch
    _fx1 = X_FRONT_LIVE + BLEED + INSET
    _fx2 = TOTAL_W - BLEED - INSET
    _fy1 = Y_BOTTOM_LIVE + INSET
    _fy2 = Y_TOP_LIVE    - INSET
    _bw, _bh = (_fx2 - _fx1) * 0.45, (_fy2 - _fy1) * 0.45
    FX1, FX2 = FC_CX - _bw, FC_CX + _bw
    FY1, FY2 = FC_CY - _bh, FC_CY + _bh

    # Double-rule border (outer)
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(1.2)
    c.rect(FX1, FY1, FX2 - FX1, FY2 - FY1, fill=0, stroke=1)
    # Inner hairline
    OFF = 0.1 * inch
    c.setLineWidth(0.4)
    c.rect(FX1 + OFF, FY1 + OFF, (FX2-FX1) - 2*OFF, (FY2-FY1) - 2*OFF, fill=0, stroke=1)

    # ── "FROM THE KITCHEN OF" byline ─────────────────────────────────────────
    centred_text(c, "FROM THE KITCHEN OF", FC_CX,
                 FY2 - 0.52 * inch, "Raleway", 22.5, C_ACCENT, char_space=1.5)

    # ── Main title ────────────────────────────────────────────────────────────
    TITLE_Y = FC_CY + 0.9 * inch
    # Draw "Debby" and "Kobrosly" as two lines in large serif
    c.setFont("Lato", 52)
    c.setFillColor(C_BLACK)
    c.drawCentredString(FC_CX, TITLE_Y + 0.05*inch, "Debby")
    c.drawCentredString(FC_CX, TITLE_Y - 0.80*inch, "Kobrosly")

    # Accent rule — centred in the visual gap between Debby descender and Kobrosly cap tops
    rule_y = TITLE_Y - 0.19 * inch
    hline(c, FC_CX - 1.1*inch, FC_CX + 1.1*inch, rule_y, C_ACCENT, 0.75)

    # ── Subtitle / ornament ───────────────────────────────────────────────────
    SUB_Y = FC_CY - 0.55 * inch
    # Thin horizontal rules flanking ornament
    hline(c, FC_CX - 1.3*inch, FC_CX - 0.22*inch, SUB_Y + 0.05*inch, C_LIGHT, 0.5)
    hline(c, FC_CX + 0.22*inch, FC_CX + 1.3*inch, SUB_Y + 0.05*inch, C_LIGHT, 0.5)
    centred_text(c, "✦", FC_CX, SUB_Y - 0.06*inch, "DejaVuSans", 16, C_LIGHT)

    # Subtitle text
    centred_text(c, "A Collection of Family Recipes", FC_CX,
                 SUB_Y - 0.42*inch, "Lato-Italic", 13.5, C_ACCENT)

    # ── Tagline at bottom ─────────────────────────────────────────────────────
    TAG_Y = FY1 + 0.38 * inch
    centred_text(c, "Cherished dishes passed down through generations,",
                 FC_CX, TAG_Y + 0.18*inch, "Lato-Italic", 9, C_MID)
    centred_text(c, "gathered with love for family and friends.",
                 FC_CX, TAG_Y - 0.02*inch, "Lato-Italic", 9, C_MID)

# ── Spine ─────────────────────────────────────────────────────────────────────

def draw_spine(c):
    """Draw the spine panel (reads bottom-to-top)."""
    # Dark background for spine
    c.setFillColor(C_DARK)
    c.rect(X_SPINE_START, 0, SPINE_W, TOTAL_H, fill=1, stroke=0)

    # Thin accent lines at top/bottom of spine
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.6)
    c.line(X_SPINE_START, Y_BOTTOM_LIVE + 0.3*inch, X_SPINE_START + SPINE_W, Y_BOTTOM_LIVE + 0.3*inch)
    c.line(X_SPINE_START, Y_TOP_LIVE    - 0.3*inch, X_SPINE_START + SPINE_W, Y_TOP_LIVE    - 0.3*inch)

    # Vertical text — save/restore state for rotation
    c.saveState()
    c.translate(X_SPINE_CX, (Y_BOTTOM_LIVE + Y_TOP_LIVE) / 2)
    c.rotate(90)

    # Book title (centred on spine, reads bottom to top)
    c.setFont("Lato-Italic", 13)
    c.setFillColor(C_LIGHT)
    c.drawCentredString(0, 0, "From the Kitchen of Debby Kobrosly")

    c.restoreState()

# ── Back cover ────────────────────────────────────────────────────────────────

def draw_back(c):
    """Draw the back cover panel."""
    # Same warm cream as front
    c.setFillColor(C_CREAM)
    c.rect(0, 0, X_SPINE_START, TOTAL_H, fill=1, stroke=0)

    # Border frame — same style as front, scaled to 90%
    INSET = 0.35 * inch
    _bx1 = BLEED + INSET
    _bx2 = X_SPINE_START - BLEED - INSET
    _by1 = Y_BOTTOM_LIVE + INSET
    _by2 = Y_TOP_LIVE    - INSET
    _bw, _bh = (_bx2 - _bx1) * 0.45, (_by2 - _by1) * 0.45
    BX1, BX2 = BC_CX - _bw, BC_CX + _bw
    BY1, BY2 = BC_CY - _bh, BC_CY + _bh

    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(1.2)
    c.rect(BX1, BY1, BX2 - BX1, BY2 - BY1, fill=0, stroke=1)
    OFF = 0.1 * inch
    c.setLineWidth(0.4)
    c.rect(BX1 + OFF, BY1 + OFF, (BX2-BX1) - 2*OFF, (BY2-BY1) - 2*OFF, fill=0, stroke=1)

    # ── Back cover headline ───────────────────────────────────────────────────
    centred_text(c, "FROM THE KITCHEN OF", BC_CX,
                 BY2 - 0.42*inch, "Raleway", 7.5, C_ACCENT, char_space=3.5)

    hline(c, BX1 + 0.2*inch, BX2 - 0.2*inch,
          BY2 - 0.6*inch, C_LIGHT, 0.5)

    # ── Back cover text block ─────────────────────────────────────────────────
    # We'll draw a short warm paragraph about the book
    LINES = [
        "In every family, there are recipes that carry",
        "the weight of memory — dishes that bring back",
        "a grandmother's kitchen, a holiday table,",
        "a smell that means home.",
        "",
        "This collection gathers the beloved recipes of",
        "Debby Kobrosly: from Lebanese kibbeh and",
        "falafel to American classics, from morning",
        "muffins to celebration cakes. Passed down,",
        "handwritten, adapted, and perfected over",
        "a lifetime of cooking with love.",
        "",
        "May these pages find a place in your kitchen,",
        "and these flavors a place at your table.",
    ]

    LINE_H = 0.215 * inch
    BLOCK_TOP = BY2 - 1.0 * inch
    TEXT_X = BC_CX

    c.setFont("Lato-Italic", 10.5)
    c.setFillColor(C_BLACK)

    for i, line in enumerate(LINES):
        y = BLOCK_TOP - i * LINE_H
        if line:
            c.drawCentredString(TEXT_X, y, line)

    # ── Ornament divider ──────────────────────────────────────────────────────
    ORN_Y = BLOCK_TOP - len(LINES) * LINE_H - 0.2*inch
    hline(c, BX1+0.4*inch, TEXT_X - 0.18*inch, ORN_Y + 0.06*inch, C_LIGHT, 0.5)
    hline(c, TEXT_X+0.18*inch, BX2-0.4*inch,   ORN_Y + 0.06*inch, C_LIGHT, 0.5)
    centred_text(c, "✦", TEXT_X, ORN_Y - 0.04*inch, "DejaVuSans", 14, C_LIGHT)

    # ── Chapter list ─────────────────────────────────────────────────────────
    CHAPTERS = [
        "Appetizers, Dips & Snacks  ·  Salads & Fruits",
        "Breakfast  ·  Soups & Stews  ·  Vegetables & Sides",
        "Pasta & Grains  ·  Seafood  ·  Poultry  ·  Meats",
        "Vegetarian Mains  ·  Bread  ·  Cakes & Cookies",
        "Desserts",
    ]
    CH_Y = ORN_Y - 0.45*inch
    for i, ch in enumerate(CHAPTERS):
        centred_text(c, ch, TEXT_X, CH_Y - i * 0.195*inch,
                     "Raleway-Light", 7.8, C_MID)


# ── Bleed marks (optional crop guide) — we'll skip; Lulu handles bleed ───────

# ── Main ─────────────────────────────────────────────────────────────────────

def build():
    out = "./output/cookbook_cover_lulu.pdf"

    c = canvas.Canvas(out, pagesize=(TOTAL_W, TOTAL_H))
    c.setTitle("From the Kitchen of Debby Kobrosly — Cover")
    c.setAuthor("Debby Kobrosly")

    draw_back(c)
    draw_spine(c)
    draw_front(c)

    # Light bleed guide lines (in a non-printing colour if desired)
    # Lulu expects bleed included but no crop marks needed
    c.save()
    print(f"✓ Cover saved → {out}")
    print(f"  Spread size: {TOTAL_W/inch:.4f}\" × {TOTAL_H/inch:.4f}\"")
    print(f"  Spine width: {SPINE_W/inch:.4f}\" (250 pages, Lulu template)")
    print(f"  Bleed: {BLEED/inch:.3f}\" all sides")

if __name__ == "__main__":
    build()
