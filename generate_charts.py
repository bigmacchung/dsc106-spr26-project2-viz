"""
Final polish v5. Addresses Maxime's critique:
- Soften causal titles ("Money Explains" → "GDP Tracks/Predicts")
- Soften "Every Path Bends" overclaim
- Replace "95% confidence band" wording on con_viz with "approximate residual band"
- Keep 10+10 residuals (159 middle), not 12+12
- Keep no jitter, keep helpers, keep collision auto-fix
"""
import sys
sys.path.insert(0, "/sessions/practical-great-brahmagupta/mnt/DSC106 Lab Opus 4.7/projects/project2")
from helpers.chart_helpers import (
    swd_style, action_title, check_label_collisions, COLORS,
)
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import warnings; warnings.filterwarnings("ignore")

OUT = "/sessions/practical-great-brahmagupta/mnt/DSC106 Lab Opus 4.7/projects/project2/images"
GDP_COL = "average_value_GDP per capita (constant 2010 US$)"

econ = pd.read_csv("/tmp/econ.csv"); social = pd.read_csv("/tmp/social.csv")
e = econ[["Country Name", "Year", GDP_COL]].rename(columns={GDP_COL: "GDP"})
social["LifeExp"] = (social["average_value_Life expectancy at birth, male (years)"]
                     + social["average_value_Life expectancy at birth, female (years)"]) / 2
df = pd.merge(e, social[["Country Name", "Year", "LifeExp"]], on=["Country Name", "Year"]).dropna()
agg = ["World","income","OECD","Asia","Europe","Africa","America","Union","Heavily","Fragile","demographic",
       "members","Sub-Saharan","developing","developed","small states","IDA","IBRD","Euro area","Arab World",
       "Caribbean","Pacific","North America","Latin America","Middle East","European"]
df = df[~df["Country Name"].apply(lambda c: any(k.lower() in str(c).lower() for k in agg))].copy()

y2019 = df[df["Year"] == 2019].copy()
log_gdp = np.log10(y2019["GDP"])
slope, intercept = np.polyfit(log_gdp, y2019["LifeExp"], 1)
y2019["pred"] = slope * log_gdp + intercept
y2019["resid"] = y2019["LifeExp"] - y2019["pred"]
r2 = np.corrcoef(log_gdp, y2019["LifeExp"])[0, 1]**2

colors = swd_style()
plt.rcParams["figure.facecolor"] = "white"; plt.rcParams["axes.facecolor"] = "white"

# ============================================================================
# PRO 1 (now AGAINST shortcut) — keep as-is, just regenerate with helpers
# ============================================================================
under = y2019.nsmallest(4, "resid"); over = y2019.nlargest(4, "resid")
fig, ax = plt.subplots(figsize=(11, 6.8))
ax.scatter(y2019["GDP"]/1000, y2019["LifeExp"], s=40, alpha=0.42,
           color=colors["gray400"], edgecolor="none", zorder=2)
under_offsets = {"Equatorial Guinea": (10, -8), "Nigeria": (10, -8),
                 "Lesotho": (-10, -10), "Eswatini": (12, 8)}
over_offsets = {"Vietnam": (10, -8), "Nicaragua": (10, -10),
                "Honduras": (-10, 10), "Bangladesh": (-10, -12)}
for _, row in under.iterrows():
    ax.scatter(row["GDP"]/1000, row["LifeExp"], s=110, color=colors["negative"],
               edgecolor="white", linewidth=1.4, zorder=3, marker="o")
    dx, dy = under_offsets.get(row["Country Name"], (10, 8))
    ax.annotate(row["Country Name"], (row["GDP"]/1000, row["LifeExp"]),
                xytext=(dx, dy), textcoords="offset points",
                fontsize=9, color="#7a1414", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=colors["negative"], lw=0.7, alpha=0.6))
for _, row in over.iterrows():
    # square marker for colorblind distinction
    ax.scatter(row["GDP"]/1000, row["LifeExp"], s=110, color=colors["success"],
               edgecolor="white", linewidth=1.4, zorder=3, marker="s")
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
             "At every income level, health outcomes vary widely. n = 179, year = 2019.")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(True, alpha=0.18, linestyle="--"); ax.set_axisbelow(True)
