import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

IMGS = "/home/user/vedasvision-whatsapp-bot/ppt_images"

# ── 1. STOCK PRICE CRASH CHART ─────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0D0D1A')
ax.set_facecolor('#1A1A2E')

months = [
    'Jan\n2022','Apr\n2022','Jul\n2022','Oct\n2022',
    'Jan\n2023','Apr\n2023','Jul\n2023','Oct\n2023',
    'Jan\n2024','Apr\n2024','Jul\n2024','Oct\n2024',
    'Jan\n2025','Apr\n2025','Jul\n2025','Oct\n2025',
    'Jan\n2026','Mar\n2026','Jun 3\n2026'
]
prices = [
    510, 540, 495, 460,
    420, 385, 350, 310,
    280, 260, 230, 210,
    195, 175, 155, 130,
    118,  105, 78
]
x = np.arange(len(months))

# Gradient fill
ax.fill_between(x, prices, alpha=0.25, color='#E03B3B')
ax.plot(x, prices, color='#E03B3B', linewidth=2.5, zorder=3)

# Peak marker
ax.scatter([1], [540], color='#D4AF37', s=120, zorder=5)
ax.annotate('PEAK ₹540\n(Jan–Apr 2022)', xy=(1, 540), xytext=(3, 535),
            color='#D4AF37', fontsize=9, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#D4AF37', lw=1.5))

# SEBI ban marker
ax.scatter([18], [78], color='#FF4444', s=180, zorder=5, marker='v')
ax.annotate('SEBI ORDER\nJun 3, 2026\n₹78', xy=(18, 78), xytext=(15, 120),
            color='#FF4444', fontsize=9, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#FF4444', lw=1.5))

# Shareholder complaint marker
complaint_x = 2.5
ax.axvline(x=complaint_x, color='#FF8C00', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(complaint_x + 0.1, 420, 'Shareholder\nComplaint\nMar 2024', color='#FF8C00',
        fontsize=8, va='top')
# Approximate position for March 2024 complaint
ax.axvline(x=8.3, color='#FF8C00', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(8.4, 390, 'Shareholder\nComplaint\nMar 2024', color='#FF8C00',
        fontsize=8, va='top')

# SEBI investigation
ax.axvline(x=12.5, color='#9B59B6', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(12.6, 300, 'SEBI\nInvestigation\nOct 2024', color='#9B59B6',
        fontsize=8, va='top')

# -85% badge
ax.text(9, 85, '−85%', color='#E03B3B', fontsize=22, fontweight='bold',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1A1A2E', edgecolor='#E03B3B', linewidth=2))

ax.set_xticks(x)
ax.set_xticklabels(months, color='#CCCCCC', fontsize=8)
ax.set_yticks([100, 200, 300, 400, 500])
ax.set_yticklabels(['₹100', '₹200', '₹300', '₹400', '₹500'], color='#CCCCCC', fontsize=9)
ax.tick_params(colors='#CCCCCC')
for spine in ax.spines.values():
    spine.set_edgecolor('#2E2E4E')

ax.set_title('RAJESH EXPORTS STOCK PRICE — THE FALL FROM GRACE',
             color='#D4AF37', fontsize=13, fontweight='bold', pad=12)
ax.set_ylabel('Share Price (₹)', color='#CCCCCC', fontsize=10)
ax.yaxis.label.set_color('#CCCCCC')

# Legend
patch1 = mpatches.Patch(color='#D4AF37', label='Peak ₹540 (Early 2022)')
patch2 = mpatches.Patch(color='#E03B3B', label='Post SEBI Order ₹78 (Jun 2026)')
patch3 = mpatches.Patch(color='#FF8C00', label='Shareholder Complaint (Mar 2024)')
ax.legend(handles=[patch1, patch2, patch3],
          facecolor='#1A1A2E', edgecolor='#444', labelcolor='white', fontsize=8,
          loc='upper right')

ax.grid(axis='y', color='#2E2E4E', linewidth=0.5, linestyle='--')
plt.tight_layout()
fig.savefig(f'{IMGS}/stock_crash_chart.png', dpi=150, bbox_inches='tight',
            facecolor='#0D0D1A')
plt.close()
print("Stock chart saved")


# ── 2. SCAM COMPARISON CHART ──────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0D0D1A')
ax.set_facecolor('#1A1A2E')

scams = ['Harshad Mehta\n(1992)', 'Satyam\n(2009)', 'PNB-Nirav Modi\n(2018)', 'Yes Bank\n(2020)', 'Rajesh Exports\n(2026)']
amounts = [4000, 14000, 13500, 73500, 1515000]
colors  = ['#9B59B6', '#E67E22', '#E74C3C', '#3498DB', '#D4AF37']

bars = ax.barh(scams, amounts, color=colors, height=0.55, edgecolor='none')

for bar, amt in zip(bars, amounts):
    label = f'₹{amt:,} Cr' if amt < 100000 else f'₹{amt//100:,} Lakh Cr'
    ax.text(bar.get_width() + 8000, bar.get_y() + bar.get_height()/2,
            label, va='center', color='white', fontsize=9, fontweight='bold')

ax.set_title("INDIA'S BIGGEST SCAMS — SCALE COMPARISON",
             color='#D4AF37', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Amount in ₹ Crore (log scale)', color='#CCCCCC', fontsize=10)
ax.set_xscale('log')
ax.tick_params(colors='#CCCCCC')
ax.xaxis.label.set_color('#CCCCCC')
for spine in ax.spines.values():
    spine.set_edgecolor('#2E2E4E')
ax.set_yticklabels(scams, color='white', fontsize=10)
ax.grid(axis='x', color='#2E2E4E', linewidth=0.5, linestyle='--')

# Highlight Rajesh Exports bar
bars[-1].set_edgecolor('#D4AF37')
bars[-1].set_linewidth(2)

ax.text(0.98, 0.04, '* Rajesh Exports is ALLEGED — SEBI Interim Order, not final conviction',
        transform=ax.transAxes, color='#999999', fontsize=7.5,
        ha='right', va='bottom', style='italic')

plt.tight_layout()
fig.savefig(f'{IMGS}/scam_comparison_chart.png', dpi=150, bbox_inches='tight',
            facecolor='#0D0D1A')
plt.close()
print("Scam comparison chart saved")


# ── 3. ₹15 LAKH CRORE CONTEXT CHART ─────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0D0D1A')
ax.set_facecolor('#1A1A2E')

labels = [
    "India Defence\nBudget FY26",
    "India Education\nBudget FY26",
    "India Health\nBudget FY26",
    "Apple Inc.\nMarket Cap",
    "RAJESH EXPORTS\nAlleged Fake Rev",
]
values  = [621541, 128000, 98311, 3200000, 1515000]
clrs    = ['#3498DB', '#2ECC71', '#E74C3C', '#9B59B6', '#D4AF37']

bars = ax.barh(labels, values, color=clrs, height=0.55)
for bar, val in zip(bars, values):
    lbl = f'₹{val//100:,} Lakh Cr' if val >= 100000 else f'₹{val:,} Cr'
    ax.text(bar.get_width() + 20000, bar.get_y() + bar.get_height()/2,
            lbl, va='center', color='white', fontsize=9, fontweight='bold')

ax.set_title("₹15 LAKH CRORE — WHAT DOES IT ACTUALLY MEAN?",
             color='#D4AF37', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Amount in ₹ Crore', color='#CCCCCC', fontsize=10)
ax.tick_params(colors='#CCCCCC')
ax.xaxis.label.set_color('#CCCCCC')
for spine in ax.spines.values():
    spine.set_edgecolor('#2E2E4E')
ax.set_yticklabels(labels, color='white', fontsize=10)
ax.grid(axis='x', color='#2E2E4E', linewidth=0.5, linestyle='--')
bars[-1].set_edgecolor('#D4AF37')
bars[-1].set_linewidth(2)

plt.tight_layout()
fig.savefig(f'{IMGS}/context_chart.png', dpi=150, bbox_inches='tight',
            facecolor='#0D0D1A')
plt.close()
print("Context chart saved")

print("\nAll charts done:")
import os
for f in ['stock_crash_chart.png','scam_comparison_chart.png','context_chart.png']:
    p = f'{IMGS}/{f}'
    if os.path.exists(p):
        from PIL import Image
        img = Image.open(p)
        print(f"  {f}: {img.size}")
