"""Generate a deterministic sample sales dataset (stdlib only).

Run once to (re)create ``data/sample_sales.csv``. The data has a gentle upward
trend, weekly seasonality (weekends sell more), per-category baselines, and a
couple of injected anomalies so the pipeline's analysis has something to find.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
DAYS = 180
CATEGORIES = {
    # name: (baseline daily units, avg unit price)
    "Electronics": (40, 320.0),
    "Clothing": (90, 55.0),
    "Home": (60, 120.0),
    "Sports": (35, 85.0),
}

OUT = Path(__file__).resolve().parent.parent / "data" / "sample_sales.csv"


def generate() -> list[dict]:
    rng = random.Random(SEED)
    start = date(2025, 1, 1)
    rows: list[dict] = []

    for d in range(DAYS):
        day = start + timedelta(days=d)
        trend = 1.0 + d / DAYS * 0.6  # +60% growth across the window
        weekend = 1.25 if day.weekday() >= 5 else 1.0

        for cat, (base_units, price) in CATEGORIES.items():
            noise = rng.uniform(0.8, 1.2)
            units = base_units * trend * weekend * noise

            # Inject a couple of anomalies.
            if cat == "Electronics" and day == date(2025, 1, 31):
                units *= 3.2  # flash-sale spike
            if cat == "Clothing" and day == date(2025, 3, 15):
                units *= 0.25  # supply outage dip

            units = max(0, round(units))
            revenue = round(units * price * rng.uniform(0.95, 1.05), 2)
            rows.append(
                {
                    "date": day.isoformat(),
                    "category": cat,
                    "units": units,
                    "revenue": revenue,
                }
            )
    return rows


def main() -> None:
    rows = generate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "category", "units", "revenue"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
