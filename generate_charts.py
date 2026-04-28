"""
Same-data persuasion. Both charts plot every country in 2019 with GDP per capita
on x and life expectancy on y. Persuasion lives in axis scaling, fitted curves,
annotations, and titles, not in country selection.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings("ignore")

OUT = "/sessions/practical-great-brahmagupta/mnt/DSC106 Lab Opus 4.7/projects/project2/images"

# Load and clean
econ = pd.read_csv("/tmp/econ.csv")
social = pd.read_csv("/tmp/social.csv")
GDP_COL = "average_value_GDP per capita (constant 2010 US$)"

e = econ[["Country Name", "Year", GDP_COL]].rename(columns={GDP_COL: "GDP"})
social["LifeExp"] = (
    social["average_value_Life expectancy at birth, male (years)"]
    + social["average_value_Life expectancy at birth, female (years)"]
) / 2
h = social[["Country Name", "Year", "LifeExp"]]
df = pd.merge(e, h, on=["Country Name", "Year"]).dropna()

# Filter out aggregate rows
agg_keywords = ["World", "income", "OECD", "Asia", "Europe", "Africa", "America",
                "Union", "Heavily", "Fragile", "demographic", "members",
                "Sub-Saharan", "developing", "developed", "small states",
                "IDA", "IBRD", "Euro area", "Arab World", "Caribbean", "Pacific",
                "North America", "Latin America", "Middle East", "European"]
mask = ~df["Country Name"].apply(lambda c: any(k.lower() in str(c).lower() for k in agg_keywords))
df = df[mask].copy()

# Cross-section: 2019 (latest year with broad coverage)
y2019 = df[df["Year"] == 2019].copy()
print(f"2019 country count: {len(y2019)}")

# Compute fit
log_gdp = np.log10(y2019["GDP"])
slope, intercept = np.polyfit(log_gdp, y2019["LifeExp"], 1)
xfit = np.logspace(np.log10(y2019["GDP"].min()), np.log10(y2019["GDP"].max()), 200)
yfit = slope * np.log10(xfit) + intercept
r = np.corrcoef(log_gdp, y2019["LifeExp"])[0, 1]
r2 = r**2
print(f"R² of LE vs log(GDP): {r2:.3f}, r={r:.3f}")

# Identify outliers for PRO annotations
y2019["resid"] = y2019["LifeExp"] - (slope * log_gdp + intercept)
under = y2019.nsmallest(4, "resid")  # countries that underperform their wealth
over = y2019.nlargest(4, "resid")    # countries that overperform their wealth
print("\nUnderperformers (poor health for their wealth):")
print(under[["Country Name", "GDP", "LifeExp", "resid"]])
print("\nOverperformers (good health despite low wealth):")
print(over[["Country Name", "GDP", "LifeExp", "resid"]])

# ==========================================================================
# PRO VIZ — getting richer has NOT made countries healthier
# ==========================================================================
fig, ax = plt.subplots(figsize=(11, 7), facecolor="white")

# Linear x-axis crushes the Preston curve into a wall
ax.scatter(y2019["GDP"]/1000, y2019["LifeExp"],
           s=42, alpha=0.55, color="#666666", edgecolor="none", zorder=2)

# Highlight underperformers (low LE despite high GDP) - red
for _, row in under.iterrows():
    ax.scatter(row["GDP"]/1000, row["LifeExp"], s=110, color="#d7191c",
               edgecolor="white", linewidth=1.3, zorder=3)
    offset_x = 1.5 if row["GDP"] > 30000 else 1.5
    offset_y = -1.2 if row["Country Name"] in ["Equatorial Guinea"] else 1.0
    ax.annotate(row["Country Name"],
                (row["GDP"]/1000, row["LifeExp"]),
                xytext=(row["GDP"]/1000 + offset_x, row["LifeExp"] + offset_y),
                fontsize=9, color="#9a1414", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color="#d7191c", lw=0.8, alpha=0.7))

# Highlight overperformers (high LE despite low GDP) - green
for _, row in over.iterrows():
    ax.scatter(row["GDP"]/1000, row["LifeExp"], s=110, color="#2ca02c",
               edgecolor="white", linewidth=1.3, zorder=3)
    ax.annotate(row["Country Name"],
                (row["GDP"]/1000, row["LifeExp"]),
                xytext=(row["GDP"]/1000 + 2, row["LifeExp"] - 1.6),
                fontsize=9, color="#1f6f1f", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color="#2ca02c", lw=0.8, alpha=0.7))

# No fit line. Tight, partly-truncated y-axis (50-90, true range ~52-85).
ax.set_xlim(-3, y2019["GDP"].max()/1000 + 5)
ax.set_ylim(50, 88)
ax.set_xlabel("GDP per capita (thousand 2010 US$)", fontsize=11)
ax.set_ylabel("Life expectancy at birth (years)", fontsize=11)
ax.set_title("Wealth Is No Cure: At Every Income Level, Health Outcomes Are All Over the Map",
             fontsize=14.5, fontweight="bold", pad=14)
ax.grid(alpha=0.25, linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Captions
ax.text(0.99, 0.02,
        "Each dot = one country, 2019. Source: World Bank.\n"
        "Red = wealthy country with disappointing health.   Green = poor country with strong health.",
        transform=ax.transAxes, fontsize=8.5, color="#555", style="italic",
        ha="right", va="bottom")

# Subtle: crammed left side of chart looks like a vertical "wall"; reader's eye
# reads "no clear pattern."
ax.text(0.02, 0.95,
        "Equatorial Guinea earns more per person than Argentina,\nyet lives 20 years less.\n"
        "Cuba is a tenth as rich as Norway,\nbut lives almost as long.",
        transform=ax.transAxes, fontsize=10, color="#222",
        ha="left", va="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff7e0",
                  edgecolor="#d7a91a", alpha=0.9))

plt.tight_layout()
plt.savefig(f"{OUT}/pro_viz.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("PRO viz done")

# ==========================================================================
# CON VIZ — getting richer HAS made countries healthier
# ==========================================================================
fig, ax = plt.subplots(figsize=(11, 7), facecolor="white")

# Log x-axis reveals Preston curve cleanly
ax.scatter(y2019["GDP"], y2019["LifeExp"],
           s=42, alpha=0.55, color="#1f6f8b", edgecolor="none", zorder=2)

# Fit line + 95% band
ax.plot(xfit, yfit, color="#222", linewidth=2.4, zorder=4,
        label=f"Best fit: each 10× increase in GDP → +{slope:.1f} years   (R² = {r2:.2f})")

# Standard error band
resid_std = (y2019["LifeExp"] - (slope * log_gdp + intercept)).std()
ax.fill_between(xfit, yfit - 1.96*resid_std, yfit + 1.96*resid_std,
                color="#222", alpha=0.10, zorder=1)

ax.set_xscale("log")
ax.set_xlim(y2019["GDP"].min()*0.7, y2019["GDP"].max()*1.4)
ax.set_ylim(48, 88)
ax.set_xlabel("GDP per capita (constant 2010 US$, log scale)", fontsize=11)
ax.set_ylabel("Life expectancy at birth (years)", fontsize=11)
ax.set_title("The Strongest Pattern in Development:\nRicher Nations, Longer Lives",
             fontsize=14.5, fontweight="bold", pad=14)
ax.grid(alpha=0.25, linestyle="--", which="both")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Annotation: highlight a few markers along the curve to lock in the trend
markers = ["Ethiopia", "India", "China", "United States", "Japan"]
for c in markers:
    row = y2019[y2019["Country Name"] == c]
    if len(row):
        r0 = row.iloc[0]
        ax.scatter(r0["GDP"], r0["LifeExp"], s=80, color="#c0392b",
                   edgecolor="white", linewidth=1.3, zorder=5)
        ax.annotate(c, (r0["GDP"], r0["LifeExp"]),
                    xytext=(r0["GDP"]*1.1, r0["LifeExp"] - 1.6),
                    fontsize=9.5, color="#722e22", fontweight="bold")

ax.legend(loc="lower right", fontsize=10, framealpha=0.95)

ax.text(0.02, 0.97,
        "Across nearly every country on Earth, doubling income\n"
        "is associated with a measurable rise in life expectancy.",
        transform=ax.transAxes, fontsize=10.5, color="#0d3a52",
        ha="left", va="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#e0f0fa",
                  edgecolor="#2c7bb6", alpha=0.9))

ax.text(0.99, 0.02,
        "Each dot = one country, 2019. Log scale on GDP. Source: World Bank.",
        transform=ax.transAxes, fontsize=8.5, color="#555", style="italic",
        ha="right", va="bottom")

plt.tight_layout()
plt.savefig(f"{OUT}/con_viz.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("CON viz done")

import os
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        print(f, os.path.getsize(os.path.join(OUT, f)))
"""
Two ADDITIONAL persuasive visualizations to pair with the existing two.

