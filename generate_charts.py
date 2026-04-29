"""
Final polish pass for Project 2 visualizations.
Applies SWD style from analytics_chart_style.mplstyle, uses chart_helpers
(swd_style, action_title, check_label_collisions, add_trendline). NO JITTER:
all scatter points sit at their literal data values. Labels are placed
algorithmically and the collision-detector auto-fixes any overlaps.
"""
import sys, os
sys.path.insert(0, "/sessions/practical-great-brahmagupta/mnt/DSC106 Lab Opus 4.7/projects/project2")
from helpers.chart_helpers import (
    swd_style, action_title, check_label_collisions, COLORS, save_chart,
)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

OUT = "/sessions/practical-great-brahmagupta/mnt/DSC106 Lab Opus 4.7/projects/project2/images"

# Load
GDP_COL = "average_value_GDP per capita (constant 2010 US$)"
econ = pd.read_csv("/tmp/econ.csv")
social = pd.read_csv("/tmp/social.csv")
e = econ[["Country Name", "Year", GDP_COL]].rename(columns={GDP_COL: "GDP"})
social["LifeExp"] = (social["average_value_Life expectancy at birth, male (years)"]
                     + social["average_value_Life expectancy at birth, female (years)"]) / 2
h = social[["Country Name", "Year", "LifeExp"]]
df = pd.merge(e, h, on=["Country Name", "Year"]).dropna()
agg = ["World","income","OECD","Asia","Europe","Africa","America","Union","Heavily","Fragile",
       "demographic","members","Sub-Saharan","developing","developed","small states","IDA","IBRD",
       "Euro area","Arab World","Caribbean","Pacific","North America","Latin America",
       "Middle East","European"]
df = df[~df["Country Name"].apply(lambda c: any(k.lower() in str(c).lower() for k in agg))].copy()

y2019 = df[df["Year"] == 2019].copy()
log_gdp = np.log10(y2019["GDP"])
slope, intercept = np.polyfit(log_gdp, y2019["LifeExp"], 1)
y2019["pred"] = slope * log_gdp + intercept
y2019["resid"] = y2019["LifeExp"] - y2019["pred"]
r2 = np.corrcoef(log_gdp, y2019["LifeExp"])[0, 1]**2

# Apply analytics SWD style
colors = swd_style()
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"

# ============================================================================
# PRO 1 — linear scatter, outliers highlighted, no fit line
# ============================================================================
under = y2019.nsmallest(4, "resid")
over = y2019.nlargest(4, "resid")

fig, ax = plt.subplots(figsize=(11, 6.8))
# Background scatter
ax.scatter(y2019["GDP"]/1000, y2019["LifeExp"],
           s=40, alpha=0.42, color=colors["gray400"], edgecolor="none", zorder=2)

# Highlights — staggered label placement to prevent collisions
under_offsets = {"Equatorial Guinea": (10, -8), "Nigeria": (10, -8),
                 "Lesotho": (-10, -10), "Eswatini": (12, 8)}
over_offsets = {"Vietnam": (10, -8), "Nicaragua": (10, -10),
                "Honduras": (-10, 10), "Bangladesh": (-10, -12)}

for _, row in under.iterrows():
    ax.scatter(row["GDP"]/1000, row["LifeExp"], s=110, color=colors["negative"],
               edgecolor="white", linewidth=1.4, zorder=3)
    dx, dy = under_offsets.get(row["Country Name"], (10, 8))
    ax.annotate(row["Country Name"], (row["GDP"]/1000, row["LifeExp"]),
                xytext=(dx, dy), textcoords="offset points",
                fontsize=9, color="#7a1414", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=colors["negative"], lw=0.7, alpha=0.6))

for _, row in over.iterrows():
    ax.scatter(row["GDP"]/1000, row["LifeExp"], s=110, color=colors["success"],
               edgecolor="white", linewidth=1.4, zorder=3)
    dx, dy = over_offsets.get(row["Country Name"], (10, 8))
    ax.annotate(row["Country Name"], (row["GDP"]/1000, row["LifeExp"]),
                xytext=(dx, dy), textcoords="offset points",
                fontsize=9, color="#1f6f1f", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=colors["success"], lw=0.7, alpha=0.6))

ax.set_xlim(-3, y2019["GDP"].max()/1000 + 5)
ax.set_ylim(50, 88)
ax.set_xlabel("GDP per capita (thousand 2010 US$)", fontsize=11, color=colors["gray600"])
ax.set_ylabel("Life expectancy at birth (years)", fontsize=11, color=colors["gray600"])
action_title(ax, "Wealth Is No Cure",
             "At every income level, health outcomes are all over the map. n = 179, year = 2019.")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(True, alpha=0.18, linestyle="--")
ax.set_axisbelow(True)

# Caption box, anchored top-right with safe padding
ax.text(0.99, 0.04,
        "Each dot = one country, plotted at its true 2019 GDP per capita and life expectancy.\n"
        "No jittering. Source: World Bank.",
        transform=ax.transAxes, fontsize=8.5, color=colors["gray600"],
        style="italic", ha="right", va="bottom")

