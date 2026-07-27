"""Run the full payments-statistics compilation pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from . import compilation, data, outliers, validation


@dataclass
class PipelineResult:
    quality_report: pd.DataFrame
    flagged_series: pd.DataFrame
    euro_area_aggregates: pd.DataFrame


def run(output_dir: str = "output", outlier_threshold: float = 3.5) -> PipelineResult:
    """Load, validate, screen for outliers, and compile euro-area aggregates."""
    payments = data.load_sample_payments()
    result = PipelineResult(
        quality_report=validation.validate(payments),
        flagged_series=outliers.flag_outliers(payments, threshold=outlier_threshold),
        euro_area_aggregates=compilation.compile_euro_area_aggregates(payments),
    )
    _write_outputs(Path(output_dir), result)
    return result


def _write_outputs(output_dir: Path, result: PipelineResult) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    result.quality_report.to_csv(output_dir / "quality_report.csv", index=False)
    result.flagged_series.to_csv(output_dir / "flagged_series.csv", index=False)
    result.euro_area_aggregates.to_csv(output_dir / "euro_area_aggregates.csv", index=False)


def main() -> None:
    result = run()
    outliers_found = int(result.flagged_series["is_outlier"].sum())
    print(f"Observations screened : {len(result.flagged_series)}")
    print(f"Data-quality issues   : {len(result.quality_report)}")
    print(f"Outliers flagged      : {outliers_found}")
    print(f"Aggregate rows        : {len(result.euro_area_aggregates)}")
    print("Results written to ./output")
