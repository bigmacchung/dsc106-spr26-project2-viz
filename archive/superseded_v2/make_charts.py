"""
DSC 106 Project 2 - chart generation.

Run from the repo root:
    python3 scripts/make_charts.py

Reads:
    data/World-Bank-Data-by-Indicators-master/health/health-raw-2021.csv
    data/World-Bank-Data-by-Indicators-master/economy-and-growth/economy-and-growth-raw-2021.csv
    data/World-Bank-Data-by-Indicators-master/health/Metadata_Country_API_8_DS2_en_csv_v2_3052924.csv

Writes:
    images/pro_chart1.png
    images/pro_chart2.png
    images/con_chart1.png
    images/con_chart2.png

Indicator codes:
    Real GDP per capita = "GDP per capita (constant 2010 US$)" (NY.GDP.PCAP.KD)
    Life expectancy     = "Life expectancy at birth, total (years)" (SP.DYN.LE00.IN)
    Population 65+      = "Population ages 65 and above (% of total population)" (SP.POP.65UP.TO.ZS)

Requires: pandas, numpy, matplotlib
    pip install pandas numpy matplotlib
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

REPO = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO / "data" / "World-Bank-Data-by-Indicators-master"
OUT_DIR = REPO / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_country_codes() -> set:
    """ISO countries only, regional aggregates excluded."""
    meta = pd.read_csv(
        DATA_ROOT / "health" / "Metadata_Country_API_8_DS2_en_csv_v2_3052924.csv",
        dtype=str,
    )
    meta.columns = [c.strip().lstrip("﻿").strip('"') for c in meta.columns]
    countries = meta[meta["Region"].notna() & (meta["Region"].str.strip() != "")]
    return set(countries["Country Code"].dropna().str.strip())


def load_indicator_long(raw_csv: Path, indicator_code: str) -> pd.DataFrame:
    df = pd.read_csv(raw_csv, skiprows=4, dtype=str)
    df = df[df["Indicator Code"] == indicator_code].copy()
    year_cols = [c for c in df.columns if c.isdigit()]
    long = df.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )
    long["year"] = long["year"].astype(int)
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long = long.dropna(subset=["value"]).rename(
        columns={"Country Name": "country", "Country Code": "code"}
    )
    return long


def latest_value_per_country(long_df: pd.DataFrame, year_max: int = 2020) -> pd.DataFrame:
    df = long_df[long_df["year"] <= year_max].copy()
    df = df.sort_values(["code", "year"])
    return df.groupby("code", as_index=False).tail(1)


def style():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 18,
            "axes.titleweight": "bold",
            "axes.labelsize": 13,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "figure.dpi": 200,
        }
    )


def save(fig, name: str):
    out = OUT_DIR / name
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"  wrote {out.relative_to(REPO)} ({out.stat().st_size/1024:.1f} KB)")
    plt.close(fig)


def main():
    print("loading data...")
    country_codes = load_country_codes()
    print(f"  {len(country_codes)} ISO countries")

    life_long = load_indicator_long(
        DATA_ROOT / "health" / "health-raw-2021.csv", "SP.DYN.LE00.IN"
    )
    gdp_long = load_indicator_long(
        DATA_ROOT / "economy-and-growth" / "economy-and-growth-raw-2021.csv",
        "NY.GDP.PCAP.KD",
    )
    pop65_long = load_indicator_long(
        DATA_ROOT / "health" / "health-raw-2021.csv", "SP.POP.65UP.TO.ZS"
    )

    life_long = life_long[life_long["code"].isin(country_codes)]
    gdp_long = gdp_long[gdp_long["code"].isin(country_codes)]
    pop65_long = pop65_long[pop65_long["code"].isin(country_codes)]

    style()

    # ---- pro chart 1 -------------------------------------------------------
    print("\nbuilding pro_chart1 ...")
    life_latest = latest_value_per_country(life_long)
    gdp_latest = latest_value_per_country(gdp_long)
    scatter = (
        life_latest.merge(gdp_latest, on="code", suffixes=("_life", "_gdp"))
        .dropna()
        .rename(columns={"value_life": "life_exp", "value_gdp": "gdp_pc"})
    )
    scatter = scatter[scatter["gdp_pc"] > 0]
    print(f"  scatter rows: {len(scatter)}")

    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    ax.scatter(
        scatter["gdp_pc"], scatter["life_exp"],
        s=42, alpha=0.55, color="#5a6b7a", edgecolor="white", linewidth=0.6,
    )
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"${int(x):,}" if x >= 1 else ""
    ))
    ax.set_xticks([200, 1000, 5000, 25000, 100000])
    ax.set_xlim(150, 150_000)
    ax.set_ylim(45, 85)
    ax.set_xlabel("GDP per capita, constant 2010 US$ (log scale)")
    ax.set_ylabel("Life expectancy at birth (years)")
    ax.set_title(
        "Economic growth does not reliably improve life expectancy",
        loc="left", pad=14,
    )
    fig.text(
        0.5, 0.005,
        "Latest available year per country, 2018-2020 · World Bank",
        ha="center", fontsize=9, color="#666", style="italic",
    )
    ax.grid(True, axis="y", alpha=0.25)
    save(fig, "pro_chart1.png")

    # ---- pro chart 2 -------------------------------------------------------
    print("\nbuilding pro_chart2 ...")
    band = scatter[(scatter["gdp_pc"] >= 5_000) & (scatter["gdp_pc"] <= 25_000)].copy()
    worst7 = band.nsmallest(7, "life_exp")
    others = band.drop(worst7.index)
    print(f"  band rows: {len(band)} | worst7: {list(worst7['country_life'])}")

    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    ax.scatter(
        others["gdp_pc"], others["life_exp"],
        s=46, alpha=0.45, color="#7f8c9b", edgecolor="white", linewidth=0.6,
        label="Wealthier countries",
    )
    ax.scatter(
        worst7["gdp_pc"], worst7["life_exp"],
        s=110, color="#c0392b", edgecolor="white", linewidth=0.8,
        label="Lowest life-expectancy", zorder=3,
    )
    for _, row in worst7.iterrows():
        ax.annotate(
            row["country_life"], (row["gdp_pc"], row["life_exp"]),
            textcoords="offset points", xytext=(7, -3),
            fontsize=9, color="#c0392b", fontweight="bold",
        )
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"${int(x):,}" if x >= 1 else ""
    ))
    ax.set_xticks([5_000, 10_000, 25_000])
    ax.set_xlim(4_500, 27_500)
    ax.set_ylim(55, 85)
    ax.set_xlabel("GDP per capita, constant 2010 US$ (log scale)")
    ax.set_ylabel("Life expectancy at birth (years)")
    ax.set_title(
        "Even among wealthier countries, wealth does not guarantee longer lives",
        loc="left", pad=14,
    )
    fig.text(
        0.5, 0.005,
        f"Countries with GDP per capita between $5,000 and $25,000 · n = {len(band)}",
        ha="center", fontsize=9, color="#666", style="italic",
    )
    ax.legend(loc="lower right", frameon=False)
    ax.grid(True, axis="y", alpha=0.25)
    save(fig, "pro_chart2.png")

    # ---- con chart 1 -------------------------------------------------------
    print("\nbuilding con_chart1 ...")
    china_gdp = gdp_long[(gdp_long["code"] == "CHN") & (gdp_long["year"] >= 2000)].sort_values("year")
    china_p65 = pop65_long[(pop65_long["code"] == "CHN") & (pop65_long["year"] >= 2000)].sort_values("year")
    print(f"  china gdp years: {china_gdp['year'].min()}-{china_gdp['year'].max()} | n={len(china_gdp)}")
    print(f"  china p65 years: {china_p65['year'].min()}-{china_p65['year'].max()} | n={len(china_p65)}")

    fig, ax1 = plt.subplots(figsize=(9.5, 6.0))
    color_gdp = "#1f6fb5"
    color_p65 = "#c0392b"
    ax1.plot(china_gdp["year"], china_gdp["value"],
             color=color_gdp, linewidth=3, marker="o", markersize=5)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("GDP per capita, constant 2010 US$", color=color_gdp)
    ax1.tick_params(axis="y", labelcolor=color_gdp)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x):,}"))
    ax1.grid(True, axis="y", alpha=0.2)

    ax2 = ax1.twinx()
    ax2.plot(china_p65["year"], china_p65["value"],
             color=color_p65, linewidth=3, marker="s", markersize=5)
    ax2.set_ylabel("Population aged 65 and above (% of total)", color=color_p65)
    ax2.tick_params(axis="y", labelcolor=color_p65)
    ax2.spines["top"].set_visible(False)
    ax1.set_ylim(0, china_gdp["value"].max() * 1.05)
    ax2.set_ylim(0, china_p65["value"].max() * 1.05)
    ax1.set_title(
        "The wealth cure: economic growth drives longer, healthier lives in China",
        loc="left", pad=14,
    )
    fig.text(
        0.5, 0.005,
        "China, 2000-2020 · GDP per capita and share of population aged 65+ · World Bank",
        ha="center", fontsize=9, color="#666", style="italic",
    )
    save(fig, "con_chart1.png")

    # ---- con chart 2 -------------------------------------------------------
    print("\nbuilding con_chart2 ...")
    annual = (
        gdp_long.merge(life_long, on=["code", "year"], suffixes=("_gdp", "_life"))
        .dropna()
    )
    annual = annual[(annual["year"] >= 2000) & (annual["year"] <= 2020)]
    yearly = annual.groupby("year", as_index=False).agg(
        mean_gdp=("value_gdp", "mean"), mean_life=("value_life", "mean")
    )
    print(f"  annual means rows: {len(yearly)} (2000-2020)")

    x = yearly["mean_gdp"].values
    y = yearly["mean_life"].values
    b, a = np.polyfit(x, y, 1)
    y_pred = a + b * x
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    print(f"  fit: y = {a:.4f} + {b:.6f} * x | R^2 = {r2:.3f}")

    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    sc = ax.scatter(x, y, c=yearly["year"], cmap="viridis",
                    s=120, edgecolor="white", linewidth=1.0, zorder=3)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, a + b * xs, color="#1f6fb5", linewidth=2.5, alpha=0.85,
            zorder=2, label=f"Linear fit  R² = {r2:.2f}")
    for year_label in (yearly["year"].min(), yearly["year"].max()):
        row = yearly[yearly["year"] == year_label].iloc[0]
        ax.annotate(
            str(year_label), (row["mean_gdp"], row["mean_life"]),
            textcoords="offset points", xytext=(8, -12),
            fontsize=11, fontweight="bold",
        )
    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("Year")
    ax.set_xlabel("Global mean GDP per capita, constant 2010 US$")
    ax.set_ylabel("Global mean life expectancy at birth (years)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${int(v):,}"))
    ax.set_title("Globally, wealth and health rise together", loc="left", pad=14)
    fig.text(
        0.5, 0.005,
        "Annual cross-country means, 2000-2020 · World Bank",
        ha="center", fontsize=9, color="#666", style="italic",
    )
    ax.legend(loc="lower right", frameon=False)
    ax.grid(True, alpha=0.25)
    save(fig, "con_chart2.png")

    print("\nDone. Wrote 4 charts into images/.")


if __name__ == "__main__":
    main()
