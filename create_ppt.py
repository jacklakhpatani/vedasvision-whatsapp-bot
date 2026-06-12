from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

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


def blank_slide(layout_idx=6):
    layout = prs.slide_layouts[layout_idx]
    return prs.slides.add_slide(layout)


def fill_bg(slide, color=DARK_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill_color, alpha=None):
    shape = slide.shapes.add_shape(
        1, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def add_text(slide, text, left, top, width, height,
             font_size=18, bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_bullet_box(slide, items, left, top, width, height,
                   font_size=15, title=None, title_color=GOLD,
                   bullet_color=WHITE, box_color=DARK2):
    add_rect(slide, left, top, width, height, box_color)
    y = top + 0.15
    if title:
        add_text(slide, title, left + 0.15, y, width - 0.3, 0.38,
                 font_size=font_size + 2, bold=True, color=title_color, align=PP_ALIGN.LEFT)
        y += 0.42
    for item in items:
        add_text(slide, f"  {item}", left + 0.1, y, width - 0.25, 0.35,
                 font_size=font_size, color=bullet_color)
        y += 0.37


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


# ══════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
add_rect(s, 0, 0, 13.33, 0.18, GOLD)
add_rect(s, 0, 7.32, 13.33, 0.18, GOLD)

# Big warning stripe
add_rect(s, 0, 1.8, 13.33, 4.2, RGBColor(0x11, 0x11, 0x22))

add_text(s, "🚨  INDIA'S BIGGEST MARKET SCAM", 0.4, 0.22, 12.5, 0.7,
         font_size=18, bold=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)

add_text(s, "RAJESH EXPORTS\nFRAUD EXPOSED", 0.3, 1.85, 12.7, 2.2,
         font_size=52, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

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

facts = [
    ("🏢  Founded", "1995  |  Bengaluru, Karnataka"),
    ("📈  Listed on", "BSE & NSE"),
    ("💰  Peak Market Cap", "~₹20,000 Crore"),
    ("🌍  Key Asset", "Valcambi SA, Switzerland (world's largest gold refinery)"),
    ("👤  Promoter", "Rajesh Mehta  —  Chairman & MD"),
    ("🏦  Key Investor", "LIC of India  —  10.79% stake (public money)"),
    ("📊  Reported Revenue FY25", "₹4.23 LAKH CRORE (consolidated)"),
    ("✅  Actual Verifiable Revenue", "~₹423 crore  —  0.1% of claimed figure"),
]

y = 1.45
for label, val in facts:
    add_rect(s, 0.4, y, 5.5, 0.42, DARK2)
    add_rect(s, 6.2, y, 6.7, 0.42, DARK2)
    add_text(s, label, 0.55, y + 0.06, 5.2, 0.32, font_size=14, bold=True, color=GOLD)
    add_text(s, val, 6.35, y + 0.06, 6.4, 0.32, font_size=14, color=WHITE)
    y += 0.52

add_text(s, "⚠️  Stock fell 80% over 3 years. Post SEBI order it hit lower circuit at ₹103.92",
         0.4, 6.85, 12.5, 0.4, font_size=13, color=ORANGE, align=PP_ALIGN.CENTER, bold=True)


# ══════════════════════════════════════════════════════════════════
# SLIDE 3 — HOW IT STARTED
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "HOW THE SCAM UNRAVELED", "One complaint → 2 years → ₹15.15 lakh crore fraud exposed")

# Timeline boxes
steps = [
    (GOLD,      "MARCH 2024",
     "A shareholder files a complaint with SEBI.\nReason: Company's trade receivables (money owed TO the company) were\npending for 2+ years — a major red flag in any business."),
    (ORANGE,    "OCT 2024",
     "SEBI launches formal investigation.\nForensic auditor BDO India is appointed to examine books.\nCompany is asked to submit all financial records, ERP data, journal dumps."),
    (RED_ALERT, "ONGOING",
     "Company refuses full cooperation:\n• Does not give ERP access\n• Statutory auditors don't submit working papers\n• Cites Swiss data protection laws to avoid sharing Valcambi records"),
    (GREEN_OK,  "JUNE 3, 2026",
     "SEBI issues landmark INTERIM ORDER:\n• Bars Rajesh Mehta from securities markets\n• Orders fresh forensic audit\n• Publishes 99% revenue misrepresentation findings\n• Estimates ₹12,726 crore shareholder wealth destruction"),
]

y = 1.35
for col, title, desc in steps:
    add_rect(s, 0.35, y, 12.6, 1.12, DARK2)
    add_rect(s, 0.35, y, 1.85, 1.12, col)
    add_text(s, title, 0.35, y + 0.3, 1.85, 0.52, font_size=14, bold=True,
             color=DARK_BG, align=PP_ALIGN.CENTER)
    add_text(s, desc, 2.4, y + 0.08, 10.3, 0.96, font_size=12.5, color=WHITE)
    y += 1.22


# ══════════════════════════════════════════════════════════════════
# SLIDE 4 — CORPORATE STRUCTURE (THE SHELL GAME)
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE SHELL COMPANY WEB", "How 4 layers of subsidiaries hid the fraud")

# Draw hierarchy
boxes = [
    (4.9,  1.35, 3.5, 0.7, GOLD,      DARK_BG, "REL — Rajesh Exports Limited", "LISTED IN INDIA  |  NSE / BSE"),
    (4.9,  2.5,  3.5, 0.7, ORANGE,    DARK_BG, "REL Singapore Pte Ltd", "100% Subsidiary  |  Singapore  |  NO Operations"),
    (3.2,  3.65, 3.5, 0.7, RED_ALERT, WHITE,   "GGR — Global Gold Refineries AG", "95% Held by REL Singapore  |  Switzerland  |  NO Operations ⚠️"),
    (6.65, 3.65, 3.5, 0.7, DARK2,     GOLD,    "BAB AL Rayan Jewellery LLC", "100% REL Singapore  |  CEASED Operations"),
    (4.9,  4.8,  3.5, 0.7, GREEN_OK,  DARK_BG, "Valcambi SA", "Wholly Owned by GGR  |  REAL Refinery  |  Switzerland"),
]

for lft, tp, w, h, bg, tc, title, sub in boxes:
    add_rect(s, lft, tp, w, h, bg)
    add_text(s, title, lft + 0.1, tp + 0.05, w - 0.2, 0.38, font_size=13, bold=True, color=RGBColor(*tc) if isinstance(tc, tuple) else tc)
    add_text(s, sub, lft + 0.1, tp + 0.37, w - 0.2, 0.28, font_size=10, color=GRAY_LIGHT)

# Connectors (simple lines as thin rects)
add_rect(s, 6.6, 2.05, 0.04, 0.47, GOLD)    # REL → Singapore
add_rect(s, 6.6, 3.22, 0.04, 0.45, GOLD)    # Singapore → GGR

# Key insight box
add_rect(s, 0.4, 5.7, 12.5, 1.5, RGBColor(0x1E, 0x0A, 0x0A))
add_rect(s, 0.4, 5.7, 0.06, 1.5, RED_ALERT)
add_text(s, "🔑  THE KEY FRAUD", 0.6, 5.75, 4.0, 0.38, font_size=15, bold=True, color=RED_ALERT)
add_text(s,
         "GGR (the middle holding company) was NEVER independently audited.\n"
         "REL booked ₹15 lakh crore revenue AT THE GGR LEVEL — but Valcambi (the actual working refinery) reported\n"
         "only ₹423–543 crore in the SAME years. The gap = the fraud.",
         0.6, 6.12, 12.1, 1.0, font_size=12.5, color=WHITE)


# ══════════════════════════════════════════════════════════════════
# SLIDE 5 — REVENUE FRAUD (CORE MECHANISM)
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE REVENUE ILLUSION", "How ₹15.15 Lakh Crore of 'Revenue' was manufactured")

# Left panel
add_rect(s, 0.35, 1.3, 6.0, 5.55, DARK2)
add_text(s, "WHAT THEY REPORTED", 0.5, 1.35, 5.7, 0.4,
         font_size=16, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

reported = [
    ("FY21", "₹2.02 Lakh Crore"),
    ("FY22", "₹3.31 Lakh Crore"),
    ("FY23", "₹3.28 Lakh Crore"),
    ("FY24", "₹2.38 Lakh Crore"),
    ("FY25", "₹4.23 Lakh Crore"),
    ("TOTAL", "₹15.22 Lakh Crore"),
]
y = 1.85
for yr, rev in reported:
    col = RED_ALERT if yr == "TOTAL" else ORANGE
    sz = 16 if yr == "TOTAL" else 14
    add_text(s, yr, 0.5, y, 2.0, 0.44, font_size=sz, bold=True, color=GOLD_LIGHT)
    add_text(s, rev, 2.6, y, 3.5, 0.44, font_size=sz, bold=True, color=col)
    y += 0.5

# Right panel
add_rect(s, 6.95, 1.3, 5.95, 5.55, RGBColor(0x1E, 0x0A, 0x0A))
add_text(s, "WHAT WAS ACTUALLY VERIFIED", 7.1, 1.35, 5.65, 0.4,
         font_size=15, bold=True, color=GREEN_OK, align=PP_ALIGN.CENTER)

add_text(s, "Valcambi SA (KPMG Audited)\nActual 5-Year Revenue:",
         7.1, 1.85, 5.5, 0.72, font_size=15, color=WHITE, bold=True)
add_text(s, "~₹3,000 Crore", 7.1, 2.62, 5.5, 0.65,
         font_size=32, bold=True, color=GREEN_OK, align=PP_ALIGN.LEFT)

add_text(s, "vs. ₹15.15 LAKH CRORE reported", 7.1, 3.3, 5.5, 0.42,
         font_size=14, color=RED_ALERT, bold=True)

add_rect(s, 7.1, 3.85, 5.65, 0.04, GOLD)

add_text(s, "WHY THE GAP?", 7.1, 4.0, 5.5, 0.35, font_size=13, bold=True, color=GOLD)
add_text(s,
         "Valcambi only refines gold — their revenue\n"
         "= their PROCESSING FEE only\n\n"
         "REL booked the FULL MARKET VALUE of\n"
         "all gold that passed through Valcambi\n"
         "as their own revenue — as if they OWNED\n"
         "the gold. They didn't.",
         7.1, 4.38, 5.5, 2.3, font_size=12.5, color=WHITE)


# ══════════════════════════════════════════════════════════════════
# SLIDE 6 — AFFLUENCE SECURITIES FRAUD
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE AFFLUENCE SECURITIES SCAM",
             "How company money funded the promoter's personal F&O bets")

add_rect(s, 0.35, 1.3, 12.6, 1.65, DARK2)
add_text(s, "THE SETUP", 0.55, 1.35, 3.0, 0.35, font_size=15, bold=True, color=GOLD)
add_text(s,
         "Rajesh Exports' books showed ₹11,487 crore of SALES and ₹11,488 crore of PURCHASES\n"
         "with a broking firm called 'Affluence Shares and Stocks Pvt Ltd' between FY22–FY24.\n"
         "When SEBI contacted Affluence — they said: 'We have NO client named Rajesh Exports.'",
         0.55, 1.72, 12.1, 1.18, font_size=13.5, color=WHITE)

steps2 = [
    ("STEP 1", RED_ALERT, "REL moves funds to Rajesh Mehta's\nPERSONAL account — ₹339 crore+\nwithout board approval"),
    ("STEP 2", ORANGE,    "Mehta uses personal funds to place\nhigh-risk DERIVATIVES TRADES\n(F&O — Futures & Options)"),
    ("STEP 3", GOLD,      "The derivative trade amounts are\nbooked BACK into REL's books\nas fake Sales + Purchases"),
    ("STEP 4", GREEN_OK,  "Result: Revenue looks MASSIVE\nActual loss + fund diversion\ncompletely hidden from investors"),
]
x = 0.35
for title, col, desc in steps2:
    add_rect(s, x, 3.15, 2.95, 2.5, col)
    add_text(s, title, x + 0.1, 3.2, 2.75, 0.42, font_size=17, bold=True,
             color=DARK_BG, align=PP_ALIGN.CENTER)
    add_rect(s, x, 3.62, 2.95, 2.03, DARK2)
    add_text(s, desc, x + 0.12, 3.68, 2.71, 1.9, font_size=12.5, color=WHITE)
    x += 3.15

add_text(s,
         "💸  Estimated shareholder wealth destroyed: ₹12,726 Crore  |  "
         "Stock lost 80% of value over 3 years",
         0.35, 5.85, 12.6, 0.4,
         font_size=13, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
# SLIDE 7 — AFRICA MINES + ELEST EV
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE MISSING MINES & MYSTERY MILLIONS",
             "₹10,547 crore in 'assets' that nobody can find")

# Left
add_rect(s, 0.35, 1.3, 6.1, 5.5, DARK2)
add_text(s, "🪨  AFRICA GOLD MINES", 0.5, 1.35, 5.8, 0.42,
         font_size=17, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

africa_pts = [
    "FY23: Company discloses ₹1,035 crore investment\nin 'gold mines in Africa'",
    "FY25: Same 'investment' mysteriously grows\nto ₹10,547 crore — 10× in 2 years",
    "SEBI asks for proof: ownership documents,\nlocation, valuation report — NOTHING provided",
    "Company later says it 'cannot locate'\nits own earlier response to the exchange",
    "SEBI conclusion: These assets may be\nCOMPLETELY FICTITIOUS",
]
y = 1.88
for pt in africa_pts:
    add_rect(s, 0.45, y, 5.8, 0.66, RGBColor(0x1E, 0x0A, 0x0A))
    add_rect(s, 0.45, y, 0.06, 0.66, RED_ALERT)
    add_text(s, pt, 0.65, y + 0.08, 5.45, 0.54, font_size=11.5, color=WHITE)
    y += 0.78

# Right
add_rect(s, 6.85, 1.3, 6.1, 5.5, DARK2)
add_text(s, "⚡  ELEST EV COMPANY — FUND DIVERSION", 7.0, 1.35, 5.8, 0.42,
         font_size=14, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

elest_pts = [
    "Elest = lithium battery & EV company\n(Related to the Rajesh group)",
    "₹565.88 crore transferred FROM Rajesh\nExports TO Elest (FY21–FY26)",
    "Only ₹350.03 crore returned back\n→ NET OUTFLOW: ₹215.85 crore",
    "NEVER disclosed as related-party\ntransaction to investors or SEBI",
    "Jan 1, 2025: REL's stake in ACC Energy\nStorage dropped from 100% → 51%\nSame day Elest acquired 48.95%\n₹147 crore flowed — partly reversed same day",
    "Company's own MD & CFO said they\nwere UNAWARE of these transactions",
]
y = 1.88
for pt in elest_pts:
    add_rect(s, 7.0, y, 5.8, 0.82, RGBColor(0x1A, 0x12, 0x04))
    add_rect(s, 7.0, y, 0.06, 0.82, ORANGE)
    add_text(s, pt, 7.2, y + 0.08, 5.45, 0.7, font_size=11, color=WHITE)
    y += 0.92


# ══════════════════════════════════════════════════════════════════
# SLIDE 8 — 10 RED FLAGS INVESTORS MISSED
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "10 RED FLAGS THAT WERE ALWAYS VISIBLE",
             "Every investor could have spotted these — before SEBI did")

flags = [
    ("1", "99% REVENUE FROM OVERSEAS",   "Nearly all revenue from Swiss/Singapore subs — no Indian visibility"),
    ("2", "RECEIVABLES PILING UP",        "Trade receivables unpaid for 2+ years — classic sign of fake sales"),
    ("3", "GGR NEVER AUDITED",            "The entity booking ₹15L crore revenue had ZERO independent audit"),
    ("4", "AUDITORS BLOCKED ACCESS",      "No ERP data, no journal dump, no subsidiary records — stonewalling"),
    ("5", "ONE CUSTOMER = 99% SALES",     "All revenue concentration in entities controlled by promoter group"),
    ("6", "ASSETS 10× WITHOUT REASON",   "Africa mines went from ₹1,035 Cr → ₹10,547 Cr in 2 yrs — no docs"),
    ("7", "FUND FLOWS WITHOUT APPROVAL", "₹339+ Cr to promoter personal account — no board / audit approval"),
    ("8", "STOCK FELL 80% IN 3 YEARS",   "Market sensed trouble — insiders knew before retail investors"),
    ("9", "MD/CFO UNAWARE OF OWN DEALS", "Management ignorant of own entity's transactions — governance failure"),
    ("10","RELATED PARTY NOT DISCLOSED", "Elest transactions hidden — classic earnings management technique"),
]

x_positions = [0.35, 6.75]
y = 1.32
col_idx = 0
for num, title, desc in flags:
    x = x_positions[col_idx % 2]
    add_rect(s, x, y, 6.1, 0.6, DARK2)
    add_rect(s, x, y, 0.5, 0.6, RED_ALERT)
    add_text(s, num, x, y + 0.12, 0.5, 0.38, font_size=14, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, title, x + 0.6, y + 0.05, 2.8, 0.25, font_size=11.5, bold=True, color=GOLD)
    add_text(s, desc, x + 0.6, y + 0.3, 5.3, 0.26, font_size=10.5, color=GRAY_LIGHT)
    col_idx += 1
    if col_idx % 2 == 0:
        y += 0.67


# ══════════════════════════════════════════════════════════════════
# SLIDE 9 — LIC: PUBLIC MONEY AT RISK
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "LIC: THE BIGGEST QUESTION MARK",
             "India's largest insurer held 10.79% — with YOUR premiums")

add_rect(s, 0.35, 1.35, 5.5, 5.4, DARK2)
add_text(s, "LIC's EXPOSURE", 0.5, 1.42, 5.2, 0.4,
         font_size=18, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
add_text(s, "10.79%\nStake in Rajesh Exports",
         0.5, 1.95, 5.2, 0.95,
         font_size=28, bold=True, color=RED_ALERT, align=PP_ALIGN.CENTER)

lic_pts = [
    "LIC invests public premium money —\nEVERY Indian's insurance savings",
    "At peak, LIC's stake was worth\n₹2,000+ crore",
    "Stock fell 80% → LIC's investment\ndeclined massively",
    "LIC performs 'due diligence' before\nevery large investment — it was missed",
    "SEBI order raises governance questions\nfor ALL institutional investors",
]
y = 2.98
for pt in lic_pts:
    add_rect(s, 0.45, y, 5.25, 0.66, RGBColor(0x1A, 0x08, 0x08))
    add_rect(s, 0.45, y, 0.06, 0.66, ORANGE)
    add_text(s, pt, 0.62, y + 0.08, 4.98, 0.52, font_size=11.5, color=WHITE)
    y += 0.76

# Right — what should due diligence look like
add_rect(s, 6.25, 1.35, 6.7, 5.4, DARK2)
add_text(s, "WHAT PROPER DUE DILIGENCE SHOULD INCLUDE", 6.4, 1.42, 6.4, 0.42,
         font_size=13, bold=True, color=GREEN_OK, align=PP_ALIGN.CENTER)

dd_items = [
    ("✅", "Verify revenue AT SUBSIDIARY LEVEL, not just consolidated"),
    ("✅", "Demand independent audit of all material overseas entities"),
    ("✅", "Cross-check trade receivables aging — >90 days is a red flag"),
    ("✅", "Confirm 3rd-party transactions with COUNTERPARTIES directly"),
    ("✅", "Validate all disclosed assets with supporting ownership docs"),
    ("✅", "Check related-party disclosures against actual fund flows"),
    ("✅", "Scrutinize if revenue concentration >50% in one entity/region"),
    ("✅", "Monitor promoter's personal financial activity vs company funds"),
]
y = 1.95
for icon, text in dd_items:
    add_text(s, f"{icon}  {text}", 6.35, y, 6.45, 0.44, font_size=11.5, color=WHITE)
    y += 0.52


# ══════════════════════════════════════════════════════════════════
# SLIDE 10 — COMPLIANCE LESSONS FOR UAE GOLD INDUSTRY
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "COMPLIANCE LESSONS FOR UAE GOLD INDUSTRY",
             "What this scam means for gold traders, refiners & dealers in the UAE")

lessons = [
    (GOLD,      "REVENUE RECOGNITION",
     "Refiners must ONLY book processing/refining fees as revenue — NOT the full market\nvalue of client gold. Using gross gold value as revenue = misrepresentation."),
    (ORANGE,    "SUBSIDIARY AUDIT TRAIL",
     "Every overseas entity in your group must be independently audited.\nConsolidated numbers without subsidiary-level verification = a hiding place for fraud."),
    (RED_ALERT, "RELATED PARTY TRANSPARENCY",
     "In UAE: CBUAE, DMCC & DIFC all require full related-party disclosure.\nAny fund flow to connected entities must be board-approved and disclosed."),
    (GREEN_OK,  "TRADE RECEIVABLES MONITORING",
     "Outstanding receivables >90 days require escalation to compliance/board.\nThis is the exact trigger that caught the Rajesh Exports fraud."),
    (RGBColor(0x9B, 0x59, 0xB6), "COUNTERPARTY VERIFICATION (AML/KYC)",
     "Always independently verify that your counterparty confirms the transaction.\nFake transactions like the Affluence deal would fail a basic FATF KYC check."),
    (RGBColor(0x1A, 0xBC, 0x9C), "ASSET DOCUMENTATION",
     "Claims of gold mining assets, inventory, or collateral MUST be supported\nby ownership docs, valuations, and third-party confirmation — no exceptions."),
]

y = 1.35
for i, (col, title, desc) in enumerate(lessons):
    row = i // 2
    col_x = 0.35 if i % 2 == 0 else 6.8
    add_rect(s, col_x, y + row * 1.85, 6.1, 1.72, DARK2)
    add_rect(s, col_x, y + row * 1.85, 0.12, 1.72, col)
    add_text(s, title, col_x + 0.25, y + row * 1.85 + 0.1, 5.7, 0.38,
             font_size=14, bold=True, color=col)
    add_text(s, desc, col_x + 0.25, y + row * 1.85 + 0.5, 5.7, 1.1,
             font_size=11.5, color=WHITE)


# ══════════════════════════════════════════════════════════════════
# SLIDE 11 — THE NUMBERS AT A GLANCE
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
slide_header(s, "THE NUMBERS AT A GLANCE", "Everything you need to remember — in one slide")

numbers = [
    ("₹15.15 Lakh Crore", "Revenue allegedly\nmisrepresented\n(FY21–FY25)", RED_ALERT),
    ("99%",               "Of consolidated\nrevenue that could\nnot be verified", ORANGE),
    ("₹12,726 Crore",     "Shareholder wealth\ndestroyed by the\nalleged fraud", RED_ALERT),
    ("₹339 Crore+",       "Diverted to promoter's\npersonal account for\nderivative trading", ORANGE),
    ("₹10,547 Crore",     "In 'Africa gold mines'\n— zero documentation\nprovided", GOLD),
    ("₹11,487 Crore",     "Fake sales booked\nwith Affluence Shares\n(they denied all)", RED_ALERT),
    ("₹215.85 Crore",     "Net outflow to\nElest EV (related\nparty, undisclosed)", ORANGE),
    ("10.79%",            "LIC's stake —\npublic money at risk\nin this company", GOLD),
]

x = 0.3
y = 1.35
for i, (num, label, col) in enumerate(numbers):
    row = i // 4
    cx = 0.3 + (i % 4) * 3.22
    cy = 1.35 + row * 2.2
    add_rect(s, cx, cy, 3.1, 2.0, DARK2)
    add_rect(s, cx, cy, 3.1, 0.06, col)
    add_text(s, num, cx + 0.1, cy + 0.15, 2.9, 0.75,
             font_size=20, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s, label, cx + 0.1, cy + 0.88, 2.9, 1.0,
             font_size=11.5, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
# SLIDE 12 — KEY TAKEAWAYS & CALL TO ACTION
# ══════════════════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s, DARK_BG)
gold_line(s, 0)
gold_line(s, 7.3)

add_text(s, "KEY TAKEAWAYS", 0.4, 0.1, 12.5, 0.6,
         font_size=30, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

takeaways = [
    "The Rajesh Exports case is India's largest alleged revenue misrepresentation — ₹15.15 lakh crore over 5 years",
    "The fraud was hidden through a 4-layer offshore subsidiary structure — with the key entity (GGR) never independently audited",
    "Fake transactions with Affluence Securities allowed the promoter to funnel company funds into personal derivative bets",
    "Basic due diligence — checking receivable aging, verifying counterparties, and demanding subsidiary audits — could have exposed this earlier",
    "For UAE gold industry: gross gold value CANNOT be booked as refiner revenue — this is a core compliance principle",
    "LIC's 10.79% stake shows even institutional investors can miss these red flags — compliance cannot rely on others to catch fraud",
    "SEBI's interim order marks a new era of scrutiny for gold companies with opaque overseas structures",
]

y = 0.82
for ta in takeaways:
    add_rect(s, 0.4, y, 12.5, 0.54, DARK2)
    add_rect(s, 0.4, y, 0.08, 0.54, GOLD)
    add_text(s, ta, 0.62, y + 0.1, 12.1, 0.38, font_size=12.5, color=WHITE)
    y += 0.63

add_rect(s, 0.4, 6.28, 12.5, 0.92, RGBColor(0x1A, 0x13, 0x00))
add_rect(s, 0.4, 6.28, 12.5, 0.06, GOLD)
add_text(s, "🔔  Follow VedasVision for weekly compliance & gold industry insights  |  "
            "Share this with your team — knowledge protects your business",
         0.5, 6.38, 12.2, 0.72,
         font_size=14, bold=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)


# ── Save ──────────────────────────────────────────────────────────
output_path = "/home/user/vedasvision-whatsapp-bot/Rajesh_Exports_Scam_VedasVision.pptx"
prs.save(output_path)
print(f"PPT saved: {output_path}")
print(f"Total slides: {len(prs.slides)}")
