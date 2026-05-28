from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from energy_analytics.quality import validate_record


def load_csv_records(path: str | Path) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def clean_records(records: list[dict[str, str]]) -> list[dict[str, object]]:
    cleaned: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()

    for record in records:
        if validate_record(record):
            continue

        dedupe_key = (record["meter_id"], record["reading_timestamp"])
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        timestamp = datetime.fromisoformat(record["reading_timestamp"].replace("Z", "+00:00"))
        cleaned.append(
            {
                "meter_id": record["meter_id"],
                "reading_timestamp": record["reading_timestamp"],
                "usage_date": timestamp.date().isoformat(),
                "usage_hour": timestamp.hour,
                "region": record["region"],
                "household_type": record["household_type"],
                "consumption_kwh": round(float(record["consumption_kwh"]), 2),
                "temperature_f": round(float(record["temperature_f"]), 2),
                "tariff_band": record["tariff_band"],
            }
        )
    return cleaned


def aggregate_daily(records: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], dict[str, object]] = defaultdict(
        lambda: {
            "total_kwh": 0.0,
            "peak_kwh": 0.0,
            "reading_count": 0,
            "peak_period": "",
        }
    )

    for record in records:
        key = (str(record["usage_date"]), str(record["region"]))
        bucket = grouped[key]
        consumption = float(record["consumption_kwh"])
        bucket["total_kwh"] += consumption
        bucket["reading_count"] += 1
        if consumption > float(bucket["peak_kwh"]):
            bucket["peak_kwh"] = consumption
            bucket["peak_period"] = str(record["tariff_band"])

    output: list[dict[str, object]] = []
    for (usage_date, region), bucket in sorted(grouped.items()):
        output.append(
            {
                "usage_date": usage_date,
                "region": region,
                "total_kwh": round(float(bucket["total_kwh"]), 2),
                "avg_kwh_per_reading": round(
                    float(bucket["total_kwh"]) / int(bucket["reading_count"]), 2
                ),
                "peak_kwh": round(float(bucket["peak_kwh"]), 2),
                "peak_period": bucket["peak_period"],
            }
        )
    return output


def write_csv(path: str | Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

