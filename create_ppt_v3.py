"""
PPT v3 — 16 slides
All 12 original + 4 new:
  S2-b: ₹15L Crore Context chart
  S6-b: Paisa Kahan Gaya flowchart
  S9-a: Stock price crash chart
  S10-a: Scam comparison chart
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

BASE  = "/home/user/vedasvision-whatsapp-bot"
IMGS  = f"{BASE}/ppt_images"

GOLD       = RGBColor(0xD4,0xAF,0x37)
GOLD_LIGHT = RGBColor(0xF5,0xE6,0xA3)
DARK_BG    = RGBColor(0x0D,0x0D,0x1A)
DARK2      = RGBColor(0x1A,0x1A,0x2E)
RED_ALERT  = RGBColor(0xE0,0x3B,0x3B)
WHITE      = RGBColor(0xFF,0xFF,0xFF)
GRAY       = RGBColor(0xCC,0xCC,0xCC)
GREEN      = RGBColor(0x2E,0xCC,0x71)
ORANGE     = RGBColor(0xFF,0x8C,0x00)
PURPLE     = RGBColor(0x9B,0x59,0xB6)
TEAL       = RGBColor(0x1A,0xBC,0x9C)
BLUE       = RGBColor(0x34,0x98,0xDB)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

# ── helpers ──────────────────────────────────────────────────────
def blank():
    return prs.slides.add_slide(prs.slide_layouts[6])

def bg(slide, c=DARK_BG):
    f = slide.background.fill; f.solid(); f.fore_color.rgb = c

def rect(slide, l,t,w,h, c, line=None):
    sh = slide.shapes.add_shape(1,Inches(l),Inches(t),Inches(w),Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = c
    if line: sh.line.color.rgb = line; sh.line.width = Inches(0.015)
    else: sh.line.fill.background()
    return sh

def txt(slide, text, l,t,w,h, sz=16, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(Inches(l),Inches(t),Inches(w),Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    p  = tf.paragraphs[0]; p.alignment = align
    r  = p.add_run(); r.text = text
    r.font.size = Pt(sz); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    return tb

def img(slide, fname, l,t, width=None, height=None):
    path = os.path.join(IMGS, fname)
    if not os.path.exists(path): return
    try:
        if width and height:
            slide.shapes.add_picture(path,Inches(l),Inches(t),Inches(width),Inches(height))
        elif width:
            slide.shapes.add_picture(path,Inches(l),Inches(t),width=Inches(width))
        elif height:
            slide.shapes.add_picture(path,Inches(l),Inches(t),height=Inches(height))
    except Exception as e:
        print(f"  [img skip] {fname}: {e}")

def framed_img(slide, fname, l,t,w,h, border=GOLD, label=None):
    pad=0.06
    rect(slide, l-pad, t-pad, w+2*pad, h+2*pad+(0.28 if label else 0), border)
    rect(slide, l, t, w, h, DARK2)
    img(slide, fname, l, t, w, h)
    if label:
        txt(slide, label, l-pad, t+h+0.02, w+2*pad, 0.25,
            sz=9, color=GOLD_LIGHT, align=PP_ALIGN.CENTER, bold=True)

def gold_bar(slide, top):
    rect(slide, 0, top, 13.33, 0.04, GOLD)

def header(slide, title, subtitle=None, img_file=None, img_x=None):
    gold_bar(slide, 0)
    txt(slide, title, 0.4, 0.08, 11.5, 0.65, sz=29, bold=True, color=GOLD)
    if subtitle:
        txt(slide, subtitle, 0.4, 0.75, 11.5, 0.4, sz=15, color=GRAY, italic=True)
    if img_file and img_x:
        framed_img(slide, img_file, img_x, 0.08, 1.6, 1.0)
    gold_bar(slide, 1.2)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 1 — TITLE
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
rect(s,0,0,13.33,0.18,GOLD); rect(s,0,7.32,13.33,0.18,GOLD)
rect(s,0,1.8,13.33,4.2,RGBColor(0x11,0x11,0x22))
txt(s,"INDIA'S BIGGEST MARKET SCAM — EXPOSED",0.4,0.22,12.5,0.7,
    sz=17,bold=True,color=GOLD_LIGHT,align=PP_ALIGN.CENTER)
framed_img(s,"rajesh_exports_logo.png",0.5,1.95,2.5,1.5,label="RAJESH EXPORTS LTD")
txt(s,"FRAUD\nEXPOSED",3.3,1.9,6.5,2.1,sz=54,bold=True,color=GOLD,align=PP_ALIGN.CENTER)
framed_img(s,"valcambi_logo_rgba.png",10.3,1.95,2.5,1.5,label="VALCAMBI SA")
txt(s,"₹15.15 LAKH CRORE REVENUE SCAM",0.3,4.05,12.7,0.65,
    sz=26,bold=True,color=RED_ALERT,align=PP_ALIGN.CENTER)
txt(s,"How India's Top Gold Exporter Allegedly Fabricated 99% of Its Revenue",
    0.3,4.75,12.7,0.5,sz=17,color=GRAY,align=PP_ALIGN.CENTER,italic=True)
txt(s,"SEBI Interim Order  |  June 3, 2026  |  A VedasVision Compliance Insight",
    0.3,6.85,12.7,0.4,sz=13,color=GOLD_LIGHT,align=PP_ALIGN.CENTER)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 2 — WHO IS RAJESH EXPORTS?
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"WHO IS RAJESH EXPORTS?","The company that claimed to be India's largest gold exporter")
framed_img(s,"rajesh_mehta_large.jpg",0.4,1.35,3.2,2.0,label="RAJESH MEHTA — Chairman & MD")
framed_img(s,"rajesh_exports_logo.png",0.4,3.65,3.2,1.6,label="Rajesh Exports Limited")
facts=[
    ("🏢  Founded","1995  |  Bengaluru, Karnataka"),
    ("📈  Listed","BSE 531500 & NSE RAJESHEXPO"),
    ("🌍  Key Asset","Valcambi SA — World's largest gold refinery"),
    ("📊  Reported Rev FY25","₹4.23 LAKH CRORE (consolidated)"),
    ("✅  Actual Verified","~₹423 Cr — only 0.1% of claimed"),
    ("🏦  LIC Stake","10.79% — YOUR insurance premium"),
    ("📉  Stock fall","80%+ in 3 years"),
    ("⚡  Post-order","Lower circuit ₹78 on Jun 3, 2026"),
]
y=1.38
for lbl,val in facts:
    rect(s,3.9,y,4.8,0.44,DARK2); rect(s,8.85,y,4.1,0.44,DARK2)
    txt(s,lbl,4.05,y+0.07,4.5,0.32,sz=13,bold=True,color=GOLD)
    txt(s,val,9.0,y+0.07,3.8,0.32,sz=13,color=WHITE)
    y+=0.54
txt(s,"⚠️  Harshad Mehta = ₹4,000 Cr  |  Rajesh Exports = ₹15,15,000 Cr  → 3,787× BIGGER",
    0.4,6.88,12.5,0.38,sz=13,bold=True,color=ORANGE,align=PP_ALIGN.CENTER)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 3 (NEW) — ₹15 LAKH CRORE CONTEXT CHART
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"₹15 LAKH CRORE — WHAT DOES THIS NUMBER MEAN?",
       "Put the alleged fraud in perspective — it's bigger than India's entire defence + education + health budget combined")
img(s,"context_chart.png",0.35,1.3,12.6,5.8)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 4 — HOW IT STARTED
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"HOW THE SCAM UNRAVELED","One shareholder complaint → 2-year investigation → India's biggest alleged fraud",
       img_file="sebi_logo.jpg", img_x=11.3)
steps=[
    (GOLD,     "MARCH 2024","Shareholder complaint to SEBI: Trade receivables unpaid for 2+ years.\n(If sales are real — why is the payment not coming?)"),
    (ORANGE,   "OCT 2024",  "SEBI launches formal investigation. Forensic auditor BDO India appointed.\nCompany asked for ERP access, books, journal entries, subsidiary records."),
    (RED_ALERT,"ONGOING",   "Company refuses cooperation: No ERP access. Auditors don't get working papers.\nCites Swiss data protection laws to block Valcambi records."),
    (GREEN,    "JUN 3,2026","SEBI Interim Order: Rajesh Mehta BANNED from markets.\n99% revenue misrepresentation confirmed. ₹12,726 Cr shareholder wealth destroyed."),
]
y=1.35
for col,title,desc in steps:
    rect(s,0.35,y,12.6,1.2,DARK2); rect(s,0.35,y,2.0,1.2,col)
    txt(s,title,0.35,y+0.35,2.0,0.5,sz=13,bold=True,color=DARK_BG,align=PP_ALIGN.CENTER)
    txt(s,desc,2.55,y+0.12,10.2,0.96,sz=13,color=WHITE)
    y+=1.3


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 5 — CORPORATE STRUCTURE
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"THE SHELL COMPANY WEB","4 layers — the middle layer NEVER audited, yet booked ₹15 lakh crore")
boxes=[
    (4.9,1.35,3.5,0.72,GOLD,      DARK_BG,"REL — Rajesh Exports Limited",   "LISTED IN INDIA  |  NSE/BSE"),
    (4.9,2.52,3.5,0.72,ORANGE,    DARK_BG,"REL Singapore Pte Ltd",           "100% Subsidiary  |  NO Operations"),
    (2.8,3.7, 3.5,0.72,RED_ALERT, WHITE,  "GGR — Global Gold Refineries AG", "NEVER AUDITED  ⚠️  Fraud booked here"),
    (7.0,3.7, 3.5,0.72,DARK2,     GOLD,   "BAB AL Rayan Jewellery LLC",      "CEASED Operations"),
    (4.9,4.9, 3.5,0.72,GREEN,     DARK_BG,"Valcambi SA",                     "REAL Refinery — Balerna, Switzerland"),
]
for lft,tp,w,h,bg_c,tc,title,sub in boxes:
    rect(s,lft,tp,w,h,bg_c)
    tc_r=RGBColor(*tc) if isinstance(tc,tuple) else tc
    txt(s,title,lft+0.1,tp+0.06,w-0.2,0.38,sz=12,bold=True,color=tc_r)
    txt(s,sub,  lft+0.1,tp+0.42,w-0.2,0.26,sz=10,color=GRAY)
rect(s,6.63,2.06,0.04,0.47,GOLD); rect(s,6.63,3.24,0.04,0.46,GOLD)
img(s,"rajesh_exports_logo.png",0.38,1.42,width=1.5)
img(s,"valcambi_logo_rgba.png", 11.4,4.88,width=1.5)
rect(s,0.35,5.8,12.6,1.52,RGBColor(0x1E,0x0A,0x0A))
rect(s,0.35,5.8,0.07,1.52,RED_ALERT)
txt(s,"THE CORE FRAUD",0.57,5.85,3.5,0.35,sz=13,bold=True,color=RED_ALERT)
txt(s,"GGR — between REL Singapore and Valcambi — was NEVER independently audited. "
      "Yet REL booked ₹15 lakh crore revenue at this level.\n"
      "Valcambi (KPMG audited) reported ₹423 Cr. The gap between them = ₹15 lakh crore of alleged fake revenue.",
    0.57,6.22,12.1,1.0,sz=12,color=WHITE)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 6 — REVENUE ILLUSION
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"THE REVENUE ILLUSION","How ₹15.15 Lakh Crore was manufactured — the dry-cleaner trick")
framed_img(s,"valcambi_img.jpg",10.55,1.3,2.4,2.4,label="Valcambi Gold Bar")
rect(s,0.35,1.3,5.5,5.55,DARK2)
txt(s,"WHAT REL REPORTED",0.5,1.37,5.2,0.4,sz=15,bold=True,color=GOLD,align=PP_ALIGN.CENTER)
reported=[("FY21","₹2.02 Lakh Crore"),("FY22","₹3.31 Lakh Crore"),
          ("FY23","₹3.28 Lakh Crore"),("FY24","₹2.38 Lakh Crore"),
          ("FY25","₹4.23 Lakh Crore"),("TOTAL","₹15.22 Lakh Crore")]
y=1.87
for yr,rev in reported:
    col=RED_ALERT if yr=="TOTAL" else ORANGE
    sz=17 if yr=="TOTAL" else 14
    txt(s,yr, 0.5,y,2.0,0.47,sz=sz,bold=True,color=GOLD_LIGHT)
    txt(s,rev,2.6,y,3.1,0.47,sz=sz,bold=True,color=col)
    y+=0.52
rect(s,6.15,1.3,4.15,5.55,RGBColor(0x1E,0x0A,0x0A))
txt(s,"ACTUALLY VERIFIED",6.3,1.37,3.85,0.4,sz=14,bold=True,color=GREEN,align=PP_ALIGN.CENTER)
txt(s,"Valcambi SA (KPMG)\n5-Year Revenue:",6.3,1.87,3.85,0.75,sz=14,color=WHITE,bold=True)
txt(s,"~₹3,000 Cr",6.3,2.66,3.85,0.65,sz=32,bold=True,color=GREEN)
txt(s,"vs ₹15.15 LAKH CRORE reported",6.3,3.35,3.85,0.45,sz=13,color=RED_ALERT,bold=True)
rect(s,6.3,3.88,3.85,0.04,GOLD)
txt(s,"WHY THE GAP?",6.3,3.98,3.85,0.35,sz=13,bold=True,color=GOLD)
txt(s,"Valcambi refines gold → earns\na PROCESSING FEE only.\n\n"
      "REL booked the FULL MARKET\nVALUE of ALL gold processed\nas their 'revenue'.\n\n"
      "Like a drycleaner counting\n₹10 lakh suit value as sales\ninstead of ₹500 fee.",
    6.3,4.38,3.85,2.35,sz=11.5,color=WHITE)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 7 (NEW) — PAISA KAHAN GAYA — MONEY TRAIL FLOWCHART
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"PAISA KAHAN GAYA? — THE COMPLETE MONEY TRAIL",
       "Follow every rupee from company accounts to personal F&O bets")

# ── Node helper ──
def node(slide, l,t,w,h,bg_c,line_c,title,sub=None,sz=12):
    rect(slide,l,t,w,h,bg_c,line=line_c)
    txt(slide,title,l+0.1,t+0.08,w-0.2,0.38 if sub else h-0.16,
        sz=sz,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    if sub:
        txt(slide,sub,l+0.08,t+0.45,w-0.16,h-0.52,sz=10,color=GRAY,align=PP_ALIGN.CENTER)

def arrow(slide,x,y1,y2,c=GOLD):
    rect(slide,x-0.015,y1,0.03,y2-y1,c)
    # arrowhead
    slide.shapes.add_shape(5,Inches(x-0.1),Inches(y2-0.12),Inches(0.2),Inches(0.14)
        ).fill.solid(); slide.shapes[-1].fill.fore_color.rgb=c

def arrow_h(slide,x1,x2,y,c=GOLD):
    rect(slide,x1,y-0.015,x2-x1,0.03,c)

# Top: REL Company
node(s,5.0,1.3,3.3,0.78,DARK2,GOLD,"RAJESH EXPORTS LTD (REL)","Listed company | ₹15L Cr revenue claimed")
arrow(s,6.65,2.08,2.45)

# Middle: Two paths
node(s,1.5,2.45,3.3,0.78,RGBColor(0x1E,0x0A,0x0A),RED_ALERT,
     "RAJESH MEHTA\nPERSONAL ACCOUNT","₹339 Cr+ moved — NO board approval",sz=11)
node(s,8.5,2.45,3.3,0.78,RGBColor(0x1A,0x12,0x04),ORANGE,
     "GGR (Switzerland)","₹15L Cr fake revenue\nbooked here",sz=11)

# Connect REL to both with diagonal arrows
arrow_h(s,3.3,5.0,2.84)
arrow_h(s,8.3,8.5,2.84)

arrow(s,3.15,3.23,3.7)
arrow(s,10.15,3.23,3.7)

# Level 3
node(s,0.4,3.7,3.9,0.85,RGBColor(0x1E,0x0A,0x0A),RED_ALERT,
     "DERIVATIVES TRADING (F&O)","High-risk personal bets\nwith company money",sz=11)
node(s,5.0,3.7,3.3,0.85,RGBColor(0x0A,0x1A,0x0A),GREEN,
     "ELEST EV COMPANY","₹215 Cr net outflow\nundisclosed related party",sz=11)
node(s,8.5,3.7,3.9,0.85,RGBColor(0x1E,0x0A,0x0A),RED_ALERT,
     "AFFLUENCE SECURITIES","₹11,487 Cr fake sales+purchases\n'We have NO such client'",sz=11)

arrow(s,2.35,4.55,5.1)
arrow(s,6.65,4.55,5.1)
arrow(s,10.45,4.55,5.1)

# Level 4 — outcomes
node(s,0.4,5.1,3.9,0.82,DARK2,ORANGE,
     "PERSONAL LOSS","Booked back into\ncompany accounts",sz=11)
node(s,5.0,5.1,3.3,0.82,DARK2,ORANGE,
     "CAPITAL GONE","₹215 Cr never\nfully returned",sz=11)
node(s,8.5,5.1,3.9,0.82,DARK2,ORANGE,
     "FAKE REVENUE","Company looks\nbigger than reality",sz=11)

# Bottom summary
rect(s,0.35,6.1,12.6,1.1,RGBColor(0x1E,0x0A,0x0A))
rect(s,0.35,6.1,12.6,0.06,RED_ALERT)
txt(s,"NET RESULT: Investors lost ₹12,726 Cr of wealth | LIC lost thousands of crores | Stock crashed 85%",
    0.5,6.2,12.2,0.38,sz=13,bold=True,color=RED_ALERT,align=PP_ALIGN.CENTER)
txt(s,"All while company reported record revenues and management claimed everything was fine.",
    0.5,6.6,12.2,0.4,sz=12,color=WHITE,align=PP_ALIGN.CENTER)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 8 — AFFLUENCE SECURITIES
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"THE AFFLUENCE SECURITIES SCAM","How company money funded the promoter's personal F&O bets")
rect(s,0.35,1.3,12.6,1.55,DARK2)
txt(s,"THE SETUP",0.55,1.35,3.0,0.35,sz=14,bold=True,color=GOLD)
txt(s,"REL books: ₹11,487 Cr SALES + ₹11,488 Cr PURCHASES with 'Affluence Shares & Stocks Pvt Ltd' (FY22-FY24).\n"
      "SEBI contacted Affluence. Reply: 'We have NO client named Rajesh Exports. These transactions NEVER happened.'",
    0.55,1.7,12.1,1.05,sz=13,color=WHITE)
framed_img(s,"rajesh_mehta_large.jpg",0.35,3.02,2.75,1.75,border=RED_ALERT,label="RAJESH MEHTA")
steps2=[
    ("STEP 1",RED_ALERT, "REL funds to Mehta's\nPERSONAL account\n₹339 Cr+\nNo board approval"),
    ("STEP 2",ORANGE,    "Personal DERIVATIVES\nTRADES (F&O)\nHigh-risk bets\nwith company funds"),
    ("STEP 3",GOLD,      "Trade amounts booked\nas fake Sales +\nPurchases in REL\nvia 'Affluence'"),
    ("STEP 4",GREEN,     "Revenue inflated.\nFund diversion\nhidden from all\ninvestors/board."),
]
x=3.35
for title,col,desc in steps2:
    rect(s,x,3.02,2.3,1.75,col)
    txt(s,title,x+0.1,3.07,2.1,0.4,sz=15,bold=True,color=DARK_BG,align=PP_ALIGN.CENTER)
    rect(s,x,3.47,2.3,1.3,DARK2)
    txt(s,desc,x+0.12,3.53,2.06,1.18,sz=11,color=WHITE)
    x+=2.45
txt(s,"Shareholder wealth destroyed: ₹12,726 Crore  |  Stock: −80% in 3 years",
    0.35,5.0,12.6,0.4,sz=13,bold=True,color=ORANGE,align=PP_ALIGN.CENTER)
rect(s,0.35,5.52,12.6,1.75,RGBColor(0x1E,0x0A,0x0A))
rect(s,0.35,5.52,0.07,1.75,RED_ALERT)
txt(s,"UAE COMPLIANCE LINK",0.57,5.57,5.0,0.35,sz=13,bold=True,color=RED_ALERT)
txt(s,"CBUAE & FATF DNFBP: ANY fund transfer from company to director/promoter personal account MUST have "
      "board approval AND be disclosed as related-party transaction. "
      "Undisclosed fund flows = AML red flag = regulatory action (fines, licence suspension, criminal referral).",
    0.57,5.94,12.1,1.25,sz=12,color=WHITE)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 9 — AFRICA MINES + ELEST
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"THE MISSING MINES & MYSTERY MILLIONS","₹10,547 crore in 'assets' — zero documentation")
rect(s,0.35,1.3,6.1,5.5,DARK2)
txt(s,"AFRICA GOLD MINES",0.5,1.35,5.8,0.42,sz=16,bold=True,color=GOLD,align=PP_ALIGN.CENTER)
for y,pt in enumerate([
    "FY23: ₹1,035 Cr investment in 'gold mines in Africa'\n(no mine name, no location given)",
    "FY25: Same 'investment' became ₹10,547 Cr\n— 10× jump in 2 years, zero explanation",
    "SEBI demanded: Ownership docs, location,\nvaluation report — company provided NOTHING",
    "Company said it 'cannot locate its earlier\nresponse' — their own words to SEBI",
    "SEBI conclusion: These assets may be\nCOMPLETELY FICTITIOUS — fake asset inflation",
],start=0):
    yp=1.88+y*0.9
    rect(s,0.45,yp,5.8,0.78,RGBColor(0x1E,0x0A,0x0A))
    rect(s,0.45,yp,0.07,0.78,RED_ALERT)
    txt(s,pt,0.65,yp+0.1,5.45,0.6,sz=12,color=WHITE)
rect(s,6.85,1.3,6.1,5.5,DARK2)
txt(s,"ELEST EV COMPANY — SILENT DRAIN",7.0,1.35,5.8,0.42,sz=14,bold=True,color=ORANGE,align=PP_ALIGN.CENTER)
for y,pt in enumerate([
    "Elest = lithium-ion battery & EV startup\nDirectly related to the Rajesh group",
    "₹565.88 Cr transferred FROM REL → Elest\nover FY21–FY26",
    "Only ₹350.03 Cr returned\n→ NET OUTFLOW: ₹215.85 Cr — gone",
    "NEVER disclosed as related-party\ntransaction to investors or SEBI",
    "Jan 1, 2025: REL stake in ACC Energy Storage\n100% → 51%; Elest got 49% SAME DAY\n₹147 Cr flowed — partly reversed same day",
    "Company's own MD & CFO:\n'WE WERE UNAWARE of these transactions'",
],start=0):
    yp=1.88+y*0.82
    rect(s,7.0,yp,5.8,0.72,RGBColor(0x1A,0x12,0x04))
    rect(s,7.0,yp,0.07,0.72,ORANGE)
    txt(s,pt,7.2,yp+0.08,5.45,0.58,sz=11,color=WHITE)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 10 (NEW) — STOCK PRICE CRASH CHART
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"THE MARKET KNEW — STOCK FELL 85% IN 3 YEARS",
       "Investors who held Rajesh Exports since 2022 lost 85% of their money")
img(s,"stock_crash_chart.png",0.35,1.28,12.6,5.88)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 11 — 10 RED FLAGS
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"10 RED FLAGS THAT WERE ALWAYS VISIBLE","Any careful investor could have spotted these years before SEBI")
flags=[
    ("1", "99% REVENUE OVERSEAS",     "Nearly all from Swiss/Singapore subs — no Indian visibility"),
    ("2", "RECEIVABLES PILING UP",    "Unpaid 2+ years — classic sign of fake/non-existent sales"),
    ("3", "GGR NEVER AUDITED",        "₹15L Cr revenue booked — ZERO independent audit of that entity"),
    ("4", "AUDITORS BLOCKED ACCESS",  "No ERP, no journal dump, no subsidiary records provided"),
    ("5", "ONE ENTITY = 99% SALES",   "All revenue in promoter-controlled entities — circular"),
    ("6", "ASSETS 10× W/O PROOF",    "Africa mines ₹1,035 → ₹10,547 Cr — no ownership docs"),
    ("7", "FUNDS W/O BOARD APPROVAL", "₹339+ Cr to personal account — no sanction trail"),
    ("8", "STOCK FELL 85% IN 3 YRS", "Market sensed trouble long before retail investors"),
    ("9", "MD/CFO UNAWARE OF DEALS",  "Management ignorant of own entity's large transactions"),
    ("10","RPT NOT DISCLOSED",        "Elest transactions completely hidden — earnings management"),
]
y=1.32
for i,(num,title,desc) in enumerate(flags):
    x=0.35 if i%2==0 else 6.75
    rect(s,x,y,6.1,0.6,DARK2); rect(s,x,y,0.5,0.6,RED_ALERT)
    txt(s,num,x,y+0.12,0.5,0.38,sz=14,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    txt(s,title,x+0.6,y+0.05,2.8,0.26,sz=11,bold=True,color=GOLD)
    txt(s,desc, x+0.6,y+0.3, 5.35,0.26,sz=10,color=GRAY)
    if i%2==1: y+=0.67


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 12 (NEW) — SCAM COMPARISON
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"INDIA'S BIGGEST SCAMS — WHERE DOES RAJESH EXPORTS RANK?",
       "Scale comparison — alleged amount only, SEBI interim order not final conviction")
img(s,"scam_comparison_chart.png",0.35,1.28,12.6,4.7)
# Bottom context boxes
data=[
    (PURPLE,  "HARSHAD MEHTA\n1992","₹4,000 Cr\nBanking securities fraud"),
    (ORANGE,  "SATYAM\n2009",       "₹14,000 Cr\nAccounts manipulation"),
    (RED_ALERT,"NIRAV MODI\n2018",  "₹13,500 Cr\nPNB letters of credit"),
    (BLUE,    "YES BANK\n2020",     "₹73,500 Cr\nNPA masking fraud"),
    (GOLD,    "RAJESH EXPORTS\n2026","₹15.15 LAKH Cr\nRevenue misrepresentation *alleged"),
]
x=0.3
for col,name,detail in data:
    rect(s,x,6.1,2.56,1.22,DARK2,line=col)
    txt(s,name,  x+0.1,6.15,2.36,0.5,sz=11,bold=True,color=col,align=PP_ALIGN.CENTER)
    txt(s,detail,x+0.1,6.65,2.36,0.6,sz=10,color=GRAY,align=PP_ALIGN.CENTER)
    x+=2.66


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 13 — LIC: PUBLIC MONEY AT RISK
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"LIC: THE BIGGEST QUESTION MARK","India's largest insurer held 10.79% — funded by your insurance premiums")
framed_img(s,"lic_logo.png",0.38,1.38,4.5,2.1,label="LIC — Life Insurance Corporation of India")
rect(s,0.38,3.7,4.5,3.05,DARK2)
txt(s,"LIC's EXPOSURE",0.52,3.75,4.2,0.38,sz=16,bold=True,color=GOLD,align=PP_ALIGN.CENTER)
txt(s,"10.79%",0.52,4.15,4.2,0.62,sz=36,bold=True,color=RED_ALERT,align=PP_ALIGN.CENTER)
txt(s,"At peak: ₹2,000+ Cr\nPost-crash: massive loss\nAll = public premiums",0.52,4.82,4.2,0.78,sz=14,color=GRAY,align=PP_ALIGN.CENTER)
framed_img(s,"sebi_logo.jpg",0.38,5.78,4.5,1.55,label="SEBI — Issued Interim Order Jun 3, 2026")
rect(s,5.25,1.38,7.7,5.95,DARK2)
txt(s,"WHAT PROPER DUE DILIGENCE MUST INCLUDE",5.4,1.44,7.4,0.42,sz=13,bold=True,color=GREEN,align=PP_ALIGN.CENTER)
dd=[
    "✅  Verify revenue AT SUBSIDIARY LEVEL — not just consolidated numbers",
    "✅  Demand independent audit of ALL material overseas entities (GGR was the key miss)",
    "✅  Cross-check trade receivables aging — >90 days = mandatory red flag",
    "✅  Confirm 3rd-party transactions by contacting counterparties DIRECTLY",
    "✅  Validate all disclosed assets with ownership docs and independent valuation",
    "✅  Screen related-party disclosures against actual banking fund flows",
    "✅  Scrutinize revenue concentration >50% in any single entity or region",
    "✅  Monitor promoter personal financial activity vs company account flows",
    "✅  Request ERP/system access — refusal is itself a major red flag",
]
y=1.96
for d in dd:
    txt(s,d,5.4,y,7.35,0.44,sz=11.5,color=WHITE); y+=0.52


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 14 — UAE COMPLIANCE LESSONS
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"COMPLIANCE LESSONS FOR UAE GOLD INDUSTRY",
       "Direct application for gold traders, refiners & dealers in the UAE")
framed_img(s,"valcambi_img.jpg",11.85,1.28,1.1,1.1,label="Gold Refining")
lessons=[
    (GOLD,      "REVENUE RECOGNITION",
     "Refiners book PROCESSING FEE only — NOT full market value of client gold.\nRajesh Exports' core fraud was booking gross gold value as revenue."),
    (ORANGE,    "SUBSIDIARY AUDIT TRAIL",
     "Every overseas entity in your group must be independently audited.\nConsolidated numbers without subsidiary verification = fraud hiding place."),
    (RED_ALERT, "RELATED PARTY TRANSPARENCY",
     "CBUAE, DMCC & DIFC require full RPT disclosure.\nBoard-approved + disclosed = compliant. Hidden = regulatory action."),
    (GREEN,     "TRADE RECEIVABLES MONITORING",
     "Outstanding receivables >90 days = escalation to compliance/board.\nThis exact trigger exposed the Rajesh Exports fraud."),
    (PURPLE,    "COUNTERPARTY VERIFICATION (AML)",
     "Independently verify ALL counterparties confirm their transactions.\nFake Affluence entries would FAIL a basic FATF CDD check."),
    (TEAL,      "ASSET DOCUMENTATION",
     "Gold inventory, mining assets, collateral claims MUST have ownership docs,\nindependent valuations, third-party confirmation — no assertion without evidence."),
]
y=1.38
for i,(col,title,desc) in enumerate(lessons):
    row=i//2; cx=0.35 if i%2==0 else 6.82
    rect(s,cx,y+row*1.9,6.1,1.78,DARK2)
    rect(s,cx,y+row*1.9,0.12,1.78,col)
    txt(s,title,cx+0.25,y+row*1.9+0.1,5.7,0.4,sz=13,bold=True,color=col)
    txt(s,desc, cx+0.25,y+row*1.9+0.52,5.7,1.15,sz=11,color=WHITE)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 15 — NUMBERS AT A GLANCE
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
header(s,"THE NUMBERS AT A GLANCE","Everything you need to remember — in one slide")
numbers=[
    ("₹15.15\nLakh Crore","Revenue allegedly misrepresented\n(FY21–25)", RED_ALERT),
    ("99%",              "Of consolidated revenue\nthat could NOT be verified", ORANGE),
    ("₹12,726 Cr",       "Shareholder wealth\ndestroyed", RED_ALERT),
    ("₹339 Cr+",         "Diverted to promoter's\npersonal derivatives account", ORANGE),
    ("₹10,547 Cr",       "'Africa gold mines'\n— zero documentation", GOLD),
    ("₹11,487 Cr",       "Fake Affluence sales\n(they denied everything)", RED_ALERT),
    ("₹215 Cr",          "Net outflow to Elest EV\n(undisclosed related party)", ORANGE),
    ("10.79%",           "LIC's stake —\npublic money at risk", GOLD),
]
for i,(num,label,col) in enumerate(numbers):
    cx=0.3+(i%4)*3.22; cy=1.35+(i//4)*2.2
    rect(s,cx,cy,3.1,2.0,DARK2)
    rect(s,cx,cy,3.1,0.07,col)
    txt(s,num,  cx+0.1,cy+0.15,2.9,0.9,sz=22,bold=True,color=col,align=PP_ALIGN.CENTER)
    txt(s,label,cx+0.1,cy+1.02,2.9,0.88,sz=11,color=GRAY,align=PP_ALIGN.CENTER)


# ╔══════════════════════════════════════════════════════════════╗
# SLIDE 16 — KEY TAKEAWAYS + CTA
# ╚══════════════════════════════════════════════════════════════╝
s = blank(); bg(s)
gold_bar(s,0); gold_bar(s,7.32)
txt(s,"KEY TAKEAWAYS",0.4,0.1,12.5,0.6,sz=30,bold=True,color=GOLD,align=PP_ALIGN.CENTER)
img(s,"sebi_logo.jpg",9.9,0.15,width=1.5)
img(s,"rajesh_exports_logo.png",11.5,0.15,width=1.5)
takeaways=[
    "Rajesh Exports = India's largest alleged revenue fraud — ₹15.15 lakh crore over 5 years (bigger than Harshad Mehta by 3,787×)",
    "4-layer offshore structure: REL → REL Singapore → GGR → Valcambi. Middle entity GGR was NEVER independently audited",
    "Affluence Securities: promoter moved ₹339 Cr to personal account, bet on F&O, booked losses as company sales",
    "Africa mines: ₹1,035 Cr → ₹10,547 Cr in 2 years — ZERO ownership documentation, possibly completely fictitious",
    "Basic due diligence (receivable aging + counterparty verification + subsidiary audit) could have exposed this years earlier",
    "UAE gold industry: gross gold value ≠ refiner revenue — only the processing/refining fee is your income",
    "LIC's 10.79% loss shows no institution is immune — compliance cannot rely on someone else to catch fraud",
]
y=0.88
for ta in takeaways:
    rect(s,0.4,y,12.5,0.56,DARK2); rect(s,0.4,y,0.09,0.56,GOLD)
    txt(s,ta,0.62,y+0.11,12.1,0.38,sz=12,color=WHITE); y+=0.65
rect(s,0.4,6.4,12.5,0.82,RGBColor(0x1A,0x13,0x00))
rect(s,0.4,6.4,12.5,0.06,GOLD)
txt(s,"Follow VedasVision for weekly Compliance & Gold Industry insights  |  "
      "Share this with your team — knowledge protects your business",
    0.5,6.5,12.2,0.62,sz=14,bold=True,color=GOLD_LIGHT,align=PP_ALIGN.CENTER)


# ── Save ─────────────────────────────────────────────────────────
out = f"{BASE}/Rajesh_Exports_Scam_VedasVision_v3_FINAL.pptx"
prs.save(out)
print(f"\nSaved: {out}")
print(f"Total slides: {len(prs.slides)}")
