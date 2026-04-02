re2 figure3 · PY
Copy

"""
Figure 2 – Finance Constraints in Small Island Economies: Cabo Verde in Perspective
Figure 3 – Market Access Constraints: Cabo Verde in Perspective
 
Course:  Entrepreneurial Ecosystems & Economic Development (USEMEEED)
Client:  Innovation for Policy Foundation (i4Policy)
Authors: Beike de Bok, Madelon Jansen, Koen Vonk
Data:    Africa Entrepreneurial Ecosystem Index (AEEI), Stam et al. (2025)
 
Requirements:
  pip install pandas numpy matplotlib openpyxl
 
Usage:
  Place this script in the same folder as the AEEI Excel file and run:
  python figure2_figure3.py
"""
 
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
 
# ── File path ─────────────────────────────────────────────────────────────────
AEEI_FILE = "Mendeley_data_AEEI_WD__1_.xlsx"
# ─────────────────────────────────────────────────────────────────────────────
 
 
# =============================================================================
# 0. LOAD AND PREPARE AEEI DATA
# =============================================================================
 
df = pd.read_excel(AEEI_FILE, sheet_name="Index Calculations")
data = df.iloc[1:].copy()
data.columns = [
    'country', 'iso', 'governance', 'rullaw', 'corrupt', 'busreg',
    'culture', 'trust', 'entpers', 'support', 'profnet', 'hubs',
    'finance', 'credpris', 'vc', 'smarcap',
    'infrastructure', 'elec', 'road', 'inte',
    'market_access', 'hhincap', 'gdp', 'pop', 'impexp',
    'human_capital', 'lifeexp', 'literat', 'tert', 'rd'
]
 
numeric_cols = [
    'governance', 'culture', 'support', 'finance', 'infrastructure',
    'market_access', 'human_capital', 'credpris', 'vc', 'smarcap',
    'hhincap', 'gdp', 'pop', 'impexp'
]
for c in numeric_cols:
    data[c] = pd.to_numeric(data[c], errors='coerce')
 
data = data[data['country'].notna() & (data['country'].str.strip() != '')]
 
 
# =============================================================================
# FIGURE 2 – FINANCE DEEP DIVE BAR CHART
# Finance Constraints in Small Island Economies: Cabo Verde in Perspective
# Sub-indicators: domestic credit, venture capital, stock market capitalisation
# =============================================================================
 
fin_countries = ['Cabo Verde', 'Seychelles', 'Mauritius']
d_fin = data[data['country'].isin(fin_countries)].set_index('country')
 
indicators_fin = ['Domestic credit\nto private sector',
                  'Venture\ncapital',
                  'Stock market\ncapitalisation']
fin_data = {
    'Cabo Verde': d_fin.loc['Cabo Verde', ['credpris', 'vc', 'smarcap']].values.astype(float).tolist(),
    'Seychelles': d_fin.loc['Seychelles', ['credpris', 'vc', 'smarcap']].values.astype(float).tolist(),
    'Mauritius':  d_fin.loc['Mauritius',  ['credpris', 'vc', 'smarcap']].values.astype(float).tolist(),
}
 
colors_bar = {'Cabo Verde': '#C0392B', 'Seychelles': '#7F8C8D', 'Mauritius': '#1A5276'}
x      = np.arange(len(indicators_fin))
width  = 0.26
offsets = [-width, 0, width]
 
fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')
for spine in ax.spines.values():
    spine.set_visible(False)
ax.yaxis.grid(True, color='#E5E5E5', linewidth=0.7, zorder=0)
ax.set_axisbelow(True)
 
for i, country in enumerate(fin_countries):
    vals = fin_data[country]
    bars = ax.bar(x + offsets[i], vals, width,
                  label=country, color=colors_bar[country],
                  alpha=0.88 if country == 'Cabo Verde' else 0.72,
                  edgecolor='white', linewidth=0.8, zorder=3)
    for bar, val in zip(bars, vals):
        label = f'{val:.2f}' if val >= 0.01 else '0.00'
        ypos  = val + 0.02 if val >= 0.01 else 0.03
        ax.text(bar.get_x() + bar.get_width() / 2, ypos, label,
                ha='center', va='bottom', fontsize=9.5,
                fontweight='bold', color=colors_bar[country])
 
