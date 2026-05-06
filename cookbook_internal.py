"""
From the Kitchen of Debby Kobrosly — Full Cookbook PDF Generator
6 x 9 inches | Single column | Raleway + Lato + Times Roman
"""

from reportlab.lib.pagesizes import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, Flowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ── Register fonts ────────────────────────────────────────────────────────────
FD = "/home/roni/.local/share/fonts"
pdfmetrics.registerFont(TTFont("Raleway",         f"{FD}/Raleway-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Raleway-Bold",    f"{FD}/Raleway-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lato",            f"{FD}/Lato-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lato-Bold",       f"{FD}/Lato-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lato-Italic",     f"{FD}/Lato-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Lato-BoldItalic", f"{FD}/Lato-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Lato-Light",      f"{FD}/Lato-Light.ttf"))
registerFontFamily("Lato", normal="Lato", bold="Lato-Bold",
                   italic="Lato-Italic", boldItalic="Lato-BoldItalic")

DEJAVU_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DejaVuSerif",        f"{DEJAVU_DIR}/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif-Bold",   f"{DEJAVU_DIR}/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif-Italic", f"{DEJAVU_DIR}/DejaVuSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans",         f"{DEJAVU_DIR}/DejaVuSans.ttf"))
registerFontFamily("DejaVuSerif", normal="DejaVuSerif", bold="DejaVuSerif-Bold",
                   italic="DejaVuSerif-Italic", boldItalic="DejaVuSerif-Bold")

# ── Page setup ────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H  = 6 * inch, 9 * inch
MARGIN_TOP      = 0.875 * inch
MARGIN_BOTTOM   = 0.875 * inch
MARGIN_INNER    = 0.875 * inch
MARGIN_OUTER    = 0.75  * inch
BODY_W          = PAGE_W - MARGIN_INNER - MARGIN_OUTER  # 4.375"

# ── Palette ───────────────────────────────────────────────────────────────────
C_BLACK  = colors.HexColor("#1A1A1A")
C_ACCENT = colors.HexColor("#8B6F47")
C_MID    = colors.HexColor("#5A5A5A")
C_LIGHT  = colors.HexColor("#D4C5A9")

# ── Font aliases ──────────────────────────────────────────────────────────────
RAL   = "Raleway";    RAL_B  = "Raleway-Bold"
LATO  = "Lato";       LATO_B = "Lato-Bold"
LATO_I= "Lato-Italic"; LATO_BI="Lato-BoldItalic"
SERIF = "DejaVuSerif"; SERIF_B="DejaVuSerif-Bold"; SERIF_I="DejaVuSerif-Italic"


# ── Styles ────────────────────────────────────────────────────────────────────
def mk(name, **kw):
    return ParagraphStyle(name, **kw)

ST = {
    # Cover
    "cover_from":    mk("cf",  fontName=RAL,    fontSize=9,  textColor=C_ACCENT, alignment=TA_CENTER, charSpace=4, spaceAfter=12),
    "cover_title":   mk("ct",  fontName=RAL_B,  fontSize=38, leading=46, textColor=C_BLACK,  alignment=TA_CENTER, spaceAfter=10),
    "cover_sub":     mk("cs",  fontName=SERIF_I,fontSize=15, leading=22, textColor=C_ACCENT, alignment=TA_CENTER, spaceAfter=6),
    "cover_tag":     mk("cta", fontName=SERIF_I,fontSize=10.5,leading=16,textColor=C_MID,   alignment=TA_CENTER),
    # TOC
    "toc_head":      mk("th",  fontName=RAL_B,  fontSize=22, leading=28, textColor=C_BLACK,  alignment=TA_CENTER, spaceAfter=6),
    "toc_ch":        mk("tc",  fontName=LATO_B, fontSize=10.5,leading=15,textColor=C_BLACK,  spaceBefore=10, spaceAfter=2),
    "toc_rec":       mk("tr",  fontName=LATO,   fontSize=9.5, leading=14,textColor=C_MID,    leftIndent=14, spaceAfter=1),
    "toc_pg":        mk("tp",  fontName=LATO,   fontSize=9.5, leading=14,textColor=C_MID,    alignment=TA_RIGHT),
    # Chapter
    "ch_num":        mk("cn",  fontName=RAL,    fontSize=8.5, leading=12,textColor=C_ACCENT, alignment=TA_CENTER, spaceBefore=30, spaceAfter=4, charSpace=3),
    "ch_title":      mk("cht", fontName=RAL_B,  fontSize=26, leading=32, textColor=C_BLACK,  alignment=TA_CENTER, spaceAfter=6),
    "ch_intro":      mk("chi", fontName=SERIF_I,fontSize=11, leading=17, textColor=C_MID,    alignment=TA_CENTER, spaceAfter=20),
    # Recipe
    "rec_title":     mk("rt",  fontName=RAL_B,  fontSize=20, leading=26, textColor=C_BLACK,  spaceBefore=16, spaceAfter=4),
    "rec_yield":     mk("ry",  fontName=RAL,    fontSize=8,  leading=12, textColor=C_ACCENT, spaceAfter=5, charSpace=1.5),
    "rec_meta":      mk("rm",  fontName=LATO_I, fontSize=9,  leading=13, textColor=C_MID,    spaceAfter=4),
    "rec_intro":     mk("ri",  fontName=LATO_I, fontSize=10.5,leading=16.5,textColor=C_MID,  alignment=TA_JUSTIFY, spaceAfter=12),
    "sec_label":     mk("sl",  fontName=RAL_B,  fontSize=7,  leading=10, textColor=C_ACCENT, spaceAfter=4, charSpace=2),
    "ingredient":    mk("ing", fontName=LATO,   fontSize=10.5,leading=16,textColor=C_BLACK,  leftIndent=10, spaceAfter=2),
    "sub_head":      mk("sh",  fontName=LATO_B, fontSize=10, leading=14, textColor=C_BLACK,  spaceBefore=8, spaceAfter=3),
    "step_num":      mk("sn",  fontName=LATO_B, fontSize=10.5,leading=16,textColor=C_ACCENT),
    "step_text":     mk("st",  fontName=LATO,   fontSize=10.5,leading=16.5,textColor=C_BLACK,alignment=TA_JUSTIFY, spaceAfter=7),
    "rec_note":      mk("rn",  fontName=LATO_I, fontSize=9.5, leading=14,textColor=C_MID,    spaceBefore=8, spaceAfter=4),
    "rec_tip":       mk("rtip",fontName=LATO_I, fontSize=9,  leading=13, textColor=C_MID,    leftIndent=10, spaceAfter=3),
    "blockquote":    mk("bq",  fontName=LATO_I, fontSize=9.5, leading=14,textColor=C_MID,    leftIndent=14, spaceAfter=4),
    # About
    "about_head":    mk("ah",  fontName=RAL_B,  fontSize=20, leading=26, textColor=C_BLACK,  alignment=TA_CENTER, spaceAfter=14),
    "about_body":    mk("ab",  fontName=LATO,   fontSize=10.5,leading=17,textColor=C_BLACK,  alignment=TA_JUSTIFY, spaceAfter=10),
}


# ── Running footer canvas ─────────────────────────────────────────────────────
class CookbookCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self._page_data   = kwargs.pop("page_data", {})
        self._total_pages = kwargs.pop("total_pages", None)
        super().__init__(*args, **kwargs)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved:
            self.__dict__.update(state)
            self._footer()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _footer(self):
        pg = self._pageNumber
        # Suppress on the 2 leading blanks + cover + edition page (pages 1–4)
        if pg <= 4:
            return
        # Suppress on the 2 trailing blank pages
        if self._total_pages and pg > self._total_pages - 2:
            return
        self.saveState()
        ry = MARGIN_BOTTOM
        self.setStrokeColor(C_LIGHT); self.setLineWidth(0.5)
        self.line(MARGIN_INNER, ry, PAGE_W - MARGIN_OUTER, ry)
        ny = ry - 0.18 * inch
        self.setFont(RAL, 7.5); self.setFillColor(C_MID)
        chap = self._page_data.get(pg, "")
        if pg % 2 == 0:
            self.drawString(MARGIN_INNER, ny, str(pg))
            self.drawCentredString(PAGE_W/2, ny, "From the Kitchen of Debby Kobrosly")
        else:
            self.drawCentredString(PAGE_W/2, ny, chap)
            self.drawRightString(PAGE_W - MARGIN_OUTER, ny, str(pg))
        self.restoreState()


# ── Flowables ─────────────────────────────────────────────────────────────────
from reportlab.platypus import Image as RLImage

def PortraitPhoto(path):
    """Return a centred author photo scaled to fit 2.2×2.8" with aspect ratio preserved."""
    W_MAX, H_MAX = 2.2 * inch, 2.8 * inch
    try:
        img = RLImage(path)
        scale = min(W_MAX / img.imageWidth, H_MAX / img.imageHeight)
        img.drawWidth  = img.imageWidth  * scale
        img.drawHeight = img.imageHeight * scale
        img.hAlign = "CENTER"
        return img
    except Exception:
        # Fallback placeholder if image can't be loaded
        class _Placeholder(Flowable):
            def __init__(self): super().__init__(); self.width=W; self.height=H; self.hAlign="CENTER"
            def draw(self):
                self.canv.setFillColor(C_LIGHT); self.canv.roundRect(0,0,W,H,4,fill=1,stroke=0)
                self.canv.setFont(SERIF_I,9); self.canv.setFillColor(C_MID)
                self.canv.drawCentredString(W/2, H/2-5, "Author Photograph")
        return _Placeholder()


# ── Helper functions ──────────────────────────────────────────────────────────
def hr(story, width="100%", thick=0.5, color=C_LIGHT, before=3, after=3):
    story.append(HRFlowable(width=width, thickness=thick, color=color,
                             hAlign="LEFT", spaceBefore=before, spaceAfter=after))

def accent_hr(story, width="100%", before=0, after=6):
    story.append(HRFlowable(width=width, thickness=0.75, color=C_ACCENT,
                             hAlign="LEFT", spaceBefore=before, spaceAfter=after))

def step_table(story, num, text):
    STS = TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                      ("LEFTPADDING",(0,0),(-1,-1),0),
                      ("RIGHTPADDING",(0,0),(-1,-1),0),
                      ("BOTTOMPADDING",(0,0),(-1,-1),5)])
    t = Table([[Paragraph(f"{num}.", ST["step_num"]),
                Paragraph(text, ST["step_text"])]],
              colWidths=[0.28*inch, BODY_W - 0.28*inch])
    t.setStyle(STS)
    story.append(t)


# ── Cover ─────────────────────────────────────────────────────────────────────
def build_cover(story):
    story.append(Spacer(1, 0.5*inch))
    story.append(HRFlowable(width="85%", thickness=2,   color=C_ACCENT, hAlign="CENTER", spaceAfter=6))
    story.append(HRFlowable(width="85%", thickness=0.5, color=C_ACCENT, hAlign="CENTER", spaceAfter=0.45*inch))
    story.append(Paragraph("FROM THE KITCHEN OF", ST["cover_from"]))
    story.append(Paragraph("Debby<br/>Kobrosly",  ST["cover_title"]))
    story.append(Spacer(1, 0.12*inch))
    story.append(Paragraph("A Collection of Family Recipes", ST["cover_sub"]))
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("✦", ParagraphStyle("orn", fontName="DejaVuSans", fontSize=18,
        textColor=C_LIGHT, alignment=TA_CENTER, spaceAfter=0.4*inch)))
    story.append(Paragraph(
        "Cherished dishes passed down through generations,\n"
        "gathered with love for family and friends.", ST["cover_tag"]))
    story.append(Spacer(1, 0.6*inch))
    story.append(HRFlowable(width="85%", thickness=0.5, color=C_ACCENT, hAlign="CENTER", spaceAfter=6))
    story.append(HRFlowable(width="85%", thickness=2,   color=C_ACCENT, hAlign="CENTER"))
    story.append(PageBreak())


# ── Edition / copyright-style page ───────────────────────────────────────────
_EDITION_SMALL = mk("ed_sm", fontName=LATO, fontSize=8.5, leading=13,
                    textColor=C_MID, alignment=TA_LEFT, spaceAfter=8)
_EDITION_URL   = mk("ed_url", fontName=LATO, fontSize=8.5, leading=13,
                    textColor=C_MID, alignment=TA_LEFT, spaceAfter=0)

def build_edition_page(story):
    """Verso-style edition/license page — small Lato text anchored to bottom-left."""
    # Large spacer pushes text block to the bottom of the page
    story.append(Spacer(1, 4.0 * inch))
    story.append(Paragraph("v1.0.0 · May 1, 2026", _EDITION_SMALL))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph("Lulu Press, Inc., Morrisville, North Carolina", _EDITION_SMALL))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A free PDF copy of <i>From the Kitchen of Debby Kobrosly: "
        "A Collection of Family Recipes</i> is available at:",
        _EDITION_SMALL))
    story.append(Paragraph(
        "https://github.com/ronikobrosly/debby_cookbook/tree/main/output",
        _EDITION_URL))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "This book and its recipes are released under the MIT License. "
        "The MIT License grants anyone the freedom to use, copy, modify, merge, "
        "publish, distribute, sublicense, and/or sell copies of this work, provided "
        "that this source notice appears in all copies or substantial portions of the work. "
        "The work is provided “as is,” without warranty of any kind, express or implied.",
        _EDITION_SMALL))
    story.append(PageBreak())


# ── TOC chapter/recipe data (shared between TOC and body) ─────────────────────
TOC_CHAPTERS = [
    ("1", "Appetizers, Dips and Snacks", [
        "Greek Pies","Cheese Pies","Kishk and Walnuts Pies","Dough for Spinach Pies",
        "Aisha Shervani's Samosas","Aisha Shervani's Potato Pancake","Chili Peanuts & Pumpkin Snack Mix",
        "Seasoned Nuts","Pimiento Cheese","Spinach-Parmesan Dip",
        "Light & Fluffy Zucchini Slice","Sylvie Shirazi's Turmeric Roasted Cauliflower Poppers",
        "Sweet Corn Hush Puppies with Lime-Cilantro Aioli","Falafel",
        "Pickling Fresh Green Olives","Pickled Turnips"]),
    ("2", "Salads and Fruits", [
        "Honey Lime Rainbow Fruit Salad","Mediterranean Bread Salad (Chickpea Panzanella)",
        "Spinach-Apple Salad with Maple-Cider Vinaigrette",
        "Southwestern Chopped Salad with Cilantro Lime Dressing",
        "Black Bean and Corn Salad","Thanksgiving Slaw",
        "Viral Dressing Recipe (Winter Chopped Salad)"]),
    ("3", "Breakfast", [
        "Pat Cappola's Buttermilk Waffles","Scrambled Tofu","Breakfast Egg Muffins 3 Ways",
        "Farmers' Market Frittata","Zucchini & Cheddar Frittata","Hash Browns"]),
    ("4", "Soups and Stews", [
        "Spicy Black Bean Soup","Butternut Soup with Cumin",
        "Creamy Potato Cheese Soup","Pat Moussa's Green Pea Soup","Minestrone Soup",
        "Tomato Basil Soup","Red Lentil Soup with Lemon",
        "Lentil Soup (Brown Whole Lentils)"]),
    ("5", "Vegetables and Sides", [
        "Spicy Oven Roasted Sweet Potato Fries","Quinoa Stuffed Peppers",
        "Corn Casserole (Mom's)","Garlic Parmesan Sautéed Shaved Brussels Sprouts",
        "Rosemary Garlic Hasselback Potatoes","Spanish Rice",
        "Fresh Herb & Lemon Bulgur Pilaf","Corn Cakes","Grilled Potatoes"]),
    ("6", "Sauces and Salad Dressings", [
        "Authentic Homemade Ranchero Sauce"]),
    ("7", "Pasta and Grains", [
        "Linda Bailey's Manicotti","Pastitso Casserole","Roni's Curried Rice Patties","Curried Quinoa",
        "Rice Pudding","Kushari","Mediterranean Pasta with Fire Roasted Tomatoes",
        "Fettuccine with Pistachio-Mint Pesto and Tomatoes",
        "Garlic-and-Herb Pasta with Broccoli Rabe","Homemade Pasta"]),
    ("8", "Seafood", [
        "Samkeh Harra (Baked Spicy Fish)","Shrimp & Mango Skewers",
        "One-Pan Skillet Shrimp Destin with Orzo","Baked Cod with Panko",
        "Almond-Crusted Tilapia","Spicy Shrimp Lo Mein",
        "20-Minute Skillet Blackened Shrimp Fajitas"]),
    ("9", "Poultry", [
        "Blackened Chicken","Joann Hartman's Chicken Kabobs","Honey Fried Chicken",
        "Jewel of the Nile Chicken Kabobs","Linda Bailey's Chicken Parmesan",
        "Pollo Con Pico De Gallo","Shawarma Chicken","Linda Bailey's Sticky Roasted Chicken",
        "Chicken Enchilada","Creamy Chicken Quesadillas","Cornell Chicken",
        "Turkish Yogurt Chicken Kebabs with Aleppo Pepper",
        "Chicken Chimichangas"]),
    ("10", "Meats", ["Amal's Shawarma Beef"]),
    ("11", "Vegetarian Mains", [
        "Grilled Tofu Steaks","Fül Medamis (Instant Pot)",
        "Fül Medamis (Pressure Cooker)","Lentils Medamis","Cauliflower Pizza Crust"]),
    ("12", "Bread", [
        "Orange-Date Muffins","Orange Spice Muffins","Pear-Walnut Muffins",
        "Raisin Bran Muffins","Lemon Poppy Seed Muffins","Morning Glory Muffins",
        "Sour Cream Lemon Muffins","Pumpkin-Cranberry Muffins",
        "Budapest Tea Bread","Best Ever Zucchini Bread",
        "Homemade Cinnamon Swirl Bread","Hot Bread Nan-e Barbari Persian Flatbread",
        "Ridiculously Easy Almond Croissants","Sullivan Street Bakery Bread",
        "No-Knead Harvest Bread","Chai-Spiced Banana Bread",
        "Pistachio Cardamom Loaf","Best Lemon Loaf (Starbucks Copycat)","Date Nut Bread"]),
    ("13", "Cakes, Cookies and Cupcakes", [
        "Old-Fashioned Buttermilk Pound Cake","Cinnamon Crown Cake",
        "Coconut Carrot Cake","Dark Chocolate Cake","Hummingbird Cake",
        "Italian Cake (Mom's)","Grandma Sabol's Lemon-Lime Refrigerator Sheet Cake",
        "Pistachio Cake – Mom's","Pistachio Cake – Linda Bailey",
        "Pat Holloway's Sour Cream Coffee Cake","Orange Walnut Cake",
        "Sour Cream Chocolate Pound Cake","Italian Almond Ricotta Cake, My Way",
        "Brownies","Marta Baldelli's Italian Cookie","Press Cookie",
        "Russian Tea Cakes","Snickerdoodles","Peppermint Crunch Bark",
        "Pecan Tassie Tarts","Almond Biscotti"]),
    ("14", "Desserts", [
        "Apple Dumplings (Grandma Sabol's)","Cinnamon Rolls (Mom)",
        "Bavarian Apple Torte","Claudette Murray's Cheesecake Supreme","Mini Blueberry Cups",
        "Molten Chocolate Lava Cakes","Watermelon Granita","Blackberry Sorbet",
        "Strawberry Banana Ice Cream","Creamy Mango Sorbet","Pie Crust",
        "Italian Waffle Pizzelles","Mary Hemeida's Namoura","Aishi Shervani's Namoura",
        "Sfoof Cake","Atayef (Pancake Batter)","Ashta Cream",
        "Qudrat Al Qader","Meghli","Rice Pudding"]),
]

def _make_label(text):
    """Convert a title string to a stable dict key."""
    return text.lower().replace(" ", "_").replace("/","_").replace("'","").replace("(","").replace(")","").replace("–","")[:60]


# ── Labeled Paragraph (carries a registry key for page tracking) ───────────────
class LabeledParagraph(Paragraph):
    def __init__(self, text, style, label=None):
        super().__init__(text, style)
        self._label = label


# ── Tracking document template ─────────────────────────────────────────────────
class TrackingDoc(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        self.page_registry = {}   # label -> page number
        self._chapter_pages = {}  # page number -> chapter title (for footer)
        super().__init__(*args, **kwargs)

    def afterFlowable(self, flowable):
        if hasattr(flowable, '_label') and flowable._label:
            self.page_registry[flowable._label] = self.page


# ── TOC ───────────────────────────────────────────────────────────────────────
def build_toc(story, registry=None):
    """
    registry: dict of label -> page_number (None on first pass → show blank).
    """
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Contents", ST["toc_head"]))
    story.append(Spacer(1, 0.1*inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_LIGHT,
                             hAlign="CENTER", spaceAfter=16))

    COLS = [3.6*inch, 0.9*inch]
    TS = TableStyle([
        ("VALIGN",   (0,0),(-1,-1),"TOP"),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),
    ])

    def pg_str(label):
        if registry and label in registry:
            return str(registry[label])
        return ""

    for num, title, recipes in TOC_CHAPTERS:
        ch_label = _make_label(f"ch_{num}_{title}")
        pg = Paragraph(pg_str(ch_label), ST["toc_pg"])
        t = Table([[Paragraph(f"Chapter {num} — {title}", ST["toc_ch"]), pg]],
                  colWidths=COLS)
        t.setStyle(TS); story.append(t)
        for r in recipes:
            rec_label = _make_label(r)
            pg = Paragraph(pg_str(rec_label), ST["toc_pg"])
            t = Table([[Paragraph(r, ST["toc_rec"]), pg]], colWidths=COLS)
            t.setStyle(TS); story.append(t)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 0.15*inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_LIGHT,
                             hAlign="CENTER", spaceAfter=8))
    about_label = "about_the_author"
    pg = Paragraph(pg_str(about_label), ST["toc_pg"])
    t = Table([[Paragraph("About the Author", ST["toc_ch"]), pg]], colWidths=COLS)
    t.setStyle(TS); story.append(t)
    story.append(PageBreak())


# ── Chapter opener ────────────────────────────────────────────────────────────
def chapter_opener(story, num, title, tag=""):
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph(f"Chapter {num}", ST["ch_num"]))
    ch_label = _make_label(f"ch_{num}_{title}")
    story.append(LabeledParagraph(title, ST["ch_title"], label=ch_label))
    story.append(HRFlowable(width="50%", thickness=0.75, color=C_ACCENT,
                             hAlign="CENTER", spaceBefore=6, spaceAfter=12))
    intro = tag if tag else "ADD CHAPTER INTRO TEXT HERE"
    story.append(Paragraph(intro, ST["ch_intro"]))
    story.append(PageBreak())