PRO 2: residuals dot plot — even granting the con side's log-linear fit, 30% of
       life expectancy variance is unexplained, and the worst residuals span ±12
       years. "Money explains 70%; the other 30% is a 20-year gap."

CON 2: small-multiples time series 1960-2019 for six anchor countries — the
       wealth/health correlation is not just a 2019 snapshot, it holds within
       every country longitudinally.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

OUT = "/sessions/practical-great-brahmagupta/mnt/DSC106 Lab Opus 4.7/projects/project2/images"
GDP_COL = "average_value_GDP per capita (constant 2010 US$)"

econ = pd.read_csv("/tmp/econ.csv")
social = pd.read_csv("/tmp/social.csv")

e = econ[["Country Name", "Year", GDP_COL]].rename(columns={GDP_COL: "GDP"})
social["LifeExp"] = (
    social["average_value_Life expectancy at birth, male (years)"]
    + social["average_value_Life expectancy at birth, female (years)"]
) / 2
h = social[["Country Name", "Year", "LifeExp"]]
df = pd.merge(e, h, on=["Country Name", "Year"]).dropna()

agg_keywords = ["World", "income", "OECD", "Asia", "Europe", "Africa", "America",
                "Union", "Heavily", "Fragile", "demographic", "members", "Sub-Saharan",
                "developing", "developed", "small states", "IDA", "IBRD", "Euro area",
                "Arab World", "Caribbean", "Pacific", "North America", "Latin America",
                "Middle East", "European"]
