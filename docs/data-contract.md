# Data Contract

## Raw Input Schema

| Column | Type | Description |
| --- | --- | --- |
| `meter_id` | string | Unique smart-meter identifier |
| `reading_timestamp` | ISO-8601 string | UTC reading timestamp |
| `region` | string | Reporting geography |
| `household_type` | string | Residential, Commercial, or Industrial |
| `consumption_kwh` | double | Energy consumed in kilowatt-hours |
| `temperature_f` | double | Ambient temperature at read time |
| `tariff_band` | string | Off-Peak, Mid-Peak, or Peak |

## Curated Output Fields

- `usage_date`
- `region`
- `total_kwh`
- `avg_kwh_per_reading`
- `peak_kwh`
- `peak_period`

