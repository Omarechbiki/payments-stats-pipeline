"""Compile euro-area payments statistics from country-level submissions."""

from .compilation import compile_euro_area_aggregates
from .data import load_sample_payments
from .outliers import flag_outliers
from .pipeline import PipelineResult, run
from .validation import validate

__all__ = [
    "load_sample_payments",
    "validate",
    "flag_outliers",
    "compile_euro_area_aggregates",
    "run",
    "PipelineResult",
]