mask = ~df["Country Name"].apply(lambda c: any(k.lower() in str(c).lower() for k in agg_keywords))
df = df[mask].copy()

y2019 = df[df["Year"] == 2019].copy()
log_gdp = np.log10(y2019["GDP"])
slope, intercept = np.polyfit(log_gdp, y2019["LifeExp"], 1)
y2019["pred"] = slope * log_gdp + intercept
y2019["resid"] = y2019["LifeExp"] - y2019["pred"]
r2 = np.corrcoef(log_gdp, y2019["LifeExp"])[0, 1]**2

# ============================================================================
# PRO 2 — Residuals dot plot
# ============================================================================
top_pos = y2019.nlargest(12, "resid").sort_values("resid")
top_neg = y2019.nsmallest(12, "resid").sort_values("resid")
labelled = pd.concat([top_neg, top_pos])
middle_count = len(y2019) - len(labelled)

fig, ax = plt.subplots(figsize=(10, 11), facecolor="white")

# Plot the labelled tails as lollipops
y_positions = np.arange(len(labelled))
for i, (_, row) in enumerate(labelled.iterrows()):
    color = "#2ca02c" if row["resid"] >= 0 else "#d7191c"
    ax.hlines(y=i, xmin=0, xmax=row["resid"], color=color, linewidth=2.2, alpha=0.85)
    ax.scatter(row["resid"], i, s=90, color=color,
               edgecolor="white", linewidth=1.2, zorder=3)

# Strong axis at zero
ax.axvline(0, color="black", linewidth=1.0, zorder=2)

# Country labels positioned at the dot ends (away from zero)
for i, (_, row) in enumerate(labelled.iterrows()):
    txt_color = "#1f6f1f" if row["resid"] >= 0 else "#9a1414"
    if row["resid"] >= 0:
        ax.text(row["resid"] + 0.3, i, f"{row['Country Name']}  (+{row['resid']:.1f})",
                fontsize=9.5, color=txt_color, va="center", fontweight="bold")
    else:
        ax.text(row["resid"] - 0.3, i, f"{row['Country Name']}  ({row['resid']:.1f})",
                fontsize=9.5, color=txt_color, va="center", ha="right", fontweight="bold")

# Collapsed middle band annotation
band_y_low = len(top_neg) - 0.5
band_y_high = len(top_neg) + 0.5
ax.axhspan(band_y_low, band_y_high, color="#dddddd", alpha=0.5, zorder=1)
ax.text(0, (band_y_low + band_y_high)/2,
        f"  …{middle_count} other countries within ±3 years of the fit",
        fontsize=10, color="#444", style="italic", va="center", ha="left")

