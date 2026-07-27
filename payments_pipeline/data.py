"""Sample payments panel shaped like the ECB payments statistics dataset."""

from __future__ import annotations

import numpy as np
import pandas as pd

EURO_AREA_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]
PAYMENT_INSTRUMENTS = ["card_payments", "credit_transfers", "direct_debits", "e_money"]


def load_sample_payments(
    start_quarter: str = "2018Q1",
    num_quarters: int = 24,
    seed: int = 42,
) -> pd.DataFrame:
    """Return a quarterly payments panel with realistic trend and seasonality.

    Values are synthetic so the pipeline runs offline. Replace this function with a
    CSV read to compile official statistics from the ECB Data Portal.
    """
    rng = np.random.default_rng(seed)
    quarters = pd.period_range(start_quarter, periods=num_quarters, freq="Q")

    records = []
    for country in EURO_AREA_COUNTRIES:
        for instrument in PAYMENT_INSTRUMENTS:
            transactions = _simulate_transactions(rng, num_quarters)
            value_per_transaction = rng.uniform(0.02, 0.08)
            for quarter, count in zip(quarters, transactions):
                records.append(
                    {
                        "period": str(quarter),
                        "country": country,
                        "instrument": instrument,
                        "transactions_millions": round(count, 1),
                        "value_eur_billions": round(count * value_per_transaction, 2),
                    }
                )
    return pd.DataFrame.from_records(records)


def _simulate_transactions(rng: np.random.Generator, num_quarters: int) -> np.ndarray:
    """Simulate one series as a growing, mildly seasonal transaction volume."""
    base_volume = rng.uniform(80, 600)
    trend = np.linspace(1.0, rng.uniform(1.2, 1.8), num_quarters)
    quarter_of_year = np.arange(num_quarters) % 4
    seasonal = 1 + 0.06 * np.sin(2 * np.pi * quarter_of_year / 4)
    noise = rng.normal(1.0, 0.02, num_quarters)
    return base_volume * trend * seasonal * noise