ax.text(0.99, 0.04,
        "Each dot = one country, plotted at its true 2019 GDP per capita and life expectancy.\n"
        "No jitter applied. Red circles: countries below predicted life expectancy. "
        "Green squares: countries above. Source: World Bank.",
        transform=ax.transAxes, fontsize=8.5, color=colors["gray600"],
        style="italic", ha="right", va="bottom")
check_label_collisions(fig, ax, fix=True, pad_px=4)
plt.tight_layout()
plt.savefig(f"{OUT}/pro_viz.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("PRO 1 saved")

# ============================================================================
# PRO 2 (now AGAINST shortcut) — softened title
# ============================================================================
top_neg = y2019.nsmallest(10, "resid").sort_values("resid", ascending=True)
top_pos = y2019.nlargest(10, "resid").sort_values("resid", ascending=False)
middle_count = len(y2019) - len(top_neg) - len(top_pos)

fig, ax = plt.subplots(figsize=(10, 12.5))
n_neg = len(top_neg); n_pos = len(top_pos); gap = 2.0
neg_ys = np.arange(n_pos + gap, n_pos + gap + n_neg) * 1.15
pos_ys = np.arange(0, n_pos) * 1.15

for y, (_, row) in zip(neg_ys, top_neg.iterrows()):
    ax.hlines(y=y, xmin=0, xmax=row["resid"], color=colors["negative"], linewidth=2.5, alpha=0.85)
    # circle marker
    ax.scatter(row["resid"], y, s=95, color=colors["negative"], edgecolor="white",
               linewidth=1.3, zorder=3, marker="o")
    ax.text(row["resid"] - 0.4, y, f"{row['Country Name']}  ({row['resid']:.1f})",
            fontsize=10, color="#7a1414", va="center", ha="right", fontweight="bold")

for y, (_, row) in zip(pos_ys, top_pos.iterrows()):
    ax.hlines(y=y, xmin=0, xmax=row["resid"], color=colors["success"], linewidth=2.5, alpha=0.85)
    # square marker for colorblind distinction
    ax.scatter(row["resid"], y, s=95, color=colors["success"], edgecolor="white",
               linewidth=1.3, zorder=3, marker="s")
    ax.text(row["resid"] + 0.4, y, f"{row['Country Name']}  (+{row['resid']:.1f})",
            fontsize=10, color="#1f6f1f", va="center", ha="left", fontweight="bold")

ax.axvline(0, color=colors["gray900"], linewidth=1.0, zorder=2)
gap_y_center = (n_pos - 0.5 + (n_pos + gap)) / 2 * 1.15
ax.axhspan((n_pos - 0.5) * 1.15, (n_pos + gap) * 1.15, color=colors["gray100"], alpha=0.6, zorder=1)
ax.text(0, gap_y_center,
        f"…and {middle_count} other countries within ±5 years of the fitted line",
        fontsize=10, color=colors["gray600"], style="italic", va="center", ha="center")

ax.set_yticks([])
ax.set_xlabel("Life expectancy minus GDP-predicted life expectancy (years)", fontsize=11, color=colors["gray600"], labelpad=10)
ax.set_xlim(-19, 12)
ax.set_ylim(-1.2, (n_pos + gap + n_neg) * 1.15)

# Softened title: GDP Tracks, not Money Explains
action_title(ax, "GDP Tracks 70% of Life Expectancy, but a 20-Year Gap Remains",
             f"Residuals from a log-GDP regression on all 179 countries, 2019 (R² = {r2:.2f}).")

fig.text(0.5, -0.01,
         "Same 179 countries and same regression line as the AGAINST visualization. "
         "Red circles = wealth predicts longer life than reality. "
         "Green squares = wealth predicts shorter life than reality. "
         "If income alone determined health, every lollipop would sit at zero.",
         fontsize=9, color=colors["gray600"], style="italic", ha="center", va="top",
         wrap=True)

ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.spines["left"].set_visible(False)
ax.grid(axis="x", alpha=0.2, linestyle="--"); ax.set_axisbelow(True)
check_label_collisions(fig, ax, fix=True, pad_px=2)
plt.tight_layout()
plt.savefig(f"{OUT}/pro_viz2.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print(f"PRO 2 saved (10+10 residuals, {middle_count} middle, softened title)")

# ============================================================================
# CON 1 (now FOR shortcut) — replace "95% confidence band" with residual band wording
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
                color=colors["gray900"], alpha=0.10, zorder=1,
                label="Residual spread (~95% of countries)")
ax.set_xscale("log")
ax.set_xlim(y2019["GDP"].min()*0.7, y2019["GDP"].max()*1.4)
ax.set_ylim(48, 88)
ax.set_xlabel("GDP per capita (constant 2010 US$, log scale)", fontsize=11, color=colors["gray600"])
ax.set_ylabel("Life expectancy at birth (years)", fontsize=11, color=colors["gray600"])
action_title(ax, "GDP Tracks 70% of the Life Expectancy Pattern",
             "Richer nations live longer, with a strong fitted association. n = 179, year = 2019.")
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
                    fontsize=9.5, color="#7a1414", fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none", alpha=0.85))
ax.legend(loc="lower right", fontsize=9.5, framealpha=0.95, frameon=True)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(True, alpha=0.2, linestyle="--", which="both"); ax.set_axisbelow(True)
ax.text(0.99, 0.04,
        "Each dot = one country at its true 2019 values. No jitter. Source: World Bank.",
        transform=ax.transAxes, fontsize=8.5, color=colors["gray600"],
        style="italic", ha="right", va="bottom")
check_label_collisions(fig, ax, fix=True, pad_px=4)
plt.tight_layout()
plt.savefig(f"{OUT}/con_viz.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("CON 1 saved (residual band wording, softened title 'GDP Tracks')")

# ============================================================================
# CON 2 (now FOR shortcut) — soften "Every Path Bends" overclaim
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
        ax.set_xticks([]); ax.set_yticks([]); continue
    ax.plot(sub["Year"], sub["LifeExp"], color="#2c7bb6", linewidth=2.7, zorder=3)
    ax.fill_between(sub["Year"], sub["LifeExp"], 30, color="#2c7bb6", alpha=0.07, zorder=1)
    ax.set_ylim(28, 88)
    ax.tick_params(axis="y", colors="#2c7bb6", labelsize=8)
    ax2 = ax.twinx()
    ax2.plot(sub["Year"], sub["GDP"], color=colors["gray400"], linewidth=1.6, alpha=0.85, zorder=2)
    ax2.set_yscale("log")
    ax2.tick_params(axis="y", colors=colors["gray600"], labelsize=7)
    ax2.spines["top"].set_visible(False)
    le_start = sub["LifeExp"].iloc[0]; le_end = sub["LifeExp"].iloc[-1]
    gain = le_end - le_start
    ax.text(0.97, 0.06, f"+{gain:.0f} yrs\nlife",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=11, color="#1f6f1f", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#e0f5e0", edgecolor=colors["success"]))
    ax.set_title(DISPLAY[country], fontsize=12, fontweight="bold", pad=6)
    ax.spines["top"].set_visible(False)
    ax.grid(True, alpha=0.18, linestyle="--"); ax.set_axisbelow(True)

fig.text(0.5, 0.02, "Year (1960–2019)", ha="center", fontsize=11, color=colors["gray600"])
fig.text(0.005, 0.5, "Life expectancy (blue, years)", va="center", rotation=90,
         fontsize=11, color="#2c7bb6")
fig.text(0.99, 0.5, "GDP per capita (gray, log scale, 2010 US$, contextual second axis)",
         va="center", rotation=270, fontsize=9, color=colors["gray600"])

# Softened title: was "Every Path Bends Toward Longer Life"
fig.suptitle("Across Six Decades, Income and Life Expectancy Climbed Together in These Six Countries",
             fontsize=14.5, fontweight="bold", y=1.005, color=colors["gray900"])

for ax_i in axes:
    check_label_collisions(fig, ax_i, fix=True, pad_px=3)

plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.99])
plt.savefig(f"{OUT}/con_viz2.png", dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("CON 2 saved (softened title, dual axis disclosed as contextual)")