# Run collision detector + auto-fix
collisions = check_label_collisions(fig, ax, fix=True, pad_px=4)
print(f"PRO 1 collisions detected/fixed: {len(collisions)}")

plt.tight_layout()
plt.savefig(f"{OUT}/pro_viz.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# PRO 2 — residuals lollipop chart
# ============================================================================
top_neg = y2019.nsmallest(12, "resid").sort_values("resid", ascending=True)
top_pos = y2019.nlargest(12, "resid").sort_values("resid", ascending=False)
middle_count = len(y2019) - len(top_neg) - len(top_pos)

fig, ax = plt.subplots(figsize=(10, 11))

n_neg = len(top_neg); n_pos = len(top_pos); gap = 1.5
neg_ys = np.arange(n_pos + gap, n_pos + gap + n_neg)
pos_ys = np.arange(0, n_pos)

for y, (_, row) in zip(neg_ys, top_neg.iterrows()):
    ax.hlines(y=y, xmin=0, xmax=row["resid"], color=colors["negative"], linewidth=2.2, alpha=0.85)
    ax.scatter(row["resid"], y, s=85, color=colors["negative"], edgecolor="white",
               linewidth=1.2, zorder=3)
    ax.text(row["resid"] - 0.3, y, f"{row['Country Name']}  ({row['resid']:.1f})",
            fontsize=9.5, color="#7a1414", va="center", ha="right", fontweight="bold")

for y, (_, row) in zip(pos_ys, top_pos.iterrows()):
    ax.hlines(y=y, xmin=0, xmax=row["resid"], color=colors["success"], linewidth=2.2, alpha=0.85)
    ax.scatter(row["resid"], y, s=85, color=colors["success"], edgecolor="white",
               linewidth=1.2, zorder=3)
    ax.text(row["resid"] + 0.3, y, f"{row['Country Name']}  (+{row['resid']:.1f})",
            fontsize=9.5, color="#1f6f1f", va="center", ha="left", fontweight="bold")

ax.axvline(0, color=colors["gray900"], linewidth=1.0, zorder=2)

# Gap band
gap_y = n_pos + gap/2
ax.axhspan(n_pos - 0.4, n_pos + gap, color=colors["gray100"], alpha=0.7, zorder=1)
ax.text(0, gap_y, f"…and {middle_count} other countries within ±5 years of the fit line",
        fontsize=10, color=colors["gray600"], style="italic", va="center", ha="center")

ax.set_yticks([])
ax.set_xlabel("Life expectancy minus what GDP predicts (years)", fontsize=11, color=colors["gray600"])
ax.set_xlim(-18, 11)
ax.set_ylim(-0.7, n_pos + gap + n_neg - 0.3)

action_title(ax, "Money Explains 70% of Life Expectancy",
             f"The other 30% is a 20-year gap.   Residuals from log-GDP regression on all 179 countries, 2019 (R² = {r2:.2f}).")

# Single caption, top-right
ax.text(0.99, 0.99,
        "Same 179 countries and same regression line as Visualization 2 (con side).\n"
        "Red = wealth predicts a longer life than the country actually has.\n"
        "Green = wealth predicts a shorter life than the country actually has.\n"
        "If wealth alone bought health, every lollipop would be near zero.",
        transform=ax.transAxes, fontsize=9.5, color=colors["gray900"],
        ha="right", va="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff7e0",
                  edgecolor="#d7a91a", alpha=0.95))

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.grid(axis="x", alpha=0.2, linestyle="--")
ax.set_axisbelow(True)

collisions = check_label_collisions(fig, ax, fix=True, pad_px=3)
print(f"PRO 2 collisions detected/fixed: {len(collisions)}")