ax.annotate('Seychelles: unusually\nhigh VC score*',
            xy=(x[1] + offsets[1], 1.0), xytext=(x[1] + 0.55, 0.82),
            fontsize=8.5, color='#7F8C8D', fontstyle='italic',
            arrowprops=dict(arrowstyle='->', color='#AAAAAA', lw=1.2))
 
ax.set_xticks(x)
ax.set_xticklabels(indicators_fin, fontsize=12, color='#222222', fontweight='bold')
ax.set_ylabel('Normalised score (0–1)', fontsize=11, color='#444444', labelpad=10)
ax.set_ylim(0, 1.15)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'],
                   fontsize=9, color='#888888')
ax.tick_params(colors='#444444', length=0)
 
fig.text(0.5, 0.97,
         'Finance Constraints in Small Island Economies: Cabo Verde in Perspective',
         ha='center', va='top', fontsize=13, fontweight='bold',
         color='#111111', fontfamily='serif')
fig.text(0.5, 0.925,
         'AEEI finance sub-indicators (normalised 0–1) | Source: Stam et al. (2025)',
         ha='center', va='top', fontsize=9.5, color='#666666', fontstyle='italic')
fig.text(0.5, 0.01,
         '* Seychelles\' VC score = 1.00 reflects limited data availability for very small economies; interpret with caution.',
         ha='center', va='bottom', fontsize=8, color='#999999', fontstyle='italic')
 
ax.legend(fontsize=11, frameon=True, framealpha=0.95,
          edgecolor='#CCCCCC', loc='upper right')
 
plt.tight_layout(rect=[0, 0.04, 1, 0.91])
plt.savefig('figure2_finance.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 2 saved: figure2_finance.png")
 
 
# =============================================================================
# FIGURE 3 – MARKET ACCESS DEEP DIVE BAR CHART
# Market Access Constraints: Cabo Verde in Perspective
# Sub-indicators: trade openness, household income per capita
# =============================================================================
 
mkt_countries = ['Cabo Verde', 'Seychelles', 'Mauritius']
d_mkt = data[data['country'].isin(mkt_countries)].set_index('country')
 
indicators_mkt = ['Trade openness', 'Household income\nper capita']
mkt_data = {
    'Cabo Verde': d_mkt.loc['Cabo Verde', ['impexp', 'hhincap']].values.astype(float).tolist(),
    'Seychelles': d_mkt.loc['Seychelles', ['impexp', 'hhincap']].values.astype(float).tolist(),
    'Mauritius':  d_mkt.loc['Mauritius',  ['impexp', 'hhincap']].values.astype(float).tolist(),
}
 
x = np.arange(len(indicators_mkt))
 
fig, ax = plt.subplots(figsize=(9, 6.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')
for spine in ax.spines.values():
    spine.set_visible(False)
ax.yaxis.grid(True, color='#E8E8E8', linewidth=0.7, zorder=0)
ax.set_axisbelow(True)
 
for i, country in enumerate(mkt_countries):
    vals = mkt_data[country]
    bars = ax.bar(x + offsets[i], vals, width,
                  label=country, color=colors_bar[country],
                  alpha=0.88 if country == 'Cabo Verde' else 0.68,
                  edgecolor='white', linewidth=1.0, zorder=3)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.016,
                f'{val:.2f}', ha='center', va='bottom',
                fontsize=10.5, fontweight='bold', color=colors_bar[country])
 
ax.set_xticks(x)
ax.set_xticklabels(indicators_mkt, fontsize=13, color='#222222', fontweight='bold')
ax.set_ylabel('Normalised score (0–1)', fontsize=11, color='#555555', labelpad=10)
ax.set_ylim(0, 1.18)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'],
                   fontsize=9.5, color='#888888')
ax.tick_params(colors='#444444', length=0)
 
fig.text(0.5, 0.97,
         'Market Access Constraints: Cabo Verde in Perspective',
         ha='center', va='top', fontsize=13, fontweight='bold',
         color='#111111', fontfamily='serif')
fig.text(0.5, 0.925,
         'AEEI market access sub-indicators (0–1) | Source: Stam et al. (2025)',
         ha='center', va='top', fontsize=9, color='#888888', fontstyle='italic')
 
ax.legend(fontsize=11, frameon=True, framealpha=0.95,
          edgecolor='#DDDDDD', loc='upper left',
          handlelength=2, handleheight=1.2)
 
plt.tight_layout(rect=[0, 0, 1, 0.91])
plt.savefig('figure3_market_access.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 3 saved: figure3_market_access.png")
