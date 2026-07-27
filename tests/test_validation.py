import pandas as pd

from payments_pipeline import validation


def _clean_panel() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "period": ["2020Q1", "2020Q2"],
            "country": ["DE", "DE"],
            "instrument": ["card_payments", "card_payments"],
            "transactions_millions": [100.0, 110.0],
            "value_eur_billions": [5.0, 5.5],
        }
    )


def test_clean_data_reports_no_issues():
    report = validation.validate(_clean_panel())
    assert report.empty


def test_detects_negative_values():
    panel = _clean_panel()
    panel.loc[0, "transactions_millions"] = -1.0
    report = validation.validate(panel)
    assert "negative_values" in report["check"].values


def test_detects_duplicate_keys():
    panel = _clean_panel()
    panel = pd.concat([panel, panel.iloc[[0]]], ignore_index=True)
    report = validation.validate(panel)
    assert "duplicate_keys" in report["check"].values


def test_detects_missing_column():
    panel = _clean_panel().drop(columns=["value_eur_billions"])
    report = validation.validate(panel)
    assert "missing_columns" in report["check"].values