# ── Recipe builder ────────────────────────────────────────────────────────────
def recipe(story, title, yld=None, meta=None, source=None, intro=None,
           sections=None, notes=None, tips=None, variations=None):
    """
    sections: list of dicts with keys:
        - 'head': optional sub-heading (str)
        - 'ingredients': list of str
        - 'steps': list of str (numbered) or str paragraphs
        - 'type': 'ingredients' | 'steps' | 'para' | 'blockquote'
    """
    block = []
    rec_label = _make_label(title)
    block.append(LabeledParagraph(title, ST["rec_title"], label=rec_label))
    block.append(HRFlowable(width="100%", thickness=0.75, color=C_ACCENT,
                             hAlign="LEFT", spaceAfter=5))
    if yld:
        block.append(Paragraph(yld.upper(), ST["rec_yield"]))
    if meta:
        block.append(Paragraph(meta, ST["rec_meta"]))
    if source:
        block.append(Paragraph(f"<i>{source}</i>", ST["rec_meta"]))
    if intro:
        block.append(Paragraph(intro, ST["rec_intro"]))

    story.extend(block)

    if sections:
        for sec in sections:
            stype = sec.get("type", "ingredients")
            head  = sec.get("head", None)

            if head:
                story.append(Paragraph(head, ST["sub_head"]))

            if stype == "ingredients":
                story.append(Paragraph("INGREDIENTS", ST["sec_label"]))
                hr(story)
                for ing in sec.get("items", []):
                    story.append(Paragraph(f"• {ing}", ST["ingredient"]))
                story.append(Spacer(1, 10))

            elif stype == "steps":
                story.append(Paragraph("METHOD", ST["sec_label"]))
                hr(story)
                for i, s in enumerate(sec.get("items", []), 1):
                    step_table(story, i, s)

            elif stype == "para":
                for p in sec.get("items", []):
                    story.append(Paragraph(p, ST["step_text"]))

            elif stype == "blockquote":
                for p in sec.get("items", []):
                    story.append(Paragraph(p, ST["blockquote"]))

    if notes:
        hr(story, width="40%", before=8)
        for n in (notes if isinstance(notes, list) else [notes]):
            story.append(Paragraph(f"<i>Note: {n}</i>", ST["rec_note"]))
    if tips:
        for t in (tips if isinstance(tips, list) else [tips]):
            story.append(Paragraph(f"<i>Tip: {t}</i>", ST["rec_tip"]))
    if variations:
        hr(story, width="40%", before=6)
        story.append(Paragraph("<i>Variations: " + variations + "</i>", ST["rec_note"]))

    story.append(PageBreak())


# ── About ─────────────────────────────────────────────────────────────────────
def build_about(story, photo_path):
    story.append(Spacer(1, 0.5*inch))
    story.append(LabeledParagraph("About the Author", ST["about_head"], label="about_the_author"))
    story.append(HRFlowable(width="60%", thickness=0.75, color=C_ACCENT,
                             hAlign="CENTER", spaceBefore=4, spaceAfter=20))
    story.append(PortraitPhoto(photo_path))
    story.append(Spacer(1, 0.25*inch))
    story.append(Paragraph("Debby was born in Johnson City, NY and lives in Austin, TX with her husband Walid. She has two sons Roni and Danny, and grandchildren Noah and Cora.", ST["about_body"]))
    story.append(Spacer(1, 0.25*inch))
    story.append(Paragraph("She is a true master of flavors, weaving together aromatic herbs and rich textures. Beyond making friends and family feel at home with her food, she loves traveling, exploring other cultures, and reading.", ST["about_body"]))


# ══════════════════════════════════════════════════════════════════════════════
#  RECIPE DATA
# ══════════════════════════════════════════════════════════════════════════════

