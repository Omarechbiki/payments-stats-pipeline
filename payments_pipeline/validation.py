"""Data-quality checks for the payments panel."""

from __future__ import annotations

import pandas as pd

KEY_COLUMNS = ["period", "country", "instrument"]
NUMERIC_COLUMNS = ["transactions_millions", "value_eur_billions"]
REQUIRED_COLUMNS = KEY_COLUMNS + NUMERIC_COLUMNS


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Run every data-quality check and return one row per issue found."""
    checks = [
        _check_missing_columns,
        _check_null_values,
        _check_negative_values,
        _check_duplicate_keys,
        _check_panel_completeness,
    ]
    issues = [issue for check in checks for issue in check(df)]
    return pd.DataFrame(issues, columns=["check", "detail"])


def _check_missing_columns(df: pd.DataFrame) -> list[dict]:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if not missing:
        return []
    return [{"check": "missing_columns", "detail": ", ".join(missing)}]


def _check_null_values(df: pd.DataFrame) -> list[dict]:
    present = [column for column in REQUIRED_COLUMNS if column in df.columns]
    null_counts = df[present].isna().sum()
    return [
        {"check": "null_values", "detail": f"{column}: {count} nulls"}
        for column, count in null_counts.items()
        if count > 0
    ]


def _check_negative_values(df: pd.DataFrame) -> list[dict]:
    issues = []
    for column in NUMERIC_COLUMNS:
        if column in df.columns and (df[column] < 0).any():
            negatives = int((df[column] < 0).sum())
            issues.append(
                {"check": "negative_values", "detail": f"{column}: {negatives} rows"}
            )
    return issues


def _check_duplicate_keys(df: pd.DataFrame) -> list[dict]:
    if not set(KEY_COLUMNS).issubset(df.columns):
        return []
    duplicates = int(df.duplicated(subset=KEY_COLUMNS).sum())
    if duplicates == 0:
        return []
    return [{"check": "duplicate_keys", "detail": f"{duplicates} duplicate rows"}]


def _check_panel_completeness(df: pd.DataFrame) -> list[dict]:
    """Every country and instrument should report in every period."""
    if not set(KEY_COLUMNS).issubset(df.columns):
        return []
    expected = (
        df["period"].nunique() * df["country"].nunique() * df["instrument"].nunique()
    )
    observed = len(df.drop_duplicates(subset=KEY_COLUMNS))
    gap = expected - observed
    if gap <= 0:
        return []
    return [{"check": "incomplete_panel", "detail": f"{gap} missing series-periods"}]
