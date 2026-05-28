from energy_analytics.transformations import aggregate_daily, clean_records


def test_clean_records_removes_duplicates_and_casts_types() -> None:
    raw = [
        {
            "meter_id": "A1",
            "reading_timestamp": "2026-05-01T00:00:00Z",
            "region": "Northeast",
            "household_type": "Residential",
            "consumption_kwh": "2.5",
            "temperature_f": "60",
            "tariff_band": "Off-Peak",
        },
        {
            "meter_id": "A1",
            "reading_timestamp": "2026-05-01T00:00:00Z",
            "region": "Northeast",
            "household_type": "Residential",
            "consumption_kwh": "2.5",
            "temperature_f": "60",
            "tariff_band": "Off-Peak",
        },
    ]

    cleaned = clean_records(raw)

    assert len(cleaned) == 1
    assert cleaned[0]["usage_hour"] == 0
    assert cleaned[0]["consumption_kwh"] == 2.5


def test_aggregate_daily_summarizes_region_totals() -> None:
    cleaned = [
        {
            "usage_date": "2026-05-01",
            "region": "Northeast",
            "consumption_kwh": 2.5,
            "tariff_band": "Off-Peak",
        },
        {
            "usage_date": "2026-05-01",
            "region": "Northeast",
            "consumption_kwh": 4.5,
            "tariff_band": "Peak",
        },
    ]

    aggregated = aggregate_daily(cleaned)

    assert aggregated == [
        {
            "usage_date": "2026-05-01",
            "region": "Northeast",
            "total_kwh": 7.0,
            "avg_kwh_per_reading": 3.5,
            "peak_kwh": 4.5,
            "peak_period": "Peak",
        }
    ]

