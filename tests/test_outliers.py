import pandas as pd

from payments_pipeline import outliers


def _series_with_spike() -> pd.DataFrame:
    periods = [f"2020Q{q}" for q in range(1, 5)] + [f"2021Q{q}" for q in range(1, 5)]
    transactions = [100, 101, 99, 102, 100, 101, 300, 101]  # spike in 2021Q3
    return pd.DataFrame(
        {
            "period": periods,
            "country": ["DE"] * 8,
            "instrument": ["card_payments"] * 8,
            "transactions_millions": transactions,
            "value_eur_billions": [value * 0.05 for value in transactions],
        }
    )


def test_flags_an_obvious_spike():
    flagged = outliers.flag_outliers(_series_with_spike())
    spike = flagged.loc[flagged["period"] == "2021Q3", "is_outlier"].iloc[0]
    assert bool(spike) is True


def test_flat_series_has_no_outliers():
    panel = _series_with_spike()
    panel["transactions_millions"] = 100
    flagged = outliers.flag_outliers(panel)
    assert not flagged["is_outlier"].any()
