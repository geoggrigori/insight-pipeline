import pandas as pd

from insight.transform import clean, daily_revenue, revenue_by_category


def _raw():
    return pd.DataFrame(
        {
            "date": ["2025-01-01", "2025-01-03", "2025-01-01", "bad-date"],
            "category": ["A", "B", "B", "A"],
            "units": [1, 2, 3, 4],
            "revenue": [100.0, 200.0, 50.0, -5.0],
        }
    )


def test_clean_coerces_and_drops_bad_rows():
    df = clean(_raw())
    # The unparseable date and the negative revenue rows are dropped.
    assert len(df) == 3
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert (df["revenue"] >= 0).all()
    # Sorted chronologically.
    assert df["date"].is_monotonic_increasing


def test_daily_revenue_sums_and_fills_gaps():
    df = clean(_raw())
    daily = daily_revenue(df)
    # 2025-01-01 has 100 + 50; 01-02 is missing -> filled 0; 01-03 has 200.
    assert daily.loc["2025-01-01"] == 150.0
    assert daily.loc["2025-01-02"] == 0.0
    assert daily.loc["2025-01-03"] == 200.0
    assert len(daily) == 3  # continuous date range


def test_revenue_by_category_sorted_desc():
    df = clean(_raw())
    by_cat = revenue_by_category(df)
    assert list(by_cat.index) == ["B", "A"]  # B=250, A=100
    assert by_cat.iloc[0] == 250.0
