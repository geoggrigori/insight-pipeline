"""Optional live data source: the free Frankfurter FX API (no API key required).

Demonstrates ingesting from a public HTTP API and mapping it into the pipeline's
``date / category / units / revenue`` schema (here: currency pair / 1 / rate).
The analysis (trend, moving average, anomalies, growth) is fully meaningful on a
rate series.
"""

from __future__ import annotations

import json
import urllib.request
from datetime import date, timedelta

import pandas as pd

BASE_URL = "https://api.frankfurter.app"


def fetch_frankfurter(
    days: int = 180,
    base: str = "EUR",
    symbols: tuple[str, ...] = ("USD", "GBP", "BRL", "JPY"),
) -> pd.DataFrame:
    end = date.today()
    start = end - timedelta(days=days)
    url = f"{BASE_URL}/{start.isoformat()}..{end.isoformat()}?from={base}&to={','.join(symbols)}"

    with urllib.request.urlopen(url, timeout=20) as resp:  # noqa: S310 (trusted host)
        payload = json.loads(resp.read().decode())

    rows = [
        {"date": day, "category": f"{base}/{sym}", "units": 1, "revenue": rate}
        for day, rates in payload.get("rates", {}).items()
        for sym, rate in rates.items()
    ]
    if not rows:
        raise RuntimeError("No data returned from the Frankfurter API.")
    return pd.DataFrame(rows)
