from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class PipelineConfig:
    environment: str
    raw_data_path: str
    processed_output_path: str
    aws_region: str
    s3_raw_bucket: str
    s3_curated_bucket: str
    athena_database: str
    athena_table: str


def load_config(path: str | Path) -> PipelineConfig:
    with open(path, "r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    return PipelineConfig(**payload)

