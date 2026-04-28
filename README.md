# DSC 106 Project 2: Persuasive or Deceptive Visualization

This repo contains our DSC 106 Project 2 submission on persuasive and deceptive visualization.

## Proposition

> **Since 2000, economic growth has not made countries healthier.**

Two pairs of charts are built from the same World Bank dataset. The pro pair argues the
proposition is true; the con pair argues it is false.

## Live Report
Open `project2_report.html` in a browser, or
[view it on GitHub](https://github.com/bigmacchung/dsc106-spr26-project2-viz/blob/main/project2_report.html).

## Course Website
[DSC 106 Project 2 instructions](https://dsc106.com/projects/project2/) ·
[Report template](https://dsc106.com/projects/project2_report.html)

## Repo Structure
- `project2_report.html` — final project report (the deliverable)
- `PROJECT2_AGENT_CONTEXT.md` — agent / human handoff notes (proposition, chart decisions, checklist)
- `scripts/make_charts.py` — regenerates all four charts into `images/`
- `data/` — World Bank Human Development Indicators (1960–2020)
- `images/` — exported chart PNGs
- `archive/` — previous checkpoint PDF

## One-time setup (regenerate charts)

The four chart PNGs referenced by `project2_report.html` are produced by
`scripts/make_charts.py`. Run this once after cloning or pulling:

```bash
cd "$(dirname "$0")"           # or just cd into the repo root
pip install pandas numpy matplotlib
python3 scripts/make_charts.py
```

This reads from `data/World-Bank-Data-by-Indicators-master/...` and writes
`images/pro_chart1.png`, `images/pro_chart2.png`, `images/con_chart1.png`,
`images/con_chart2.png`. The script is deterministic, so reruns are safe.

## Team
- Maxime Chung — mac050@ucsd.edu
- Sana Gupta — svgupta@ucsd.edu
- Rose Park — sep032@ucsd.edu

## What's included
The final report includes:

- the proposition
- four charts (two pro, two con) built from the same dataset
- design decisions and rationale for each chart, scored from −2 to +2
- a reflection on the line between persuasion and deception in visualization

## Notes
For the full write-up and figures, open `project2_report.html` in a browser.
