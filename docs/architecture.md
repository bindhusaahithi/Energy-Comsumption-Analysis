# Architecture

## Layers

- `data/raw/`: landing-zone representation of source smart-meter files
- `jobs/glue/`: cloud ETL job responsible for schema normalization and Parquet output
- `code/sql/`: Athena-facing analytical queries
- `orchestration/airflow/`: scheduling and operational workflow examples
- `infra/terraform/`: infrastructure bootstrap for buckets, catalog database, and Athena workgroup

## Operational Concerns

- Deduplication by `meter_id` and `reading_timestamp`
- Partitioning by `usage_date` and `region`
- Clear separation between development config and production config
- Testable local transformation logic isolated from managed cloud runtime

