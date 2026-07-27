"""Aggregate national payments series into euro-area totals."""

from __future__ import annotations

import pandas as pd

AGGREGATE_COLUMNS = ["transactions_millions", "value_eur_billions"]


def compile_euro_area_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Sum national series into one euro-area total per instrument and period."""
    aggregates = df.groupby(["period", "instrument"], as_index=False)[
        AGGREGATE_COLUMNS
    ].sum()
    return aggregates.sort_values(["period", "instrument"]).reset_index(drop=True)
