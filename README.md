# DSC 106 Project 2: Persuasive or Deceptive Visualization

This repo contains our DSC 106 Project 2 submission on persuasive and deceptive visualization.

## Proposition

> **Since 2000, economic growth has not made countries healthier.**

Two pairs of charts are built from the same World Bank dataset. The pro pair argues the
proposition is true; the con pair argues it is false.

## Live Report

Open `index.html` in a browser, or
[view it on GitHub](https://github.com/bigmacchung/dsc106-spr26-project2-viz/blob/main/index.html).

## Course Website

[DSC 106 Project 2 instructions](https://dsc106.com/projects/project2/) ·
[Report template](https://dsc106.com/projects/project2_report.html)

## Repo Structure

- `index.html` — final project report (the deliverable)
- `generate_charts.py` — regenerates the four chart PNGs into `images/`
- `helpers/` — shared chart styling, palette, and helper functions used by `generate_charts.py`
- `data/` — World Bank Human Development Indicators (1960–2020)
- `images/` — exported chart PNGs (`pro_viz.png`, `pro_viz2.png`, `con_viz.png`, `con_viz2.png`)
- `archive/` — checkpoint PDF and superseded earlier drafts of the report and chart scripts

## One-time setup (regenerate charts)

The four chart PNGs referenced by `index.html` are produced by `generate_charts.py`. Run
this once after cloning or pulling:

```bash
cd "$(dirname "$0")"           # or just cd into the repo root
pip install pandas numpy matplotlib
python3 generate_charts.py
```

This reads from `data/World-Bank-Data-by-Indicators-master/...` and writes
`images/pro_viz.png`, `images/pro_viz2.png`, `images/con_viz.png`, `images/con_viz2.png`.
The script is deterministic, so reruns are safe.

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

For the full write-up and figures, open `index.html` in a browser.
