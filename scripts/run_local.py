from argparse import ArgumentParser

from energy_analytics.config import load_config
from energy_analytics.transformations import (
    aggregate_daily,
    clean_records,
    load_csv_records,
    write_csv,
)


def main() -> None:
    parser = ArgumentParser(description="Run the energy pipeline locally against sample data.")
    parser.add_argument("--config", required=True, help="Path to the YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)
    raw_records = load_csv_records(config.raw_data_path)
    curated_records = clean_records(raw_records)
    daily_summary = aggregate_daily(curated_records)
    write_csv(config.processed_output_path, daily_summary)

    print(f"Environment: {config.environment}")
    print(f"Raw records: {len(raw_records)}")
    print(f"Curated records: {len(curated_records)}")
    print(f"Wrote summary to: {config.processed_output_path}")


if __name__ == "__main__":
    main()

