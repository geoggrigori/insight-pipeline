<!-- ══════════════════════════ TITLE ══════════════════════════ -->
<div align="center">
  <img src="docs/title-banner.svg" width="100%" alt="Insight"/>
</div>

<br/>

<!-- ══════════════════════ IDIOMAS / LANGUAGES ══════════════════════ -->
<div align="center">
<a href="README.md"><img src="https://img.shields.io/badge/Português-555555?style=for-the-badge" alt="Português"/></a>
<a href="README.en.md"><img src="https://img.shields.io/badge/English-1987F0?style=for-the-badge" alt="English"/></a>
<a href="README.es.md"><img src="https://img.shields.io/badge/Español-555555?style=for-the-badge" alt="Español"/></a>
</div>

<br/>

<div align="center">
<img src="https://github.com/geoggrigori/insight-pipeline/actions/workflows/ci.yml/badge.svg" alt="CI"/>
<br/>
<img src="https://img.shields.io/badge/Python_3.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="python"/>
<img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas"/>
<img src="https://img.shields.io/badge/matplotlib-11557C?style=flat-square" alt="matplotlib"/>
<img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="pytest"/>
<img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="actions"/>
</div>

<div align="center">
<a href="#about"><img src="https://img.shields.io/badge/▸_ABOUT-1987F0?style=for-the-badge" alt="about"/></a>
<a href="#what-it-does"><img src="https://img.shields.io/badge/▸_WHAT_IT_DOES-000000?style=for-the-badge" alt="whatitdoes"/></a>
<a href="#architecture"><img src="https://img.shields.io/badge/▸_ARCHITECTURE-1987F0?style=for-the-badge" alt="architecture"/></a>
<a href="#usage"><img src="https://img.shields.io/badge/▸_USAGE-000000?style=for-the-badge" alt="usage"/></a>
<a href="#automation"><img src="https://img.shields.io/badge/▸_AUTOMATION-1987F0?style=for-the-badge" alt="automation"/></a>
</div>

<br/>

> 💡 **One command, CSV to report.** `python -m insight run` generates the HTML dashboard using the bundled sample dataset.

<div align="center">
  <img src="docs/revenue.png" width="100%" alt="Insight — daily revenue and 7-day trend, anomalies in red"/>
</div>

## About

**Insight** is a small but complete data pipeline: it ingests a CSV (or fetches a live public API), cleans and aggregates the data, detects trends and anomalies, and renders an HTML/Markdown report with charts — all from one command.

## What it does

- **Ingest** — load a CSV (validated schema) or fetch live FX rates from a free public API (no key).
- **Transform** — coerce types, drop bad rows, fill date gaps, aggregate to a daily series and per-category totals (pandas).
- **Analyze** — 7-day moving average trend, period-over-period growth, z-score anomaly detection, per-category growth ranking, best/worst day, and plain-English insights generated from the numbers.
- **Report** — matplotlib charts + a self-contained HTML dashboard + a Markdown report.

**Example output:**
```
• Total revenue of $7,027,351 across 180 days (2025-01-01 → 2025-06-29).
• Revenue is up 10.0% over the last 30 days vs the previous 30.
• Top category is Electronics ($3,217,331, 46% of revenue).
• Fastest-growing category: Sports (+12.8%).
• Detected 2 anomalous day(s); biggest is a spike on 2025-01-31 (z=+2.8).
```

| Revenue by category | Category growth |
|:---:|:---:|
| ![By category](docs/category.png) | ![Growth](docs/growth.png) |

## Architecture

<div align="center">
  <img src="docs/architecture.svg" width="100%" alt="Architecture"/>
</div>

| Module | Responsibility |
|---|---|
| `insight/ingest.py` | Load + validate the input CSV |
| `insight/transform.py` | Clean, type-coerce, aggregate (daily series, by category) |
| `insight/analyze.py` | Moving average, growth, z-score anomalies, category movers, insights |
| `insight/report.py` | Render charts and the HTML/Markdown report |
| `insight/sources.py` | Optional live source (Frankfurter FX API) |
| `insight/cli.py` | `python -m insight run` command-line interface |

## Usage

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m insight run
python -m insight run --input data/sample_sales.csv --out report --window 30 --z 2.5
python -m insight run --source frankfurter   # live public dataset
```

Open `report/index.html` to view the dashboard.

**Tests:**
```bash
pytest -q
```

## Automation

`.github/workflows/report.yml` regenerates the report **every Monday** (and on demand), uploading it as a downloadable artifact — scheduled analytics with no infrastructure. `ci.yml` runs the test suite on every push.

## License

[MIT](LICENSE).

<div align="center">
  <img src="https://file.loading.io/color/feature/thumb/Blues-8.png?" width="100%" height="10px" alt="divider"/>
</div>

<p align="center"><sub>Built by <strong><a href="https://github.com/geoggrigori">Grigori</a></strong> · 2026</sub></p>
