# PROJECT2_AGENT_CONTEXT.md

> Single source of truth for the **DSC 106 Project 2: Persuasive or Deceptive Visualization** assignment.
> Every Claude / agent session must read this file before doing any work, and update it after major progress.

---

## 1. Project identity

- **Course:** DSC 106 (Spring '26)
- **Assignment:** Project 2 — Persuasive Visualization
- **Repo:** `https://github.com/bigmacchung/dsc106-spr26-project2-viz`
- **Local path:** `/Users/maximechung/Documents/Claude/Projects/DSC106 Spr '26 Project 1/dsc106-spr26-project2-viz`
- **Report file:** `project2_report.html` (live deliverable)
- **NOT a portfolio project.** Do **not** copy this work into the personal-website folder
  (`/Users/maximechung/Documents/Claude/Projects/DSC106 Lab Opus 4.7`). That folder is for a separate
  portfolio assignment.

## 2. Group members (preserve)

| Name          | Email             |
| ------------- | ----------------- |
| Maxime Chung  | mac050@ucsd.edu   |
| Sana Gupta    | svgupta@ucsd.edu  |
| Rose Park     | sep032@ucsd.edu   |

Source of truth: `archive/project2_checkpoint_v1.pdf` and the previous checkpoint writeup
(`project2_checkpoint_writeup.md` in the related desktop folder). Do not invent new emails.

## 3. Final proposition

> **"Since 2000, economic growth has not made countries healthier."**

This is the sharpened version of the checkpoint proposition. It is intentionally short so a reader
who has not seen the data can understand it in 5 seconds. The pro side argues this is **true**;
the con side argues it is **false**.

## 4. Dataset

World Bank Human Development Indicators, 1960–2020. Files we touch:

- `data/World-Bank-Data-by-Indicators-master/economy-and-growth/economy-and-growth.csv`
  - Indicator: `GDP per capita (constant 2010 US$)` (preferred; "real" GDP per capita)
  - Fallback: `GDP per capita (current US$)` if constant-2010 series is sparse
- `data/World-Bank-Data-by-Indicators-master/health/health.csv`
  - Indicator: `Life expectancy at birth, total (years)`
  - Indicator: `Population ages 65 and above (% of total population)` (con-side proxy)

## 5. Final chart list (4 charts)

The pro and con sides use **the same Y-variable (life expectancy)** for the scatter charts so they
are directly comparable. The con side keeps `% age 65+` for the dual-axis time series only, where
the proxy substitution is documented as a deliberate deceptive technique.

### Pro side — argues the proposition is TRUE ("growth ≠ health")

1. **Pro Chart 1 — `images/pro_chart1.png`**
   Global scatter of **GDP per capita (constant 2010 US$, log x-axis)** vs **life expectancy at birth**,
   most recent year per country (2018–2020). Intentionally slanted title:
   *"Economic Growth Does Not Reliably Improve Life Expectancy"*.
   Deceptive devices: log x-axis (compresses income gradient), slanted title, Y-axis cropped from
   45–85 (visually flattens the slope), regression line omitted.

2. **Pro Chart 2 — `images/pro_chart2.png`**
   Filtered middle-income band (GDP per capita 5,000–25,000 USD), with the seven lowest-life-expectancy
   countries highlighted in red and labeled. Title: *"Even Among Wealthier Countries, Wealth Does Not
   Guarantee Longer Lives."*
   Deceptive devices: cherry-picked one-sided highlight (no equivalent green dots for top performers),
   "wealthier countries" label is misleading (5k–25k is middle-income), filter cut excludes the
   countries where the relationship is strongest.

### Con side — argues the proposition is FALSE ("growth ⇒ health")

3. **Con Chart 3 — `images/con_chart1.png`**
   Dual-axis line chart for **China, 2000–2020**: GDP per capita (constant 2010 US$, left axis, blue)
   vs **% population aged 65+** (right axis, red). Title: *"The Wealth Cure: Economic Growth Drives
   Longer, Healthier Lives in China."*
   Deceptive devices: dual-axis synchronization (each axis is independently scaled to make the lines
   appear to track), proxy substitution (% age 65+ is driven as much by falling birth rates as by
   improved survival), single cherry-picked country.

4. **Con Chart 4 — `images/con_chart2.png`**
   Global annual-mean scatter, 2000–2020: mean GDP per capita (constant 2010 US$) across all countries
   vs mean **life expectancy at birth** across all countries, with a fitted regression line and R²
   reported. Title: *"Globally, Wealth and Health Rise Together."*
   Deceptive devices: aggregation washes out within- and between-country variance, regression on
   annual means inflates R² vs the messier country-level relationship, the time-confounded
   correlation is presented as causal.

> Why life expectancy on both pro charts and con chart 4 (matching Y), but % 65+ on con chart 3:
> matching the Y-variable in three of four charts keeps the comparison fair and prevents the project
> from looking like a mismatch bug. The single use of % 65+ on the China dual-axis chart is the
> documented "proxy substitution" deception — and we **explain it honestly** in that chart's design
> decisions section so the deception is auditable rather than hidden.

## 6. Bug fix from prior agent runs

- **Pro side previously used a "Discrepancy" GDP column** that was a calculation bug, not a
  deceptive choice. The fix is to use **`GDP per capita (constant 2010 US$)` directly** from the
  World Bank `economy-and-growth.csv` for all four charts. The log-axis compression on Pro Chart 1
  remains as a real deceptive technique — that is a *visual* choice, not a data bug.

## 7. Design-decision scoring

Each chart gets 3–5 design decisions, each scored from **−2 to +2** (−2 = severely misleading,
+2 = strongly persuasive in an honest way). Use a real spread; do not flatten everything to ±2 or 0.
Include a 2–3 sentence rationale per decision. See `project2_report.html` for the final list.

## 8. Reflection

2–3 paragraphs. Must cover:

- What was easy / hard about building two opposing charts from the same data.
- What surprised us (e.g. how much a slanted title changes a clean chart's story).
- Our working definition of ethical visualization.
- Where we draw the line between persuasive and misleading.

Final paragraph should take a real position (not a vague "both sides have a point") on the line
between persuasion and deception.

## 9. File layout

```
dsc106-spr26-project2-viz/
├── PROJECT2_AGENT_CONTEXT.md          ← this file
├── README.md
├── project2_report.html               ← deliverable
├── images/
│   ├── pro_chart1.png
│   ├── pro_chart2.png
│   ├── con_chart1.png
│   └── con_chart2.png
├── scripts/
│   └── make_charts.py                 ← chart-generation script
├── data/                              ← World Bank Data by Indicators (master)
├── archive/                           ← previous checkpoint PDF
└── resources/                         ← test_img.png placeholder (kept)
```

## 10. Submission checklist

- [x] Sharpened proposition documented
- [x] Group members + UCSD emails preserved
- [x] Real GDP per capita (constant 2010 US$) used everywhere (bug fix from prior agent run)
- [x] Chart-generation script committed to repo (`scripts/make_charts.py`)
- [x] `project2_report.html` populated from the DSC 106 template
- [x] Each chart has 3–5 design decisions (5/4/5/5), each scored −2…+2, with rationale
- [x] Reflection takes a real position on ethical visualization
- [x] README.md updated with proposition, team, repo structure, and one-time setup
- [ ] **Run `python3 scripts/make_charts.py` once to materialize the four PNGs into `images/`** ← user action
- [ ] Repo committed and pushed via GitHub Desktop (manual, owner action)
- [ ] Page opened locally in a browser to spot any rendering issue (manual review)

## 11. Known issues / open items for human review

- **Charts must be generated locally.** This scheduled session ran in a sandbox that cannot
  write binary PNGs to the repo path. The chart-generation script lives at
  `scripts/make_charts.py` and is committed to the repo. After pulling, run it once:

  ```bash
  cd "/Users/maximechung/Documents/Claude/Projects/DSC106 Spr '26 Project 1/dsc106-spr26-project2-viz"
  pip install pandas numpy matplotlib  # if not already installed
  python3 scripts/make_charts.py
  ```

  This produces `images/pro_chart1.png`, `images/pro_chart2.png`, `images/con_chart1.png`,
  `images/con_chart2.png`. Until then, the report HTML will show four broken-image icons.
  We verified the script runs end-to-end on a fresh checkout of the data and produces all
  four PNGs (≈150 KB each, 1900×1200 px @ 200 dpi).

- **Con-side dual-axis chart still uses % age 65+ rather than life expectancy.** This is the
  documented proxy-substitution deception in the writeup. If the grader prefers full Y-variable
  consistency across all four charts, swap to a dual-axis with life expectancy on the right
  axis (`SP.DYN.LE00.IN`) and remove the proxy-substitution row from Con Chart 1's design
  decision table.

- **Group member ordering on the page: Maxime, Sana, Rose.** Names/emails sourced from the prior
  checkpoint writeup. Reconfirm with team if anything has changed.

- **Resolution.** The chart script writes PNGs at ~1900×1200 px, 200 dpi. Should look crisp on
  retina screens. File sizes are ~150 KB each, fine for git.

## 12. Commands Maxime should run next (manual)

```bash
cd "/Users/maximechung/Documents/Claude/Projects/DSC106 Spr '26 Project 1/dsc106-spr26-project2-viz"

# 1. Materialize the four PNG charts referenced by the HTML report
pip install pandas numpy matplotlib   # if not already installed
python3 scripts/make_charts.py        # writes 4 PNGs into images/

# 2. Spot-check the report
open project2_report.html             # default browser

# 3. Confirm and push
git status                             # see what changed
# Then commit + push via GitHub Desktop (or `git add -A && git commit -m "..." && git push`)
```

## 13. Session log

- **2026-04-22:** Checkpoint v1 PDF saved to `archive/`. Initial proposition drafted
  ("Since 2000, economic growth has not consistently improved health outcomes across
  countries"). Pro side (chart 1 GDP-vs-LE scatter, chart 2 middle-income filtered), con
  side (chart 1 China dual-axis, chart 2 global annual means).

- **2026-04-28 (this scheduled run, ~02:20 PT):**
  - Read prior checkpoint PDF and writeup; pulled team / proposition.
  - Sharpened proposition to "Since 2000, economic growth has not made countries healthier."
  - Picked life expectancy as the shared Y-variable across pro charts and con chart 2; kept
    % age 65+ on the China dual-axis (con chart 1) as the documented proxy-substitution
    deception.
  - Fixed the GDP-column bug: all four charts now use `GDP per capita (constant 2010 US$)`
    (`NY.GDP.PCAP.KD`) — not the bogus "Discrepancy in expenditure estimate of GDP" column.
  - Generated all four charts in the sandbox; verified n=199 country scatter, China 2000–2020
    dual-axis, and global annual-means R² = 0.86.
  - Wrote `scripts/make_charts.py` into the repo as the reproducible source. This script
    reads from the local `data/World-Bank-Data-by-Indicators-master/` folder and writes the
    four PNGs into `images/`.
  - Populated `project2_report.html` from the DSC 106 template: proposition, four figures,
    19 scored design decisions (mix of −2, −1, 0, +1, +2), three-paragraph reflection that
    takes a position on where persuasion ends and deception begins.
  - Updated `README.md` and this handoff file. **Open item:** Maxime needs to run
    `python3 scripts/make_charts.py` once to materialize the PNGs into `images/` because
    this scheduled session could not write binary files into the repo.