# Reset y axis to integer ticks but hide them
ax.set_yticks([])
ax.set_xlabel("Life expectancy minus what GDP predicts (years)", fontsize=11)
ax.set_xlim(-15, 10)
ax.set_title("Money Explains 70% of Life Expectancy.\nThe Other 30% Is a 20-Year Gap.",
             fontsize=14.5, fontweight="bold", pad=14)

ax.text(0.99, 1.02,
        f"Residuals from a log-GDP regression on all 179 countries, 2019 (R² = {r2:.2f}).",
        transform=ax.transAxes, fontsize=9, color="#555", style="italic",
        ha="right", va="bottom")

ax.text(0.02, 0.02,
        "Same 179 countries and same regression line as Visualization 2 (con side).\n"
        "Each red lollipop is a country whose people die younger than their wealth predicts.\n"
        "Each green lollipop is a country whose people outlive what their wealth predicts.\n"
        "If wealth genuinely bought health, these gaps would not exist.",
        transform=ax.transAxes, fontsize=9.5, color="#222",
        ha="left", va="bottom",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff7e0",
                  edgecolor="#d7a91a", alpha=0.9))

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.grid(axis="x", alpha=0.25, linestyle="--")

plt.tight_layout()
plt.savefig(f"{OUT}/pro_viz2.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("PRO 2 done")

# ============================================================================
# CON 2 — Small multiples time series, 1960-2019
# ============================================================================
ANCHORS = ["Ethiopia", "India", "China", "Korea, Rep.", "United States", "Japan"]
DISPLAY = {"Ethiopia": "Ethiopia", "India": "India", "China": "China",
           "Korea, Rep.": "South Korea", "United States": "United States", "Japan": "Japan"}

# Check Korea, Rep. is the right name
korea_check = df[df["Country Name"].str.contains("Korea", na=False)]["Country Name"].unique()
print("Korea names found:", korea_check)

fig, axes = plt.subplots(2, 3, figsize=(13, 7.5), facecolor="white", sharey=True)
axes = axes.flatten()

for ax, country in zip(axes, ANCHORS):
    sub = df[df["Country Name"] == country].sort_values("Year")
    if len(sub) < 5:
        ax.text(0.5, 0.5, f"{country}\nno data", transform=ax.transAxes, ha="center", va="center")
        ax.set_xticks([]); ax.set_yticks([])
        continue
    # Life expectancy - primary axis
    ax.plot(sub["Year"], sub["LifeExp"], color="#2c7bb6", linewidth=2.7, zorder=3)
    ax.fill_between(sub["Year"], sub["LifeExp"], 30, color="#2c7bb6", alpha=0.07, zorder=1)
    ax.set_ylim(28, 88)
    ax.tick_params(axis="y", colors="#2c7bb6")
    
    # GDP - twin axis, log scale
    ax2 = ax.twinx()
    ax2.plot(sub["Year"], sub["GDP"], color="#999999", linewidth=1.6, linestyle="-", alpha=0.8, zorder=2)
    ax2.set_yscale("log")
    ax2.tick_params(axis="y", colors="#666", labelsize=8)
    ax2.spines["top"].set_visible(False)
    
    # Annotation: total LE gain
    le_start = sub["LifeExp"].iloc[0]
    le_end = sub["LifeExp"].iloc[-1]
    gain = le_end - le_start
    ax.text(0.97, 0.06, f"+{gain:.0f} yrs\nlife",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=11, color="#1f6f1f", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#e0f5e0", edgecolor="#2ca02c"))
    
    ax.set_title(DISPLAY[country], fontsize=12, fontweight="bold", pad=6)
    ax.spines["top"].set_visible(False)
    ax.grid(alpha=0.2, linestyle="--")

# Shared labels
fig.text(0.5, 0.02, "Year (1960–2019)", ha="center", fontsize=11)
fig.text(0.005, 0.5, "Life expectancy (blue, years)", va="center", rotation=90,
         fontsize=11, color="#2c7bb6")
fig.text(0.99, 0.5, "GDP per capita (gray, log scale, 2010 US$)", va="center", rotation=270,
         fontsize=10, color="#666")

fig.suptitle("Six Decades, Six Countries: Every Path Bends Toward Longer Life as Wealth Climbs",
             fontsize=15, fontweight="bold", y=1.005)

plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.99])
plt.savefig(f"{OUT}/con_viz2.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("CON 2 done")

import os
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        print(f, os.path.getsize(os.path.join(OUT, f)))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings; warnings.filterwarnings("ignore")

OUT = "/sessions/practical-great-brahmagupta/mnt/DSC106 Lab Opus 4.7/projects/project2/images"
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
y2019["resid"] = y2019["LifeExp"] - (slope * log_gdp + intercept)
r2 = np.corrcoef(log_gdp, y2019["LifeExp"])[0, 1]**2

# Combine: top 12 negatives at top of plot, gap-row, top 12 positives at bottom
top_neg = y2019.nsmallest(12, "resid").sort_values("resid", ascending=True)  # most negative first
top_pos = y2019.nlargest(12, "resid").sort_values("resid", ascending=False)  # most positive first
middle_count = len(y2019) - len(top_neg) - len(top_pos)

fig, ax = plt.subplots(figsize=(10, 11.5), facecolor="white")

# Build y positions: negatives at top (high y), gap, positives at bottom
n_neg = len(top_neg)
n_pos = len(top_pos)
gap = 1.5
neg_ys = np.arange(n_pos + gap, n_pos + gap + n_neg)
pos_ys = np.arange(0, n_pos)

for y, (_, row) in zip(neg_ys, top_neg.iterrows()):
    ax.hlines(y=y, xmin=0, xmax=row["resid"], color="#d7191c", linewidth=2.2, alpha=0.85)
    ax.scatter(row["resid"], y, s=90, color="#d7191c", edgecolor="white", linewidth=1.2, zorder=3)
    ax.text(row["resid"] - 0.3, y, f"{row['Country Name']}  ({row['resid']:.1f})",
            fontsize=9.5, color="#9a1414", va="center", ha="right", fontweight="bold")

for y, (_, row) in zip(pos_ys, top_pos.iterrows()):
    ax.hlines(y=y, xmin=0, xmax=row["resid"], color="#2ca02c", linewidth=2.2, alpha=0.85)
    ax.scatter(row["resid"], y, s=90, color="#2ca02c", edgecolor="white", linewidth=1.2, zorder=3)
    ax.text(row["resid"] + 0.3, y, f"{row['Country Name']}  (+{row['resid']:.1f})",
            fontsize=9.5, color="#1f6f1f", va="center", ha="left", fontweight="bold")

ax.axvline(0, color="black", linewidth=1.0, zorder=2)

# Gap band centered between
gap_y = n_pos + gap/2
ax.axhspan(n_pos - 0.4, n_pos + gap, color="#eeeeee", alpha=0.7, zorder=1)
ax.text(0, gap_y, f"…and {middle_count} other countries within ±5 years of the fit line",
        fontsize=10, color="#555", style="italic", va="center", ha="center")

ax.set_yticks([])
ax.set_xlabel("Life expectancy minus what GDP predicts (years)", fontsize=11)
ax.set_xlim(-18, 11)
ax.set_ylim(-0.7, n_pos + gap + n_neg - 0.3)

# Title with breathing room
fig.suptitle("Money Explains 70% of Life Expectancy. The Other 30% Is a 20-Year Gap.",
             fontsize=14, fontweight="bold", y=0.985)
ax.set_title(f"Residuals from a log-GDP regression on all 179 countries, 2019  (R² = {r2:.2f})",
             fontsize=10, color="#555", style="italic", pad=10, loc="left")

# Caption box at top, well clear of the data
ax.text(0.99, 0.99,
        "Same 179 countries and same regression line as Visualization 2 (con side).\n"
        "Red = country whose people die younger than its wealth predicts.\n"
        "Green = country whose people outlive what its wealth predicts.\n"
        "If wealth genuinely bought health, these gaps would not exist.",
        transform=ax.transAxes, fontsize=9.5, color="#222",
        ha="right", va="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff7e0",
                  edgecolor="#d7a91a", alpha=0.95))

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.grid(axis="x", alpha=0.25, linestyle="--")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f"{OUT}/pro_viz2.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("pro_viz2 fixed")
