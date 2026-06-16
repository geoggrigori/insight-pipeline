"""Analysis — turn cleaned data into metrics and human-readable insights."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .transform import daily_revenue, revenue_by_category


# --- Pure, individually-testable analysis functions ---------------------------

def moving_average(series: pd.Series, window: int = 7) -> pd.Series:
    """Trailing moving average; early points average what's available so far."""
    return series.rolling(window, min_periods=1).mean()


def period_growth(series: pd.Series, window: int = 30) -> float:
    """Percent change of the last `window` days vs the previous `window` days.

    Falls back to half the series when there isn't enough history. Returns NaN
    if the baseline period sums to zero.
    """
    n = len(series)
    if n < 2:
        return float("nan")
    w = min(window, n // 2)
    if w == 0:
        return float("nan")
    recent = series.iloc[-w:].sum()
    previous = series.iloc[-2 * w : -w].sum()
    if previous == 0:
        return float("nan")
    return (recent - previous) / previous * 100.0


def detect_anomalies(series: pd.Series, z: float = 2.5) -> pd.DataFrame:
    """Flag points whose z-score exceeds `z`. Returns date/value/z, biggest first."""
    if len(series) < 3:
        return pd.DataFrame(columns=["date", "value", "z"])
    std = series.std(ddof=0)
    if std == 0:
        return pd.DataFrame(columns=["date", "value", "z"])
    zscores = (series - series.mean()) / std
    flagged = zscores[zscores.abs() >= z]
    out = pd.DataFrame(
        {"date": flagged.index, "value": series.loc[flagged.index].to_numpy(), "z": flagged.to_numpy()}
    )
    return out.reindex(out["z"].abs().sort_values(ascending=False).index).reset_index(drop=True)


def category_growth(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """Per-category revenue for the last vs previous `window` days, with growth %."""
    if df.empty:
        return pd.DataFrame(columns=["category", "recent", "previous", "growth_pct"])
    end = df["date"].max()
    recent_start = end - pd.Timedelta(days=window - 1)
    prev_start = recent_start - pd.Timedelta(days=window)

    recent = df[df["date"] >= recent_start]
    previous = df[(df["date"] >= prev_start) & (df["date"] < recent_start)]

    r = recent.groupby("category")["revenue"].sum()
    p = previous.groupby("category")["revenue"].sum()
    out = pd.DataFrame({"recent": r, "previous": p}).fillna(0.0)
    out["growth_pct"] = out.apply(
        lambda row: (row["recent"] - row["previous"]) / row["previous"] * 100.0
        if row["previous"] > 0
        else float("nan"),
        axis=1,
    )
    return out.sort_values("growth_pct", ascending=False).reset_index()


# --- Orchestration ------------------------------------------------------------

@dataclass
class Analysis:
    total_revenue: float
    total_units: int
    start: pd.Timestamp
    end: pd.Timestamp
    days: int
    window: int
    daily: pd.Series
    moving_avg: pd.Series
    by_category: pd.Series
    growth_pct: float
    category_growth: pd.DataFrame
    anomalies: pd.DataFrame
    best_day: tuple
    worst_day: tuple
    insights: list[str]


def _money(v: float) -> str:
    return f"${v:,.0f}"


def analyze(df: pd.DataFrame, window: int = 30, anomaly_z: float = 2.5) -> Analysis:
    if df.empty:
        raise ValueError("No data to analyze after cleaning.")

    daily = daily_revenue(df)
    by_cat = revenue_by_category(df)
    ma = moving_average(daily, 7)
    growth = period_growth(daily, window)
    cat_growth = category_growth(df, window)
    anomalies = detect_anomalies(daily, anomaly_z)

    best_day = (daily.idxmax(), float(daily.max()))
    worst_day = (daily.idxmin(), float(daily.min()))

    insights = _build_insights(df, daily, by_cat, growth, window, cat_growth, anomalies, best_day, worst_day)

    return Analysis(
        total_revenue=float(df["revenue"].sum()),
        total_units=int(df["units"].sum(skipna=True)),
        start=daily.index.min(),
        end=daily.index.max(),
        days=len(daily),
        window=window,
        daily=daily,
        moving_avg=ma,
        by_category=by_cat,
        growth_pct=growth,
        category_growth=cat_growth,
        anomalies=anomalies,
        best_day=best_day,
        worst_day=worst_day,
        insights=insights,
    )


def _build_insights(df, daily, by_cat, growth, window, cat_growth, anomalies, best_day, worst_day) -> list[str]:
    out: list[str] = []
    total = float(df["revenue"].sum())
    out.append(
        f"Total revenue of {_money(total)} across {len(daily)} days "
        f"({daily.index.min():%Y-%m-%d} → {daily.index.max():%Y-%m-%d})."
    )

    if pd.notna(growth):
        direction = "up" if growth >= 0 else "down"
        out.append(
            f"Revenue is {direction} {abs(growth):.1f}% over the last {window} days "
            f"vs the previous {window}."
        )

    if not by_cat.empty:
        top = by_cat.index[0]
        share = by_cat.iloc[0] / total * 100 if total else 0
        out.append(f"Top category is {top} ({_money(by_cat.iloc[0])}, {share:.0f}% of revenue).")

    growers = cat_growth.dropna(subset=["growth_pct"])
    if not growers.empty:
        fastest = growers.iloc[0]
        slowest = growers.iloc[-1]
        out.append(f"Fastest-growing category: {fastest['category']} ({fastest['growth_pct']:+.1f}%).")
        if slowest["category"] != fastest["category"]:
            out.append(f"Weakest category: {slowest['category']} ({slowest['growth_pct']:+.1f}%).")

    out.append(
        f"Best day: {best_day[0]:%Y-%m-%d} ({_money(best_day[1])}); "
        f"slowest day: {worst_day[0]:%Y-%m-%d} ({_money(worst_day[1])})."
    )

    if not anomalies.empty:
        n = len(anomalies)
        first = anomalies.iloc[0]
        kind = "spike" if first["z"] > 0 else "dip"
        out.append(
            f"Detected {n} anomalous day(s); biggest is a {kind} on "
            f"{first['date']:%Y-%m-%d} ({_money(first['value'])}, z={first['z']:+.1f})."
        )
    else:
        out.append("No statistically significant anomalies detected.")

    return out
