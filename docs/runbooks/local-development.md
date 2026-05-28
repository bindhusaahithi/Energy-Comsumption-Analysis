# Local Development Runbook

## Run the pipeline locally

```bash
python3 -m pip install -e ".[dev]"
python3 scripts/run_local.py --config configs/dev.yaml
```

## Run tests

```bash
python3 -m pytest
```

## Expected output

The local runner rewrites `data/processed/daily_consumption_summary.csv` from the sample raw input in `data/raw/`.

