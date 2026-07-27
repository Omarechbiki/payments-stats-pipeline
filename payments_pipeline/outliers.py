"""Outlier detection on quarter-on-quarter growth of each payments series."""

from __future__ import annotations

import pandas as pd

SERIES_KEYS = ["country", "instrument"]
GROWTH_COLUMN = "qoq_growth"
ZSCORE_COLUMN = "growth_zscore"


def flag_outliers(
    df: pd.DataFrame,
    value_column: str = "transactions_millions",
    threshold: float = 3.5,
) -> pd.DataFrame:
    """Flag anomalous quarter-on-quarter movements within each series.

    A robust z-score (median/MAD) is used instead of mean/standard deviation so a
    few extreme quarters cannot inflate the spread and hide genuine anomalies.
    """
    ordered = df.sort_values([*SERIES_KEYS, "period"]).copy()
    ordered[GROWTH_COLUMN] = ordered.groupby(SERIES_KEYS)[value_column].pct_change()
    ordered[ZSCORE_COLUMN] = ordered.groupby(SERIES_KEYS)[GROWTH_COLUMN].transform(
        _robust_zscore
    )
    ordered["is_outlier"] = ordered[ZSCORE_COLUMN].abs() > threshold
    return ordered


def _robust_zscore(values: pd.Series) -> pd.Series:
    median = values.median()
    median_abs_deviation = (values - median).abs().median()
    if pd.isna(median_abs_deviation) or median_abs_deviation == 0:
        return pd.Series(0.0, index=values.index)
    # 0.6745 rescales the MAD to be comparable to a standard-deviation z-score.
    return 0.6745 * (values - median) / median_abs_deviation
