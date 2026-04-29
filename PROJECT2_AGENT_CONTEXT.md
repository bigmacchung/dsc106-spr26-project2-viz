# PROJECT2_AGENT_CONTEXT.md

> **Single source of truth for DSC 106 Project 2.** Every agent or human working on this project should read this file FIRST before making changes, and update it after major progress. This file lives in the project repo root: `dsc106-spr26-project2-viz/`.

---

## Project goal

Build a persuasive (and gently deceptive) data visualization report for **DSC 106 Project 2** ("Persuasive or Deceptive Visualization?"). Two opposing visualizations argue both sides of a single proposition built on the World Bank Human Development Indicators dataset (1960 to 2020). The deliverable is a publicly hosted HTML page on GitHub Pages.

- **Course:** DSC 106, Spring 2026
- **Final due:** Tuesday, April 28, 2026, 11:59pm
- **Repo:** https://github.com/bigmacchung/dsc106-spr26-project2-viz
- **Local path:** `/Users/maximechung/Documents/Claude/Projects/DSC106 Spr '26 Project 1/dsc106-spr26-project2-viz`
- **Dataset:** https://github.com/light-and-salt/World-Bank-Data-by-Indicators

## Group members

- Maxime Chung — mac050@ucsd.edu
- Sana Gupta — svgupta@ucsd.edu
- Rose Park — sep032@ucsd.edu

## Final proposition (sharpened)

> **"Wealth does not buy health: getting richer has not made countries healthier."**

Defensible from both sides because both sides plot the same data; the proposition is supported or refuted purely by design choices.

## Final chart strategy (v2 — same-data version)

**Both charts plot the SAME 179 countries in 2019, with the SAME indicators (GDP per capita constant 2010 US$ on x, life expectancy at birth on y).** No country is added or dropped between sides. The earlier "different country selection per side" approach was abandoned because curating different samples is unfair framing dressed up as deception, not the kind of design rhetoric the assignment is asking for.

**Pro side (proposition TRUE — wealth is no cure):**
- Linear x-axis on GDP, which crushes 90% of countries into a vertical wall on the left.
- No fit line, no R².
- Cherry-picked outlier highlights: 4 rich-but-sick countries (Equatorial Guinea, Nigeria, Lesotho, Eswatini) in red; 4 poor-but-healthy countries (Vietnam, Nicaragua, Honduras, Bangladesh) in green.
- Slanted title: "Wealth Is No Cure: At Every Income Level, Health Outcomes Are All Over the Map."
- Mild y-axis truncation (starts at 50 not 0).

**Con side (proposition FALSE — strongest pattern in development):**
- Logarithmic x-axis on GDP, revealing the Preston curve.
- Fitted OLS regression line on log10(GDP) with R² = 0.70 disclosed in the legend.
- 95% confidence band.
- Five reference countries marked along the curve (Ethiopia, India, China, US, Japan).
- Slanted title: "The Strongest Pattern in Development: Richer Nations, Longer Lives."

**Same data. Different rhetoric.** This is the actual lesson of the assignment.

Both saved as `pro_viz.png` and `con_viz.png` in `images/`, AND embedded as base64 inside `index.html` so the HTML renders in any viewer.

## Final file structure

```
dsc106-spr26-project2-viz/
├── PROJECT2_AGENT_CONTEXT.md       <-- this file
├── index.html                       <-- final report, base64-embedded images, ~647 KB
├── images/
│   ├── pro_viz.png
│   └── con_viz.png
└── generate_charts.py               <-- reproducible chart generation
```

The `data/World-Bank-Data-by-Indicators-master/` subfolder contains the raw source CSVs and is left as-is.

## Design decisions (5 per side, scored -2 to +2)

Full text in `index.html`. Score range used: -1.5 to +1.5, calibrated.

**Pro side (v2 — same data, design rhetoric):**
| Decision | Score |
|---|---|
| Linear x-axis on GDP | -1.5 |
| Cherry-picked outlier highlights | -1.5 |
| No fit line / no R² | -1 |
| Slanted title and inset callout | -1.5 |
| Y-axis truncation at 50 | -0.5 |

**Con side (v2):**
| Decision | Score |
|---|---|
| Logarithmic x-axis on GDP | +1.5 |
| Fitted regression line with R² disclosed | +1 |
| 95% confidence band | +0.5 |
| Slanted title and inset callout | -1.5 |
| Annotated only countries along the curve | -0.5 |

## Reflection

Three paragraphs in `index.html`. Takes the position that ethical visualization is defined by whether the FRAME (country selection, time window, title) survives a critical reader's inspection, not just whether the encoding is technically true. Working test offered: "Would you defend this design choice publicly to a critical reader who will look at the data themselves?"

## Methodology and validation (`/data:validate-data` pass)

- GDP per capita: constant 2010 US$, column `average_value_GDP per capita (constant 2010 US$)` from `economy-and-growth.csv`. The earlier "Discrepancy in expenditure estimate of GDP" column bug from the checkpoint is **fixed**.
- Life expectancy: unweighted mean of male and female from `social-development.csv`. Population-weighted total LE differs by ~0.1 years; does not flip any conclusion.
- Source files have zero duplicate `(Country, Year)` keys. Inner join produces 14,982 rows across 247 entities.
- Null rates documented (22% econ, 5% social), dropped before plotting.
- All 12 chosen countries spot-checked against published World Bank figures, match to within rounding.
- Methodology section is included at the bottom of `index.html`.

## Submission checklist