def add_all_recipes(story):

    # ── CHAPTER 1 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "1", "Appetizers, Dips and Snacks",
        tag="A great meal starts long before the main course. From flaky Cheese Pies and crispy Falafel to a last-minute bowl of Seasoned Nuts, these are the bites that set the tone — and empty the fastest.")

    recipe(story, "Greek Pies",
        sections=[
            {"type":"ingredients","items":[
                "1 package phyllo dough","1 package fresh spinach",
                "Large onions, sliced","3 or 4 stalks celery",
                "2 bunches of green onion","1 bunch of parsley","Fresh dill",
                "2 sticks of butter","1 cup Crisco"]},
            {"type":"steps","items":[
                "In a large pot, pour ¼ cup of olive oil and canola oil.",
                "Slice 3 large onions and add celery stalk (cut up and skin off), green onions (cut up), parsley (cut up), salt, pepper, fresh dill and sauté.",
                "Add cut up spinach.",
                "Cook down mixture.",
                "Cool and drain excess liquid.",
                "After mixture is cool, add some cheese mixture (see Cheese Pies).",
                "Brush cookie pans with butter.",
                "Brush phyllo with mixture of melted 2 sticks butter and Crisco. Assemble layers and bake at 350°F for 20–30 minutes."]}])

    recipe(story, "Cheese Pies",
        notes="You can assemble the pies and freeze them, then later bake as directed.",
        sections=[
            {"type":"ingredients","items":[
                "1 small container large curd cottage cheese",
                "8 oz. cream cheese, grated","½ pound Feta cheese, grated",
                "16 oz. ricotta cheese","6 to 8 eggs","Salt & pepper"]},
            {"type":"steps","items":[
                "Mix all ingredients. Add some mixture to the spinach pies.",
                "Cut phyllo dough into strips. Assemble 2 layers of phyllo dough, brush with butter, and add 2 more layers of dough.",
                "Add heaping spoon of either spinach or cheese mixture and fold up like a flag.",
                "Place pie on the buttered pans. Bake at 350°F for 20 to 30 minutes."]}])

    recipe(story, "Kishk and Walnuts Pies",
        sections=[
            {"type":"ingredients","items":[
                "1 cup kishk","½ cup crushed walnuts",
                "1 tsp. tomato paste","Vegetable oil",
                "Hot spice or minced hot pepper","Onion mixed with salt and cinnamon"]},
            {"type":"steps","items":[
                "Mix all ingredients, add to dough and bake."]}])

    recipe(story, "Dough for Spinach Pies",
        sections=[
            {"type":"ingredients","items":[
                "3 cups flour","¼ cup olive oil","2 tbsp. vegetable oil",
                "1 tbsp. yeast","½ cup warm water","½ tsp. sugar","½ tsp. salt"]},
            {"type":"steps","items":[
                "Mix flour, salt and oils together in food processor.",
                "Mix yeast and sugar, then add warm water to mixture.",
                "Add the water and yeast mixture to the flour. Add more water to get the right consistency.",
                "Knead the dough mixture by hand. Let rise."]}])

    recipe(story, "Aisha Shervani's Samosas",
        notes="Filling can be made up to two days in advance.",
        sections=[
            {"type":"ingredients","items":[
                "4 tbsp. vegetable oil","2 tsp. coriander seed",
                "½ cup finely chopped onions","1½ tsp. finely chopped ginger root",
                "7 medium potatoes, boiled","½ cup cooked peas",
                "2–3 green chilies, chopped","½ tsp. red pepper","Salt",
                "Fresh tortillas for assembling"]},
            {"type":"steps","items":[
                "Heat oil and add coriander seed; fry till light brown.",
                "Add onions & ginger root; fry 4 to 5 minutes.",
                "Add slightly smashed potatoes and peas until potatoes begin to dry.",
                "Add remaining ingredients and salt. Set aside.",
                "Use fresh tortilla to assemble samosa. Fry."]}])

    recipe(story, "Aisha Shervani's Potato Pancake",
        sections=[
            {"type":"ingredients","items":[
                "Potatoes, cooked and skin peeled","5 or 6 green onions",
                "Half bunch of fresh coriander, cut up","1 tsp. cumin",
                "1 tsp. coriander","½ tsp. diced chilies","Salt","Oil for frying"]},
            {"type":"steps","items":[
                "Mash potatoes and add cumin, coriander, diced chilies, and salt.",
                "Add onions and fresh coriander.",
                "Make into patties.",
                "Drizzle some oil on a Teflon pan and fry. Flip and cook until light brown."]}])

    recipe(story, "Chili Peanuts & Pumpkin Snack Mix",
        notes="Keep in airtight storage for up to one week.",
        sections=[
            {"type":"ingredients","items":[
                "2 cups unsalted dry roasted peanuts","2 tbsp. fresh lime juice",
                "2 tsp. chili powder","1 tsp. salt","1 cup unsalted pumpkin seeds",
                "½ cup golden raisins","½ cup chopped dried apricots"]},
            {"type":"steps","items":[
                "Preheat oven to 250°F. Position rack in the middle.",
                "In a medium bowl, toss peanuts with the lime juice until moistened. Sprinkle evenly with chili powder; toss until coated.",
                "Spread nuts on a baking sheet. Bake 20 to 30 minutes till the chili powder has formed a light crust.",
                "Remove from oven & sprinkle with salt.",
                "Place pumpkin seeds in a large skillet over medium heat. When the first seed pops, stir constantly until all seeds have gone from flat to round, about 5 minutes.",
                "Combine pumpkin seeds with peanuts, raisins and apricots."]}])

    recipe(story, "Seasoned Nuts",
        intro="Perfect for November and December.",
        sections=[
            {"type":"ingredients","items":[
                "1 egg white","2 tbsp. water","1 lb. pecans","1 cup white sugar",
                "½ cup brown sugar","1 tsp. cinnamon","½ tsp. nutmeg","½ tsp. salt"]},
            {"type":"steps","items":[
                "Beat egg whites & add water until frothy. Pour over nuts & stir well.",
                "Mix all the seasoning. Add to nuts. Again stir well.",
                "Coat all & spread on cookie sheet.",
                "Bake at 250°F for 45 minutes. Stir occasionally.",
                "Remove to wax paper when cooled."]}])

    recipe(story, "Pimiento Cheese",
        intro="Cut recipe in half — good for 8–10 mason jars.",
        sections=[
            {"type":"ingredients","items":[
                "½ lb. cream cheese","½ lb. Monterey cheese, grated",
                "½ lb. cheddar cheese, grated","1 cup mayo",
                "1 cup red pepper, roasted, seeded & chopped",
                "1 tsp. Worcestershire sauce","1 tsp. sherry vinegar","½ tsp. salt"]},
            {"type":"steps","items":[
                "Whisk together all ingredients in mixer.",
                "Store in refrigerator. Serve with chips."]}])

    recipe(story, "Spinach-Parmesan Dip",
        yld="2 cups (serving size: ¼ cup)",
        notes="Serve with crudités or hearty wheat crackers.",
        sections=[
            {"type":"ingredients","items":[
                "1 tsp. olive oil","3 garlic cloves, chopped","¼ tsp. salt",
                "1 (10 oz.) package fresh spinach","½ cup basil leaves, loosely packed",
                "⅓ cup ⅓-less-fat cream cheese, softened","⅛ tsp. black pepper",
                "⅓ cup plain fat-free yogurt","¼ cup grated fresh Parmesan cheese"]},
            {"type":"steps","items":[
                "Heat olive oil in a large skillet over medium-high heat. Add garlic; sauté 1 minute. Add salt and spinach; sauté 3 minutes or until the spinach wilts. Place spinach mixture in a colander, pressing until mixture is barely moist.",
                "Place spinach mixture, basil, cream cheese, and pepper in a food processor; process until smooth. Spoon spinach mixture into a medium bowl. Add yogurt and Parmesan; stir to combine. Chill."]}])

    recipe(story, "Light & Fluffy Zucchini Slice",
        sections=[
            {"type":"ingredients","items":[
                "3 cups grated zucchini, well drained (about 1–2 zucchini)",
                "3 slices Applewood smoked bacon, diced into ½-inch pieces",
                "1 small red onion, roughly chopped","5 eggs","½ cup olive oil",
                "Freshly ground black pepper","1 cup flour","2 tsp. baking powder",
                "⅔ cup crumbled goat cheese"]},
            {"type":"steps","items":[
                "Preheat oven to 350°F. Line an 8×8 square pan with parchment paper. Coat with cooking spray.",
                "Using a box grater, shred the zucchini. Line a bowl with a clean kitchen towel and place the zucchini inside. Twist to close, and squeeze out as much liquid as possible. Set aside.",
                "In a large nonstick skillet, sauté the bacon over medium-low heat, about 2–3 minutes. Add the onion and continue to cook until soft.",
                "Crack the eggs into a large bowl. Add the olive oil. Season with black pepper and whisk well to combine. Toss in the sautéed bacon and onions, and the reserved zucchini.",
                "Add the flour and baking powder. Continue to mix until it looks like pancake batter.",
                "Pour into lined baking pan. Sprinkle the goat cheese over the top.",
                "Bake until set and golden."]}])

    recipe(story, "Sylvie Shirazi's Turmeric Roasted Cauliflower Poppers",
        sections=[
            {"type":"ingredients","head":"Turmeric Roasted Cauliflower","items":[
                "3 tbsp. coconut oil, melted","1 tbsp. turmeric powder",
                "1-inch piece of fresh ginger, finely grated",
                "1 clove of garlic, finely grated","1 tsp. sea salt",
                "¼ tsp. freshly ground black pepper",
                "1 large or 2 small heads of cauliflower, cored and cut into florets"]},
            {"type":"ingredients","head":"Cilantro Chutney","items":[
                "1 small bunch of cilantro, stems removed",
                "1 small green onion, chopped","1 small clove of garlic, chopped",
                "1 Serrano (or jalapeño) pepper, chopped","1 tsp. fresh lemon juice",
                "¼ cup full-fat yogurt"]},
            {"type":"steps","items":[
                "Preheat oven to 425°F. In a small bowl, combine the oil, turmeric, ginger, garlic, salt and pepper.",
                "Place cauliflower florets on a rimmed baking sheet, toss with spiced oil to coat. Spread out in an even layer and roast for about 20–25 minutes, until tender and lightly golden.",
                "Meanwhile, make the cilantro chutney by placing the cilantro, green onion, garlic and pepper into a small food processor. Pulse until finely chopped, then add the lemon juice and yogurt and pulse again until combined.",
                "Transfer the cauliflower to a large serving bowl and serve with chutney on the side."]}])

    recipe(story, "Sweet Corn Hush Puppies with Lime-Cilantro Aioli",
        yld="12 hush puppies",
        sections=[
            {"type":"ingredients","head":"Hush Puppies","items":[
                "2 ears of corn","1 cup cornmeal","½ cup all-purpose flour",
                "1 tbsp. granulated sugar","2 tsp. baking powder","¾ tsp. salt",
                "¼ tsp. cayenne","½ cup plus 2 tbsp. buttermilk",
                "1 tbsp. unsalted butter, melted","1 tsp. hot sauce",
                "2 tbsp. chopped scallions","Vegetable oil for frying"]},
            {"type":"ingredients","head":"Lime-Cilantro Aioli (make ahead)","items":[
                "2 tbsp. chopped cilantro","½ cup mayonnaise",
                "Zest of 1 lime","4 tsp. lime juice"]},
            {"type":"steps","items":[
                "Slice off corn kernels. Stir cornmeal, flour, sugar, baking powder, salt, and cayenne in a medium bowl. Add buttermilk, melted butter, hot sauce, corn, and scallions, and stir until just combined.",
                "Pour 2 inches of oil into a heavy-duty pot. Heat over medium-high heat until temperature reaches 375°F. Working in batches, gently roll dough into 1½-inch sized balls and carefully lower into hot oil. Do not crowd pot. Fry until golden brown and cooked through, 2–3 minutes.",
                "Lime-Cilantro Aioli: Whisk together all ingredients in a small bowl. Store in refrigerator overnight. Serve with hush puppies."]}])

    recipe(story, "Falafel",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. fava beans, soaked overnight and ground",
                "3 lbs. chickpeas, soaked overnight and ground",
                "½ medium onion","5 garlic cloves",
                "1 heaping tsp. falafel spice mix","1 tsp. salt",
                "1 tsp. rice flour","2 tbsp. water",
                "½ tsp. baking soda (added just before frying)",
                "2 tbsp. water (added just before frying)","Oil for frying"]},
            {"type":"steps","items":[
                "Soak fava beans and chickpeas overnight. Grind them together halfway (not fully smooth). Portion into quart-size freezer bags and freeze.",
                "Thaw one quart-size bag of the ground fava bean and chickpea mixture and add to a food processor.",
                "Add onion, garlic, falafel spice mix, salt, rice flour, and 2 tbsp. water. Process vegetables first, then add the fava and chickpea mixture on top. Mix until paste-like. Cover and refrigerate for at least 1 hour.",
                "Just before frying, add ½ tsp. baking soda and 2 tbsp. water to the falafel mixture. Stir until the mixture becomes slightly gummy.",
                "Fry falafel in hot oil until crisp. Do not overcrowd the pan."]}])

    recipe(story, "Pickling Fresh Green Olives",
        sections=[
            {"type":"ingredients","items":[
                "1.3 lbs. fresh raw green olives per jar",
                "2 cups brine per jar (20:1 water-to-pickling-salt ratio)",
                "½ jalapeño pepper per jar",
                "2 slices of lemon per jar, plus 2 additional slices for the top"]},
            {"type":"steps","items":[
                "Prepare the brine: starting with a 20:1 water-to-pickling-salt ratio, add salt gradually and stir. Stop adding salt when a submerged raw egg slowly and partially floats to the top.",
                "Sterilize the brine by bringing it to a boil. Let it cool completely before using.",
                "Add ½ jalapeño pepper and 2 lemon slices to each jar, then pack in the olives.",
                "Pour cooled brine over the olives. Place 2 additional lemon slices on top of the jar before closing to help prevent spoilage."]}])

    recipe(story, "Pickled Turnips",
        sections=[
            {"type":"ingredients","items":[
                "Turnips, peeled and sliced","2 cups water",
                "1 cup white vinegar","2 tbsp. pickling salt",
                "1 Serrano pepper",
                "2 large slices of beets (for color and to prevent spoilage)"]},
            {"type":"steps","items":[
                "Pack sliced turnips and the Serrano pepper into a sterilized jar.",
                "Combine water, vinegar, and pickling salt; stir until salt dissolves.",
                "Pour brine over turnips. Place beet slices on top of the jar before closing to lend a pink color and help prevent spoilage."]}])

    # ── CHAPTER 2 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "2", "Salads and Fruits",
        tag="Proof that a salad can be the best thing on the table. The Southwestern Chopped Salad with Cilantro Lime Dressing has a way of disappearing before dinner is even ready.")

    recipe(story, "Honey Lime Rainbow Fruit Salad",
        notes="Fruit can be chopped 1 day in advance (except banana) and dressing can be made 1 day in advance; keep separate and chilled, then toss together just before serving.",
        sections=[
            {"type":"ingredients","head":"Fruit","items":[
                "1 lb. fresh strawberries, chopped",
                "1 lb. chopped fresh pineapple","12 oz. fresh blueberries",
                "12 oz. red grapes, sliced into halves","4 kiwis, peeled and chopped",
                "3 mandarin oranges (or 1 can mandarin oranges, drained)",
                "2 bananas, sliced (optional)"]},
            {"type":"ingredients","head":"Honey Lime Dressing","items":[
                "¼ cup honey","2 tsp. lime zest (zest of 2 medium limes)",
                "1½ tbsp. fresh lime juice"]},
            {"type":"steps","items":[
                "Add all fruit to a large mixing bowl.",
                "In a small mixing bowl, whisk together the honey, lime zest and lime juice.",
                "Pour over fruit and toss to evenly coat. Serve immediately."]}])

    recipe(story, "Mediterranean Bread Salad (Chickpea Panzanella)",
        sections=[
            {"type":"ingredients","items":[
                "1 (8 oz.) ciabatta loaf","2 cups cherry tomatoes, halved",
                "1 (15 oz.) can unsalted chickpeas, drained and rinsed",
                "1 (8.5 oz.) can quartered artichoke hearts, drained",
                "3 oz. feta cheese, crumbled (about ¾ cup)",
                "½ cup thinly sliced red onion",
                "¼ cup chopped fresh basil, plus more for garnish",
                "¼ cup extra-virgin olive oil","1½ tbsp. red wine vinegar",
                "½ tsp. dried oregano","¼ tsp. black pepper","⅛ tsp. kosher salt",
                "Suggested additions: avocado, cucumber & radish"]},
            {"type":"steps","items":[
                "Preheat oven to 350°F. Remove and discard crust from ciabatta; cut bread into ½-inch cubes. Spread bread cubes in an even layer on a baking sheet. Bake at 350°F for 12 minutes or until toasted and golden.",
                "Combine toasted bread, tomatoes, chickpeas, artichoke hearts, feta, onion, and basil in a large bowl.",
                "In a separate smaller bowl, combine oil, vinegar, oregano, pepper, and salt. Stir with a whisk. Pour over salad; toss to combine. Garnish with chopped fresh basil."]}])

    recipe(story, "Spinach-Apple Salad with Maple-Cider Vinaigrette",
        intro="Great make-ahead dish for parties.",
        yld="8 servings",
        notes="Pecans may be made up to 1 week ahead — store in an airtight container. Vinaigrette may be made up to 3 days ahead.",
        sections=[
            {"type":"ingredients","head":"Sugared Curried Pecans","items":[
                "1 (6 oz.) package pecan halves","2 tbsp. butter, melted",
                "3 tbsp. sugar","¼ tsp. ground ginger","¼ tsp. curry powder",
                "⅛ tsp. kosher salt","⅛ tsp. ground red pepper"]},
            {"type":"ingredients","head":"Maple-Cider Vinaigrette","items":[
                "⅓ cup cider vinegar","2 tbsp. pure maple syrup",
                "1 tbsp. Dijon mustard","¼ tsp. kosher salt",
                "¼ tsp. pepper","⅔ cup olive oil"]},
            {"type":"ingredients","head":"Salad","items":[
                "1 (10 oz.) package fresh baby spinach, thoroughly washed",
                "1 Gala apple, thinly sliced","1 small red onion, thinly sliced",
                "1 (4 oz.) package crumbled goat cheese"]},
            {"type":"steps","items":[
                "Prepare Pecans: Preheat oven to 350°F. Toss pecans in butter. Stir together sugar, ginger, curry powder, salt and red pepper in a bowl; add pecans, tossing to coat. Spread in a single layer in a nonstick foil-lined pan. Bake 10 to 13 minutes or until lightly browned and toasted. Cool in pan on a wire rack 20 minutes; separate pecans with a fork.",
                "Prepare Vinaigrette: Whisk together cider vinegar, maple syrup, Dijon mustard, salt and pepper. Gradually whisk in oil until well blended.",
                "Prepare Salad: Combine spinach, apple, red onion and goat cheese in a bowl. Drizzle with desired amount of Maple-Cider Vinaigrette; toss to coat. Sprinkle with pecans."]}])

    recipe(story, "Southwestern Chopped Salad with Cilantro Lime Dressing",
        yld="2 servings",
        sections=[
            {"type":"ingredients","head":"Salad","items":[
                "5 cups chopped romaine lettuce","½ cup cherry tomatoes, halved",
                "½ cup canned corn kernels, drained",
                "½ cup canned black beans, drained and rinsed",
                "2 tbsp. chopped fresh cilantro leaves",
                "1 avocado, halved, seeded, peeled and diced",
                "¼ cup tortilla strips, for garnish"]},
            {"type":"ingredients","head":"Cilantro Lime Dressing","items":[
                "1 cup loosely packed cilantro, stems removed",
                "½ cup plain Greek yogurt","2 cloves garlic",
                "Juice of 1 lime","Pinch of salt","¼ cup olive oil",
                "2 tbsp. apple cider vinegar"]},
            {"type":"steps","items":[
                "To make the cilantro lime dressing, combine cilantro, Greek yogurt, garlic, lime juice and salt in the bowl of a food processor. With the motor running, add olive oil and vinegar in a slow stream until emulsified; set aside.",
                "To assemble the salad, place romaine lettuce in a large bowl; top with tomatoes, corn, black beans and cilantro. Pour the dressing on top of the salad and gently toss to combine. Stir in avocado.",
                "Serve immediately, garnished with tortilla strips, if desired."]}])

    recipe(story, "Black Bean and Corn Salad",
        yld="4 to 6 servings",
        notes="Best to cook your own black beans for texture and flavor. If making ahead, wait to add the avocado until right before serving. Keeps up to 3 days in the fridge.",
        sections=[
            {"type":"ingredients","head":"Dressing","items":[
                "¼ cup fresh lime juice","3 tbsp. avocado oil",
                "1 small garlic clove, grated","½ tsp. ground cumin",
                "¾ tsp. sea salt","Freshly ground black pepper"]},
            {"type":"ingredients","head":"Salad","items":[
                "1½ cups cooked black beans, drained and rinsed",
                "Kernels from 2 ears fresh corn (about 1½ cups)",
                "1 red bell pepper, stemmed, seeded, and diced",
                "½ cup chopped fresh cilantro, plus more for garnish",
                "½ to 1 jalapeño pepper, seeded and diced, or 1 Serrano, sliced",
                "⅓ cup diced red onion","3 tbsp. Cotija cheese",
                "1 ripe but firm avocado, pitted and diced",
                "2 tbsp. toasted pepitas (optional)"]},
            {"type":"steps","items":[
                "In a large mixing bowl, whisk together the lime juice, avocado oil, garlic, cumin, salt, and several grinds of pepper.",
                "Add the black beans, corn, red pepper, cilantro, jalapeño, and red onion and toss to coat.",
                "Fold in the cheese and avocado and season to taste. Sprinkle with cilantro leaves and toasted pepitas, if desired."]}])

    recipe(story, "Thanksgiving Slaw",
        yld="8 servings",
        sections=[
            {"type":"ingredients","head":"Dressing","items":[
                "½ medium red onion","⅓ cup vegetable or olive oil",
                "¼ cup apple cider vinegar","2 tbsp. maple syrup",
                "4 tsp. Dijon mustard","½ tsp. kosher salt"]},
            {"type":"ingredients","head":"Salad","items":[
                "1 small head green cabbage (about 10 cups shredded)",
                "1 bunch fresh parsley","¾ cup toasted, sliced almonds",
                "¾ cup dried cranberries",
                "Kosher salt and freshly ground black pepper"]},
            {"type":"steps","items":[
                "Make the dressing: Finely chop ½ medium red onion and add to a large bowl. Whisk in oil, apple cider vinegar, maple syrup, Dijon mustard, and salt. Let sit for at least 10 minutes for the flavors to meld. Meanwhile, prepare the cabbage.",
                "Make the salad: Cut cabbage into 8 wedges through the core, then cut the core from each piece. Thinly slice the cabbage wedges crosswise to shred. Coarsely chop the parsley leaves. Add shredded cabbage, chopped parsley, toasted almonds, and dried cranberries to the dressing. Toss to combine. Taste and season with salt and pepper as needed."]}])

    recipe(story, "Viral Dressing Recipe (Winter Chopped Salad)",
        notes="Can be served as a main topped with your favorite protein (serves 4) or as a side dish for up to 6 people.",
        sections=[
            {"type":"ingredients","head":"Salad","items":[
                "2 slices sourdough bread","Pinch salt, pepper and garlic powder",
                "1 cup cooked farro (½ cup dry farro)",
                "2 small bunches black/lacinato kale, spines removed & chopped",
                "1 tbsp. olive oil","½ cup candied pecans",
                "½ cup crumbled goat cheese",
                "2 cups thinly sliced Brussels sprouts",
                "1 apple, thinly sliced (Honeycrisp recommended)"]},
            {"type":"ingredients","head":"Dressing","items":[
                "2 tbsp. grainy or Dijon mustard","2 tbsp. red wine vinegar",
                "6 tbsp. olive oil","1 tbsp. liquid honey",
                "1 tsp. salt","½ tsp. ground pepper",
                "1 garlic clove, grated","½ tsp. chili flakes"]},
            {"type":"steps","items":[
                "To prepare the croutons, preheat the oven to 375°F. Cut 2 slices of sourdough bread into cubes, drizzle with olive oil and season with a big pinch of salt, pepper and garlic powder. Bake until golden, about 10–15 minutes.",
                "To prepare the farro, cook as per your package instructions to your preferred doneness. Set aside, cool slightly.",
                "To make the dressing, combine all dressing ingredients in a bowl and whisk. Set aside.",
                "To prepare the kale, add a tablespoon of olive oil and massage with your hands for about a minute to break down some of the tough fibers.",
                "Add your farro to a large serving plate or salad bowl. Add the chopped kale, Brussels sprouts and croutons. Arrange the goat cheese, candied pecans and thinly sliced apples on top.",
                "Drizzle the dressing over, toss and serve."]}])

    # ── CHAPTER 3 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "3", "Breakfast",
        tag="Buttermilk Waffles for the weekends you want to feel like you're doing something right, Breakfast Egg Muffins for the mornings you need to feel like you have it together, and a Farmers' Market Frittata for when you want both.")

    recipe(story, "Pat Cappola's Buttermilk Waffles",
        intro="Can halve the recipe to get 4 waffles.",
        sections=[
            {"type":"ingredients","items":[
                "2 cups all-purpose flour (white whole wheat works well)",
                "2 tbsp. sugar (half white, half brown sugar works well)",
                "2 tsp. baking powder","1 tsp. baking soda","½ tsp. salt",
                "2 cups buttermilk","1 stick unsalted butter, melted",
                "2 large eggs","Vegetable oil or spray for waffle iron"]},
            {"type":"steps","items":[
                "Whisk dry ingredients together in a medium bowl. Set aside.",
                "In a large bowl, whisk together buttermilk, butter, and eggs.",
                "Add flour mixture and mix just until batter is combined.",
                "Heat waffle iron to manufacturer's directions.",
                "Pour or spread batter onto iron, leaving about ½-inch border. For a standard iron, use about a ½ cup dry measuring cup, and thin batter as needed.",
                "Close iron and cook until crisp, about 5 to 6 minutes."]}])

    recipe(story, "Scrambled Tofu",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. extra firm tofu, drained and pressed for more than 1 hour",
                "2 tbsp. olive oil","1 medium onion, chopped",
                "3 cloves garlic, minced",
                "¼ cup red & green peppers, chopped","1 Serrano pepper, chopped",
                "2–3 tsp. cumin","2 tsp. ginger","2 tsp. turmeric",
                "1 tsp. salt","1 tsp. thyme","1 tsp. paprika",
                "½ tsp. cayenne red pepper"]},
            {"type":"steps","items":[
                "Put oil in skillet on medium heat. Sauté onion, garlic and peppers until soft.",
                "Add all spices. Sauté for a few minutes.",
                "Crumble up the tofu into small pieces and put into the skillet.",
                "Sauté everything for another 5 to 10 minutes."]}])

    recipe(story, "Breakfast Egg Muffins 3 Ways",
        yld="12 muffins",
        sections=[
            {"type":"ingredients","head":"Base","items":[
                "12 large eggs",
                "2 tbsp. finely chopped onion (red, white or yellow)",
                "Salt and pepper, to taste"]},
            {"type":"ingredients","head":"Tomato Spinach Mozzarella","items":[
                "¼ cup fresh spinach, roughly chopped",
                "8 grape or cherry tomatoes, halved",
                "¼ cup shredded mozzarella cheese"]},
            {"type":"ingredients","head":"Bacon Cheddar","items":[
                "¼ cup cooked bacon, chopped","¼ cup shredded cheddar cheese"]},
            {"type":"ingredients","head":"Garlic Mushroom Pepper","items":[
                "¼ cup sliced brown mushrooms","¼ cup red bell pepper, diced",
                "1 tbsp. fresh chopped parsley",
                "¼ tsp. garlic powder or ⅓ tsp. minced garlic"]},
            {"type":"steps","items":[
                "Preheat oven to 350°F. Lightly spray a 12-cup capacity muffin tin with nonstick oil spray.",
                "In a large bowl, whisk together eggs and onion. Season with salt and pepper, to taste.",
                "Add egg mixture halfway up into each tin of a greased muffin tin.",
                "Divide the three topping combinations into 4 muffin cups each.",
                "Bake for 20 minutes."]}])

    recipe(story, "Farmers' Market Frittata",
        yld="8 servings",
        sections=[
            {"type":"ingredients","items":[
                "12 large eggs, lightly beaten",
                "8 oz. sharp cheddar cheese, shredded (about 2 cups)",
                "1 cup heavy whipping cream",
                "1 tbsp. chopped fresh chives, plus more for garnish",
                "1½ tsp. kosher salt","½ tsp. black pepper",
                "2 tbsp. olive oil, divided",
                "¾ cup thinly sliced red onion (from 1 small onion)",
                "2 red sweet mini peppers, thinly sliced crosswise (½ cup)",
                "4 cups roughly chopped curly kale leaves (from 1 bunch)",
                "1 large garlic clove, grated","Chopped fresh dill"]},
            {"type":"steps","items":[
                "Preheat oven to 400°F. Whisk together eggs, cheese, cream, chives, salt, and black pepper in a large bowl until combined. Set aside.",
                "Heat 1 tablespoon of the olive oil in a 10-inch cast-iron skillet over medium. Add sliced red onion and peppers; cook, stirring occasionally, until softened, 4 to 6 minutes. Transfer to a plate.",
                "Heat remaining 1 tablespoon olive oil in skillet. Add kale and garlic; cook, stirring often, until kale is wilted, 1 to 2 minutes. Transfer half of kale mixture to a plate, and set aside. Return half of onion and peppers to skillet; stir to combine. Pour egg mixture over vegetables; sprinkle with reserved kale mixture, onion, and peppers. Cook on medium-low until edges are set, 1 to 2 minutes.",
                "Transfer to preheated oven, and bake until center is set, about 20 minutes. Let stand 10 minutes before serving. Garnish with fresh chives and dill."]}])

    recipe(story, "Zucchini & Cheddar Frittata",
        yld="2 to 4 servings",
        notes="Be sure to keep a dish towel over the pan handle after you remove it from the oven. The cooked frittata can be frozen for up to 3 months.",
        sections=[
            {"type":"ingredients","items":[
                "¾ lb. zucchini (about 2 small zucchini)","2 tbsp. unsalted butter",
                "¼ cup finely chopped shallots, from 1–2 shallots",
                "¾ tsp. salt, divided","6 large eggs","¼ cup heavy cream",
                "¼ tsp. freshly ground black pepper",
                "3 oz. (about 1 cup) grated cheddar cheese"]},
            {"type":"steps","items":[
                "Preheat the oven to 325°F.",
                "Using a food processor or box grater, grate the zucchini. Place the grated zucchini on top of several layers of paper towels and wring dry. Repeat 1–2 times to remove any excess moisture.",
                "In an 8 or 10-inch ovenproof, nonstick sauté pan, melt the butter over medium heat. Add the shallot, zucchini and ½ tsp. salt and cook, stirring occasionally, until the moisture evaporates and the zucchini is tender, 6–7 minutes.",
                "Meanwhile, in a medium bowl, whisk together the eggs, heavy cream, remaining ¼ tsp. salt and pepper.",
                "Add the cooked zucchini and grated cheese to the egg mixture and stir to combine. Pour the frittata mixture into the pan (no need to wash it), then place in the oven and bake until set, 20–23 minutes."]}])

    recipe(story, "Hash Browns",
        yld="4 servings",
        sections=[
            {"type":"ingredients","items":[
                "1½ lbs. russet potatoes (about 3 medium), peeled or unpeeled and scrubbed clean",
                "¼ cup olive oil or vegetable oil","Salt and pepper"]},
            {"type":"steps","items":[
                "Shred potatoes on the large holes of a box grater. Transfer to a fine mesh sieve or colander and rinse potatoes while tossing a couple of times. Drain.",
                "Preheat a 12-inch cast iron pan over medium-high heat.",
                "Transfer half of the potatoes to several layers of cheesecloth and squeeze as much liquid out as possible, then spread onto a double layer of paper towels. Repeat with second half of potatoes.",
                "Spread paper towels over potatoes and press dry. Season potatoes with salt and pepper, toss.",
                "Add oil to pan coating bottom evenly then add potatoes and spread even. Press down on potatoes with a spatula to flatten so bottom browns evenly.",
                "Let cook undisturbed about 3–4 minutes until golden brown on bottom, then flip potatoes (in several portions) to opposite side.",
                "Let brown on bottom about 3–4 minutes. Toss once more and let cook until tender, about 2 minutes longer. Serve immediately."]}])

    # ── CHAPTER 4 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "4", "Soups and Stews",
        tag="There's a reason soup has been feeding people for thousands of years: it works. Red Lentil Soup with Lemon, Tomato Basil Soup, and Minestrone are the ones that make the whole house smell like home.")

    recipe(story, "Spicy Black Bean Soup",
        sections=[
            {"type":"ingredients","items":[
                "2 tbsp. oil","½ cup cilantro, chopped",
                "1 cup chopped onion","1 (4 oz.) can diced green chili peppers",
                "1 tbsp. chopped Serrano pepper","1 tbsp. cumin",
                "2 cloves of minced garlic",
                "2 (15 oz.) cans black beans, undrained",
                "2 cups chicken or vegetable broth"]},
            {"type":"steps","items":[
                "Heat oil, add onion, green chilis, garlic, peppers and cumin.",
                "Sauté about 5 minutes.",
                "Add beans with juice and broth.",
                "Bring to a boil and then reduce heat to medium. Cover and simmer for 15 minutes.",
                "Purée soup in batches in a blender. Leave some beans whole.",
                "Return mixture to pot.",
                "Chop ½ cup of fresh cilantro and drop into soup.",
                "Season with salt & pepper."]}])

    recipe(story, "Butternut Soup with Cumin",
        sections=[
            {"type":"ingredients","items":[
                "1 tbsp. olive oil","1 medium onion, chopped",
                "3-lb. butternut squash, peeled & cubed (8 cups)",
                "1 tsp. salt & pepper","1 tsp. cumin",
                "2 cloves garlic, minced","2 tsp. curry powder",
                "3 cups chicken or vegetable broth"]},
            {"type":"steps","items":[
                "Heat oil and stir in onions and garlic. Cover, reduce heat for 10 minutes.",
                "Add squash, salt, pepper, cumin, curry powder and sauté for 10 minutes.",
                "Add broth, bring to a boil. Cover and reduce heat; simmer 30 minutes or until the squash is tender.",
                "Purée soup in blender and return soup to pot. Keep warm."]}])

    recipe(story, "Creamy Potato Cheese Soup",
        sections=[
            {"type":"ingredients","items":[
                "4 tbsp. butter","4 oz. cream cheese",
                "1 cup chopped onion","1½ cups milk",
                "1 cup grated sharp cheddar cheese",
                "1 large garlic clove, minced","2 large red potatoes",
                "1 large carrot, chopped","3 cups vegetable stock",
                "1 tsp. dill","Salt & pepper"]},
            {"type":"steps","items":[
                "Make vegetable stock: use 10 cups water, add 2 potatoes, carrots, celery & onion. Bring to a boil and reduce stock for 1 hour.",
                "In a large pot, sauté onion and garlic in butter.",
                "Add fresh cubed potatoes and chopped carrots. Sauté for 5 to 10 minutes longer.",
                "Add stock and dill; cook until all vegetables are tender.",
                "Cool slightly, put vegetables with broth in blender with cream cheese and milk.",
                "Return mixture to pot. Stir in cheese, salt & pepper. Simmer until cheese is all melted."]}])

    recipe(story, "Pat Moussa's Green Pea Soup",
        sections=[
            {"type":"ingredients","items":[
                "1 package dried split peas, cleaned and washed",
                "1 large onion, chopped","2 tbsp. olive oil",
                "3 medium sized potatoes, peeled and chopped",
                "3 carrots, peeled and chopped","4 cups water",
                "2 tsp. salt","1 tsp. cumin","1 tsp. coriander",
                "½ tsp. pepper","½ tsp. cayenne pepper"]},
            {"type":"steps","items":[
                "In a large pot, sauté chopped onion in olive oil until golden brown.",
                "Add the peas, potatoes, carrots and the water. Bring to a boil, then turn to low heat.",
                "Add the salt, cumin, coriander, pepper and cayenne pepper.",
                "Simmer for 1½ to 2 hours, checking frequently to stir and if necessary add more water to thin out the soup."]}])

    recipe(story, "Minestrone Soup",
        sections=[
            {"type":"ingredients","items":[
                "3 tbsp. olive oil","1½ cups onion, sliced",
                "1 cup carrots, diced","1 cup celery, diced",
                "1 tbsp. garlic, minced","½ cup potatoes, peeled and cubed",
                "1 cup green beans, trimmed and cut","½ cup white beans",
                "½ cup zucchini, diced","½ cup shredded green cabbage",
                "1 (14 oz.) can whole tomatoes, coarsely chopped",
                "10 cups chicken stock",
                "1 tbsp. fresh basil, minced","1 tsp. fresh oregano, minced",
                "1 tsp. fresh thyme leaves","1 tsp. parsley, minced","Salt & pepper"]},
            {"type":"steps","items":[
                "Heat olive oil in a large soup pot. Sauté onions 10 minutes over medium heat.",
                "Add carrots, celery, garlic, potatoes, green beans, zucchini and cabbage. Sauté for five more minutes.",
                "Add tomatoes, chicken stock, beans and herbs.",
                "Simmer 1 hour. Salt and pepper to taste."]}])

    recipe(story, "Tomato Basil Soup",
        sections=[
            {"type":"ingredients","items":[
                "1 (28 oz.) can whole tomatoes","1 (14 oz.) can whole tomatoes",
                "1 can chicken broth","12 fresh leaves of basil",
                "1 cup heavy cream","¼ stick of butter",
                "Salt & pepper to taste","Optional: ¼ cup Parmesan cheese"]},
            {"type":"steps","items":[
                "Combine tomatoes, chicken broth and basil in a saucepan. Simmer for 30 minutes.",
                "Purée ingredients in a blender.",
                "Return mixture back to saucepan and add butter, cream, Parmesan cheese, salt & pepper to taste.",
                "Continue simmering for 20 minutes. Serve."]}])

    recipe(story, "Red Lentil Soup with Lemon",
        sections=[
            {"type":"ingredients","items":[
                "3 tbsp. olive oil","1 large onion, chopped",
                "2 garlic cloves, minced","1 tbsp. tomato paste",
                "1 tsp. cumin","¼ tsp. salt","¼ tsp. black pepper",
                "Pinch of cayenne pepper","1 qt. chicken or vegetable broth",
                "2 cups water","1 cup red lentils","1 carrot, peeled and diced",
                "Juice of ½ lemon","Cilantro, sliced, for garnish"]},
            {"type":"steps","items":[
                "In a pot, heat oil and add onion and garlic. Sauté till golden.",
                "Stir in tomato paste, cumin, salt, pepper, and cayenne and sauté for 2 minutes.",
                "Add broth, water, lentils and carrot. Cover pot and simmer on medium-low until lentils are soft, about 30 minutes.",
                "Taste, add salt if needed.",
                "Use a blender or immersion blender to purée half the soup and return to pot. Soup should be chunky.",
                "Stir in lemon juice and sliced cilantro."]}])

    recipe(story, "Lentil Soup (Brown Whole Lentils)",
        notes="To cook in a regular pot, bring water to a boil, add lentils, then reduce heat and simmer for at least 30 minutes. For Lentils Medamis, cook for 25 minutes, until slightly firm.",
        sections=[
            {"type":"ingredients","items":[
                "2 lbs. brown whole lentils","2½ tbsp. kibbe spice",
                "½ tbsp. cumin","3½ tbsp. salt","¼ cup Egyptian rice",
                "1 bunch fresh parsley, stems removed","1 large onion, chopped"]},
            {"type":"steps","items":[
                "Wash lentils and soak for 1 hour.",
                "Sauté parsley and onion, then add spices.",
                "Cook lentils in a pressure cooker for 5 minutes after the whistle sounds."]}])

    # ── CHAPTER 5 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "5", "Vegetables and Sides",
        tag="Corn Casserole (Mom's) belongs at every holiday table, the Rosemary Garlic Hasselback Potatoes will make you forget every other potato recipe you've ever made, and the Spicy Oven Roasted Sweet Potato Fries are exactly as good as they sound.")

    recipe(story, "Spicy Oven Roasted Sweet Potato Fries",
        sections=[
            {"type":"ingredients","items":[
                "2 tbsp. canola oil",
                "½ to 1 tsp. dry Rogan Josh seasoning or Rogan Josh paste",
                "3 medium sweet potatoes","Salt & pepper to taste"]},
            {"type":"steps","items":[
                "Set oven at 400°F.",
                "In a large bowl, combine the oil and seasoning or paste. Mix with a fork or whisk to release the flavor and color.",
                "Wash the potatoes and pat dry (you can leave the skin on). Slice lengthwise into wedges.",
                "In batches, toss the potatoes in the oil and seasoning until thoroughly coated.",
                "Arrange in a single layer on baking sheet (do not crowd the pan).",
                "Roast for 15 minutes, turn over, and continue roasting for an additional 10 minutes.",
                "Remove when edges are golden brown and fries are tender. Sprinkle with salt & pepper if needed."]}])

    recipe(story, "Quinoa Stuffed Peppers",
        sections=[
            {"type":"ingredients","items":[
                "1 cup raw quinoa","6 medium bell peppers",
                "3 tbsp. olive oil","1 cup chopped onions",
                "3 minced garlic cloves","1½ tsp. ground cumin",
                "1½ tsp. ground coriander","½ tsp. red pepper flakes",
                "½ tsp. salt","1 cup diced carrots","¾ cup diced celery",
                "1 cup diced zucchini","1½ cups fresh corn",
                "Parmesan cheese or grated cheddar cheese"]},
            {"type":"steps","items":[
                "Preheat oven to 400°F. Lightly oil a baking pan.",
                "Rinse quinoa well. In a covered pot, bring 2 cups of water to a boil. Lower heat and simmer about 15 minutes until quinoa is soft and water is absorbed.",
                "Cut bell peppers in half lengthwise, leaving stems on; seed them. Brush shells with about 2 tbsp. oil, inside and out.",
                "Place cut side down on baking sheet and roast for 15 to 20 minutes until soft and slightly brown. Reduce oven to 350°F.",
                "In a skillet, warm remaining oil and sauté onions and garlic on medium heat for about 5 minutes.",
                "Stir in cumin, coriander, red pepper flakes, salt, carrots, celery, zucchini and corn. Cover and cook for 10 minutes until tender.",
                "Combine sautéed vegetables and cooked quinoa; add salt to taste.",
                "Spoon filling into each pepper half. Sprinkle with cheese.",
                "Bake for 10 to 15 minutes until cheese is melted."]}])

    recipe(story, "Corn Casserole (Mom's)",
        sections=[
            {"type":"ingredients","items":[
                "½ cup butter, melted","2 eggs",
                "1 (16 oz.) can whole corn, drained",
                "2 (16 oz.) cans cream style corn",
                "1 (9 oz.) Jiffy Box Corn Muffin mix",
                "1 cup sour cream (use sour cream & onion)"]},
            {"type":"steps","items":[
                "Melt butter and beat eggs together.",
                "Drain whole kernel corn. Combine all ingredients, adding muffin mix last.",
                "Pour mixture into a greased 7×11 baking dish.",
                "Bake at 375°F for 35 to 40 minutes."]}])

    recipe(story, "Garlic Parmesan Sautéed Shaved Brussels Sprouts",
        yld="5 servings",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. Brussels sprouts, ends trimmed and thinly sliced",
                "2 tbsp. olive oil","2 cloves garlic, minced",
                "½ cup finely chopped shallots","Salt to taste",
                "⅓ cup grated Parmesan cheese, plus extra for garnish"]},
            {"type":"steps","items":[
                "Heat the olive oil in a large pan over medium heat. Once hot, add the shaved Brussels sprouts and shallots. Toss around to coat in the oil and cook for 5 minutes.",
                "Season with salt and add garlic. Cook until the garlic is fragrant and the vegetables are tender, about 2 to 3 minutes.",
                "Remove from heat and toss with Parmesan cheese. Garnish with extra Parmesan."]}])

    recipe(story, "Rosemary Garlic Hasselback Potatoes",
        notes="If potatoes begin to get too brown, lightly cover with foil and turn heat down to 400°F until tender. Total baking time is 60 to 70 minutes for medium sized potatoes.",
        sections=[
            {"type":"ingredients","items":[
                "5 Russet or Yukon Gold potatoes, scrubbed, patted dry, not peeled",
                "4 tbsp. olive oil, divided","8 garlic cloves, thinly sliced lengthwise",
                "6 sprigs rosemary","Salt and pepper"]},
            {"type":"steps","items":[
                "Preheat oven to 425°F with a rack in the lower-middle position.",
                "Wash and dry the potatoes — leave thin skins on. Cut thin ⅛-inch slits into the potato, stopping just before you cut through so that the slices stay connected at the bottom.",
                "Slice the garlic very thinly, lengthwise. Slip a piece of garlic in every other slit in the potatoes. Tuck a rosemary leaf or two into the other slits.",
                "Brush the bottom of the baking dish or cast iron skillet with olive oil and sprinkle with salt and pepper.",
                "Brush top and sides of potatoes with 1–2 tbsp. olive oil (reserving 1 tbsp. for brushing again halfway through baking).",
                "Arrange the potatoes in a baking dish and sprinkle generously with salt and pepper.",
                "Bake for 35–40 minutes. At this point, the layers will start separating. Brush the potatoes again with a little oil, making sure some of it drips down into the space between the slices.",
                "Bake for another 25 to 35 minutes, until the potatoes are crispy on the edges and fork tender. Garnish with fresh rosemary leaves."]}])

    recipe(story, "Spanish Rice",
        yld="6 servings",
        sections=[
            {"type":"ingredients","items":[
                "2 tbsp. olive oil","½ onion, minced",
                "2 cloves garlic, minced","1 jalapeño, seeded and minced",
                "2 cups uncooked white rice","3 cups chicken broth",
                "2 tbsp. tomato paste","1 tsp. cumin","1 tsp. salt",
                "½ tsp. pepper","½ tsp. oregano"]},
            {"type":"steps","items":[
                "Heat olive oil in a large skillet over high heat. Add your onions and sauté until tender, about 4–5 minutes.",
                "Add in your garlic, jalapeños, and uncooked rice. Cook, stirring constantly to brown the rice, about 7–8 minutes.",
                "Add the chicken broth, tomato paste, cumin, salt, pepper, and oregano. Whisk to combine.",
                "Bring to a rolling boil, then reduce heat to low, cover, and simmer for 20–25 minutes undisturbed. All the moisture should be absorbed by the rice. Add more time if needed.",
                "Fluff with a fork and serve fresh."]}])

    recipe(story, "Fresh Herb & Lemon Bulgur Pilaf",
        yld="6 servings, about 1 cup each",
        notes="Make ahead: cover and refrigerate up to 2 days; add more lemon juice and/or salt before serving.",
        sections=[
            {"type":"ingredients","items":[
                "2 tbsp. extra-virgin olive oil","2 cups chopped onion",
                "1 clove garlic, finely chopped",
                "1½ cups bulgur, preferably medium or coarse",
                "½ tsp. ground turmeric","½ tsp. ground cumin",
                "2 cups vegetable or chicken broth",
                "1½ cups chopped carrot",
                "2 tsp. grated or finely chopped fresh ginger",
                "1 tsp. coarse salt",
                "¼ cup lightly packed finely chopped fresh dill",
                "¼ cup lightly packed finely chopped fresh mint",
                "¼ cup lightly packed finely chopped flat-leaf parsley",
                "3 tbsp. lemon juice, or more to taste",
                "½ cup chopped walnuts, toasted"]},
            {"type":"steps","items":[
                "Heat oil in a large high-sided skillet over medium heat. Add onion, reduce heat to medium-low and cook, stirring often, until golden brown, 12 to 18 minutes. Stir in garlic and cook for 1 minute. Add bulgur, turmeric and cumin and cook, stirring, until the bulgur is coated with oil, about 1 minute.",
                "Add broth, carrot, ginger and salt and bring to a boil, stirring. Cover and cook over medium-low heat until all the broth is absorbed and there are indentations in the surface of the bulgur, about 15 minutes. Do not stir the pilaf. Remove from the heat and let stand, covered, for 5 minutes.",
                "Stir in dill, mint, parsley and lemon juice. Serve topped with walnuts."]}])

    recipe(story, "Corn Cakes",
        intro="Very good as a side dish.",
        sections=[
            {"type":"ingredients","items":[
                "1 cup cornmeal","½ cup flour","2 tsp. salt",
                "¾ tsp. baking soda","½ tsp. ground pepper",
                "2 tsp. maple syrup","2 tsp. butter","1 egg",
                "1 cup buttermilk","1 cup fresh corn (2 ears)",
                "¼ cup green onion, chopped","1 hot pepper, diced",
                "½ cup grated cheese"]},
            {"type":"steps","items":[
                "Combine cornmeal, flour, salt, baking soda, and pepper in a small bowl.",
                "Whisk butter, maple syrup, egg, and buttermilk together.",
                "Combine the two and add corn, onion, pepper, and cheese.",
                "Heat griddle, melt butter and drop batter in batches. Cook 2–3 minutes each side until golden."]}])

    recipe(story, "Grilled Potatoes",
        notes="Avoid high heat to prevent burning; medium heat for 55 minutes is recommended.",
        sections=[
            {"type":"ingredients","items":[
                "5–6 red potatoes, peeled and sliced",
                "1 small onion, sliced","⅓ stick butter, melted",
                "½ tsp. cayenne pepper","¼ tsp. garlic powder","Salt to taste"]},
            {"type":"steps","items":[
                "Place butter in a large glass bowl, cover with wax paper, and melt in microwave.",
                "Add sliced potatoes, sliced onion, cayenne pepper, and garlic powder to the melted butter. Toss to coat.",
                "Wrap potato mixture tightly in aluminum foil.",
                "Grill over medium heat for approximately 55 minutes, turning once.",
                "Season with salt when cooked."]}])

    # ── CHAPTER 6 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "6", "Sauces and Salad Dressings",
        tag="Short chapter, long flavor. One sauce — the Authentic Homemade Ranchero — is all it takes to transform tacos, eggs, enchiladas, or anything else lucky enough to end up on the same plate.")

    recipe(story, "Authentic Homemade Ranchero Sauce",
        yld="About 3½ cups",
        sections=[
            {"type":"ingredients","items":[
                "1 tbsp. olive oil","1 medium yellow onion, chopped",
                "2 jalapeño peppers, chopped","4 cloves garlic, chopped",
                "16 oz. can diced tomatoes","1 cup chicken broth",
                "¼ cup chopped cilantro, or more as desired",
                "1 tbsp. ancho powder","1 tbsp. guajillo powder",
                "1 tbsp. chipotle powder","1 tsp. cayenne",
                "1 tsp. Mexican oregano","1 tsp. cumin",
                "Salt and pepper to taste","Juice from 1 lime (optional)"]},
            {"type":"steps","items":[
                "Heat a large pan to medium-high heat and add the olive oil.",
                "Cook the onions and peppers down about 5 minutes to soften.",
                "Add the garlic and cook another minute, stirring a bit.",
                "Add the tomato and chicken broth. Stir.",
                "Stir in the cilantro and seasonings.",
                "Bring to a quick boil then reduce the heat and simmer for 20–25 minutes to let the flavors develop. The sauce will thicken up.",
                "Transfer the mixture to a blender or food processor and pour in the lime juice. Process until nice and smooth.",
                "Use immediately or store in the refrigerator in a covered glass container."]}])

    # ── CHAPTER 7 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "7", "Pasta and Grains",
        tag="Comfort in every form. Manicotti for the Sundays that call for something slow and satisfying, Kushari for the weeknights when you want something hearty, and Fettuccine with Pistachio-Mint Pesto for the night someone calls it the best pasta they've ever had.")

    recipe(story, "Linda Bailey's Manicotti",
        sections=[
            {"type":"ingredients","head":"Crepes","items":[
                "1 cup sifted flour","4 eggs (3 for batter, 1 for filling)",
                "1 cup water","Salt","Vegetable oil"]},
            {"type":"ingredients","head":"Filling","items":[
                "½ lb. ricotta cheese","¼ lb. mozzarella cheese, shredded",
                "¼ cup Parmesan cheese","2 tbsp. parsley","Salt & pepper"]},
            {"type":"steps","items":[
                "Beat 3 eggs well, gradually adding flour, beating constantly. Add salt to taste and add water. Stir to make a light batter.",
                "Heat small pan, brush slightly with vegetable oil. Make sure pan is hot. Add 2 tbsp. of batter at a time. Cook crepe on one side only until set, about 1 minute. Don't brown. Transfer to wax paper.",
                "Filling: Combine ricotta, mozzarella (shredded), remaining egg, Parmesan cheese, parsley, salt and pepper.",
                "Place one crepe, uncooked side up, on flat surface. Add 1–2 tbsp. of filling and roll up.",
                "Arrange in baking dish with some spaghetti sauce on bottom. Place crepes, then add sauce on top. Shred some mozzarella cheese on top. Cover with foil.",
                "Bake at 350°F for 45 minutes."]}])

    recipe(story, "Pastitso Casserole",
        sections=[
            {"type":"ingredients","head":"Pasta","items":[
                "8 oz. ziti","1 tbsp. olive oil"]},
            {"type":"ingredients","head":"Meat Filling","items":[
                "1 oz. butter","¾ cup dry red wine (optional)",
                "1 large onion, finely chopped","1½ pounds ground meat",
                "2 tbsp. tomato paste","½ tsp. nutmeg","Salt & pepper",
                "¼ tsp. cinnamon","¼ to ½ cup dried bread crumbs",
                "1½ cups Parmesan cheese"]},
            {"type":"ingredients","head":"Cheese Sauce","items":[
                "4 cups milk","5 oz. butter","⅔ cup flour",
                "¼ tsp. nutmeg","3 egg yolks, beaten"]},
            {"type":"steps","items":[
                "Cook ziti and set aside.",
                "Melt butter in fry pan and sauté onion till soft. Add meat and cook until done.",
                "Add tomato paste to meat mixture. Continue cooking and add nutmeg, salt, pepper. Can add dry wine here. Cook about 30 minutes. If too dry, add some water. Take off heat and cool. Mix ½ bread crumbs with ½ grated cheese. Set aside.",
                "Cream Sauce: Melt butter and add flour, gradually add milk; cook until thick, keep stirring. Remove, and when slightly cooled, stir in egg yolks and ¼ cup cheese.",
                "To assemble: Grease baking dish (13×9) and sprinkle with 2 tbsp. bread crumbs. Spread half of cooked pasta over dish & sprinkle with ¼ cup reserved cheese-bread crumb mixture. Spread all of meat mixture over noodles. Pour ½ of the sauce over the meat and spread rest of pasta over it. Sprinkle with 2 tbsp. cheese. Pour rest of sauce on top and smooth with a spatula. Sprinkle with rest of cheese & bread crumbs. Dot with remaining butter.",
                "Bake at 350°F for 50 to 60 minutes. Let stand for 10 minutes before serving."]}])

    recipe(story, "Roni's Curried Rice Patties",
        sections=[
            {"type":"ingredients","items":[
                "⅓ cup rice","2 tbsp. olive oil","1 small onion, finely chopped",
                "2 garlic cloves, minced","2 tsp. curry powder",
                "1 Serrano pepper, diced","¼ cup red bell pepper, diced",
                "¾ cup frozen peas, thawed","3 green onions, chopped",
                "1 tomato, chopped","1 cup garbanzo beans, drained",
                "1½ cups bread crumbs","1 egg","Salt & pepper",
                "1–2 tbsp. fresh chopped cilantro"]},
            {"type":"steps","items":[
                "Heat oil in a large pan. Add the onion and garlic and cook until beginning to soften.",
                "Stir in the curry powder and Serrano pepper and cook for 2 minutes.",
                "Add the red pepper, peas, green onion and tomato; cook gently for about 7 minutes until tender. Set aside.",
                "Process the garbanzo beans in a food processor until smooth. Add half of the vegetables and process again.",
                "Transfer to a large bowl and add the remaining vegetable mixture, bread crumbs, cilantro and egg. Mix well.",
                "Stir in the cooked rice and season with salt & pepper.",
                "Chill for one hour in the refrigerator, then shape into patties.",
                "Cook the patties in oil for 6 to 8 minutes, until golden."]}])

    recipe(story, "Curried Quinoa",
        sections=[
            {"type":"ingredients","items":[
                "1 cup quinoa","1½ tbsp. oil","½ cup diced onions",
                "1 tsp. grated fresh ginger","⅛ tsp. cayenne",
                "1 diced Serrano pepper","½ tsp. turmeric",
                "½ tsp. ground coriander","¼ tsp. ground cinnamon",
                "½ tsp. salt","1¾ cups water","½ cup frozen peas",
                "1 or 2 tbsp. chopped fresh coriander"]},
            {"type":"steps","items":[
                "Place quinoa in a fine mesh strainer and rinse with cold water. Drain well.",
                "In a heavy saucepan, warm the oil and sauté the onions on medium heat for 5 minutes.",
                "Add the ginger, pepper, cayenne and the quinoa; cook for a minute, stirring.",
                "Stir in the turmeric, coriander, cinnamon and salt; cook for another few minutes.",
                "Add water and bring to a boil. Cover and reduce heat; simmer for 15 minutes.",
                "Stir in peas, cover and cook for 5 minutes, until peas are tender and water has been absorbed.",
                "Before serving, fluff with a fork and add chopped cilantro if desired."]}])

    recipe(story, "Rice Pudding",
        notes="Optional: broil for 10 minutes. Garnish with ground pistachio nuts.",
        sections=[
            {"type":"ingredients","items":[
                "½ gallon milk (8 cups)","1 cup short grain rice",
                "1 cup sugar","2 tsp. mazaher (orange blossom water)"]},
            {"type":"steps","items":[
                "Rinse rice in water and set aside.",
                "Bring milk to a boil and add rice.",
                "Keep stirring until the mixture becomes creamy and thick (about 1 hour).",
                "Stir in sugar and after 10 minutes, add mazaher."]}])

    recipe(story, "Kushari",
        sections=[
            {"type":"ingredients","head":"Tomato Sauce (make earlier)","items":[
                "4 medium tomatoes, skins off, cut into small pieces",
                "2–3 tbsp. olive oil","3–4 cloves garlic, cut up",
                "Salt to taste","Cumin to taste","Cayenne pepper to taste",
                "1 tbsp. tomato paste"]},
            {"type":"ingredients","head":"Main Dish","items":[
                "Onions, sliced (for frying)","1 cup lentils",
                "7 kinds of pepper (spice blend), to taste",
                "1–1¼ cup small elbow pasta","1 cup rice",
                "1 tbsp. oil","Salt and cumin to taste"]},
            {"type":"steps","items":[
                "Tomato Sauce: Process tomatoes in food processor. In a saucepan, add olive oil, sauté garlic, add salt, cumin to taste, cayenne pepper, and tomato paste. Add tomatoes, bring to boil and simmer, covered, for 45 minutes.",
                "Onions: Fry onions until golden. Save some of the oil the onions were fried in. Set aside.",
                "Lentils: In a medium pot, add 1½ cups water, bring to boil. Add lentils, salt, 7 kinds of pepper spice blend, and 1–2 tbsp. oil from fried onions. Lower temp, cover till tender, about 20 minutes. Drain. Set aside.",
                "Pasta: In a medium pot, bring salted water to boil and add elbow pasta. Drain. Stir in a little tomato sauce. Set aside.",
                "Rice: In a medium pot, add 1½ cups water, salt, cumin to taste, 1 cup rice, and 1 tbsp. oil. Cook. Set aside.",
                "To serve: Layer pasta, rice, lentils, and onions. Serve with tomato sauce on the side."]}])

    recipe(story, "Mediterranean Pasta with Fire Roasted Tomatoes",
        yld="6 servings",
        sections=[
            {"type":"ingredients","items":[
                "2 lbs. medium plum tomatoes (10 to 12), halved lengthwise",
                "½ cup olive oil, divided","2 cloves garlic, minced",
                "1 tbsp. Italian seasoning","½ tsp. crushed red pepper",
                "½ tsp. sea salt","¼ tsp. coarse grind black pepper",
                "8 oz. pasta, such as fettuccine",
                "Shredded Parmesan cheese, for serving"]},
            {"type":"steps","items":[
                "Place tomato halves, cut-sides up, in foil-lined 15×10×1-inch pan sprayed with nonstick cooking spray.",
                "Mix ¼ cup oil, garlic and seasonings in small bowl. Spoon over tomatoes. Drizzle with 2 tablespoons of the remaining oil.",
                "Roast in preheated 400°F oven 45 to 60 minutes until tomatoes are soft and browned on top.",
                "Prepare pasta as directed on package. Drain well.",
                "Place ½ of the roasted tomatoes and remaining 2 tablespoons oil in large bowl. Coarsely mash tomatoes.",
                "Add pasta and remaining tomatoes; toss to mix well. Sprinkle with shredded Parmesan cheese."]}])

    recipe(story, "Fettuccine with Pistachio-Mint Pesto and Tomatoes",
        yld="4 servings (serving size: 1 cup)",
        sections=[
            {"type":"ingredients","items":[
                "½ cup fresh mint leaves","½ cup fresh flat-leaf parsley leaves",
                "¼ cup plus 4 tsp. unsalted, shelled dry-roasted pistachios, divided",
                "3 tbsp. extra-virgin olive oil","⅝ tsp. kosher salt",
                "¼ tsp. freshly ground black pepper","1 large garlic clove",
                "1 (9 oz.) package refrigerated fettuccine",
                "12 cherry tomatoes, halved",
                "1 oz. fresh pecorino Romano cheese, shaved (about ¼ cup)"]},
            {"type":"steps","items":[
                "Combine mint leaves, parsley leaves, ¼ cup pistachios, olive oil, kosher salt, ground black pepper, and garlic in a mini food processor; pulse mixture until coarsely chopped.",
                "Cook fettuccine according to the package directions, omitting salt and fat. Drain fettuccine over a bowl, reserving ¼ cup of the cooking liquid. Combine pesto mixture and reserved cooking liquid in a large bowl, stirring with a whisk. Add pasta to bowl; toss well to coat. Gently fold in cherry tomatoes. Coarsely chop remaining 4 tsp. pistachios. Top pasta evenly with pecorino Romano cheese and chopped pistachios."]}])

    recipe(story, "Garlic-and-Herb Pasta with Broccoli Rabe",
        yld="4 servings (serving size: about 1½ cups)",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. broccoli rabe, trimmed and cut into 2-inch pieces",
                "8 oz. uncooked orecchiette pasta",
                "2 tbsp. extra-virgin olive oil",
                "¼ cup thinly sliced garlic (4 to 5 large garlic cloves)",
                "¼ tsp. crushed red pepper",
                "¾ tsp. plus ⅛ tsp. kosher salt, divided",
                "1 (5.2 oz.) pkg. garlic-and-herb spreadable cheese (such as Boursin)",
                "1 tsp. lemon zest"]},
            {"type":"steps","items":[
                "Bring a large saucepan of water to a boil over high. Add broccoli rabe; boil until crisp-tender, about 2 minutes. Using tongs or a slotted spoon, transfer broccoli rabe to a colander. Rinse under cold water to cool; squeeze gently to remove excess water. Set aside.",
                "Return water in pan to a boil over high. Add pasta; cook until al dente, about 12 minutes. Reserve ⅔ cup cooking liquid. Drain pasta; set aside.",
                "Heat oil in a large skillet over medium-low. Add garlic, red pepper, and ⅛ tsp. salt; cook, stirring often, until garlic is tender, about 5 minutes. Add cheese and reserved ⅔ cup cooking liquid; stir until cheese melts. Stir in broccoli rabe and pasta; cook until warmed, about 2 minutes. Sprinkle with zest and remaining ¾ tsp. salt. Toss well."]}])

    recipe(story, "Homemade Pasta",
        yld="2 lbs. (double recipe)",
        notes="Do half recipe for 1 lb. Knead till soft. Roll sections thin. Hang to dry 1–1.5 hours before cooking.",
        sections=[
            {"type":"ingredients","items":[
                "4 eggs (room temperature)",
                "3½ cups flour (\"00\" flour, semolina, all-purpose, or a blend; used 2¼ cups \"00\" + ½ cup fine semolina)",
                "½ tsp. salt","1 tbsp. olive oil",
                "3 tbsp. water, plus a little more as needed"]},
            {"type":"steps","items":[
                "Food Processor Method: Add all ingredients to the bowl of a food processor fitted with the normal blade attachment. Pulse for about 10 seconds, or until the mixture reaches a crumbly texture.",
                "Remove the dough and form it into a ball with your hands, then place on a lightly-floured cutting board. Knead the dough for 1–2 minutes until smooth and elastic. If the dough seems too dry, add an extra tablespoon or two of water. If wet or sticky, add some extra flour — dough should be fairly dry.",
                "Form the dough into a ball, wrap tightly in plastic wrap. Let rest at room temperature for 30 minutes. Use immediately or refrigerate for up to 1 day.",
                "Roll out the pasta dough into your desired shape, either by hand or using a pasta maker. Cook in a large pot of generously-salted boiling water until al dente, usually 1–5 minutes depending on thickness. Drain and use immediately.",
                "Stand Mixer Method: Add all ingredients to the bowl of a stand mixer fitted with the dough hook. Knead on low speed for 8–10 minutes until smooth and elastic. Adjust with water or flour as needed. Form into a ball, wrap and rest 30 minutes.",
                "By Hand Method: Place the flour in a mound on a large cutting board. Create a well in the middle. Add the eggs in the center of the well. Sprinkle the salt and drizzle the olive oil on top of the eggs. Use a fork to begin whisking the eggs until combined, then gradually whisk in the surrounding flour until the egg mixture is nice and thick. Use your hands to fold in the rest of the dough until it forms a loose ball. Knead for about 10 minutes until smooth and elastic. Form into a ball, wrap and rest 30 minutes."]}])

    # ── CHAPTER 8 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "8", "Seafood",
        tag="Fast, bright, and hard to improve on. Samkeh Harra brings bold Lebanese spice to a whole baked fish, the Shrimp &amp; Mango Skewers are summer on a stick, and the Blackened Shrimp Fajitas are done in twenty minutes — though they taste like they weren't.")

    recipe(story, "Samkeh Harra (Baked Spicy Fish)",
        sections=[
            {"type":"ingredients","items":[
                "Fish","1 cup tahini","1 cup lemon juice",
                "1 cup water","Salt & pepper","½ tsp. hot red pepper"]},
            {"type":"steps","items":[
                "Clean fish, rub it with salt & pepper inside and outside. Rub fish with oil.",
                "Place in baking dish in oven for 25 minutes.",
                "Cook tahini with lemon juice, salt, water, and hot pepper. Cook for 10 minutes, stirring constantly.",
                "Pour sauce over fish and put back into oven for 15 minutes.",
                "Brown some pine nuts in oil. Finish with toasted pine nuts on top of fish."]}])

    recipe(story, "Shrimp & Mango Skewers",
        meta="Total Time: 25 minutes | Makes 4 main-dish servings",
        tips="To tell if a mango is ripe, squeeze gently — it should yield slightly. Space shrimp ¼ inch from fruit for even cooking.",
        sections=[
            {"type":"ingredients","items":[
                "1 cup plain low-fat yogurt",
                "½ cup packed fresh mint leaves, finely chopped",
                "¼ tsp. curry powder","1 cup whole wheat couscous",
                "5 oz. baby spinach",
                "1 lb. shelled and deveined shrimp (26 to 30 ct.)",
                "2 ripe mangoes, peeled, cut into 1-inch chunks","1 lime"]},
            {"type":"steps","items":[
                "If using bamboo skewers, soak in cold water at least 30 minutes to prevent burning. Prepare outdoor grill for direct grilling on medium-high.",
                "From lime, grate 1 teaspoon peel and squeeze 2 teaspoons juice into medium bowl; stir in yogurt, half of chopped mint, curry powder, and ¼ teaspoon each salt and freshly ground black pepper.",
                "In a 4-quart saucepan, heat 1¾ cups water to boiling on high. Stir in couscous. Cover and remove from heat. Let stand 5 minutes; fluff with fork. Lay spinach on top of couscous; cover and let stand another 5 minutes.",
                "Thread shrimp and mango chunks alternately onto skewers. Place half of yogurt mixture in small bowl; set aside for serving. Brush remaining mixture all over shrimp and mango. Grill 5 to 7 minutes or until shrimp turn opaque, turning over once.",
                "Toss spinach and couscous until combined; transfer to large platter. Top with shrimp skewers. Drizzle reserved yogurt mixture over couscous. Garnish with remaining mint."]}])

    recipe(story, "One-Pan Skillet Shrimp Destin with Orzo",
        meta="Active: 35 min | Total: 35 min | Serves 4",
        sections=[
            {"type":"ingredients","items":[
                "1¾ tsp. kosher salt, divided","2 Tbsp. olive oil",
                "3 garlic cloves, minced (about 1 Tbsp.)",
                "⅔ cup dry white wine","2 cups uncooked orzo (1 lb.)",
                "3¼ cups vegetable stock",
                "2 Tbsp. chopped fresh flat-leaf parsley","2 Tbsp. chopped fresh dill",
                "1 bunch scallions",
                "12 oz. medium-size peeled, deveined raw shrimp"]},
            {"type":"steps","items":[
                "Slice dark green scallion tops to equal ¼ cup; slice light green and white bottom parts separately. Set aside. Toss together shrimp, lemon zest, and ½ teaspoon of the kosher salt in a large bowl.",
                "Heat oil in a large, deep skillet over medium. Add garlic and scallion bottoms; cook, stirring often, until translucent. Add orzo; cook, stirring often, until lightly toasted, about 2 minutes. Stir in wine; cook, stirring constantly, 1 minute. Add stock and remaining 1 teaspoon salt; bring to a simmer over medium-high.",
                "Cover and reduce heat to low. Cook, undisturbed, until orzo is tender, about 12 minutes, adding shrimp during the final 3 minutes. Remove pan from heat. Sprinkle evenly with scallion tops, parsley, and dill."]}])

    recipe(story, "Baked Cod with Panko",
        meta="Prep: 10 min | Cook: 12 min | Total: 22 min | Yield: 1 pound",
        intro="Easy, flavorful, and light. Cod fillets are topped with seasoned, buttery panko breadcrumbs then baked to perfection!",
        sections=[
            {"type":"ingredients","items":[
                "1 pound cod fillets (3 to 4 pieces)",
                "2 tablespoons freshly squeezed lemon juice, divided",
                "1 teaspoon sea salt, divided","¾ teaspoon pepper",
                "¾ cup panko bread crumbs",
                "3 tablespoons fresh parsley, chopped",
                "2 tablespoons unsalted butter, melted",
                "½ teaspoon garlic powder","¼ teaspoon paprika"]},
            {"type":"steps","items":[
                "Preheat the oven to 425°F and line a baking sheet with parchment paper.",
                "In a small bowl, combine the panko breadcrumbs, lemon juice (reserve about 2 teaspoons), parsley, melted butter, garlic powder, and paprika.",
                "Use paper towels to pat the cod fillets dry. Drizzle the remaining 2 teaspoons of lemon juice over the fillets, then sprinkle with salt and pepper.",
                "Place 2 to 3 tablespoons of panko topping on top of each piece of fish and press down gently so the topping sticks. Bake for 12 to 14 minutes until the cod flakes easily.",
                "Serve immediately with a side salad or sautéed vegetables."]}])

    recipe(story, "Almond-Crusted Tilapia",
        meta="Prep: 15 min | Cook: 9 min | Makes 4 servings",
        intro="You can substitute catfish, flounder, or orange roughy for tilapia.",
        sections=[
            {"type":"ingredients","items":[
                "1 cup sliced almonds, divided","¼ cup all-purpose flour",
                "½ tsp. salt","4 (6-oz.) tilapia fillets",
                "2 Tbsp. butter","2 Tbsp. olive oil"]},
            {"type":"steps","items":[
                "Process ½ cup almonds in a food processor until finely chopped, and combine with flour in a shallow bowl. Sprinkle fish evenly with salt; dredge in almond mixture.",
                "Melt butter with olive oil in a large heavy skillet over medium heat; add fish, and cook 4 minutes on each side or until golden. Remove fillets to a serving plate.",
                "Add remaining ½ cup almonds to skillet, and cook, stirring often, 1 minute or until golden. Remove almonds with a slotted spoon, and sprinkle over fish."]}])

    recipe(story, "Spicy Shrimp Lo Mein",
        yld="4 servings",
        sections=[
            {"type":"ingredients","items":[
                "6 oz. soba noodles (weight before cooking), cooked and drained",
                "Sesame oil for sautéing",
                "1 pound medium-sized shrimp (31/40), peeled, deveined, and dried very well",
                "3 green onions, chopped (plus more for garnish)",
                "3 garlic cloves, minced","½ tbsp. freshly ground ginger",
                "2 cups bok choy, sliced","2 large carrots, julienned",
                "4–5 baby portobello mushrooms, cut in quarters",
                "1 large sweet chili pepper, chopped",
                "1 cup snow peas, julienned","½ cup soy sauce",
                "1 tbsp. cooking sherry",
                "1 tsp. hot chili paste or sauce (more if desired)"]},
            {"type":"steps","items":[
                "Heat a large wok or shallow skillet on high. Add 1 tbsp. of sesame oil and coat the pan. Add the shrimp and cook about one minute on each side. Remove the shrimp and set aside.",
                "Add the green onion, garlic, and ginger. Sauté one minute.",
                "Add the remaining vegetables and sauté until the bok choy starts to wilt and shrink.",
                "Add the soy sauce, sherry, and hot chili paste.",
                "Add the shrimp back to the wok along with the noodles. Heat through and adjust seasonings if needed.",
                "Serve with freshly chopped green onion for garnish."]}])

    recipe(story, "20-Minute Skillet Blackened Shrimp Fajitas",
        meta="Prep: 5 min | Cook: 15 min | Total: 20 min | Serves 4",
        intro="Excellent — served on seasoned rice, add lime juice and cilantro at end!",
        sections=[
            {"type":"ingredients","items":[
                "1 pound large shrimp, peeled and deveined",
                "1 tablespoon chili powder","2 teaspoons paprika",
                "1 teaspoon onion powder","1 teaspoon cumin",
                "½ teaspoon garlic powder","1 teaspoon salt",
                "¼ teaspoon pepper","2 tablespoons olive oil, divided",
                "1 red bell pepper, sliced","1 green bell pepper, sliced",
                "1 yellow bell pepper, sliced","1 medium-sized onion, sliced",
                "Optional toppings: avocado, chopped cilantro, sour cream"]},
            {"type":"steps","items":[
                "In a large bowl, add the shrimp, chili powder, paprika, onion powder, cumin, garlic powder, salt, and pepper. Set aside.",
                "In a medium-sized skillet over medium-high heat, add 1 tablespoon olive oil, bell peppers, and onion. Sauté until tender, about 5–7 minutes. Slide to the side of the skillet.",
                "Add 1 tablespoon olive oil and shrimp and cook for 2–3 minutes or until no longer pink.",
                "Serve in tortillas with optional toppings."]}])

    # ── CHAPTER 9 ─────────────────────────────────────────────────────────────
    chapter_opener(story, "9", "Poultry",
        tag="Something for every occasion — from Honey Fried Chicken on a Sunday to Shawarma Chicken on a Tuesday, Jewel of the Nile Kabobs for the grill, and Chicken Parmesan when comfort is non-negotiable.")

    recipe(story, "Blackened Chicken",
        sections=[
            {"type":"ingredients","items":[
                "1½ cups buttermilk","Chicken",
                "2 tsp. each: cayenne pepper, oregano, thyme, paprika, fresh chopped parsley",
                "Salt"]},
            {"type":"steps","items":[
                "Mix all together. Marinate overnight.",
                "Broil in oven or barbecue."]}])

    recipe(story, "Joann Hartman's Chicken Kabobs",
        sections=[
            {"type":"ingredients","head":"Kabobs","items":[
                "6 boneless chicken breasts, cut into chunks",
                "1 small can pineapple chunks",
                "Green peppers, cut into chunks","Cherry tomatoes",
                "Fresh mushrooms","Water chestnuts"]},
            {"type":"ingredients","head":"Marinade","items":[
                "½ cup pineapple juice","½ cup soy sauce","¼ cup oil",
                "1 tsp. dry mustard","1 tbsp. brown sugar",
                "2 tsp. ground ginger","1 tsp. garlic salt","¼ tsp. pepper"]},
            {"type":"steps","items":[
                "Simmer marinade ingredients for 5 minutes. Cool.",
                "Combine with chicken. Marinate 1 hour.",
                "Skewer chicken & vegetables.",
                "Grill 20 minutes or until chicken is done."]}])

    recipe(story, "Honey Fried Chicken",
        sections=[
            {"type":"ingredients","items":[
                "½ cup honey","2 tbsp. wine vinegar",
                "3-lb. chicken, cut into serving size",
                "½ cup flour","2 tbsp. whole wheat flour",
                "2 tsp. cayenne pepper","Salt & pepper"]},
            {"type":"steps","items":[
                "Combine honey, wine vinegar and chicken. Toss to coat. Marinate at least 2 hours.",
                "Combine flours and cayenne pepper.",
                "Dredge chicken with flour and fry till brown."]}])

    recipe(story, "Jewel of the Nile Chicken Kabobs",
        intro="Danny's favorite.",
        sections=[
            {"type":"ingredients","head":"Marinade","items":[
                "½ cup plain yogurt","½ cup chopped parsley",
                "1 tbsp. chopped fresh coriander","¼ cup fresh lemon juice",
                "2 tbsp. olive oil","1½ cloves garlic, minced",
                "1 tbsp. paprika","1 tbsp. curry powder",
                "2 tsp. ground cumin","½ tsp. salt","½ tsp. fresh pepper"]},
            {"type":"ingredients","head":"Kabobs","items":[
                "1½ lb. boneless chicken breast, cut into chunks",
                "1 small yellow bell pepper",
                "1 yellow squash, cut into ½ inch rounds",
                "2 small onions, cut into wedges","12 cherry tomatoes"]},
            {"type":"steps","items":[
                "Prepare grill. Make the marinade in a bowl. Stir together all ingredients, add the chicken, toss to coat.",
                "Chill, covered with plastic wrap, for 20 minutes or longer.",
                "Drop the pepper into boiling water and blanch for 2 minutes. Remove with slotted spoon.",
                "Alternate chicken cubes, pepper, yellow squash, onion and cherry tomatoes on skewers.",
                "Grill for 4 minutes per side."]}])

    recipe(story, "Linda Bailey's Chicken Parmesan",
        sections=[
            {"type":"ingredients","head":"Chicken","items":[
                "Deboned chicken breast, cut into small pieces and flattened with mallet",
                "Egg batter","¼ cup bread crumbs",
                "¼ cup grated cheese","Oil for sautéing"]},
            {"type":"ingredients","head":"Sauce","items":[
                "3 cloves garlic, minced","3 tbsp. oil","1 onion, chopped",
                "2½ cups whole tomatoes","¼ tsp. pepper","¼ tsp. salt",
                "1 small can tomato sauce","Thyme"]},
            {"type":"ingredients","head":"Topping","items":[
                "Grated mozzarella cheese","Parmesan cheese"]},
            {"type":"steps","items":[
                "Dip chicken into egg batter, then dip into mixture of bread crumbs and grated cheese.",
                "Sauté chicken in pan with oil until brown.",
                "Sauce: Sauté garlic and onion in oil. Add tomatoes, pepper, salt, tomato sauce, and thyme. Simmer for 20 minutes.",
                "Place some sauce in pan, layer chicken pieces, then add some more sauce. Top with grated mozzarella & Parmesan cheese.",
                "Bake at 350°F for 30 to 45 minutes."]}])

    recipe(story, "Pollo Con Pico De Gallo",
        sections=[
            {"type":"ingredients","items":[
                "Chicken breast",
                "½ cup Kikkoman Teriyaki Sauce","½ tsp. grated lime peel",
                "1 tbsp. lime juice","1 clove garlic, pressed"]},
            {"type":"steps","items":[
                "Place chicken in large plastic bag. Combine all ingredients.",
                "Remove and grill. Brush chicken with marinade.",
                "Slice and serve."]}])

    recipe(story, "Shawarma Chicken",
        sections=[
            {"type":"ingredients","head":"Chicken","items":[
                "Chicken breast, cut into strips","7 kinds of pepper",
                "2 to 3 cloves garlic, crushed","Pepper, salt","Cayenne pepper",
                "1 Arabic size coffee cup of vinegar",
                "1 Arabic size coffee cup of canola oil","Shawarma spice"]},
            {"type":"ingredients","head":"Garlic Sauce","items":[
                "1 boiled potato","1 heaping spoon yogurt",
                "1 tsp. lemon juice","Salt","Garlic, smashed"]},
            {"type":"steps","items":[
                "Mix chicken with spices. Cover and marinate overnight.",
                "In a fry pan, cook until chicken is done. Serve with garlic sauce.",
                "Garlic Sauce: Mash or purée all sauce ingredients together."]}])

    recipe(story, "Linda Bailey's Sticky Roasted Chicken",
        sections=[
            {"type":"ingredients","items":[
                "2 tsp. salt","1 tsp. paprika","¾ tsp. cayenne pepper",
                "½ tsp. onion powder","½ tsp. thyme","½ tsp. white pepper",
                "¼ tsp. garlic powder","¼ tsp. black pepper",
                "3 pounds of chicken","1 onion, quartered"]},
            {"type":"steps","items":[
                "Combine all spices and rub inside and outside of chicken with the spices.",
                "Place chicken in a sealed plastic bag overnight.",
                "When ready to roast, stuff cavity with the onion, uncovered.",
                "Bake at 250°F for 5 hours."]}])

    recipe(story, "Chicken Enchilada",
        sections=[
            {"type":"ingredients","head":"Filling","items":[
                "1 cup chopped onion","1 clove minced garlic",
                "½ cup chopped green pepper","1 chopped jalapeño pepper",
                "2 tbsp. butter","2 cups cooked, chopped chicken",
                "1 (4 oz.) can diced green chili pepper",
                "1 package tortillas"]},
            {"type":"ingredients","head":"Sauce","items":[
                "3 tbsp. butter, melted","¼ cup flour",
                "½ tsp. ground cumin","½ tsp. coriander","¾ tsp. salt",
                "2½ cups chicken broth","1 cup sour cream",
                "1½ cups shredded cheese"]},
            {"type":"steps","items":[
                "In a large fry pan, melt butter and add onion, all peppers, garlic and sauté. Add chopped chicken. Set aside.",
                "In another sauce pan, melt butter, add flour and gradually add chicken broth with spices. Stir until thick.",
                "Remove from heat and stir in sour cream and cheese.",
                "Use ½ of this sauce in the chicken mixture.",
                "Roll up the chicken mixture with the tortillas, then use the remaining sauce on top.",
                "Bake at 350°F for 30 minutes."]}])

    recipe(story, "Creamy Chicken Quesadillas",
        meta="Active: 15 min | Total: 15 min | Serves 4",
        intro="A creamy base helps the cheese go further and keeps the chicken moist.",
        sections=[
            {"type":"ingredients","items":[
                "1 Tbsp. olive oil","½ cup unsalted chicken stock",
                "1 Tbsp. hot sauce (such as Cholula)",
                "¼ cup coarsely chopped spinach","⅛ tsp. black pepper",
                "¼ tsp. kosher salt",
                "6 oz. skinless, boneless rotisserie chicken breast, shredded (about 1¾ cups)",
                "4 oz. preshredded mozzarella cheese (about 1 cup)",
                "4 (8-in.) whole-wheat flour tortillas",
                "Cooking spray","1 ripe avocado, quartered"]},
            {"type":"steps","items":[
                "Heat oil in a small saucepan over medium. Slowly add stock; cook 30 seconds, stirring constantly. Remove pan from heat; stir in spinach, hot sauce, salt, pepper, chicken, and cheese.",
                "Heat a large skillet over medium. Divide chicken mixture evenly over half of each tortilla. Fold tortillas in half over filling. Carefully coat both sides of quesadillas with cooking spray. Add 2 quesadillas to pan; cook 2 minutes on each side or until browned and cheese is melted. Repeat with remaining quesadillas. Cut each into 4 wedges. Serve with avocado."]}])

    recipe(story, "Cornell Chicken",
        meta="Prep: 10 min | Cook: 50 min | Marinate: 4 hrs | Serves 6",
        sections=[
            {"type":"ingredients","items":[
                "2 cups cider vinegar","1 cup vegetable oil","1 large egg",
                "3 tablespoons salt","1 tablespoon poultry seasoning",
                "½ teaspoon ground black pepper",
                "1 (3 to 3½ pound) broiler-fryer chicken, cut in half"]},
            {"type":"steps","items":[
                "Purée cider vinegar, oil, egg, salt, poultry seasoning, and pepper in a blender until smooth.",
                "Pour marinade into a resealable plastic bag. Add chicken halves, coat with marinade, squeeze out excess air, and seal the bag. Marinate in the refrigerator for at least 4 hours or overnight.",
                "Preheat an outdoor grill for medium-high heat and lightly oil the grate.",
                "Remove chicken halves from the bag and transfer to a paper towel-lined baking sheet. Pat chicken dry with more paper towels. Reserve marinade.",
                "Place chicken on the preheated grill, skin side up. Grill for about 20 minutes, basting frequently with reserved marinade.",
                "Flip chicken and continue grilling, basting occasionally, until no longer pink at the bone and juices run clear, about 25 to 30 more minutes. An instant-read thermometer inserted near the bone should read 165°F.",
                "Remove from grill and let rest a few minutes before serving."]}])

    recipe(story, "Turkish Yogurt Chicken Kebabs with Aleppo Pepper",
        sections=[
            {"type":"ingredients","items":[
                "2 lb. chicken, cut into cubes","6 cloves garlic, smashed",
                "1 cup Greek-style yogurt","3 Tbsp. Aleppo pepper",
                "3 Tbsp. olive oil","2 Tbsp. red wine vinegar",
                "2 tsp. salt","1 tsp. black pepper","1 Tbsp. tomato paste"]},
            {"type":"steps","items":[
                "Place Aleppo pepper in a bowl and mix with 1 Tbsp. of water; let stand until it forms a paste, about 5 minutes. Add yogurt, olive oil, red wine vinegar, and tomato paste. Stir to combine. Add garlic and sliced lemon. Can be made 1 day ahead.",
                "Thread chicken onto skewers and grill over medium-high heat, turning, until cooked through."]}])

    recipe(story, "Chicken Chimichangas (Baked or Pan Fried)",
        meta="Prep: 10 min | Cook: 20 min | Total: 30 min | Serves 4",
        sections=[
            {"type":"ingredients","items":[
                "2 cups cooked and shredded chicken","1 tablespoon chili powder",
                "½ teaspoon cumin","¼ teaspoon paprika","½ teaspoon salt",
                "½ cup salsa","2 cups Colby jack cheese, shredded",
                "2 ounces cream cheese, softened",
                "2 tablespoons green onions, chopped",
                "1 (15 oz.) can refried beans",
                "4 burrito-size tortillas","1 tablespoon olive oil"]},
            {"type":"steps","items":[
                "Preheat oven to 400°F. In a medium-sized mixing bowl, combine chicken, chili powder, cumin, paprika, salt, salsa, cheese, cream cheese, and green onions.",
                "Spoon 2 tablespoons refried beans onto the tortilla, 2 inches from the edge. Add about ½ cup of the meat mixture in the center. Fold in the sides of the tortilla, then roll up from the bottom and place seam side down on a baking sheet. Brush the tops with olive oil. Bake for 20 minutes or until golden brown and heated through.",
                "To pan fry: Add 1 tablespoon oil to a medium-sized skillet over medium heat. Add the chimichanga seam side down. Fry on each side 2–3 minutes until golden brown and crispy."]}])

    # ── CHAPTER 10 ────────────────────────────────────────────────────────────
    chapter_opener(story, "10", "Meats",
        tag="One recipe, done right. Shawarma Beef is the kind of dish that fills the kitchen with a smell that makes everyone wander in to ask what's for dinner. Worth every step.")

    recipe(story, "Amal's Shawarma Beef",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. beef (London Broil), cut into strips",
                "7 kinds of pepper","5 cardamoms, crushed",
                "1 (Arabic coffee cup size) vinegar",
                "1 (Arabic coffee cup size) corn oil",
                "Salt","Shawarma spice","Mistika, crushed"]},
            {"type":"steps","items":[
                "Marinate meat with spices for 4 hours (preferably overnight).",
                "Put meat mixture in pressure cooker. Process for 7 minutes.",
                "Put meat mixture in dish and broil for 5 minutes.",
                "Serve with tahini sauce."]}])

    # ── CHAPTER 11 ────────────────────────────────────────────────────────────
    chapter_opener(story, "11", "Vegetarian Mains",
        tag="Filling, satisfying, and anything but an afterthought. Fül Medamis is a centuries-old Egyptian breakfast, the Cauliflower Pizza Crust will surprise you, and the Grilled Tofu Steaks will convert a skeptic or two.")

    recipe(story, "Grilled Tofu Steaks",
        notes="You can grill button mushrooms, onions or other vegetables on skewers alongside.",
        sections=[
            {"type":"ingredients","items":[
                "2 (16 oz.) pkgs. extra firm tofu",
                "⅓ cup soy sauce","¼ cup hoisin sauce",
                "2 tbsp. minced fresh ginger",
                "2 tbsp. frozen orange juice concentrate, thawed",
                "1 tbsp. toasted sesame oil","1 tsp. chili-garlic sauce"]},
            {"type":"steps","items":[
                "Cut tofu blocks lengthwise into 4 slices. Place tofu between two plates with paper towels to drain liquid. Drain 1 hour, then pat dry.",
                "Combine soy sauce, hoisin sauce, ginger, orange juice concentrate, sesame oil and chili-garlic sauce. Add tofu and toss to coat.",
                "Refrigerate 3 hours or up to 2 days.",
                "Oil grill grates and preheat grill to medium. Drain tofu, reserving marinade.",
                "Grill 8 minutes, or until browned and crispy.",
                "Heat reserved marinade in small saucepan until simmering. Pour over tofu steaks."]}])

    recipe(story, "Fül Medamis (Instant Pot)",
        notes="Do not cook more than 2 lbs. (5 cups) of beans at a time. For 2 lbs., cook for 45 minutes.",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. (about 2½ cups) fül beans","⅓ tsp. baking soda",
                "1 tsp. salt","1 tsp. orange split lentils",
                "Fresh water for cooking","Juice of 3–4 lemons",
                "4–5 garlic cloves, minced","Fresh cilantro, chopped",
                "Extra-virgin olive oil"]},
            {"type":"steps","items":[
                "Soak fül beans in a large bowl for at least 8 hours or overnight. Water level should be about 3 inches above the beans. Stir in baking soda. After soaking, drain off the water (do not rinse).",
                "Place the Instant Pot metal rack into the bottom of the pot. Add the drained fül beans and cover with fresh water to just above the level of the beans.",
                "Add salt and orange split lentils; stir to combine.",
                "Close the lid and set the valve to \"Sealing.\" Press the \"Pressure Cook\" button and set the timer for 40 minutes (50 minutes for 2 lbs.).",
                "When finished, press \"Keep Warm\" to turn off the keep-warm function. Allow the pressure to release naturally, then use the quick-release valve to remove any remaining pressure.",
                "Serve topped with lemon juice, garlic, chopped cilantro, and a drizzle of extra-virgin olive oil."]}])

    recipe(story, "Fül Medamis (Pressure Cooker)",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. (about 2½ cups) fül beans","⅓ tsp. baking soda",
                "Fresh water for cooking","Juice of 3–4 lemons",
                "4–5 garlic cloves, minced","Fresh cilantro, chopped",
                "Extra-virgin olive oil"]},
            {"type":"steps","items":[
                "Soak fül beans in a large bowl for at least 8 hours or overnight. Water should be about 3 inches above the level of the beans. Stir in baking soda. After soaking, drain off the water (do not rinse).",
                "Place fül beans in pressure cooker. Add fresh water to just above the level of the beans.",
                "Cook for 14 minutes. Watch for liquid leaking from the top of the pressure cooker and wipe away any excess liquid with a paper towel.",
                "Serve topped with lemon juice, garlic, chopped cilantro, and a drizzle of extra-virgin olive oil."]}])

    recipe(story, "Lentils Medamis (Adas Medamis)",
        yld="4 servings",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. light, large lentils","3 heads of garlic, smashed",
                "Juice of 2–3 lemons","Fresh cilantro, minced","Olive oil"]},
            {"type":"steps","items":[
                "Rinse lentils twice while soaking for 10 minutes.",
                "Pressure cook for 5 minutes, with water just slightly above the level of the lentils.",
                "Add smashed garlic, lemon juice, and minced cilantro to the cooked lentils.",
                "Drizzle olive oil into a bowl before serving and ladle the lentils over."]}])

    recipe(story, "Cauliflower Pizza Crust",
        meta="Prep: 15 min | Cook: 30 min | Total: 45 min | 8 slices",
        intro="Great — almost like dough! Easy to make and when you are done, you won't be able to even tell that it's the healthy version!",
        sections=[
            {"type":"ingredients","items":[
                "1 large cauliflower head, riced; or refrigerated or frozen riced cauliflower",
                "1 cup parmesan cheese, shredded","1 large egg",
                "¼ teaspoon granulated garlic powder","½ teaspoon kosher salt",
                "1 teaspoon Italian seasoning",
                "Homemade pizza sauce and toppings of your choice"]},
            {"type":"steps","items":[
                "Preheat oven to 400°F. Line a baking sheet with parchment paper and set aside.",
                "To rice the cauliflower, cut the head into florets and place them in a food processor. Process until finely ground. Use enough florets to yield 2 cups of riced cauliflower.",
                "Place riced cauliflower in a microwaveable bowl and heat for about 8 minutes. Once the cauliflower is steamed and softened, place it into a tea towel and squeeze out the liquid by twisting the towel. It is important to squeeze out as much liquid as possible to avoid a soggy crust.",
                "In a large bowl, add riced cauliflower, egg, parmesan cheese, garlic powder, Italian seasoning, and kosher salt. Mix until combined.",
                "Form a ball with the mixture and place on the prepared pan. Press and shape into a 9-inch circle, making sure the thickness is consistent from the middle out to the edges, about ¼ inch thick.",
                "Bake in preheated oven for 20 minutes. To get both sides of the crust crispy, remove the pizza crust from the oven after it bakes. Allow it to cool a few minutes before flipping. Place another piece of parchment paper on top of the crust, and carefully flip the pizza over. Return the pizza to the oven and cook an additional 5 minutes to crisp the bottom.",
                "Add the pizza sauce and toppings of choice, and place back into the oven on broil for 5 minutes until the cheese is melted."]}])

    # ── CHAPTER 12 ────────────────────────────────────────────────────────────
    chapter_opener(story, "12", "Bread",
        tag="The chapter that makes the house smell like a bakery. No-Knead Harvest Bread and Sullivan Street Bakery Bread for the patient bakers; Chai-Spiced Banana Bread and the Pistachio Cardamom Loaf for everyone else. And then there are the muffins — all eight of them, each better than the last.")

    recipe(story, "Orange-Date Muffins",
        yld="1½ dozen",
        sections=[
            {"type":"ingredients","items":[
                "2 cups flour","1 tsp. baking powder","1 tsp. baking soda",
                "½ tsp. salt","1 tsp. grated orange rind","¾ cup sugar",
                "1 orange, peeled & sectioned","½ cup butter",
                "½ cup pitted dates, chopped","½ cup orange juice","1 egg"]},
            {"type":"steps","items":[
                "Combine first 6 dry ingredients in a large bowl, make a well in the center of mixture. Set aside.",
                "Position knife blade in food processor bowl; add orange sections, butter, dates, orange juice, and egg. Process 30 seconds or until mixture is blended but not smooth.",
                "Add to dry ingredients, stirring just until moist.",
                "Place paper baking cups in muffin pan. Spoon batter into paper cups.",
                "Bake at 400°F for 15 minutes or until golden brown."]}])

    recipe(story, "Orange Spice Muffins",
        sections=[
            {"type":"ingredients","items":[
                "1 cup flour","1 cup whole wheat flour",
                "1 tbsp. baking powder","¼ tsp. cinnamon",
                "¼ tsp. cloves","¼ tsp. nutmeg","¼ tsp. salt",
                "1 egg","1 cup sour cream","4 tbsp. butter, melted",
                "1 tbsp. frozen orange juice concentrate",
                "Grated zest of 1 large orange","⅓ cup brown sugar","1 tbsp. sugar"]},
            {"type":"steps","items":[
                "Butter muffin pan. Mix together flours, baking powder, cinnamon, & spices.",
                "Beat egg with sour cream and butter & orange juice. Stir in orange zest & brown sugar.",
                "Add sour cream mixture to dry ingredients.",
                "Combine sugar with cinnamon and sprinkle over muffins.",
                "Bake at 400°F for 20–25 minutes."]}])

    recipe(story, "Pear-Walnut Muffins",
        sections=[
            {"type":"ingredients","head":"Muffins","items":[
                "1½ cups flour","½ cup brown sugar","2 tsp. baking powder",
                "1 tsp. cinnamon","½ tsp. ginger","⅛ tsp. salt",
                "1 egg","½ cup oil","½ cup plain low-fat yogurt",
                "½ tsp. vanilla","1 pear, cored and finely chopped"]},
            {"type":"ingredients","head":"Topping","items":[
                "3 tbsp. finely chopped walnuts","2 tbsp. brown sugar"]},
            {"type":"steps","items":[
                "In a bowl, stir together flour, brown sugar, baking powder, cinnamon, ginger and salt. Make a well in center.",
                "In a bowl, beat egg; stir in oil, yogurt and vanilla. Add all at once to flour mixture. Stir until moist. Stir in pear.",
                "Lightly grease muffin cups or line with baking cups. Fill two-thirds full.",
                "For topping, combine walnuts and 2 tbsp. brown sugar. Sprinkle on batter in cups.",
                "Bake at 400°F for 20 minutes."]}])

    recipe(story, "Raisin Bran Muffins",
        notes="This mixture can be refrigerated for up to 6 weeks.",
        sections=[
            {"type":"ingredients","items":[
                "1 cup oil","2 to 3 cups sugar","4 eggs, beaten",
                "1 qt. buttermilk",
                "5 cups flour (3 cups regular, 2 cups whole wheat)",
                "3 tsp. baking soda","13 oz. total raisin bran"]},
            {"type":"steps","items":[
                "Mix all together. Let sit overnight in refrigerator.",
                "Bake at 400°F for 15–20 minutes in paper-lined muffin tins."]}])

    recipe(story, "Lemon Poppy Seed Muffins",
        notes="Wonderful for a shower — bake in mini muffin tins.",
        sections=[
            {"type":"ingredients","items":[
                "½ cup butter","1 cup sugar","2 eggs",
                "1 tbsp. poppy seeds","1 tsp. grated lemon peel",
                "4 tbsp. lemon juice","1½ cups flour",
                "2 tsp. baking powder","½ tsp. salt"]},
            {"type":"steps","items":[
                "Grease or line muffin tin.",
                "In a large mixing bowl, cream butter & sugar. Beat in eggs, poppy seeds, lemon peel & lemon juice.",
                "In a separate bowl, combine flour, baking powder & salt.",
                "Stir into creamed mixture. Spoon batter into muffin tin.",
                "Bake at 350°F for 15 to 20 minutes."]}])

    recipe(story, "Morning Glory Muffins",
        yld="16 muffins",
        sections=[
            {"type":"ingredients","items":[
                "1½ cups sugar","1¼ cups flour","1 cup whole wheat flour",
                "1 tbsp. cinnamon","2 tsp. baking soda","½ tsp. salt",
                "2 cups shredded coconut","½ cup raisins",
                "2 cups grated carrots",
                "1 (8 oz.) can crushed pineapple, drained",
                "1 cup chopped pecans","3 eggs",
                "1 cup vegetable oil","1 tsp. vanilla"]},
            {"type":"steps","items":[
                "Grease or line muffin cups.",
                "In a large mixing bowl, combine dry ingredients. Stir in coconut, raisins, carrots, pineapple, and pecans.",
                "In a small bowl, whisk together eggs, oil, & vanilla.",
                "Stir into rest of ingredients, just until moistened.",
                "Spoon into muffin cups. Bake at 350°F for 25 minutes."]}])

    recipe(story, "Sour Cream Lemon Muffins",
        notes="Use a ¼ cup measure to spoon batter into muffin tin for uniform-sized muffins.",
        sections=[
            {"type":"ingredients","items":[
                "2 cups flour","½ cup sugar","1 tbsp. baking powder",
                "1 tsp. grated lemon peel","½ tsp. salt","½ cup butter, melted",
                "½ cup sour cream","½ cup milk","1 egg","Sugar to sprinkle"]},
            {"type":"steps","items":[
                "Grease or line muffin tin.",
                "Combine first 5 dry ingredients in a large mixing bowl.",
                "In a separate bowl, combine butter, sour cream, milk & egg. Stir into dry ingredients.",
                "Spoon into muffin tin. Sprinkle tops with sugar.",
                "Bake at 400°F for 15 to 20 minutes."]}])

    recipe(story, "Pumpkin-Cranberry Muffins",
        yld="1 dozen",
        intro="These moist muffins get a burst of sweet and sour notes from the cranberries. Best warm; can be made ahead and frozen up to one month.",
        sections=[
            {"type":"ingredients","items":[
                "1½ cups all-purpose flour (about 6¾ ounces)",
                "1 teaspoon baking soda","¾ teaspoon ground ginger",
                "½ teaspoon baking powder","½ teaspoon ground cinnamon",
                "¼ teaspoon salt","⅛ teaspoon ground cloves",
                "1 cup granulated sugar","1 cup canned pumpkin",
                "½ cup low-fat buttermilk","¼ cup packed light brown sugar",
                "2 tablespoons canola oil","1 large egg",
                "⅔ cup sweetened dried cranberries, chopped (such as Craisins)",
                "Cooking spray"]},
            {"type":"steps","items":[
                "Preheat oven to 375°F.",
                "Lightly spoon flour into dry measuring cups; level with a knife. Combine flour, baking soda, and next 5 ingredients (through cloves); stir well with a whisk.",
                "Combine granulated sugar and next 5 ingredients (through egg) in a large bowl; beat with a mixer at medium speed until well blended, about 3 minutes. Add flour mixture to sugar mixture; beat at low speed just until combined. Fold in cranberries.",
                "Place 12 paper muffin cup liners in muffin cups; coat liners with cooking spray. Spoon batter into prepared cups. Bake at 375°F for 25 minutes or until muffins spring back when touched lightly in center."]}])

    recipe(story, "Budapest Tea Bread",
        intro="Light cake.",
        sections=[
            {"type":"ingredients","items":[
                "½ cup brown sugar","3 tbsp. cocoa","3 tbsp. cinnamon",
                "¼ cup raisins","¾ cup walnuts or pecans",
                "1½ sticks margarine","1½ cups sugar","1 tsp. vanilla",
                "2 eggs, slightly beaten","2½ cups flour",
                "1 tsp. baking soda","1 tsp. baking powder","Pinch of salt"]},
            {"type":"steps","items":[
                "Preheat oven to 350°F. Grease and flour a large bundt pan and set aside.",
                "In a small bowl, combine brown sugar, cocoa, cinnamon, raisins and nuts. Set aside.",
                "In a large mixing bowl, cream together margarine and sugar. Add vanilla and eggs, mixing to blend.",
                "By hand, fold in brown sugar-nut mixture.",
                "Pour batter into prepared pan. Bake at 350°F for 50 to 60 minutes."]}])

    recipe(story, "Best Ever Zucchini Bread",
        yld="16 servings",
        sections=[
            {"type":"ingredients","items":[
                "1 cup white sugar","1 cup brown sugar","3 eggs",
                "1 cup vegetable oil (can substitute applesauce for ½ the oil)",
                "3 tsp. vanilla extract","3 cups all-purpose flour",
                "1 tsp. nutmeg","3 tsp. ground cinnamon",
                "1 tsp. baking powder","1 tsp. salt","1 tsp. baking soda",
                "2 cups grated zucchini (can add a little more)",
                "1 cup chopped walnuts"]},
            {"type":"steps","items":[
                "Grease two 8×4 inch pans or 6 mini loaf pans. Preheat oven to 325°F.",
                "Mix flour, salt, baking powder, soda, nutmeg and cinnamon together in a bowl.",
                "Beat eggs, oil, vanilla, and sugar together in a large bowl.",
                "Add dry ingredients to the creamed mixture and beat well.",
                "Grate zucchini. Stir into the mixture along with the nuts until well combined. Pour batter into prepared pans.",
                "Bake for 40 to 60 minutes, or until tester inserted in the center comes out clean. Mini-loaf pans take about 35–40 minutes. Large sized loaves take about 55 minutes.",
                "Cool in pan on rack for 20 minutes. Remove bread from pan and completely cool."]}])

    recipe(story, "Homemade Cinnamon Swirl Bread",
        yld="1 loaf",
        notes="Cover leftover bread tightly and store at room temperature for 6 days or in the refrigerator for up to 10 days. Baked bread freezes well for up to 3 months. Overnight option: allow the dough to rise overnight in the refrigerator instead of in a warm environment.",
        sections=[
            {"type":"ingredients","head":"Dough","items":[
                "½ cup water, warmed to about 110°F",
                "½ cup whole milk, warmed to about 110°F",
                "2¼ tsp. instant or active dry yeast (1 standard packet)",
                "¼ cup granulated sugar, divided",
                "4 tbsp. unsalted butter, softened and cut in 4 pieces",
                "3 cups bread flour, plus more as needed","1 tsp. salt"]},
            {"type":"ingredients","head":"Swirl & Topping","items":[
                "1 egg white, beaten",
                "¼ cup granulated sugar (used a mix of white and brown sugar — add more sugar)",
                "2 tsp. ground cinnamon","1 tbsp. unsalted butter, melted"]},
            {"type":"steps","items":[
                "Prepare the dough: Whisk the warm water, warm milk, yeast, and 2 tbsp. of sugar together in the bowl of a stand mixer fitted with a dough hook. Loosely cover and allow to sit for 5–10 minutes until foamy and frothy on top.",
                "Add the remaining sugar, the butter, 1 cup flour, and the salt. Beat on low speed for 30 seconds, scrape down the sides of the bowl, then add another cup of flour. Beat on medium speed until relatively incorporated. Add the remaining flour and beat on medium speed until the dough comes together and pulls away from the sides of the bowl, about 2 minutes. If the dough seems too wet, beat in more flour 1 tbsp. at a time.",
                "Knead the dough: Keep the dough in the mixer and beat for an additional 8–10 full minutes, or knead by hand on a lightly floured surface for 8–10 full minutes.",
                "1st Rise: Lightly grease a large bowl with oil or nonstick spray. Place the dough in the bowl, turning it to coat all sides. Cover and allow to rise in a relatively warm environment for 1.5–2 hours or until double in size.",
                "Grease a 9×5-inch loaf pan. In a small bowl, whisk ¼ cup sugar and the cinnamon together.",
                "Shape the dough: When the dough is ready, punch it down to release the air. Lightly flour a work surface and roll the dough out into a large 8×20 inch rectangle. Brush the surface with beaten egg white, then sprinkle on the cinnamon-sugar, leaving a 1-inch border uncovered. Roll it up into an 8-inch log. Place the loaf, seam-side down, into the prepared loaf pan.",
                "2nd Rise: Cover the shaped loaf and allow to rise for 1 hour, or until it's about 1 inch above the top of the loaf pan.",
                "Adjust oven rack to a lower position and preheat oven to 350°F. Lightly brush melted butter on top of the shaped loaf before baking. Bake for 35–45 minutes, or until golden brown. The bread is done when an instant-read thermometer inserted into the center registers 195–200°F.",
                "Remove from the oven and allow bread to cool for a few minutes in the pan on a cooling rack. Remove loaf from the pan and cool directly on a cooling rack for at least 10 minutes before slicing."]}])

    recipe(story, "Hot Bread Nan-e Barbari Persian Flatbread",
        yld="2 loaves",
        sections=[
            {"type":"ingredients","head":"Dough","items":[
                "4 cups bread flour",
                "1⅔–1¾ cups water (use smaller amount in summer, larger in winter)",
                "2¼ tsp. yeast","1½ tsp. salt"]},
            {"type":"ingredients","head":"Glaze","items":[
                "2 tsp. flour","½ tsp. sugar","½ tsp. canola oil","⅓ cup water"]},
            {"type":"ingredients","head":"Topping","items":[
                "1 tsp. sesame seeds",
                "1 tsp. nigella seeds (or substitute Everything Bagel Spice)"]},
            {"type":"steps","items":[
                "Make dough: Mix flour, water, yeast, and salt. Knead the dough using a KitchenAid until smooth and soft. Put dough in a lightly greased bowl. Cover the bowl until double in size, about 1 hour. Transfer the dough to a lightly floured surface. Gently deflate the dough and divide into 2 pieces. Shape each piece into a 9-inch log. Gently cover with wrap, allow to rest 30 minutes.",
                "Prepare glaze: Combine flour, sugar, oil, and water in a small saucepan. Bring to boil until it thickens. Cool.",
                "Work one piece at a time. Pat down into a 14×5 rectangle on parchment paper. Use fingers to press dough, spread glaze on dough, and sprinkle with seeds.",
                "Bake at 450°F for 15–18 minutes."]}])

    recipe(story, "Ridiculously Easy Almond Croissants",
        yld="12 croissants",
        sections=[
            {"type":"ingredients","head":"Almond Cream (Frangipane)","items":[
                "3 tbsp. very soft butter","¼ cup granulated sugar",
                "1 large egg","1 tsp. vanilla extract","¼ tsp. almond extract",
                "½ cup almond flour","1 tbsp. all-purpose flour"]},
            {"type":"ingredients","head":"Croissants & Finishing","items":[
                "1 large egg + 1 tsp. water (egg wash)",
                "17.25 oz. package of purchased puff pastry (2 sheets)",
                "½ cup sliced almonds",
                "Powdered sugar for sprinkling"]},
            {"type":"steps","items":[
                "Preheat oven to 400°F. Line a 13×18-inch sheet pan with parchment paper.",
                "Frangipane: Combine the butter and sugar in a medium bowl. Whisk together well. Add the egg and extracts. Whisk again until smooth. Add the almond flour and stir to combine. Add the all-purpose flour and stir again until smooth.",
                "Egg wash: Combine egg and 1 tsp. water in a small bowl. Stir vigorously with a fork until well combined. Set aside.",
                "Unfold thawed (but still cold) puff pastry on a work surface. With a dough cutter or sharp knife, cut the dough into 3 equal-size rectangles. Cut each rectangle into 2 long triangles.",
                "Place all of the triangles with the long end facing you. Cut a small slit at the wide end of each triangle (this will make it easier to roll up).",
                "Scoop 2 tsp. of frangipane onto each triangle. Spread the frangipane over the surface of each triangle. Add one tablespoon of milk to the leftover frangipane and set aside.",
                "Starting at the wide end, roll the dough into croissants. Repeat with the other sheet of puff pastry, then place all of the croissants onto the prepared sheet pan, spacing 1½ inches apart.",
                "Brush each croissant with the egg wash, lightly but covering all of the exposed surfaces.",
                "Bake for 15 minutes. Remove from the oven and brush with the diluted frangipane. Sprinkle each croissant with a scant tablespoon of sliced almonds. Return to the oven for another 5–7 minutes or until medium golden brown.",
                "Remove from the oven and transfer to a cooling rack. Allow the croissants to cool for 10 minutes then sprinkle with powdered sugar."]}])

    recipe(story, "Sullivan Street Bakery Bread",
        yld="1 loaf",
        sections=[
            {"type":"ingredients","items":[
                "3 cups all-purpose or bread flour, plus more for dusting",
                "¼ tsp. instant yeast","1¼ tsp. salt",
                "Cornmeal or wheat bran for dusting, if desired"]},
            {"type":"steps","items":[
                "In a large bowl, combine flour, yeast, and salt. Add 1⅝ cups water, and stir until blended; dough will be shaggy and sticky. Cover bowl with plastic wrap. Let dough rest at least 12 hours, preferably about 18, at warm room temperature, about 70°F.",
                "Dough is ready when its surface is dotted with bubbles. Lightly flour a work surface and place dough on it; sprinkle it with a little more flour and fold it over on itself once or twice. Cover loosely with plastic wrap and let rest about 15 minutes.",
                "Using just enough flour to keep dough from sticking, gently and quickly shape dough into a ball. Generously coat a cotton towel (not terry cloth) with flour, wheat bran, or cornmeal; put dough seam side down on towel and dust with more flour, bran, or cornmeal. Cover with another cotton towel and let rise for about 2 hours.",
                "At least a half hour before dough is ready, heat oven to 450°F. Put a 6- to 8-quart heavy covered pot (cast iron, enamel, Pyrex, or ceramic) in oven as it heats. When dough is ready, carefully remove pot from oven. Slide your hand under towel and turn dough over into pot, seam side up. Shake pot once or twice if dough is unevenly distributed.",
                "Cover with lid and bake 30 minutes, then remove lid and bake another 15 to 30 minutes, until loaf is beautifully browned. Cool on a rack."]}])

    recipe(story, "No-Knead Harvest Bread",
        meta="Prep: 15 min | Bake: 50 min to 1 hr | Total: 11 hrs 10 min | Yield: 1 loaf",
        intro="Very good — great for French toast! Plan ahead for this easy bread — an overnight or all-day rise gives it terrific flavor.",
        notes="Store the bread, well wrapped, at room temperature for several days; freeze for longer storage.",
        sections=[
            {"type":"ingredients","items":[
                "3¼ cups (390g) King Arthur Unbleached Bread Flour",
                "1 cup (113g) King Arthur Whole Wheat Flour",
                "2 teaspoons (12g) salt","½ teaspoon instant yeast",
                "1¾ cups (397g) cool water",
                "¾ cup (85g) dried cranberries",
                "½ cup (85g) golden raisins",
                "1 cup (113g) coarsely chopped pecans or walnuts"]},
            {"type":"steps","items":[
                "Weigh your flour; or measure it by gently spooning it into a cup, then sweeping off any excess. Mix the flours, salt, yeast, and water in a large bowl. Stir, then use your hands to bring the sticky dough together, making sure to incorporate all of the flour.",
                "Work in the fruits and nuts.",
                "Cover the bowl with plastic wrap and let the dough rest at room temperature overnight, or for at least 8 hours; it'll become bubbly and rise quite a bit, so use a large bowl.",
                "Turn the dough out onto a lightly floured surface, and form it into a log or round loaf to fit your lidded baking vessel. Place the dough in the lightly greased pan, smooth side up.",
                "Cover and let rise at room temperature for about 2 hours, until it has become puffy.",
                "Using a sharp knife or lame, slash the bread in a crosshatch pattern. Place the lid on the pan, and put the bread in the cold oven. Set the oven temperature to 450°F.",
                "Bake the bread for 45 to 50 minutes (start the timer when you place the bread into the cold oven). Remove the lid and continue to bake for another 5 to 15 minutes, until it's deep brown in color, and a digital thermometer inserted into the center registers about 205°F.",
                "Remove the bread from the oven, turn it out onto a rack, and cool completely before slicing."]}])

    recipe(story, "Chai-Spiced Banana Bread",
        yld="One 9×5-inch loaf",
        intro="Excellent! Infused with cardamom, cinnamon, ginger, and allspice, this chai-spiced banana bread is a lovely twist on basic banana bread.",
        notes="The bread can be frozen for up to 3 months. Wrap securely in aluminum foil, then thaw overnight in the refrigerator before serving.",
        sections=[
            {"type":"ingredients","items":[
                "1 stick (½ cup) unsalted butter","1 cup granulated sugar",
                "2 large eggs, room temperature",
                "1½ cups all-purpose flour, spooned into measuring cup and leveled off",
                "1 teaspoon baking soda","¾ teaspoon ground cardamom",
                "¾ teaspoon cinnamon","¼ teaspoon ground ginger",
                "¼ teaspoon allspice","¾ teaspoon salt",
                "1 cup mashed very ripe bananas, from 2–3 bananas",
                "½ cup sour cream","1 teaspoon vanilla",
                "½ cup chopped walnuts (optional)"]},
            {"type":"steps","items":[
                "Preheat oven to 350°F. Grease a 9×5-inch loaf pan with non-stick cooking spray.",
                "In a large bowl or electric mixer fitted with the paddle attachment, beat the butter and sugar until light and fluffy, about 2 minutes. Beat in eggs one at a time, incorporating well after each addition.",
                "In a medium bowl, whisk together the flour, baking soda, cardamom, cinnamon, ginger, allspice, and salt. Add to the butter mixture and beat gently until just combined. Add bananas, sour cream, and vanilla and mix on low speed until just combined. Gently stir in nuts if using.",
                "Pour batter into prepared loaf pan and bake until deep golden brown and a cake tester inserted into center comes out clean, 60–70 minutes. Let rest in pan for about 10 minutes, then turn out onto rack to cool."]}])

    recipe(story, "Pistachio Cardamom Loaf",
        yld="2 loaf pans",
        sections=[
            {"type":"ingredients","items":[
                "1 cup flour","½ cup ground pistachio",
                "½ cup chopped unsalted pistachios",
                "1 tsp. ground cardamom","½ tsp. baking soda",
                "½ tsp. baking powder","½ tsp. salt",
                "1 cup sugar","½ cup butter, softened","2 eggs",
                "1 tsp. vanilla","½ cup buttermilk",
                "1–2 drops green food coloring"]},
            {"type":"steps","items":[
                "Mix together the first 7 dry ingredients. In a separate bowl, cream together the butter and sugar, then add eggs one at a time, mixing well after each addition.",
                "Stir in the dry ingredients alternately with the buttermilk, vanilla, and food coloring until smooth.",
                "Spray loaf pans with cooking spray. Divide batter between 2 small loaf pans and bake at 350°F for 55 minutes, or until a toothpick inserted in the center comes out clean."]}])

    recipe(story, "Best Lemon Loaf (Starbucks Copycat)",
        yld="1 loaf",
        meta="Bake: 50–55 min at 350°F",
        sections=[
            {"type":"ingredients","head":"Loaf","items":[
                "3 eggs","1 cup sugar","1 cup sour cream or Greek yogurt",
                "½ cup canola oil","2 Tbsp. lemon zest",
                "1–2 Tbsp. lemon extract","1½ cups flour",
                "2 tsp. baking powder","½ tsp. salt"]},
            {"type":"ingredients","head":"Lemon Glaze","items":[
                "1 cup powdered sugar","3 Tbsp. lemon juice"]},
            {"type":"steps","items":[
                "To a bowl, add eggs, sugar, and sour cream; mix until smooth. Drizzle in oil to combine. Add lemon zest and lemon extract.",
                "Add flour, baking powder, and salt. Do not over mix.",
                "Spray pan. Bake 50–55 minutes. Cool, then apply glaze."]}])

    recipe(story, "Date Nut Bread",
        intro="Good — can be made ahead, can be frozen.",
        sections=[
            {"type":"ingredients","items":[
                "1 tsp. baking soda","1 box chopped dates",
                "1 cup boiling water","1 egg","1¼ tsp. baking powder",
                "¼ tsp. salt","1¼ cup butter, softened",
                "¾ cup sugar","1 cup chopped walnuts"]},
            {"type":"steps","items":[
                "Dissolve baking soda in boiling water. Stir in dates and set aside.",
                "Cream butter and add sugar and egg. Combine flour, baking powder, and salt. Add to creamed mixture.",
                "Add dates. Stir in nuts. Pour into greased, floured pan (4½×3).",
                "Bake at 350°F for 55 to 60 minutes."]}])

    # ── CHAPTER 13 ────────────────────────────────────────────────────────────
    chapter_opener(story, "13", "Cakes, Cookies and Cupcakes",
        tag="The big chapter — and it earns it. Pistachio Cake, Italian Almond Ricotta Cake when you want to impress, and Snickerdoodles, Russian Tea Cakes, and Almond Biscotti for the cookie tin that never stays full.")

    recipe(story, "Old-Fashioned Buttermilk Pound Cake",
        sections=[
            {"type":"ingredients","items":[
                "½ cup butter (soft)","½ cup shortening","2 cups sugar",
                "4 eggs","1 cup buttermilk","½ tsp. baking soda",
                "3 cups flour","⅛ tsp. salt",
                "2 tsp. lemon extract","1 tsp. almond extract"]},
            {"type":"steps","items":[
                "Cream butter & shortening. Then add sugar. Add eggs one at a time.",
                "Dissolve baking soda in buttermilk.",
                "Combine flour & salt. Add to creamed mixture alternating with buttermilk.",
                "Stir in lemon & almond extract.",
                "Grease 10-inch tube pan. Bake at 350°F for 1 hour, 5 minutes.",
                "Cool cake 15 minutes in pan."]}])

    recipe(story, "Cinnamon Crown Cake",
        sections=[
            {"type":"ingredients","items":[
                "3 cups flour","2 cups sugar","3 tsp. baking powder",
                "½ tsp. salt","1 cup butter (soft)","1 cup milk",
                "3 eggs","3 tsp. vanilla","½ cup chopped nuts",
                "½ cup quick cooking oats","½ cup brown sugar",
                "2 tsp. cinnamon","½ cup applesauce"]},
            {"type":"steps","items":[
                "Grease bundt or tube pan.",
                "In a large bowl, combine first 8 ingredients. Spoon half of batter in pan.",
                "Stir remaining ingredients (nuts, oats, brown sugar, cinnamon, applesauce) into leftover batter.",
                "Bake at 350°F for 55 to 65 minutes. Serve warm with ice cream."]}])

    recipe(story, "Coconut Carrot Cake",
        sections=[
            {"type":"ingredients","head":"Cake","items":[
                "2 cups flour","2½ tsp. baking soda","2 tsp. cinnamon",
                "1 tsp. salt","1 cup oil","2 cups sugar","3 eggs",
                "1 can (8 oz.) crushed pineapple in juice",
                "2 cups grated carrots","1½ cups coconut","½ cup chopped nuts"]},
            {"type":"ingredients","head":"Coconut Cream Frosting","items":[
                "1 cup coconut, toasted","1 pkg. (3 oz.) cream cheese",
                "¼ cup butter","3 cups confectioner's sugar",
                "1 tbsp. milk","½ tsp. vanilla"]},
            {"type":"steps","items":[
                "Mix flour, baking soda, cinnamon, salt.",
                "Beat oil, sugar and eggs well. Add flour mixture. Beat until smooth.",
                "Add pineapple, carrots, coconut, nuts.",
                "Pour into greased 13×9 inch pan. Bake at 350°F for 50 to 60 minutes.",
                "Cool 10 minutes. Remove from pan. Cool on rack.",
                "Frosting: Toast 1 cup coconut; cool. Cream cream cheese with butter. Alternately add confectioner's sugar, milk, and vanilla. Beat until smooth. Add ½ the coconut. Frost cake, topping with the rest of the coconut."]}])

    recipe(story, "Dark Chocolate Cake",
        sections=[
            {"type":"ingredients","head":"Cake","items":[
                "2 cups sugar","2 cups flour","2 tsp. baking powder",
                "8 tbsp. cocoa","2 cups boiling water","2 tsp. baking soda",
                "8 tbsp. oil","2 eggs","2 tsp. vanilla"]},
            {"type":"ingredients","head":"White Butter Frosting","items":[
                "⅓ cup soft butter","3 cups confectioner's sugar",
                "1½ tsp. vanilla","3 tbsp. milk"]},
            {"type":"steps","items":[
                "Add sugar, flour, baking powder, cocoa without mixing.",
                "Then add boiling water, baking soda, oil. Stir in eggs and vanilla.",
                "Pour into greased 13×9 inch pan. Bake at 350°F for 30 to 35 minutes.",
                "Frosting: Beat butter, sugar, vanilla, and milk together until smooth."]}])

    recipe(story, "Hummingbird Cake",
        sections=[
            {"type":"ingredients","head":"Cake","items":[
                "3 cups flour","2 cups sugar","1 tsp. baking soda",
                "1 tsp. salt","1 tsp. cinnamon","3 eggs","1 cup oil",
                "1½ tsp. vanilla","8 oz. crushed pineapple (not drained)",
                "1 cup chopped pecans","2 cups chopped bananas"]},
            {"type":"ingredients","head":"Frosting","items":[
                "1 (8 oz.) cream cheese, soft","½ cup butter, soft",
                "1 (16 oz.) powdered sugar","1 tsp. vanilla"]},
            {"type":"steps","items":[
                "Combine first 5 dry ingredients. Add eggs and oil. Stir in vanilla, pineapple, pecans and bananas.",
                "Spoon batter into 3 greased and floured 9-inch round pans.",
                "Bake at 350°F for 30 minutes.",
                "Frosting: Combine cheese and butter, beat until smooth. Add sugar and vanilla.",
                "When cool, spread frosting between layers, top and sides. Sprinkle ½ cup pecans on top."]}])

    recipe(story, "Italian Cake (Mom's)",
        sections=[
            {"type":"ingredients","head":"Cake","items":[
                "½ cup butter","2 cups sugar","4 eggs",
                "2 tsp. baking powder","½ tsp. salt","3 cups flour",
                "2 tsp. lemon extract","1½ cups milk"]},
            {"type":"ingredients","head":"Frosting","items":[
                "Confectioner's sugar","Milk","Lemon extract"]},
            {"type":"steps","items":[
                "Cream butter and sugar. Add eggs one at a time.",
                "Add flour mixture and alternate with milk. Add lemon extract.",
                "Grease bundt pan. Bake at 350°F for 50 to 60 minutes.",
                "Frosting: Mix confectioner's sugar, milk and lemon extract. Drizzle over cake."]}])

    recipe(story, "Grandma Sabol's Lemon-Lime Refrigerator Sheet Cake",
        notes="Cake must be stored in refrigerator.",
        sections=[
            {"type":"ingredients","head":"Cake","items":[
                "1 pkg. lime gelatin (4 serving) or any flavor",
                "1 pkg. Duncan Hines Lemon Supreme Cake mix"]},
            {"type":"ingredients","head":"Topping","items":[
                "1 envelope whipped topping mix (2–2½ cup yield)",
                "1 pkg. lemon instant pudding mix (4 serving)",
                "1½ cups cold milk"]},
            {"type":"steps","items":[
                "Dissolve gelatin in ¾ cup boiling water. Add ½ cup cold water; set aside at room temperature.",
                "Mix and bake cake as directed in a 13×9 inch pan. Cool cake 20–25 minutes.",
                "Poke deep holes through the top of warm cake (still in the pan) with a meat fork or toothpick, spaced about one inch apart.",
                "With a cup, slowly pour gelatin mixture into holes. Refrigerate cake while preparing topping.",
                "Topping: In a chilled deep bowl, blend and whip topping mixture, instant pudding, and cold milk until stiff. Frost cake."]}])

    recipe(story, "Pistachio Cake – Mom's",
        sections=[
            {"type":"ingredients","head":"Cake","items":[
                "1 box white cake mix","1 pkg. pistachio pudding",
                "3 eggs","½ cup oil","1 cup club soda"]},
            {"type":"ingredients","head":"Frosting","items":[
                "½ pint heavy cream","1 cup half & half",
                "1 pkg. pistachio pudding"]},
            {"type":"steps","items":[
                "Mix all together. Pour into well greased bundt pan.",
                "Bake at 350°F for 50 to 60 minutes.",
                "Frosting: Blend half & half and pudding together until thick. Mix heavy cream until thick, then fold together & frost cake."]}])

    recipe(story, "Pistachio Cake – Linda Bailey",
        sections=[
            {"type":"ingredients","head":"Cake","items":[
                "1 pkg. Duncan Hines Yellow cake mix","2 pkgs. pistachio pudding",
                "½ cup Crisco oil","½ pint sour cream",
                "1 tsp. almond extract","4 eggs"]},
            {"type":"ingredients","head":"Topping","items":[
                "½ cup light brown sugar","½ cup chopped walnuts","1 tsp. cinnamon"]},
            {"type":"steps","items":[
                "Beat everything together for 5 minutes.",
                "Grease tube pan and put in half of the batter. Add ½ of the topping, then put remaining batter and the rest of the topping.",
                "Bake at 350°F for 1 hour."]}])

    recipe(story, "Pat Holloway's Sour Cream Coffee Cake",
        sections=[
            {"type":"ingredients","head":"Cake","items":[
                "½ lb. butter","3 eggs","1 cup sugar",
                "3 tsp. baking powder","1 tsp. baking soda","½ tsp. salt",
                "½ pint sour cream","3 cups flour"]},
            {"type":"ingredients","head":"Topping","items":[
                "½ cup sugar","½ tsp. cinnamon","½ cup chopped nuts"]},
            {"type":"steps","items":[
                "Cream butter and sugar. Add eggs, then flour mixed with baking powder, soda and salt.",
                "Add sour cream & mix well.",
                "Blend topping ingredients.",
                "Put half of batter in greased & floured angel food pan. Sprinkle half of topping mixture in batter. Pour remaining batter, then remaining topping over final layer.",
                "Bake at 350°F for 50 minutes."]}])

    recipe(story, "Orange Walnut Cake",
        notes="Freezes well.",
        sections=[
            {"type":"ingredients","items":[
                "¾ cup butter","¾ cup sugar","3 eggs",
                "1 tbsp. fresh grated orange peel",
                "1 tbsp. frozen orange juice","2 cups flour",
                "2 tsp. baking powder","½ tsp. salt","½ cup chopped walnuts"]},
            {"type":"steps","items":[
                "Grease a 9×5×3 loaf pan. Stir flour, baking powder and salt.",
                "In a large bowl, beat butter until creamy. Add sugar, ¼ at a time, beating well after each addition.",
                "Beat eggs one at a time. At a low speed, mix in flour mixture.",
                "Scrape mixture into pan. Bake at 350°F for 55 to 60 minutes."]}])

    recipe(story, "Sour Cream Chocolate Pound Cake",
        sections=[
            {"type":"ingredients","items":[
                "1 cup butter","2 cups sugar","2 eggs",
                "2 sq. chocolate or 4 tbsp. cocoa","2 tsp. vanilla",
                "1 cup sour cream","2 tsp. baking soda",
                "2½ cups flour","¼ tsp. salt","1 cup boiling water"]},
            {"type":"steps","items":[
                "Cream butter, sugar, and add eggs one at a time. Stir in chocolate and vanilla.",
                "Mix sour cream and baking soda. Sift flour and salt. Add boiling water.",
                "Pour into greased tube pan. Dust with cocoa.",
                "Bake at 325°F for 1 to 1½ hours."]}])

    recipe(story, "Italian Almond Ricotta Cake, My Way",
        meta="Prep: 5 min | Cook: 40 min | Serves: 1 cake (9-inch)",
        intro="Excellent — serve sliced with strawberries and cream! This cake is best served on the same day that it is baked.",
        sections=[
            {"type":"ingredients","items":[
                "Pat of butter and sprinkle of sugar (for the pan)",
                "1 stick (113g) unsalted butter, melted","1 cup sugar",
                "Pinch of salt","Zest of 2 lemons",
                "1 capful of pure almond extract","4 large eggs",
                "1 cup ricotta, part skim or whole",
                "1½ cups almond meal*","1 cup all-purpose flour",
                "1½ tsp. baking powder",
                "¼ cup flaked almonds, plus more as needed",
                "Powdered sugar, for decoration",
                "*When measuring, gently spoon into measuring cup. Do not pack."]},
            {"type":"steps","items":[
                "Preheat your oven to 350°F. Lightly coat the bottom and sides of a 9-inch springform pan with butter. Sprinkle with sugar.",
                "In a large mixing bowl, add the melted butter, sugar, salt, lemon zest, and almond extract. Whisk to combine.",
                "Add the eggs, one at a time, mixing well after each addition.",
                "Add the ricotta and continue to whisk vigorously until there are no lumps present. This step is essential for a light and fluffy texture.",
                "Add the almond meal, flour, and baking powder. Mix gently to combine.",
                "Pour the batter into your prepared pan. Sprinkle with the flaked almonds.",
                "Bake for approximately 35–40 minutes (check at the 35-minute mark). Insert a toothpick into the center of the cake; if it comes out clean, it's ready.",
                "Cool in the tin for 15 minutes. Then remove the outer ring to finish cooling.",
                "Right before serving, dust with powdered sugar. Cut into slices and serve."]}])

    recipe(story, "Brownies",
        yld="16 brownies",
        notes="The espresso powder will enhance the chocolate flavor. Your brownies are done baking when the center is still moist — you should see moist crumbs, not uncooked batter. Do not overbake if you want gooey brownies.",
        sections=[
            {"type":"ingredients","items":[
                "½ cup unsalted butter (1 stick)","¾ cup granulated sugar",
                "½ cup all-purpose flour",
                "¾ cup cocoa powder (Dutch processed recommended)",
                "½ tsp. salt","½ tsp. baking powder",
                "1 tbsp. espresso powder (optional)",
                "2 large eggs, at room temperature",
                "1 cup semi-sweet chocolate chips (or your favorites)"]},
            {"type":"steps","items":[
                "Preheat your oven to 350°F. Spray an 8×8-inch baking pan with cooking oil, then line it with parchment paper.",
                "In a small saucepan, melt the butter over medium-low heat. Once melted, add the sugar and stir; bring the sugar and butter to a boil, then quickly remove from the heat.",
                "In a large bowl, add the flour, cocoa powder, salt, baking powder, and espresso powder if using; whisk well. Pour in the butter and sugar mixture slowly and whisk well.",
                "Add the eggs and continue to whisk or stir with a spatula until combined. Fold in the chocolate chips with a spatula.",
                "Transfer the batter to the prepared baking pan and smooth out the top. Bake for 20 to 25 minutes. The brownies should feel set on the edges, and the center should look very moist, but not uncooked.",
                "Let the brownies cool in the pan for about 10 minutes, then cut into squares and enjoy!"]}])

    recipe(story, "Marta Baldelli's Italian Cookie",
        sections=[
            {"type":"ingredients","head":"Cookies","items":[
                "12 eggs","2 cups sugar","1 lb. butter",
                "13 spoons baking powder","5 pounds flour",
                "½ small bottle of lemon extract"]},
            {"type":"ingredients","head":"Icing","items":[
                "Confectioner's sugar (½ bag)","3 tbsp. milk","Lemon extract"]},
            {"type":"steps","items":[
                "Cream eggs, sugar, and butter.",
                "Mix baking powder with flour. Add lemon extract.",
                "Shape into small balls. Bake at 400°F until light brown.",
                "Icing: Mix confectioner's sugar, milk, and lemon extract. Decorate right after icing."]}])

    recipe(story, "Press Cookie",
        notes="Can double recipe.",
        sections=[
            {"type":"ingredients","items":[
                "1 cup corn oil margarine","½ cup sugar","1 egg",
                "1–3 tsp. vanilla","3 cups flour",
                "½ tsp. salt","½ tsp. baking powder"]},
            {"type":"steps","items":[
                "Cream margarine and sugar. Then add egg and vanilla.",
                "Add flour mixture. Chill 3 hours before putting into cookie press.",
                "May add color to dough.",
                "Bake at 350°F for 8 to 10 minutes."]}])

    recipe(story, "Russian Tea Cakes",
        yld="4 dozen",
        sections=[
            {"type":"ingredients","items":[
                "1 cup butter","1 tsp. vanilla",
                "½ cup confectioner's sugar","¼ tsp. salt",
                "¾ cup finely chopped nuts","2¼ cups flour"]},
            {"type":"steps","items":[
                "Mix butter, sugar and vanilla well.",
                "Stir flour and salt together. Blend in nuts.",
                "Chill dough. Roll dough into very small balls (1 inch).",
                "Place on ungreased cookie sheets. Bake at 400°F for 10 minutes until set but not brown.",
                "While still warm, roll into confectioner's sugar. Cool and roll again in sugar."]}])

    recipe(story, "Snickerdoodles",
        notes="Can halve recipe.",
        sections=[
            {"type":"ingredients","items":[
                "2¼ cups flour","2 tsp. cream of tartar",
                "1 tsp. baking soda","¼ tsp. salt","1 cup butter",
                "1½ cups sugar","2 eggs",
                "¼ cup sugar & cinnamon (for rolling)"]},
            {"type":"steps","items":[
                "Cream butter, sugar and eggs for 3 minutes. Add flour and remaining ingredients.",
                "Wrap dough and chill 1 hour or longer.",
                "Roll dough in small balls & roll in sugar-cinnamon mixture.",
                "Bake at 400°F for 8 to 10 minutes on ungreased sheet."]}])

    recipe(story, "Peppermint Crunch Bark",
        intro="Christmas — Can be made ahead | Can be frozen.",
        sections=[
            {"type":"ingredients","items":[
                "1 lb. white chocolate chips",
                "⅓ lb. (¾ cup) peppermint crunch (or 1 pkg. candy canes, crushed)"]},
            {"type":"steps","items":[
                "Melt white chocolate chips in a double boiler — place a smaller pan inside a larger pan of hot water over the stovetop — and stir until smooth.",
                "Add peppermint crunch or crushed candy canes and mix well.",
                "Spread on a cookie sheet covered with waxed paper. Freeze until firm. Break into pieces."]}])

    recipe(story, "Pecan Tassie Tarts",
        yld="2 dozen",
        sections=[
            {"type":"ingredients","head":"Pastry","items":[
                "3 oz. cream cheese","½ cup butter","1 cup flour"]},
            {"type":"ingredients","head":"Pecan Filling","items":[
                "1 egg","¾ cup brown sugar","1 tbsp. butter, melted",
                "1 tsp. vanilla","Dash of salt","⅔ cup pecans, chopped"]},
            {"type":"steps","items":[
                "Let cream cheese and butter soften at room temperature. Blend. Stir in flour. Chill about 1 hour.",
                "Shape into 2 dozen 1-inch balls. Place in tiny ungreased miniature muffin tins. Press dough on bottom and sides of cups.",
                "Filling: Beat together egg, sugar, butter, vanilla and salt until smooth.",
                "Divide half the pecans among pastry-lined cups. Add egg mixture and top with remaining pecans.",
                "Bake at 325°F for 25 minutes. Cool before removing from pan."]}])

    recipe(story, "Almond Biscotti",
        yld="48 biscotti",
        notes="The dough can be frozen for up to 3 months. Shape into 2 logs, wrap securely in plastic wrap, and place in a sealable bag. When ready to bake, thaw until pliable and proceed with recipe.",
        sections=[
            {"type":"ingredients","items":[
                "2½ cups all-purpose flour, spooned into measuring cup and leveled",
                "¼ cup cornmeal (next time use less)",
                "1 tsp. baking powder","1 tsp. salt",
                "1 tsp. anise seeds, crushed with the back of a spoon into a powder",
                "10 tbsp. unsalted butter",
                "1⅓ cup sugar (next time cut to 1 cup)","2 large eggs",
                "2 tsp. vanilla extract","½ tsp. almond extract",
                "1¾ cups slivered almonds, chopped"]},
            {"type":"steps","items":[
                "Preheat the oven to 350°F and set the oven racks in the upper and middle thirds of the oven. Line two baking sheets with parchment paper.",
                "In a medium bowl, whisk together the flour, cornmeal, baking powder, salt and crushed anise seeds.",
                "In the bowl of an electric mixer, cream the butter and sugar until light and fluffy, about 2 minutes. Add the eggs, one at a time, beating well after each addition. Mix in the vanilla and almond extracts. Add the flour mixture and almonds and mix on low speed until just combined. Dust your hands lightly with flour and divide the dough evenly into two disks; wrap in plastic wrap and refrigerate for at least 15 minutes.",
                "Remove the dough from the refrigerator and divide each disk into two equal pieces. Dust your hands with flour and form each portion into logs about 2 inches wide and ¾ inch tall directly on the lined baking sheets. Leave about 4 inches of space between the logs.",
                "Bake for 25–30 minutes, rotating the pans from top to bottom and front to back midway through, until the loaves are firm to the touch and golden around the bottom edges. Remove from the oven and let cool for 20 minutes.",
                "Once cool, transfer the logs to a cutting board. Using a serrated knife and a sawing motion, cut the logs diagonally into generous ½-inch slices. Arrange the cookies, cut side down, back on one of the lined baking sheets. Return to the oven on the middle rack and cook for 5–7 minutes, until lightly golden on the underside. Remove the pan from the oven, carefully flip the biscotti over and cook for 5 minutes more.",
                "Let cool on the baking sheet completely before serving. Keeps in an airtight container for up to a month."]}])

    # ── CHAPTER 14 ────────────────────────────────────────────────────────────
    chapter_opener(story, "14", "Desserts",
        tag="The last chapter and the first one people look for. Grandma Sabol's Apple Dumplings, Mom's Cinnamon Rolls, Cheesecake Supreme — alongside the Lebanese sweets that mark every holiday: Namoura and more. Every recipe here carries a memory.")

    recipe(story, "Apple Dumplings (Grandma Sabol's)",
        sections=[
            {"type":"ingredients","head":"Pastry","items":[
                "2¼ cups flour","½ tsp. salt","¾ cup shortening",
                "7 to 8 tbsp. water"]},
            {"type":"ingredients","head":"Filling","items":[
                "Apples (McIntosh recommended)",
                "Sugar","Butter","½ tsp. cinnamon"]},
            {"type":"ingredients","head":"Syrup","items":[
                "1 cup sugar","4 tbsp. butter",
                "2 cups water","1 tsp. vanilla"]},
            {"type":"steps","items":[
                "Sift flour and salt together. Cut in shortening with knife, leaving some the size of peas. Add enough water to make flour stick together. The dough should make 5 to 6 dumplings.",
                "Divide the dough in three sections. Roll out and cut into 7-inch squares.",
                "Pare and core the apples. Place one apple on each square.",
                "Fill each cavity with some sugar, a pat of butter and cinnamon. Fold the corners up over the apple.",
                "Syrup: Mix sugar, butter, water and vanilla together; let boil for 3 minutes.",
                "Place dumplings in a baking dish. Pour hot syrup around the dumplings.",
                "Bake immediately at 500°F for 5 to 7 minutes, then reduce to 350°F for 35 minutes.",
                "Serve with vanilla ice cream."]}])

    recipe(story, "Cinnamon Rolls (Mom)",
        variations="Apple Cinnamon Rolls: Substitute 1 cup finely chopped apples for raisins. Can be mixed & rolled the night before and baked the next day. Can use a little maple syrup in the glaze.",
        sections=[
            {"type":"ingredients","head":"Dough","items":[
                "4½ to 5 cups flour","1 pkg. dry yeast","1 cup milk",
                "⅓ cup butter","⅓ cup sugar","½ tsp. salt","3 eggs"]},
            {"type":"ingredients","head":"Filling","items":[
                "¾ cup brown sugar","¼ cup flour","1 tbsp. cinnamon",
                "½ cup butter","½ cup raisins (optional)","½ cup pecans"]},
            {"type":"ingredients","head":"Glaze","items":[
                "1 tbsp. half-n-half","1¼ cup powdered sugar",
                "1 tsp. corn syrup","½ tsp. vanilla",
                "Enough half-n-half to drizzle"]},
            {"type":"steps","items":[
                "In a large bowl, combine 2¼ cups flour & yeast.",
                "In a small saucepan, heat milk, ⅓ cup butter, ⅓ cup sugar, salt to 120–130°F and butter is melted. Add to flour mix. Add eggs, beat on low speed 30 seconds, then high speed for 3 minutes.",
                "Use spoon and add rest of flour (2½ to 2¾ cups). Knead until dough is smooth. Place in greased bowl. Cover and let rise about 1 hour.",
                "Filling: Combine brown sugar, ¼ cup flour, cinnamon and add butter till crumbly.",
                "Punch dough down. Cover and let rise 10 minutes. Roll dough into 12-inch square. Sprinkle filling over dough; top with raisins and pecans. Roll up like a jellyroll, pinching edges to seal.",
                "Slice into 8 pieces (1½ inch each). Arrange cut side up in greased 13×9 pan.",
                "Cover with plastic wrap. Refrigerate 2 to 24 hours. Uncover and let stand at room temperature 30 minutes. (Or for immediate baking, skip chilling and let rise in a warm place for 45 minutes.)",
                "Brush dough with half-n-half. Bake at 375°F for 25 to 30 minutes. Remove and brush with half-n-half.",
                "Glaze: Mix powdered sugar, corn syrup, vanilla and enough half-n-half to drizzle over rolls."]}])

    recipe(story, "Bavarian Apple Torte",
        sections=[
            {"type":"ingredients","head":"Crust","items":[
                "½ cup butter, soft","⅓ cup sugar",
                "¼ tsp. vanilla","1 cup flour"]},
            {"type":"ingredients","head":"Filling","items":[
                "1 (8 oz.) cream cheese, soft","¼ cup sugar",
                "1 egg","½ tsp. vanilla"]},
            {"type":"ingredients","head":"Apple Topping","items":[
                "⅓ cup sugar","½ tsp. cinnamon",
                "4 large tart apples, peeled and sliced",
                "¼ cup sliced almonds"]},
            {"type":"steps","items":[
                "Crust: Cream butter, sugar and vanilla. Blend in flour. Pat dough on bottom and 1½ inches up sides of a greased 9-inch spring form pan.",
                "Filling: Combine cream cheese and sugar. Mix well, then add egg and vanilla. Pour into pastry-lined pan.",
                "Topping: Combine sugar and cinnamon. Toss apples into mixture. Spoon or layer apple mixture over cream cheese. Sprinkle with almonds.",
                "Bake at 450°F for 10 minutes, then reduce heat to 400°F for 25 minutes.",
                "Cool before removing rim of pan."]}])

    recipe(story, "Claudette Murray's Cheesecake Supreme",
        sections=[
            {"type":"ingredients","head":"Crust","items":[
                "¾ cup flour","3 tbsp. sugar","½ tsp. grated lemon peel",
                "6 tbsp. butter, soft","1 egg yolk","¼ tsp. vanilla"]},
            {"type":"ingredients","head":"Filling","items":[
                "3 (8 oz.) cream cheese","1 cup sugar","2 tbsp. flour",
                "¼ tsp. remaining lemon peel","½ tsp. vanilla (remaining)",
                "¼ tsp. salt","2 eggs","1 egg yolk","¼ cup milk"]},
            {"type":"steps","items":[
                "Crust: Combine ¾ cup flour, 3 tbsp. sugar, ½ tsp. lemon peel. Cut in butter until crumbly. Stir in slightly beaten egg yolk and ¼ tsp. vanilla. Mix well.",
                "Pat ¾ of mixture on bottom of spring form pan. Bake at 400°F for 7 minutes till golden.",
                "Butter sides of pan (attach to bottom). Gently pat remaining dough on sides, up to 1¾ inches.",
                "Filling: Let cream cheese soften. Beat till creamy and add remaining lemon peel and vanilla.",
                "Mix 1 cup sugar, 2 tbsp. flour, salt. Gradually add to cheese. Add 2 eggs and 1 egg yolk all at once. Stir in milk. Pour into pan.",
                "Bake at 450°F for 10 minutes, reduce to 300°F for 55 minutes till set.",
                "Remove from oven, cool 15 minutes and loosen sides. Cool ½ hour more and remove sides. Cool 2 hours or overnight."]}])

    recipe(story, "Mini Blueberry Cups",
        notes="Can halve recipe.",
        sections=[
            {"type":"ingredients","head":"Crust","items":[
                "1 cup butter","6 oz. cream cheese","2 cups flour"]},
            {"type":"ingredients","head":"Filling","items":[
                "12 oz. cream cheese","½ cup sugar",
                "½ tsp. vanilla","2 eggs"]},
            {"type":"steps","items":[
                "Crust: Let butter & cream cheese soften at room temp. Blend and then blend in flour. Chill slightly for one hour.",
                "Shape into 72 small balls. Place in ungreased miniature cupcake tin. Press dough on bottom and sides of cups.",
                "Filling: Cream together cheese and sugar until fluffy. Add vanilla & eggs; beat.",
                "Fill to the tops of tart pan. Bake at 350°F for 20 to 25 minutes.",
                "Serve a dollop of Comstock cherry filling on top."]}])

    recipe(story, "Molten Chocolate Lava Cakes",
        meta="Total: about 15 minutes | Prep: 3 min | Cook: about 12 min",
        yld="2 cakes (recipe easily doubles or triples)",
        intro="The best — double the recipe!",
        sections=[
            {"type":"ingredients","items":[
                "2 ounces dark chocolate or bittersweet baking chocolate",
                "¼ cup unsalted butter (½ of 1 stick)",
                "½ cup confectioners' sugar",
                "1 large egg + 1 egg yolk (discard white or save for another use)",
                "3 tablespoons all-purpose flour",
                "1 teaspoon instant espresso coffee granules, optional but recommended",
                "Ice cream for serving, optional but recommended",
                "Hot fudge for serving, optional but recommended"]},
            {"type":"steps","items":[
                "Preheat oven to 425°F and spray two ramekins (about 3–4 inches in diameter or about 4 ounces each) with cooking spray; place ramekins on a baking sheet and set aside.",
                "To a medium microwave-safe bowl, add the chocolate and butter, and heat on high power to melt, about 1 minute. Stop to whisk until smooth. If needed, return bowl to microwave and heat in 15-second increments until chocolate can be whisked smooth.",
                "Add the sugar, egg, and egg yolk, and whisk until smooth.",
                "Add the flour and optional espresso granules, and stir until just combined; don't overmix.",
                "Pour batter into prepared ramekins, divided evenly.",
                "Bake for about 12 minutes, or until edges are set but center is still soft; don't overbake.",
                "Allow cakes to cool in ramekins for about 1 minute, gently run the edge of a paring knife around the ramekins, and invert over serving dishes to dislodge cakes.",
                "Optionally top with ice cream and hot fudge, and serve immediately."]}])

    recipe(story, "Watermelon Granita",
        intro="Good — Can be made ahead.",
        sections=[
            {"type":"ingredients","items":[
                "6 cups peeled, seeded, cubed watermelon",
                "¼ cup sugar","⅛ cup lemon juice"]},
            {"type":"steps","items":[
                "Process watermelon in blender or food processor until smooth (about 4 cups).",
                "Pour into a bowl, add sugar and lemon juice. Stir until sugar is dissolved.",
                "Pour mixture into a 13×9 pan and freeze, stirring occasionally, for 3 hours or until firm.",
                "Scoop frozen mixture into bowls."]}])

    recipe(story, "Blackberry Sorbet",
        intro="A riff on The Easy Vegetarian Cookbook. Minimal ingredients while showcasing fresh fruit. Can substitute raspberries or blueberries.",
        sections=[
            {"type":"ingredients","items":[
                "4 cups (560g) blackberries","2½ cups (600ml) water",
                "2 tablespoons (30ml) lemon juice",
                "½ to 1 cup (100 to 200g) cane sugar"]},
            {"type":"steps","items":[
                "Rinse the blackberries, then combine in a blender with the water and lemon juice. Purée until smooth, then press the mixture through a sieve to remove the seeds.",
                "In a saucepan, whisk together the blackberry juice and sugar. Bring to a boil and reduce to a simmer. Cook for 1 to 2 minutes, until the sugar is fully dissolved. Remove from the heat, transfer to a container, and place in the refrigerator to chill completely.",
                "Freeze the sorbet mixture according to your ice cream maker's directions, or, if not using an ice cream maker, place the mixture in a shallow pan and freeze. Once frozen, break into pieces and purée in a blender or food processor until creamy."]}])

    recipe(story, "Strawberry Banana Ice Cream",
        sections=[
            {"type":"ingredients","items":[
                "2 bananas, sliced and frozen",
                "8–10 strawberries, cut and frozen","1 tsp. vanilla extract"]},
            {"type":"steps","items":[
                "Place frozen bananas and strawberries in a food processor.",
                "Process 4–5 minutes until creamy.",
                "Stir in vanilla. Serve right away as soft serve ice cream or freeze for a couple of hours."]}])

    recipe(story, "Creamy Mango Sorbet",
        intro="Can be made ahead | Can be frozen.",
        sections=[
            {"type":"ingredients","items":[
                "4 cups frozen mango chunks (Costco Organic recommended)",
                "1 cup sugar (or ½ cup sugar + ½ cup honey)",
                "1 can chilled full-fat coconut milk",
                "1 Tbsp. lime juice","¼ tsp. salt"]},
            {"type":"steps","items":[
                "Combine all ingredients in a food processor and blend until thick and smooth.",
                "Serve immediately as soft serve, or transfer to a loaf pan or glass container, cover with plastic wrap, and freeze for 2 to 3 hours. To serve from the freezer, let sit at room temperature for 15 minutes."]}])

    recipe(story, "Pie Crust",
        intro="Can be made ahead | Can be frozen.",
        yld="2 pie crusts",
        sections=[
            {"type":"ingredients","items":[
                "3 cups flour","1 tsp. salt","1 cup shortening",
                "1 egg","4 Tbsp. water","1 tsp. vinegar"]},
            {"type":"steps","items":[
                "Combine flour and salt. Cut in shortening until mixture resembles coarse cornmeal.",
                "Combine beaten egg and water. Sprinkle over flour mixture. Add a little more water if needed until it forms a ball.",
                "Wrap in plastic wrap and chill for 1 hour or more. Makes 2 pie crusts."]}])

    recipe(story, "Italian Waffle Pizzelles",
        sections=[
            {"type":"ingredients","items":[
                "6 eggs","3½ cups flour","1½ cups sugar",
                "1 cup margarine, melted","4 tsp. baking powder",
                "2 tbsp. vanilla or anise"]},
            {"type":"steps","items":[
                "Beat eggs, adding sugar gradually. Beat until smooth.",
                "Add melted margarine and vanilla. Sift flour and baking powder; add to the egg mixture.",
                "Dough will be sticky enough to be dropped by spoon. Use pizzelle maker."]}])

    recipe(story, "Mary Hemeida's Namoura",
        sections=[
            {"type":"ingredients","items":[
                "2 cups regular Cream of Wheat","1¾ cups sugar",
                "2 tbsp. butter, melted","¼ tsp. salt",
                "1 tsp. orange blossom water","1¾ cups yogurt",
                "½ tsp. baking soda"]},
            {"type":"steps","items":[
                "Mix all ingredients and let stand for 30 minutes.",
                "Grease bottom of pan. Bake at 375°F for 35 minutes.",
                "Once out of oven, pour attar syrup over hot cake.",
                "Cool and cut into diamond shapes."]}])

    recipe(story, "Aishi Shervani's Namoura",
        sections=[
            {"type":"ingredients","items":[
                "2 lbs. semolina","1½ lbs. sugar",
                "1¼ lbs. milk","Vegetable oil"]},
            {"type":"steps","items":[
                "Mix all ingredients and let sit for several hours.",
                "Grease bottom of pan with tahini.",
                "Pour mixture into pan.",
                "Bake."]}])

    recipe(story, "Sfoof Cake",
        sections=[
            {"type":"ingredients","items":[
                "3 cups fine semolina","1 cup regular flour",
                "4 tbsp. turmeric","1 cup milk","1 cup oil",
                "2 cups sugar","3 tsp. baking powder",
                "¼ cup tahini","½ cup pine nuts"]},
            {"type":"steps","items":[
                "Mix semolina with flour, turmeric, baking powder.",
                "Mix sugar and oil into mixture, blending well.",
                "Spread tahini on bottom and sides of 9×13 inch pan.",
                "Pour batter in pan and garnish with pine nuts on top.",
                "Bake at 350°F for 30 minutes.",
                "Cool and cut into diamond shapes."]}])

    recipe(story, "Atayef (Pancake Batter)",
        yld="2 dozen",
        sections=[
            {"type":"ingredients","items":[
                "1 cup semolina","1 cup flour",
                "2½ to 3 tsp. yeast","1½ tsp. baking powder",
                "Sugar","3 cups water"]},
            {"type":"steps","items":[
                "Mix together. Let sit 1½ hours, covered; stir occasionally. Mixture should be like thin pancake batter.",
                "Heat griddle. Pour a little batter onto hot griddle so it forms a little circle.",
                "Cook until golden on the underside. Do not flip. Lift out.",
                "Stuff with walnut mixture or Ashta (cream).",
                "Place on a lightly Pam-sprayed tray with a pat of butter on each atayef.",
                "Cover with foil and bake at 350°F for 20 minutes until warm.",
                "Serve with attar syrup."]}])

    recipe(story, "Ashta Cream",
        sections=[
            {"type":"ingredients","head":"Ashta Cream","items":[
                "Small container ricotta cheese",
                "Small container half-n-half",
                "Small container Cool Whip",
                "Semolina","Sugar","Orange blossom water"]},
            {"type":"ingredients","head":"Walnut Mixture (for stuffing atayef)","items":[
                "Walnuts, chopped finely","Sugar","Cinnamon"]},
            {"type":"steps","items":[
                "Mix ricotta cheese, half-n-half, semolina, and 3 tbsp. sugar in a saucepan.",
                "Cook until thick on low heat.",
                "After thick, add orange blossom water. Let cool slightly.",
                "Add 3 big spoons of Cool Whip. Mix well. Refrigerate.",
                "Walnut Mixture: Mix walnuts, sugar and cinnamon together. Ready to stuff atayef."]}])

    recipe(story, "Qudrat Al Qader",
        sections=[
            {"type":"ingredients","items":[
                "1 cup sugar","6 eggs","Zest of 1 lemon",
                "½ tsp. vanilla","1 cup water","½ cup vegetable oil",
                "½ cup milk","2¾ cups flour","2 tsp. baking powder",
                "½ cup dried cocoa (if desired)"]},
            {"type":"steps","items":[
                "Caramel layer: Heat 1 cup of sugar in a pan.",
                "Egg mixture: Mix 3 eggs in a bowl; add the zest of the lemon, the vanilla, 1 cup of sugar and 1 cup of water.",
                "Milk mixture: Mix 3 eggs in a bowl; add 1 cup of sugar, ½ cup of vegetable oil, ½ cup of milk, 1½ cups of flour and 2 tsp. of baking powder.",
                "If making with chocolate, mix ½ cup dried cocoa with 1¼ cups of flour.",
                "Pour the cake mix (caramel layer and egg mixture) over the milk mixture.",
                "Fill pan ½ full with water.",
                "Bake for 1 hour at 450°F.",
                "Refrigerate for 2 hours."]}])

    recipe(story, "Meghli",
        sections=[
            {"type":"ingredients","head":"Pudding","items":[
                "1 cup ground rice (rice flour)","1½ cups sugar",
                "1½ tbsp. fine caraway","1 tsp. fine cinnamon",
                "7 cups water"]},
            {"type":"ingredients","head":"Garnish","items":[
                "Fine coconuts, walnuts, almonds, pistachio, pine nuts"]},
            {"type":"steps","items":[
                "Soak pine nuts and skinned almonds in water overnight (refrigerated). Grind pistachio. Chop walnuts into smaller pieces.",
                "Add rice, sugar, caraway and cinnamon into a pressure cooker. Mix together.",
                "Add water slowly as you continue to mix.",
                "Heat the pressure cooker over a medium heat, stirring continuously, until it starts boiling. Continue to stir for 5 minutes after boiling. Cover pressure cooker.",
                "When the pressure cooker whistle comes on, turn the heat to medium-low and cook for 40 minutes.",
                "After 40 minutes, turn the heat off; cool the pressure cooker under cold water until the pressure is released; then open the lid carefully.",
                "Transfer the Meghli mixture into another pan to avoid the sticking (burnt) layer on the bottom.",
                "Heat the new pan over a medium heat, stirring continuously for 15–20 minutes (after boiling).",
                "Scoop Meghli into small cups, let it cool on counter, cover with saran wrap and refrigerate for 2–3 hours (or overnight).",
                "Top each cup with fine coconuts, chopped walnuts, soaked skinned almonds, ground pistachio and soaked pine nuts as desired."]}])

    recipe(story, "Rice Pudding",
        notes="Optional: broil for 10 minutes. Garnish with ground pistachio nuts.",
        sections=[
            {"type":"ingredients","items":[
                "½ gallon milk (8 cups)","1 cup short grain rice",
                "1 cup sugar","2 tsp. mazaher (orange blossom water)"]},
            {"type":"steps","items":[
                "Rinse rice in water and set aside.",
                "Bring milk to a boil and add rice.",
                "Keep stirring until the mixture becomes creamy and thick (about 1 hour).",
                "Stir in sugar and after 10 minutes, add mazaher."]}])


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN BUILD
# ══════════════════════════════════════════════════════════════════════════════
def build():
    out   = "./output/cookbook_full.pdf"
    photo = "./imgs/debby.jpg"

    doc_kwargs = dict(
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN_INNER, rightMargin=MARGIN_OUTER,
        topMargin=MARGIN_TOP,    bottomMargin=MARGIN_BOTTOM + 0.3*inch,
        title="From the Kitchen of Debby Kobrosly",
        author="Debby Kobrosly")

    def _story(registry=None, photo=photo):
        s = []
        # 2 blank pages before the title page
        s.append(PageBreak())
        s.append(PageBreak())
        build_cover(s)
        build_edition_page(s)
        build_toc(s, registry=registry)
        add_all_recipes(s)
        build_about(s, photo)
        # 2 blank pages after About the Author
        s.append(PageBreak())
        s.append(PageBreak())
        return s

    # ── PASS 1: collect page numbers ──────────────────────────────────────────
    print("Pass 1: collecting page numbers…")
    import io
    doc1 = TrackingDoc(io.BytesIO(), **doc_kwargs)
    story1 = _story(registry=None)
    doc1.build(story1,
        canvasmaker=lambda *a, **kw: CookbookCanvas(*a, page_data={}, **kw))
    registry     = doc1.page_registry
    total_pages  = doc1.page
    print(f"  Tracked {len(registry)} labels — {total_pages} pages total")

    # ── PASS 2: final PDF with real page numbers ───────────────────────────────
    print("Pass 2: building final PDF…")
    doc2 = TrackingDoc(out, **doc_kwargs)
    story2 = _story(registry=registry)
    doc2.build(story2,
        canvasmaker=lambda *a, **kw: CookbookCanvas(
            *a, page_data={}, total_pages=total_pages, **kw))
    print(f"✓ Saved → {out}  ({doc2.page} pages)")

if __name__ == "__main__":
    build()
