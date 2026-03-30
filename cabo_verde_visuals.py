"""
Cabo Verde Policy Report – All Visuals
Course:  Entrepreneurial Ecosystems & Economic Development (USEMEEED)
Client:  Innovation for Policy Foundation (i4Policy)
Authors: Beike de Bok, Madelon Jansen, Koen Vonk
Data:    Africa Entrepreneurial Ecosystem Index (AEEI), Stam et al. (2025)
         World Bank Entrepreneurship Database (2025)

This script reproduces four figures used in the report and poster:
  Figure 1 – Radar chart: ecosystem profile, Cabo Verde vs structural peers
  Figure 2 – Bar chart: finance sub-indicators deep dive
  Figure 3 – Bar chart: market access sub-indicators deep dive
  Figure 4 – Scatter plots: ecosystem conditions vs entrepreneurial output

Requirements:
  pip install pandas numpy matplotlib scikit-learn openpyxl

Usage:
  Place this script in the same folder as the AEEI Excel file and run:
  python cabo_verde_visuals.py
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

# Set Cabo Verde culture score as reported in AEEI (Stam et al., 2025)
data.loc[data['country'] == 'Cabo Verde', 'culture'] = 0.21


# =============================================================================
# FIGURE 1 – RADAR CHART
# Entrepreneurial Ecosystem Comparison: Cabo Verde and Structural Peers
# Dimensions: 6 AEEI dimensions (culture excluded — missing for Seychelles)
# =============================================================================

dims6   = ['governance', 'support', 'finance',
           'infrastructure', 'market_access', 'human_capital']
labels6 = ['Governance', 'Support', 'Finance',
           'Infrastructure', 'Market\nAccess', 'Human\nCapital']

peers = ['Cabo Verde', 'Mauritius', 'Seychelles']
d_radar = data[data['country'].isin(peers)].set_index('country')

values = {
    'Cabo Verde': d_radar.loc['Cabo Verde', dims6].values.astype(float).tolist(),
    'Mauritius':  d_radar.loc['Mauritius',  dims6].values.astype(float).tolist(),
    'Seychelles': d_radar.loc['Seychelles', dims6].values.astype(float).tolist(),
}

colors     = {'Cabo Verde': '#C0392B', 'Mauritius': '#2471A3', 'Seychelles': '#1E8449'}
linewidths = {'Cabo Verde': 2.8,       'Mauritius': 1.8,       'Seychelles': 1.8}
alphas     = {'Cabo Verde': 0.12,      'Mauritius': 0.05,      'Seychelles': 0.05}
styles     = {'Cabo Verde': '-',       'Mauritius': '--',      'Seychelles': '-.'}

N      = len(labels6)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig = plt.figure(figsize=(10, 9))
fig.patch.set_facecolor('white')
ax = fig.add_subplot(111, polar=True)
ax.set_facecolor('#FAFAFA')

ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'],
                   fontsize=8, color='#999999', fontstyle='italic')
ax.yaxis.set_tick_params(pad=6)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels6, fontsize=12, color='#222222',
                   fontweight='bold', linespacing=1.4)
ax.grid(color='#DDDDDD', linewidth=0.5)
ax.spines['polar'].set_color('#CCCCCC')
ax.spines['polar'].set_linewidth(0.8)

for country, vals in values.items():
    plot_vals = vals + vals[:1]
    ax.plot(angles, plot_vals,
            linewidth=linewidths[country], color=colors[country],
            linestyle=styles[country], label=country, zorder=4)
    ax.fill(angles, plot_vals, alpha=alphas[country], color=colors[country])
    for angle, val in zip(angles[:-1], vals):
        ax.plot(angle, val, 'o', color=colors[country],
                markersize=6 if country == 'Cabo Verde' else 5, zorder=5)

fig.text(0.5, 0.97,
         'Entrepreneurial Ecosystem Comparison: Cabo Verde and Structural Peers',
         ha='center', va='top', fontsize=13, fontweight='bold',
         color='#111111', fontfamily='serif')
fig.text(0.5, 0.925,
         'AEEI dimensions (scores 0–1) | Source: Stam et al. (2025)',
         ha='center', va='top', fontsize=9.5, color='#666666', fontstyle='italic')
fig.text(0.5, 0.005,
         'Culture excluded: data unavailable for Seychelles.',
         ha='center', va='bottom', fontsize=8, color='#999999', fontstyle='italic')

ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.16),
          ncol=3, fontsize=11, frameon=True,
          framealpha=0.95, edgecolor='#CCCCCC', handlelength=2.5)

plt.tight_layout(rect=[0, 0.03, 1, 0.92])
plt.savefig('figure1_radar.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 1 saved: figure1_radar.png")


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
x     = np.arange(len(indicators_fin))
width = 0.26
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


# =============================================================================
# FIGURE 4 – ECOSYSTEM CONDITIONS VS ENTREPRENEURIAL OUTPUT
# Scatter plots: Finance, Human Capital, Infrastructure, Support
# vs New Business Density
# New business density: World Bank Entrepreneurship Database (2025)
# =============================================================================

# Data manually combined from AEEI + World Bank Table 2
outcomes = pd.DataFrame({
    'country':        ['Cabo Verde', 'Mauritius', 'South Africa', 'Tunisia', 'Morocco'],
    'iso':            ['CPV',        'MUS',        'ZAF',          'TUN',     'MAR'],
    'finance':        [0.210,        0.551,        0.929,          0.421,     0.403],
    'human_capital':  [0.568,        0.762,        0.616,          0.791,     0.803],
    'infrastructure': [0.601,        0.601,        0.777,          0.646,     0.684],
    'support':        [0.550,        0.870,        0.289,          0.312,     0.178],
    'density':        [21.76,        13.98,        11.46,          1.82,      2.66],
})

color_cv   = '#C0392B'
color_peer = '#1A5276'
dot_colors = [color_cv if c == 'Cabo Verde' else color_peer
              for c in outcomes['country']]
dot_sizes  = [180 if c == 'Cabo Verde' else 120 for c in outcomes['country']]

panels = [
    ('finance',        'Finance score',        'Finance'),
    ('human_capital',  'Human capital score',  'Human capital'),
    ('infrastructure', 'Infrastructure score', 'Infrastructure'),
    ('support',        'Support score',        'Support'),
]

fig, axes = plt.subplots(1, 4, figsize=(16, 5.5))
fig.patch.set_facecolor('white')

for ax, (col, xlabel, title) in zip(axes, panels):
    ax.set_facecolor('#FAFAFA')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(True, color='#E8E8E8', linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)

    for _, row in outcomes.iterrows():
        c = color_cv if row['country'] == 'Cabo Verde' else color_peer
        s = 180 if row['country'] == 'Cabo Verde' else 120
        ax.scatter(row[col], row['density'], color=c, s=s, zorder=4,
                   edgecolors='white', linewidths=0.8, alpha=0.92)
        offset_y = 0.6 if row['country'] == 'Cabo Verde' else 0.4
        ax.annotate(row['iso'], (row[col], row['density']),
                    xytext=(row[col] + 0.02, row['density'] + offset_y),
                    fontsize=9, color=c, fontweight='bold')

    ax.set_xlabel(xlabel, fontsize=10, color='#333333', labelpad=6)
    ax.set_ylabel('New business density\n(per 1,000 working-age people)'
                  if title == 'Finance' else '',
                  fontsize=9.5, color='#555555', labelpad=6)
    ax.set_title(title, fontsize=11, fontweight='bold', color='#222222', pad=8)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 26)
    ax.tick_params(colors='#666666', labelsize=9)

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color_cv,
           markersize=10, label='Cabo Verde'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color_peer,
           markersize=10, label='Benchmark countries'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=2,
           fontsize=10.5, frameon=True, framealpha=0.95,
           edgecolor='#DDDDDD', bbox_to_anchor=(0.5, -0.02))

fig.suptitle('Ecosystem Conditions and Entrepreneurial Output: Cabo Verde and Benchmarks',
             fontsize=13, fontweight='bold', color='#111111',
             fontfamily='serif', y=1.01)
fig.text(0.5, 0.97,
         'New business density vs. AEEI dimension scores | Source: Stam et al. (2025); World Bank (2025)',
         ha='center', fontsize=8.5, color='#888888', fontstyle='italic')

plt.tight_layout(rect=[0, 0.06, 1, 0.97])
plt.savefig('figure4_outcomes.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 4 saved: figure4_outcomes.png")

print("\nAll figures saved successfully.")