- [x] Sharpened proposition
- [x] Both visualizations built and polished
- [x] Pro-side GDP column bug fixed
- [x] Coherent y-variable (life expectancy on both sides)
- [x] 5 scored design decisions per visualization, scores calibrated
- [x] 3-paragraph reflection with a real position
- [x] Methodology and validation section
- [x] Group members and UCSD emails
- [x] Source citation
- [x] HTML self-contained (base64-embedded images)
- [ ] **TODO:** Files copied into the real repo at `dsc106-spr26-project2-viz/` (see commands below)
- [ ] **TODO:** Local QA: open `index.html` in a browser, confirm both images render
- [ ] **TODO:** Commit and push via GitHub Desktop
- [ ] **TODO:** Enable GitHub Pages, verify URL renders
- [ ] **TODO:** Submit URL on Gradescope

## Known issues / things to watch

- The HTML is currently in the portfolio folder (`DSC106 Lab Opus 4.7/projects/project2/`) and needs to be copied into the real repo. The session sandbox could not write directly to the repo folder. Use the commands in the next section.
- The 5x-scaled bar in the pro-side inset is the most aggressive deceptive technique. Honestly disclosed. If a reviewer flags it as too visible, dial back to 3x in `generate_charts.py`.
- `oklch()` colors in the inline CSS render in Chrome 111+, Safari 16.4+, Firefox 113+. Older browsers will fall back gracefully on font but the accent color may not appear.

## Commands Maxime should run next

```bash
# 1. Copy the final files into the real repo (one-shot)
SRC="/Users/maximechung/Documents/Claude/Projects/DSC106 Lab Opus 4.7/projects/project2"
DST="/Users/maximechung/Documents/Claude/Projects/DSC106 Spr '26 Project 1/dsc106-spr26-project2-viz"
mkdir -p "$DST/images"
cp "$SRC/index.html" "$DST/"
cp "$SRC/PROJECT2_AGENT_CONTEXT.md" "$DST/"
cp "$SRC/generate_charts.py" "$DST/"
cp "$SRC/images/pro_viz.png" "$DST/images/"
cp "$SRC/images/con_viz.png" "$DST/images/"

# 2. QA locally before pushing
cd "$DST"
open index.html

# 3. Commit and push via GitHub Desktop (or CLI)
git add .
git commit -m "Final Project 2 submission: persuasive visualization report"
git push origin main

# 4. Enable GitHub Pages (Settings -> Pages -> Source: main / root)
# Verify the live URL:
#   https://bigmacchung.github.io/dsc106-spr26-project2-viz/

# 5. Submit that URL on Gradescope.
```

## Was the final page tested locally?

Not in the real repo yet (work was done in the agent sandbox). After running the copy commands above, run `open index.html` to confirm both visualizations render. The base64 embedding means the page is viewer-agnostic — it should also render in Quick Look, Cowork preview, email clients, and any browser.

## Repo ready to commit?

After running the copy commands above: **yes**.

## Update log

- 2026-04-28 (v1): Built two compound viz with different country selection per side. Maxime correctly pushed back: cherry-picking different countries is unfair framing, not deceptive design. The persuasive lesson of the assignment is missed.
- 2026-04-28 (v2): Rebuilt with same-data principle. Both charts now plot the SAME 179 countries in 2019 with identical indicators. Persuasion lives entirely in axis scaling, fit line, annotations, and titles.
- 2026-04-28 (v4, CURRENT): Polish pass with the SWD chart helpers Maxime uploaded.
  - Copied `chart_helpers.py`, `analytics_chart_style.mplstyle`, `chart_palette.py` into a `helpers/` subfolder of the project.
  - Rebuilt all four charts using `swd_style()`, `action_title()`, and `check_label_collisions(fix=True)`. Collision detector auto-resolved 4 collisions on Pro 1, 1 on Con 1, 0–1 on the others.
  - Pro 2 was redrawn at 10×12.5 inches with wider row spacing and the caption moved into figure space below the x-axis label, eliminating the prior caption-vs-title overlap.
  - Confirmed no scatter points are jittered. Every dot sits at its literal 2019 GDP and life-expectancy value. Documented the no-jitter check explicitly in the methodology section.
  - Updated methodology section in index.html to credit the helpers, the data-scientist subagent persona (from `awesome-claude-code-subagents-main/categories/05-data-ai/data-scientist.md`, spawned via the Agent tool), and the `/data:validate-data` skill pass.
  - Final HTML: 1.32 MB self-contained, 4 charts embedded as base64.
- 2026-04-28 (v3): Expanded to 4 visualizations (2 per side) per assignment requirement. New charts:
  - Pro 2: residuals lollipop chart that uses con side's own log-GDP regression line. Shows top 12 negative and top 12 positive residuals; collapses middle 155 countries into a single gray band. Title: "Money Explains 70% of Life Expectancy. The Other 30% Is a 20-Year Gap."
  - Con 2: small-multiples time series 1960-2019 for six anchor countries (Ethiopia, India, China, South Korea, US, Japan). Twin-axis: life expectancy in blue, GDP per capita on log secondary axis in gray. "+N yrs life" badge per panel. Title: "Six Decades, Six Countries: Every Path Bends Toward Longer Life as Wealth Climbs."
  - Pro 2 was specced by a "data-scientist" subagent persona spawned via the Agent tool, drawing from the awesome-claude-code-subagents-main folder. It honestly steel-mans the con side by using their regression line, which earned it the only +2 score in the project.
  - Con 2 hand-picks six poster-child countries (the most deceptive move on the con side, scored -2 in its country-selection decision and called out explicitly in the reflection).
  - Total 20 design decisions (5 per chart), score range -2 to +2, calibrated.
  - Rewrote reflection to single out the most-ethical viz (pro 2) and least-ethical viz (con 2) by name, demonstrating that the line between persuasion and deception cuts THROUGH this project's own work.
  - All four charts embedded as base64 in index.html. Final HTML is 1.3 MB self-contained.
