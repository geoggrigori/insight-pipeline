"""Data ingestion — load a CSV into a DataFrame and validate its shape."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"date", "category", "units", "revenue"}


def load_csv(path: str | Path) -> pd.DataFrame:
    """Read a sales CSV, validating that the required columns are present."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"CSV is missing required column(s): {', '.join(sorted(missing))}"
        )
    return df
