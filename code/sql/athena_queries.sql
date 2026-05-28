-- Daily consumption by region
SELECT
  usage_date,
  region,
  ROUND(SUM(consumption_kwh), 2) AS total_kwh
FROM curated_energy_readings
GROUP BY usage_date, region
ORDER BY usage_date, region;

-- Hourly demand profile
SELECT
  usage_hour,
  ROUND(AVG(consumption_kwh), 2) AS avg_hourly_kwh,
  ROUND(MAX(consumption_kwh), 2) AS peak_hourly_kwh
FROM curated_energy_readings
GROUP BY usage_hour
ORDER BY usage_hour;

-- Peak-period comparison by household type
SELECT
  household_type,
  tariff_band,
  ROUND(SUM(consumption_kwh), 2) AS total_kwh
FROM curated_energy_readings
GROUP BY household_type, tariff_band
ORDER BY household_type, tariff_band;
