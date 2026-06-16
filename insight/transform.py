"""Cleaning and aggregation."""

from __future__ import annotations

import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce types, drop unusable rows, and sort chronologically.

    - Parses ``date`` to datetime and numeric columns to numbers.
    - Drops rows with no date/revenue and any negative revenue.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["category"] = df["category"].astype("string").fillna("Unknown")

    df = df.dropna(subset=["date", "revenue"])
    df = df[df["revenue"] >= 0]
    return df.sort_values("date").reset_index(drop=True)


def daily_revenue(df: pd.DataFrame) -> pd.Series:
    """Total revenue per day, indexed by date (continuous, gaps filled with 0)."""
    series = df.groupby("date")["revenue"].sum().sort_index()
    if series.empty:
        return series
    full = pd.date_range(series.index.min(), series.index.max(), freq="D")
    return series.reindex(full, fill_value=0.0)


def revenue_by_category(df: pd.DataFrame) -> pd.Series:
    """Total revenue per category, highest first."""
    return df.groupby("category")["revenue"].sum().sort_values(ascending=False)
