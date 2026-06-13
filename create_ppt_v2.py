from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from PIL import Image
import os

IMGS = "/home/user/vedasvision-whatsapp-bot/ppt_images"

# ── Color Palette ──────────────────────────────────────────────────
GOLD       = RGBColor(0xD4, 0xAF, 0x37)
GOLD_LIGHT = RGBColor(0xF5, 0xE6, 0xA3)
DARK_BG    = RGBColor(0x0D, 0x0D, 0x1A)
DARK2      = RGBColor(0x1A, 0x1A, 0x2E)
RED_ALERT  = RGBColor(0xE0, 0x3B, 0x3B)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_LIGHT = RGBColor(0xCC, 0xCC, 0xCC)
GREEN_OK   = RGBColor(0x2E, 0xCC, 0x71)
ORANGE     = RGBColor(0xFF, 0x8C, 0x00)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)


def blank_slide():
    return prs.slides.add_slide(prs.slide_layouts[6])


def fill_bg(slide, color=DARK_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(
        1, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def add_text(slide, text, left, top, width, height,
             font_size=18, bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_img(slide, path, left, top, width=None, height=None):
    full = os.path.join(IMGS, path)
    if not os.path.exists(full):
        return None
    try:
        if width and height:
            return slide.shapes.add_picture(full, Inches(left), Inches(top),
                                            Inches(width), Inches(height))
        elif width:
            return slide.shapes.add_picture(full, Inches(left), Inches(top),
                                            width=Inches(width))
        elif height:
            return slide.shapes.add_picture(full, Inches(left), Inches(top),
                                            height=Inches(height))
        else:
            return slide.shapes.add_picture(full, Inches(left), Inches(top))
    except Exception as e:
        print(f"  [img skip] {path}: {e}")
        return None


def gold_line(slide, top):
    add_rect(slide, 0, top, 13.33, 0.04, GOLD)


def slide_header(slide, title, subtitle=None):
    gold_line(slide, 0)
    add_text(slide, title, 0.4, 0.08, 12.5, 0.65,
             font_size=30, bold=True, color=GOLD, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.4, 0.75, 12.5, 0.4,
                 font_size=16, color=GRAY_LIGHT, align=PP_ALIGN.LEFT, italic=True)
    gold_line(slide, 1.2)


def add_img_with_border(slide, path, left, top, width, height,
                        border_color=GOLD, label=None, label_color=GOLD_LIGHT):
    """Add image with a gold border frame and optional label below."""
    # Gold border (slightly larger)
    pad = 0.06
    add_rect(slide, left - pad, top - pad, width + 2*pad, height + 2*pad + (0.3 if label else 0), border_color)
    # Dark inner background
    add_rect(slide, left, top, width, height, DARK2)
    # Image
    add_img(slide, path, left, top, width, height)
    if label:
        add_text(slide, label, left - pad, top + height + 0.02, width + 2*pad, 0.28,
                 font_size=9.5, color=label_color, align=PP_ALIGN.CENTER, bold=True)


# ══════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
add_rect(s, 0, 0, 13.33, 0.18, GOLD)
add_rect(s, 0, 7.32, 13.33, 0.18, GOLD)
add_rect(s, 0, 1.8, 13.33, 4.2, RGBColor(0x11, 0x11, 0x22))

add_text(s, "INDIA'S BIGGEST MARKET SCAM — EXPOSED", 0.4, 0.22, 12.5, 0.7,
         font_size=17, bold=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)

# Rajesh Exports logo — left side
add_img_with_border(s, "rajesh_exports_logo.png", 0.5, 1.95, 2.5, 1.5,
                    label="RAJESH EXPORTS LTD")

add_text(s, "FRAUD\nEXPOSED", 3.3, 1.9, 6.5, 2.1,
         font_size=54, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

# Valcambi image — right side
add_img_with_border(s, "valcambi_logo_rgba.png", 10.3, 1.95, 2.5, 1.5,
                    label="VALCAMBI SA")

add_text(s, "₹15.15 LAKH CRORE REVENUE SCAM", 0.3, 4.05, 12.7, 0.65,
         font_size=26, bold=True, color=RED_ALERT, align=PP_ALIGN.CENTER)
add_text(s, "How India's Top Gold Exporter Allegedly Fabricated 99% of Its Revenue",
         0.3, 4.75, 12.7, 0.5,
         font_size=17, color=GRAY_LIGHT, align=PP_ALIGN.CENTER, italic=True)
add_text(s, "SEBI Interim Order  |  June 3, 2026  |  A VedasVision Compliance Insight",
         0.3, 6.85, 12.7, 0.4,
         font_size=13, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
# SLIDE 2 — WHO IS RAJESH EXPORTS?
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "WHO IS RAJESH EXPORTS?",
             "The company that claimed to be India's largest gold exporter")

# Rajesh Mehta large photo — left column
add_img_with_border(s, "rajesh_mehta_large.jpg", 0.4, 1.35, 3.2, 2.0,
                    border_color=GOLD, label="RAJESH MEHTA — Chairman & MD")
add_img_with_border(s, "rajesh_exports_logo.png", 0.4, 3.65, 3.2, 1.6,
                    border_color=GOLD, label="Rajesh Exports Limited (RAJESHEXPO)")

# Facts on the right
facts = [
    ("🏢  Founded",        "1995  |  Bengaluru, Karnataka"),
    ("📈  Listed on",       "BSE (531500) & NSE (RAJESHEXPO)"),
    ("🌍  Key Asset",       "Valcambi SA, Switzerland — world's largest gold refinery"),
    ("📊  Reported Rev FY25","₹4.23 LAKH CRORE (consolidated)"),
    ("✅  Actual Verified",  "~₹423 crore  —  only 0.1% of claimed"),
    ("🏦  Key Investor",    "LIC of India  —  10.79% stake (your & mine premium)"),
    ("📉  Stock fall",      "80% decline over 3 years before SEBI order"),
    ("⚡  Post-order",      "Hit lower circuit at ₹103.92 on June 3, 2026"),
]
y = 1.38
for label, val in facts:
    add_rect(s, 3.9, y, 4.8, 0.44, DARK2)
    add_rect(s, 8.85, y, 4.1, 0.44, DARK2)
    add_text(s, label, 4.05, y + 0.07, 4.5, 0.32, font_size=13.5, bold=True, color=GOLD)
    add_text(s, val,   9.0,  y + 0.07, 3.8, 0.32, font_size=13.5, color=WHITE)
    y += 0.54

add_text(s, "⚠️  Harshad Mehta scam = ₹4,000 crore  |  Rajesh Exports alleged = ₹15,15,000 crore  —  3787× BIGGER",
         0.4, 6.85, 12.5, 0.4,
         font_size=13, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
# SLIDE 3 — HOW IT STARTED
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "HOW THE SCAM UNRAVELED",
             "One shareholder complaint → 2-year investigation → India's biggest alleged fraud")

# SEBI logo in header area
add_img_with_border(s, "sebi_logo.jpg", 10.7, 0.1, 2.3, 1.0,
                    border_color=GOLD, label="SEBI — Regulator")

steps = [
    (GOLD,      "MARCH 2024",
     "A shareholder files complaint with SEBI.\nReason: Trade receivables pending for 2+ years — a classic fraud red flag.\n(If sales are real, why is the payment not coming?)"),
    (ORANGE,    "OCT 2024",
     "SEBI launches formal investigation.\nForensic auditor BDO India appointed.\nCompany asked for ERP access, books, journal entries, subsidiary records."),
    (RED_ALERT, "ONGOING",
     "Company refuses full cooperation:\n• Does not give ERP system access\n• Auditors don't submit working papers\n• Cites Swiss data protection laws to block Valcambi records"),
    (GREEN_OK,  "JUNE 3, 2026",
     "SEBI Interim Order issued — HISTORIC:\n• Rajesh Mehta BANNED from securities markets\n• 99% revenue misrepresentation confirmed\n• ₹12,726 crore shareholder wealth destruction estimated"),
]
y = 1.35
for col, title, desc in steps:
    add_rect(s, 0.35, y, 12.6, 1.2, DARK2)
    add_rect(s, 0.35, y, 2.0, 1.2, col)
    add_text(s, title, 0.35, y + 0.35, 2.0, 0.5, font_size=14, bold=True,
             color=DARK_BG, align=PP_ALIGN.CENTER)
    add_text(s, desc, 2.55, y + 0.08, 10.2, 1.04, font_size=12.5, color=WHITE)
    y += 1.3


# ══════════════════════════════════════════════════════════════════
# SLIDE 4 — CORPORATE STRUCTURE
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE SHELL COMPANY WEB",
             "4 layers of subsidiaries — the middle layer NEVER audited")

# Hierarchy boxes
boxes = [
    (4.9,  1.35, 3.5, 0.72, GOLD,      DARK_BG, "REL — Rajesh Exports Limited",      "LISTED IN INDIA  |  NSE / BSE"),
    (4.9,  2.52, 3.5, 0.72, ORANGE,    DARK_BG, "REL Singapore Pte Ltd",              "100% Subsidiary  |  NO Operations"),
    (2.8,  3.7,  3.5, 0.72, RED_ALERT, WHITE,   "GGR — Global Gold Refineries AG",    "95% held by REL Singapore  |  NEVER AUDITED ⚠️"),
    (7.0,  3.7,  3.5, 0.72, DARK2,     GOLD,    "BAB AL Rayan Jewellery LLC",          "100% REL Singapore  |  CEASED"),
    (4.9,  4.9,  3.5, 0.72, GREEN_OK,  DARK_BG, "Valcambi SA",                        "REAL Refinery  |  Balerna, Switzerland"),
]
for lft, tp, w, h, bg, tc, title, sub in boxes:
    add_rect(s, lft, tp, w, h, bg)
    tc_rgb = RGBColor(*tc) if isinstance(tc, tuple) else tc
    add_text(s, title, lft+0.1, tp+0.05, w-0.2, 0.37, font_size=12.5, bold=True, color=tc_rgb)
    add_text(s, sub, lft+0.1, tp+0.4, w-0.2, 0.28, font_size=10, color=GRAY_LIGHT)

# Connector lines
add_rect(s, 6.63, 2.06, 0.04, 0.47, GOLD)
add_rect(s, 6.63, 3.24, 0.04, 0.46, GOLD)

# Company logos in hierarchy boxes
add_img(s, "rajesh_exports_logo.png", 0.38, 1.42, width=1.5)
add_img(s, "valcambi_logo_rgba.png",  11.4, 4.88, width=1.5)

# Key fraud box
add_rect(s, 0.35, 5.8, 12.6, 1.5, RGBColor(0x1E, 0x0A, 0x0A))
add_rect(s, 0.35, 5.8, 0.07, 1.5, RED_ALERT)
add_text(s, "THE CORE FRAUD", 0.57, 5.86, 3.5, 0.35, font_size=14, bold=True, color=RED_ALERT)
add_text(s,
         "GGR — the holding company above Valcambi — was NEVER independently audited.\n"
         "REL booked ₹15 lakh crore revenue at GGR level. Valcambi (KPMG-audited) reported only ₹423–543 crore in the same period.\n"
         "The gap between GGR's claimed revenue and Valcambi's audited revenue = ₹15 LAKH CRORE of alleged fake revenue.",
         0.57, 6.24, 12.1, 1.0, font_size=12, color=WHITE)


# ══════════════════════════════════════════════════════════════════
# SLIDE 5 — REVENUE ILLUSION
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE REVENUE ILLUSION",
             "How ₹15.15 Lakh Crore of 'Revenue' was manufactured from thin air")

# Valcambi gold product image — top right
add_img_with_border(s, "valcambi_img.jpg", 10.55, 1.3, 2.4, 2.4,
                    border_color=GOLD, label="Valcambi Gold Bar")

# Left — reported numbers
add_rect(s, 0.35, 1.3, 5.5, 5.55, DARK2)
add_text(s, "WHAT REL REPORTED", 0.5, 1.37, 5.2, 0.4,
         font_size=16, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
reported = [
    ("FY21", "₹2.02 Lakh Crore"),
    ("FY22", "₹3.31 Lakh Crore"),
    ("FY23", "₹3.28 Lakh Crore"),
    ("FY24", "₹2.38 Lakh Crore"),
    ("FY25", "₹4.23 Lakh Crore"),
    ("TOTAL", "₹15.22 Lakh Crore"),
]
y = 1.87
for yr, rev in reported:
    col = RED_ALERT if yr == "TOTAL" else ORANGE
    sz = 17 if yr == "TOTAL" else 14
    add_text(s, yr,  0.5, y, 2.0, 0.47, font_size=sz, bold=True, color=GOLD_LIGHT)
    add_text(s, rev, 2.6, y, 3.1, 0.47, font_size=sz, bold=True, color=col)
    y += 0.52

# Right — actual
add_rect(s, 6.15, 1.3, 4.15, 5.55, RGBColor(0x1E, 0x0A, 0x0A))
add_text(s, "WHAT WAS ACTUALLY VERIFIED", 6.3, 1.37, 3.85, 0.4,
         font_size=14, bold=True, color=GREEN_OK, align=PP_ALIGN.CENTER)
add_text(s, "Valcambi SA\n(KPMG Audited)\n5-Year Revenue:",
         6.3, 1.88, 3.85, 0.82, font_size=14, color=WHITE, bold=True)
add_text(s, "~₹3,000 Cr",
         6.3, 2.74, 3.85, 0.65, font_size=34, bold=True, color=GREEN_OK)
add_text(s, "vs ₹15.15 LAKH CRORE reported",
         6.3, 3.42, 3.85, 0.45, font_size=13.5, color=RED_ALERT, bold=True)
add_rect(s, 6.3, 3.95, 3.85, 0.04, GOLD)
add_text(s, "WHY THE GAP?", 6.3, 4.05, 3.85, 0.35, font_size=13, bold=True, color=GOLD)
add_text(s,
         "Valcambi refines gold — earns\na PROCESSING FEE only.\n\n"
         "REL booked the FULL MARKET\nVALUE of all gold processed\nas their own revenue.\n\n"
         "Like a drycleaner charging\n₹500 but reporting ₹10 lakh\nsuit value as 'sales'.",
         6.3, 4.43, 3.85, 2.3, font_size=12, color=WHITE)


# ══════════════════════════════════════════════════════════════════
# SLIDE 6 — AFFLUENCE SECURITIES
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE AFFLUENCE SECURITIES SCAM",
             "How company money funded the promoter's personal F&O bets")

add_rect(s, 0.35, 1.3, 12.6, 1.55, DARK2)
add_text(s, "THE SETUP", 0.55, 1.35, 3.0, 0.35, font_size=15, bold=True, color=GOLD)
add_text(s,
         "REL books showed ₹11,487 crore SALES + ₹11,488 crore PURCHASES with 'Affluence Shares & Stocks Pvt Ltd' (FY22-FY24).\n"
         "SEBI contacted Affluence. Their reply: 'We have NO client named Rajesh Exports. These transactions NEVER happened.'",
         0.55, 1.72, 12.1, 1.05, font_size=13.5, color=WHITE)

# Rajesh Mehta photo to make it personal/real
add_img_with_border(s, "rajesh_mehta_large.jpg", 0.35, 3.05, 2.7, 1.75,
                    border_color=RED_ALERT, label="RAJESH MEHTA — Promoter")

steps2 = [
    ("STEP 1", RED_ALERT,
     "REL funds moved to\nMehta's PERSONAL account\n₹339 crore+\nNo board approval"),
    ("STEP 2", ORANGE,
     "Mehta places personal\nDERIVATIVES TRADES (F&O)\nHigh-risk bets with\ncompany money"),
    ("STEP 3", GOLD,
     "Trade amounts booked\nBACK into REL books\nas fake Sales +\nPurchases via 'Affluence'"),
    ("STEP 4", GREEN_OK,
     "Result: Revenue inflated\nActual fund diversion\ncompletely hidden\nfrom all investors"),
]
x = 3.35
for title, col, desc in steps2:
    add_rect(s, x, 3.05, 2.3, 1.75, col)
    add_text(s, title, x+0.1, 3.1, 2.1, 0.4, font_size=16, bold=True,
             color=DARK_BG, align=PP_ALIGN.CENTER)
    add_rect(s, x, 3.5, 2.3, 1.3, DARK2)
    add_text(s, desc, x+0.12, 3.56, 2.06, 1.18, font_size=11.5, color=WHITE)
    x += 2.45

add_text(s, "💸  Shareholder wealth destroyed: ₹12,726 Crore  |  Stock: -80% in 3 years",
         0.35, 5.0, 12.6, 0.4, font_size=13.5, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

add_rect(s, 0.35, 5.55, 12.6, 1.7, RGBColor(0x1E, 0x0A, 0x0A))
add_rect(s, 0.35, 5.55, 0.07, 1.7, RED_ALERT)
add_text(s, "WHAT THIS MEANS FOR UAE GOLD INDUSTRY",
         0.57, 5.58, 7.0, 0.35, font_size=13, bold=True, color=RED_ALERT)
add_text(s,
         "Under CBUAE and FATF DNFBP guidelines: ANY fund transfer from a company to a director/promoter's personal account\n"
         "MUST have board approval AND be disclosed as a related-party transaction. Undisclosed fund flows = AML red flag = regulatory action.",
         0.57, 5.96, 12.1, 1.2, font_size=12, color=WHITE)


# ══════════════════════════════════════════════════════════════════
# SLIDE 7 — AFRICA MINES + ELEST
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE MISSING MINES & MYSTERY MILLIONS",
             "₹10,547 crore in 'assets' — zero documentation")

# Left
add_rect(s, 0.35, 1.3, 6.1, 5.5, DARK2)
add_text(s, "AFRICA GOLD MINES", 0.5, 1.35, 5.8, 0.42,
         font_size=17, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
africa_pts = [
    "FY23: Disclosed ₹1,035 crore investment in\n'gold mines in Africa' (no location given)",
    "FY25: Same 'investment' grew to ₹10,547 crore\n— 10× jump in just 2 years, no explanation",
    "SEBI asked for: Ownership docs, location,\nvaluation report — company provided NOTHING",
    "Company then said it 'cannot locate its\nearlier response' — own words",
    "SEBI conclusion: These assets may be\nCOMPLETELY FICTITIOUS — inflating asset base",
]
y = 1.88
for pt in africa_pts:
    add_rect(s, 0.45, y, 5.8, 0.78, RGBColor(0x1E, 0x0A, 0x0A))
    add_rect(s, 0.45, y, 0.07, 0.78, RED_ALERT)
    add_text(s, pt, 0.65, y + 0.1, 5.45, 0.6, font_size=12, color=WHITE)
    y += 0.9

# Right
add_rect(s, 6.85, 1.3, 6.1, 5.5, DARK2)
add_text(s, "ELEST EV COMPANY — SILENT FUND DRAIN", 7.0, 1.35, 5.8, 0.42,
         font_size=14, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
elest_pts = [
    "Elest = lithium-ion battery & EV company\nDirectly related to the Rajesh group",
    "₹565.88 crore transferred FROM REL → Elest\nacross FY21–FY26",
    "Only ₹350.03 crore returned\n→ NET OUTFLOW: ₹215.85 crore — gone",
    "NEVER disclosed as a related-party transaction\nto investors, board, or SEBI",
    "Jan 1, 2025: REL's stake in ACC Energy Storage\ndropped 100% → 51% on SAME DAY Elest got 49%\n₹147 crore flowed — partially reversed same day",
    "Company's own MD & CFO stated:\n'WE WERE UNAWARE of these transactions'",
]
y = 1.88
for pt in elest_pts:
    add_rect(s, 7.0, y, 5.8, 0.82, RGBColor(0x1A, 0x12, 0x04))
    add_rect(s, 7.0, y, 0.07, 0.82, ORANGE)
    add_text(s, pt, 7.2, y + 0.1, 5.45, 0.64, font_size=11.5, color=WHITE)
    y += 0.92


# ══════════════════════════════════════════════════════════════════
# SLIDE 8 — 10 RED FLAGS
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "10 RED FLAGS THAT WERE ALWAYS VISIBLE",
             "Any careful investor could have spotted these years before SEBI did")

flags = [
    ("1",  "99% REVENUE OVERSEAS",      "Nearly all from Swiss/Singapore subs — no Indian visibility"),
    ("2",  "RECEIVABLES PILING UP",      "Unpaid 2+ years — classic sign of fake/non-existent sales"),
    ("3",  "GGR NEVER AUDITED",          "₹15L crore revenue booked — ZERO independent audit"),
    ("4",  "AUDITORS BLOCKED ACCESS",    "No ERP, no journal dump, no subsidiary records given"),
    ("5",  "ONE ENTITY = 99% SALES",     "All revenue concentrated in promoter-controlled entities"),
    ("6",  "ASSETS 10× WITHOUT PROOF",  "Africa mines ₹1,035 Cr → ₹10,547 Cr — no documentation"),
    ("7",  "FUND FLOWS W/O APPROVAL",   "₹339+ Cr to personal account — no board/audit sanction"),
    ("8",  "STOCK FELL 80% IN 3 YRS",   "Market sensed trouble before retail investors"),
    ("9",  "MD/CFO UNAWARE OF DEALS",   "Management ignorant of own entity's large transactions"),
    ("10", "RPT NOT DISCLOSED",          "Elest transactions completely hidden — earnings management"),
]
x_positions = [0.35, 6.75]
y = 1.32
col_idx = 0
for num, title, desc in flags:
    x = x_positions[col_idx % 2]
    add_rect(s, x, y, 6.1, 0.6, DARK2)
    add_rect(s, x, y, 0.5, 0.6, RED_ALERT)
    add_text(s, num,   x,      y+0.12, 0.5,  0.38, font_size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, title, x+0.6,  y+0.05, 2.8,  0.26, font_size=11.5, bold=True, color=GOLD)
    add_text(s, desc,  x+0.6,  y+0.3,  5.35, 0.26, font_size=10.5, color=GRAY_LIGHT)
    col_idx += 1
    if col_idx % 2 == 0:
        y += 0.67


# ══════════════════════════════════════════════════════════════════
# SLIDE 9 — LIC: PUBLIC MONEY AT RISK
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "LIC: THE BIGGEST QUESTION MARK",
             "India's largest insurer held 10.79% — funded by your insurance premiums")

# LIC Logo — prominent
add_img_with_border(s, "lic_logo.png", 0.38, 1.38, 4.5, 2.1,
                    border_color=GOLD, label="LIC — Life Insurance Corporation of India")

add_rect(s, 0.38, 3.7, 4.5, 3.05, DARK2)
add_text(s, "LIC's EXPOSURE", 0.52, 3.75, 4.2, 0.38,
         font_size=16, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
add_text(s, "10.79% Stake", 0.52, 4.15, 4.2, 0.65,
         font_size=30, bold=True, color=RED_ALERT, align=PP_ALIGN.CENTER)
add_text(s, "At peak worth ₹2,000+ crore\nPost 80% fall → massive loss\nMoney = public premiums",
         0.52, 4.84, 4.2, 0.85, font_size=14, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)

# SEBI logo alongside
add_img_with_border(s, "sebi_logo.jpg", 0.38, 5.78, 4.5, 1.55,
                    border_color=GOLD, label="SEBI — Issued the Interim Order, June 3, 2026")

# Right — What due diligence should look like
add_rect(s, 5.25, 1.38, 7.7, 5.95, DARK2)
add_text(s, "WHAT PROPER INSTITUTIONAL DUE DILIGENCE MUST INCLUDE",
         5.4, 1.44, 7.4, 0.42, font_size=13.5, bold=True, color=GREEN_OK, align=PP_ALIGN.CENTER)
dd = [
    ("✅", "Verify revenue AT SUBSIDIARY LEVEL, not just consolidated numbers"),
    ("✅", "Demand independent audit of ALL material overseas entities (GGR was the key miss)"),
    ("✅", "Cross-check trade receivables aging — >90 days is a mandatory red flag"),
    ("✅", "Confirm 3rd-party transactions by contacting counterparties DIRECTLY"),
    ("✅", "Validate all disclosed assets with ownership docs and independent valuation"),
    ("✅", "Screen related-party disclosures against actual banking fund flows"),
    ("✅", "Scrutinize revenue concentration >50% in any single entity or region"),
    ("✅", "Monitor promoter's personal financial activity vs company account flows"),
    ("✅", "Request ERP/system access — refusal is itself a major red flag"),
]
y = 1.95
for icon, text in dd:
    add_text(s, f"{icon}  {text}", 5.4, y, 7.35, 0.44, font_size=11.5, color=WHITE)
    y += 0.52


# ══════════════════════════════════════════════════════════════════
# SLIDE 10 — UAE COMPLIANCE LESSONS
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "COMPLIANCE LESSONS FOR UAE GOLD INDUSTRY",
             "What this case means for gold traders, refiners & dealers in the UAE")

# Valcambi gold image as accent
add_img_with_border(s, "valcambi_img.jpg", 11.85, 1.28, 1.1, 1.1,
                    border_color=GOLD, label="Gold Refining")

lessons = [
    (GOLD,                         "REVENUE RECOGNITION",
     "Refiners must ONLY book processing/refining fees as revenue — NOT the full market value of client gold.\nUsing gross gold value as revenue = misrepresentation (Rajesh Exports' core fraud)."),
    (ORANGE,                       "SUBSIDIARY AUDIT TRAIL",
     "Every overseas entity in your group must be independently audited.\nConsolidated numbers without subsidiary-level verification = a hiding place for fraud."),
    (RED_ALERT,                    "RELATED PARTY TRANSPARENCY",
     "CBUAE, DMCC & DIFC require full related-party disclosure.\nAny fund flow to connected entities must be board-approved and disclosed — no exceptions."),
    (GREEN_OK,                     "TRADE RECEIVABLES MONITORING",
     "Outstanding receivables >90 days require compliance/board escalation.\nThis was the EXACT trigger that exposed the Rajesh Exports fraud."),
    (RGBColor(0x9B, 0x59, 0xB6),  "COUNTERPARTY VERIFICATION (AML)",
     "Always independently verify that your counterparty confirms the transaction.\nFake transactions like the Affluence deal would FAIL a basic FATF KYC/CDD check."),
    (RGBColor(0x1A, 0xBC, 0x9C),  "ASSET DOCUMENTATION",
     "Claims of gold inventory, mining assets or collateral MUST be supported by ownership docs,\nthird-party valuations, and independent confirmation — no assertion without evidence."),
]
y = 1.38
for i, (col, title, desc) in enumerate(lessons):
    row = i // 2
    cx = 0.35 if i % 2 == 0 else 6.82
    add_rect(s, cx, y + row * 1.9, 6.1, 1.78, DARK2)
    add_rect(s, cx, y + row * 1.9, 0.12, 1.78, col)
    add_text(s, title, cx+0.25, y+row*1.9+0.1, 5.7, 0.4,
             font_size=14, bold=True, color=col)
    add_text(s, desc, cx+0.25, y+row*1.9+0.52, 5.7, 1.15,
             font_size=11.5, color=WHITE)


# ══════════════════════════════════════════════════════════════════
# SLIDE 11 — NUMBERS AT A GLANCE
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE NUMBERS AT A GLANCE",
             "Everything you need to remember — in one slide")

numbers = [
    ("₹15.15\nLakh Crore", "Revenue allegedly\nmisrepresented FY21–25", RED_ALERT),
    ("99%",                "Of consolidated revenue\nthat could NOT be verified", ORANGE),
    ("₹12,726 Cr",         "Shareholder wealth\ndestroyed by the fraud", RED_ALERT),
    ("₹339 Cr+",           "Diverted to promoter's\npersonal derivatives bets", ORANGE),
    ("₹10,547 Cr",         "'Africa gold mines'\n— zero documentation", GOLD),
    ("₹11,487 Cr",         "Fake sales booked with\nAffluence (they denied all)", RED_ALERT),
    ("₹215 Cr",            "Net outflow to Elest EV\n(undisclosed related party)", ORANGE),
    ("10.79%",             "LIC's stake —\npublic money at risk", GOLD),
]
for i, (num, label, col) in enumerate(numbers):
    cx = 0.3 + (i % 4) * 3.22
    cy = 1.35 + (i // 4) * 2.2
    add_rect(s, cx, cy, 3.1, 2.0, DARK2)
    add_rect(s, cx, cy, 3.1, 0.07, col)
    add_text(s, num, cx+0.1, cy+0.15, 2.9, 0.9,
             font_size=22, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s, label, cx+0.1, cy+1.02, 2.9, 0.88,
             font_size=11.5, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
# SLIDE 12 — KEY TAKEAWAYS + CTA
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
gold_line(s, 0)
gold_line(s, 7.32)

add_text(s, "KEY TAKEAWAYS", 0.4, 0.1, 12.5, 0.6,
         font_size=30, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

# Brand logos row at top right
add_img(s, "sebi_logo.jpg",          9.9,  0.15, width=1.5)
add_img(s, "rajesh_exports_logo.png", 11.5, 0.15, width=1.5)

takeaways = [
    "Rajesh Exports = India's largest alleged revenue misrepresentation — ₹15.15 lakh crore over 5 years (bigger than Harshad Mehta)",
    "Fraud hidden through 4-layer offshore subsidiaries — middle entity GGR was NEVER independently audited",
    "Affluence Securities fake transactions: promoter moved company funds to personal account for derivatives trading",
    "Basic due diligence — checking receivable aging, verifying counterparties, demanding subsidiary audits — could have exposed this much earlier",
    "For UAE gold industry: gross gold value CANNOT be your revenue if you are a refiner — only the processing/refining fee counts",
    "LIC's 10.79% stake shows even large institutional investors can miss red flags — never rely on others' due diligence",
    "SEBI's interim order marks a new era: gold companies with opaque overseas structures will face heightened regulatory scrutiny globally",
]
y = 0.88
for ta in takeaways:
    add_rect(s, 0.4, y, 12.5, 0.56, DARK2)
    add_rect(s, 0.4, y, 0.09, 0.56, GOLD)
    add_text(s, ta, 0.62, y + 0.11, 12.1, 0.38, font_size=12.5, color=WHITE)
    y += 0.65

# CTA
add_rect(s, 0.4, 6.4, 12.5, 0.82, RGBColor(0x1A, 0x13, 0x00))
add_rect(s, 0.4, 6.4, 12.5, 0.06, GOLD)
add_text(s,
         "Follow VedasVision for weekly Compliance & Gold Industry insights  "
         "|  Share this with your team — knowledge protects your business",
         0.5, 6.5, 12.2, 0.62,
         font_size=14, bold=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)


# ── Save ──────────────────────────────────────────────────────────
output = "/home/user/vedasvision-whatsapp-bot/Rajesh_Exports_Scam_VedasVision_v2.pptx"
prs.save(output)
print(f"Saved: {output}")
print(f"Slides: {len(prs.slides)}")
