"""Report generation — charts (matplotlib) + a self-contained HTML/Markdown report."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: render to files, never open a window
import matplotlib.pyplot as plt  # noqa: E402

from .analyze import Analysis  # noqa: E402

ACCENT = "#4f46e5"
ACCENT_2 = "#22c55e"
ANOMALY = "#ef4444"


def render(analysis: Analysis, outdir: str | Path, title: str = "Sales Insights") -> Path:
    """Render charts and write index.html + report.md into `outdir`. Returns the HTML path."""
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    _revenue_chart(analysis, out / "revenue.png")
    _category_chart(analysis, out / "category.png")
    _growth_chart(analysis, out / "growth.png")

    html_path = out / "index.html"
    html_path.write_text(_html(analysis, title), encoding="utf-8")
    (out / "report.md").write_text(_markdown(analysis, title), encoding="utf-8")
    return html_path


def _revenue_chart(a: Analysis, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 3.6), dpi=120)
    ax.plot(a.daily.index, a.daily.to_numpy(), color=ACCENT, lw=1, alpha=0.45, label="Daily")
    ax.plot(a.moving_avg.index, a.moving_avg.to_numpy(), color=ACCENT, lw=2.2, label="7-day avg")
    if not a.anomalies.empty:
        ax.scatter(a.anomalies["date"], a.anomalies["value"], color=ANOMALY, s=36, zorder=5, label="Anomaly")
    ax.set_title("Daily revenue", fontsize=12, fontweight="bold", loc="left")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _style(ax)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _category_chart(a: Analysis, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5, 3.4), dpi=120)
    cats = a.by_category.iloc[::-1]
    ax.barh(cats.index.astype(str), cats.to_numpy(), color=ACCENT)
    ax.set_title("Revenue by category", fontsize=12, fontweight="bold", loc="left")
    _style(ax)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _growth_chart(a: Analysis, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5, 3.4), dpi=120)
    g = a.category_growth.dropna(subset=["growth_pct"])
    colors = [ACCENT_2 if v >= 0 else ANOMALY for v in g["growth_pct"]]
    ax.bar(g["category"].astype(str), g["growth_pct"], color=colors)
    ax.axhline(0, color="#9ca3af", lw=0.8)
    ax.set_title(f"Category growth (last {a.window}d vs prev)", fontsize=12, fontweight="bold", loc="left")
    ax.set_ylabel("%")
    _style(ax)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _style(ax) -> None:
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.tick_params(labelsize=8, colors="#475569")
    ax.grid(axis="y", color="#e2e8f0", lw=0.6)
    ax.set_axisbelow(True)


def _money(v: float) -> str:
    return f"${v:,.0f}"


def _html(a: Analysis, title: str) -> str:
    insights = "\n".join(f"<li>{i}</li>" for i in a.insights)
    rows = "\n".join(
        f"<tr><td>{c}</td><td>{_money(v)}</td><td>{v / a.total_revenue * 100:.1f}%</td></tr>"
        for c, v in a.by_category.items()
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ --accent: {ACCENT}; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: ui-sans-serif, system-ui, "Segoe UI", sans-serif; margin: 0;
         background: #f8fafc; color: #0f172a; }}
  .wrap {{ max-width: 940px; margin: 0 auto; padding: 32px 20px 64px; }}
  header h1 {{ margin: 0 0 4px; font-size: 1.6rem; }}
  header p {{ margin: 0; color: #64748b; font-size: .9rem; }}
  .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr));
           gap: 12px; margin: 24px 0; }}
  .kpi {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 16px; }}
  .kpi .label {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .05em; color: #64748b; }}
  .kpi .value {{ font-size: 1.4rem; font-weight: 700; margin-top: 4px; }}
  .card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px; margin: 16px 0; }}
  .card h2 {{ margin: 0 0 12px; font-size: 1rem; }}
  ul.insights {{ margin: 0; padding-left: 20px; line-height: 1.7; }}
  img {{ width: 100%; height: auto; border-radius: 8px; }}
  .grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .9rem; }}
  th, td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #eef2f7; }}
  th {{ color: #64748b; font-weight: 600; }}
  @media (max-width: 640px) {{ .grid2 {{ grid-template-columns: 1fr; }} }}
</style></head>
<body><div class="wrap">
  <header>
    <h1>{title}</h1>
    <p>{a.start:%b %d, %Y} – {a.end:%b %d, %Y} · {a.days} days</p>
  </header>

  <div class="kpis">
    <div class="kpi"><div class="label">Total revenue</div><div class="value">{_money(a.total_revenue)}</div></div>
    <div class="kpi"><div class="label">Total units</div><div class="value">{a.total_units:,}</div></div>
    <div class="kpi"><div class="label">{a.window}d growth</div><div class="value">{a.growth_pct:+.1f}%</div></div>
    <div class="kpi"><div class="label">Anomalies</div><div class="value">{len(a.anomalies)}</div></div>
  </div>

  <div class="card"><h2>Key insights</h2><ul class="insights">{insights}</ul></div>

  <div class="card"><h2>Daily revenue & trend</h2><img src="revenue.png" alt="Daily revenue chart"></div>

  <div class="grid2">
    <div class="card"><h2>By category</h2><img src="category.png" alt="Revenue by category"></div>
    <div class="card"><h2>Category growth</h2><img src="growth.png" alt="Category growth"></div>
  </div>

  <div class="card"><h2>Category breakdown</h2>
    <table><thead><tr><th>Category</th><th>Revenue</th><th>Share</th></tr></thead>
    <tbody>{rows}</tbody></table>
  </div>

  <p style="color:#94a3b8;font-size:.8rem;text-align:center;margin-top:28px">
    Generated by the Insight pipeline.</p>
</div></body></html>"""


def _markdown(a: Analysis, title: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"_{a.start:%Y-%m-%d} → {a.end:%Y-%m-%d} · {a.days} days_",
        "",
        "## Summary",
        f"- **Total revenue:** {_money(a.total_revenue)}",
        f"- **Total units:** {a.total_units:,}",
        f"- **{a.window}-day growth:** {a.growth_pct:+.1f}%",
        f"- **Anomalies:** {len(a.anomalies)}",
        "",
        "## Key insights",
    ]
    lines += [f"- {i}" for i in a.insights]
    lines += ["", "## Revenue by category", "", "| Category | Revenue | Share |", "| --- | ---: | ---: |"]
    lines += [
        f"| {c} | {_money(v)} | {v / a.total_revenue * 100:.1f}% |"
        for c, v in a.by_category.items()
    ]
    lines += ["", "![Daily revenue](revenue.png)", "", "![By category](category.png)", "", "![Growth](growth.png)", ""]
    return "\n".join(lines)