plt.tight_layout()
plt.savefig(f"{OUT}/pro_viz2.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# CON 1 — log-axis scatter with OLS fit + R²
# ============================================================================
fig, ax = plt.subplots(figsize=(11, 6.8))

ax.scatter(y2019["GDP"], y2019["LifeExp"], s=42, alpha=0.55,
           color="#1f6f8b", edgecolor="none", zorder=2)

xfit = np.logspace(np.log10(y2019["GDP"].min()), np.log10(y2019["GDP"].max()), 200)
yfit = slope * np.log10(xfit) + intercept
ax.plot(xfit, yfit, color=colors["gray900"], linewidth=2.4, zorder=4,
        label=f"Best fit: each 10× increase in GDP → +{slope:.1f} years   (R² = {r2:.2f})")

resid_std = y2019["resid"].std()
ax.fill_between(xfit, yfit - 1.96*resid_std, yfit + 1.96*resid_std,
                color=colors["gray900"], alpha=0.10, zorder=1)

ax.set_xscale("log")
ax.set_xlim(y2019["GDP"].min()*0.7, y2019["GDP"].max()*1.4)
ax.set_ylim(48, 88)
ax.set_xlabel("GDP per capita (constant 2010 US$, log scale)", fontsize=11, color=colors["gray600"])
ax.set_ylabel("Life expectancy at birth (years)", fontsize=11, color=colors["gray600"])

action_title(ax, "The Strongest Pattern in Development",
             "Richer nations, longer lives. n = 179, year = 2019.")

# Anchor markers — staggered offsets to avoid collisions
markers = {"Ethiopia":(15, -12), "India":(12, -12), "China":(12, -12),
           "United States":(-15, -12), "Japan":(-15, 10)}
for c, (dx, dy) in markers.items():
    row = y2019[y2019["Country Name"] == c]
    if len(row):
        r0 = row.iloc[0]
        ax.scatter(r0["GDP"], r0["LifeExp"], s=80, color=colors["accent"],
                   edgecolor="white", linewidth=1.4, zorder=5)
        ax.annotate(c, (r0["GDP"], r0["LifeExp"]),
                    xytext=(dx, dy), textcoords="offset points",
                    fontsize=9.5, color="#7a1414", fontweight="bold")

ax.legend(loc="lower right", fontsize=10, framealpha=0.95, frameon=True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(True, alpha=0.2, linestyle="--", which="both")
ax.set_axisbelow(True)

ax.text(0.99, 0.04,
        "Each dot = one country at its true 2019 values. No jittering. Source: World Bank.",
        transform=ax.transAxes, fontsize=8.5, color=colors["gray600"],
        style="italic", ha="right", va="bottom")

collisions = check_label_collisions(fig, ax, fix=True, pad_px=4)
print(f"CON 1 collisions detected/fixed: {len(collisions)}")

plt.tight_layout()
plt.savefig(f"{OUT}/con_viz.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# CON 2 — small multiples, 1960-2019, six anchor countries
# ============================================================================
ANCHORS = ["Ethiopia", "India", "China", "Korea, Rep.", "United States", "Japan"]
DISPLAY = {"Ethiopia": "Ethiopia", "India": "India", "China": "China",
           "Korea, Rep.": "South Korea", "United States": "United States", "Japan": "Japan"}

fig, axes = plt.subplots(2, 3, figsize=(13, 7.5), sharey=True, facecolor="white")
axes = axes.flatten()

for ax, country in zip(axes, ANCHORS):
    sub = df[df["Country Name"] == country].sort_values("Year")
    if len(sub) < 5:
        ax.text(0.5, 0.5, f"{country}\nno data", transform=ax.transAxes, ha="center", va="center")
        ax.set_xticks([]); ax.set_yticks([])
        continue
    ax.plot(sub["Year"], sub["LifeExp"], color="#2c7bb6", linewidth=2.7, zorder=3)
    ax.fill_between(sub["Year"], sub["LifeExp"], 30, color="#2c7bb6", alpha=0.07, zorder=1)
    ax.set_ylim(28, 88)
    ax.tick_params(axis="y", colors="#2c7bb6", labelsize=8)

    ax2 = ax.twinx()
    ax2.plot(sub["Year"], sub["GDP"], color=colors["gray400"], linewidth=1.6, alpha=0.85, zorder=2)
    ax2.set_yscale("log")
    ax2.tick_params(axis="y", colors=colors["gray600"], labelsize=7)
    ax2.spines["top"].set_visible(False)

    le_start = sub["LifeExp"].iloc[0]
    le_end = sub["LifeExp"].iloc[-1]
    gain = le_end - le_start
    ax.text(0.97, 0.06, f"+{gain:.0f} yrs\nlife",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=11, color="#1f6f1f", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#e0f5e0", edgecolor=colors["success"]))

    ax.set_title(DISPLAY[country], fontsize=12, fontweight="bold", pad=6)
    ax.spines["top"].set_visible(False)
    ax.grid(True, alpha=0.18, linestyle="--")
    ax.set_axisbelow(True)

fig.text(0.5, 0.02, "Year (1960–2019)", ha="center", fontsize=11, color=colors["gray600"])
fig.text(0.005, 0.5, "Life expectancy (blue, years)", va="center", rotation=90,
         fontsize=11, color="#2c7bb6")
fig.text(0.99, 0.5, "GDP per capita (gray, log scale, 2010 US$)", va="center", rotation=270,
         fontsize=10, color=colors["gray600"])

fig.suptitle("Six Decades, Six Countries: Every Path Bends Toward Longer Life as Wealth Climbs",
             fontsize=15, fontweight="bold", y=1.005, color=colors["gray900"])

# Run collision check across all six panels
collisions_total = sum(len(check_label_collisions(fig, ax_i, fix=True, pad_px=3)) for ax_i in axes)
print(f"CON 2 collisions detected/fixed: {collisions_total}")

plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.99])
plt.savefig(f"{OUT}/con_viz2.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()

print("All four charts polished with SWD helpers.")
import os
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        print(f"  {f} {os.path.getsize(os.path.join(OUT, f)):,} bytes")
