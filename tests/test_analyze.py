import math

import pandas as pd

from insight.analyze import (
    analyze,
    category_growth,
    detect_anomalies,
    moving_average,
    period_growth,
)


def test_moving_average_trailing_window():
    s = pd.Series([1, 2, 3, 4, 5])
    ma = moving_average(s, window=3)
    assert list(ma) == [1.0, 1.5, 2.0, 3.0, 4.0]


def test_period_growth_doubles():
    s = pd.Series([10, 10, 20, 20])
    # last 2 (=40) vs previous 2 (=20) -> +100%
    assert period_growth(s, window=2) == 100.0


def test_period_growth_nan_without_baseline():
    assert math.isnan(period_growth(pd.Series([5]), window=2))


def test_detect_anomalies_flags_spike():
    s = pd.Series([10.0] * 20 + [100.0], index=pd.date_range("2025-01-01", periods=21))
    flagged = detect_anomalies(s, z=2.5)
    assert len(flagged) == 1
    assert flagged.iloc[0]["value"] == 100.0
    assert flagged.iloc[0]["z"] > 2.5


def test_detect_anomalies_none_when_flat():
    s = pd.Series([10.0] * 10, index=pd.date_range("2025-01-01", periods=10))
    assert detect_anomalies(s, z=2.5).empty


def test_category_growth_ranks_winners_and_losers():
    dates = pd.to_datetime(
        ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"]
    )
    rows = []
    # Category A: previous window (days 1-2) = 20, recent (days 3-4) = 40 -> +100%
    # Category B: previous = 40, recent = 20 -> -50%
    for d, a, b in zip(dates, [10, 10, 20, 20], [20, 20, 10, 10]):
        rows.append({"date": d, "category": "A", "units": 1, "revenue": a})
        rows.append({"date": d, "category": "B", "units": 1, "revenue": b})
    df = pd.DataFrame(rows)

    g = category_growth(df, window=2)
    assert list(g["category"]) == ["A", "B"]  # sorted by growth desc
    assert g.iloc[0]["growth_pct"] == 100.0
    assert g.iloc[-1]["growth_pct"] == -50.0


def test_analyze_end_to_end_small():
    dates = pd.to_datetime(["2025-01-01", "2025-01-02"])
    df = pd.DataFrame(
        {
            "date": list(dates) * 2,
            "category": ["A", "A", "B", "B"],
            "units": [1, 1, 1, 1],
            "revenue": [100.0, 150.0, 50.0, 50.0],
        }
    )
    a = analyze(df, window=1)
    assert a.total_revenue == 350.0
    assert a.days == 2
    assert a.by_category.loc["A"] == 250.0
    assert isinstance(a.insights, list) and len(a.insights) >= 3
