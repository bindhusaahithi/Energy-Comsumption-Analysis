from typing import Iterable


REQUIRED_FIELDS = (
    "meter_id",
    "reading_timestamp",
    "region",
    "household_type",
    "consumption_kwh",
    "temperature_f",
    "tariff_band",
)


def validate_record(record: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if not record.get(field):
            errors.append(f"missing_{field}")

    try:
        if float(record["consumption_kwh"]) < 0:
            errors.append("negative_consumption")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid_consumption")

    return errors


def quality_summary(records: Iterable[dict[str, str]]) -> dict[str, int]:
    summary = {"valid_records": 0, "invalid_records": 0}
    for record in records:
        if validate_record(record):
            summary["invalid_records"] += 1
        else:
            summary["valid_records"] += 1
    return summary
