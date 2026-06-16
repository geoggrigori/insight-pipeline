"""Command-line interface: `python -m insight run [...]`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .analyze import analyze
from .ingest import load_csv
from .report import render
from .transform import clean

DEFAULT_INPUT = Path(__file__).resolve().parent.parent / "data" / "sample_sales.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="insight",
        description="Ingest data, analyze it, and generate an insights report.",
    )
    parser.add_argument("--version", action="version", version=f"insight {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run the full pipeline")
    run.add_argument("--input", "-i", default=str(DEFAULT_INPUT), help="Input CSV path")
    run.add_argument(
        "--source",
        choices=["csv", "frankfurter"],
        default="csv",
        help="Data source (default: csv). 'frankfurter' fetches live FX rates.",
    )
    run.add_argument("--out", "-o", default="report", help="Output directory")
    run.add_argument("--window", "-w", type=int, default=30, help="Comparison window in days")
    run.add_argument("--z", type=float, default=2.5, help="Anomaly z-score threshold")
    run.add_argument("--title", default="Sales Insights", help="Report title")
    return parser


def main(argv: list[str] | None = None) -> int:
    # Ensure Unicode (→, •, ✅) prints on consoles with a legacy code page (Windows).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except (AttributeError, OSError):
            pass

    args = build_parser().parse_args(argv)
    if args.command == "run":
        return _run(args)
    return 0


def _run(args: argparse.Namespace) -> int:
    if args.source == "frankfurter":
        from .sources import fetch_frankfurter

        print("Fetching FX rates from the Frankfurter API…")
        df = fetch_frankfurter()
        title = "FX Rate Insights (EUR base)" if args.title == "Sales Insights" else args.title
    else:
        print(f"Loading {args.input} …")
        df = load_csv(args.input)
        title = args.title

    df = clean(df)
    analysis = analyze(df, window=args.window, anomaly_z=args.z)
    out_path = render(analysis, args.out, title=title)

    print("\nKey insights:")
    print("\n".join(f"  • {i}" for i in analysis.insights))
    print(f"\n✅ Report written to {out_path}")
    return 0
