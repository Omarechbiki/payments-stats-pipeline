# payments-stats-pipeline

A small, reproducible pipeline that compiles euro-area payments statistics the way
a statistical production team would: load country submissions, run data-quality
checks, detect outliers in the quarterly series, and compile euro-area aggregates.

The bundled dataset is **synthetic** but shaped like the ECB payments statistics
(country × payment instrument × quarter). Point `load_sample_payments` at a CSV
export from the [ECB Data Portal](https://data.ecb.europa.eu/) to run on official data.

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python -m payments_pipeline
```

This validates the data, flags outliers, compiles euro-area aggregates, and writes
the results to `output/`.

## Test

```bash
pytest
```

## Layout

| Module | Responsibility |
| --- | --- |
| `data.py` | Load the payments panel (synthetic sample or your own CSV) |
| `validation.py` | Data-quality checks (nulls, negatives, duplicates, completeness) |
| `outliers.py` | Robust quarter-on-quarter outlier detection per series |
| `compilation.py` | Aggregate national series into euro-area totals |
| `pipeline.py` | Orchestration and output writing |
