from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "energy_readings_sample.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "daily_consumption_summary.csv"
ARCHITECTURE_DIAGRAM_PATH = BASE_DIR / "visuals" / "architecture" / "aws-pipeline-diagram.svg"


st.set_page_config(
    page_title="Energy Consumption Analysis Demo",
    page_icon="⚡",
    layout="wide",
)


@st.cache_data
def load_raw_data() -> pd.DataFrame:
    frame = pd.read_csv(RAW_DATA_PATH, parse_dates=["reading_timestamp"])
    frame["usage_date"] = frame["reading_timestamp"].dt.date.astype(str)
    return frame


@st.cache_data
def load_processed_data() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DATA_PATH)


raw_df = load_raw_data()
processed_df = load_processed_data()

st.title("Energy Consumption Analysis")
st.caption(
    "Interactive Streamlit demo for a production-style AWS energy analytics pipeline."
)

with st.sidebar:
    st.header("Filters")
    regions = st.multiselect(
        "Region",
        options=sorted(raw_df["region"].unique()),
        default=sorted(raw_df["region"].unique()),
    )
    household_types = st.multiselect(
        "Household type",
        options=sorted(raw_df["household_type"].unique()),
        default=sorted(raw_df["household_type"].unique()),
    )
    tariff_bands = st.multiselect(
        "Tariff band",
        options=sorted(raw_df["tariff_band"].unique()),
        default=sorted(raw_df["tariff_band"].unique()),
    )


filtered_raw_df = raw_df[
    raw_df["region"].isin(regions)
    & raw_df["household_type"].isin(household_types)
    & raw_df["tariff_band"].isin(tariff_bands)
].copy()

filtered_processed_df = processed_df[processed_df["region"].isin(regions)].copy()

if filtered_raw_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

total_consumption = round(filtered_raw_df["consumption_kwh"].sum(), 2)
peak_reading = round(filtered_raw_df["consumption_kwh"].max(), 2)
average_temperature = round(filtered_raw_df["temperature_f"].mean(), 2)
record_count = int(len(filtered_raw_df))

metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("Total Consumption (kWh)", total_consumption)
metric_two.metric("Peak Reading (kWh)", peak_reading)
metric_three.metric("Average Temperature (F)", average_temperature)
metric_four.metric("Meter Reads", record_count)

overview_col, architecture_col = st.columns([1.35, 1])

with overview_col:
    st.subheader("Project Summary")
    st.markdown(
        """
        This demo simulates how smart-meter energy readings move through an AWS pipeline:

        - raw CSV files land in Amazon S3
        - AWS Glue standardizes and enriches the data
        - Parquet outputs support cost-efficient Athena queries
        - dashboards reveal daily and hourly consumption patterns
        """
    )

with architecture_col:
    st.subheader("Architecture")
    st.image(str(ARCHITECTURE_DIAGRAM_PATH), use_container_width=True)

daily_totals = (
    filtered_raw_df.groupby(["usage_date", "region"], as_index=False)["consumption_kwh"].sum()
    .rename(columns={"consumption_kwh": "total_kwh"})
)

hourly_profile = (
    filtered_raw_df.groupby("reading_timestamp", as_index=False)["consumption_kwh"].sum()
    .sort_values("reading_timestamp")
)

household_mix = (
    filtered_raw_df.groupby("household_type", as_index=False)["consumption_kwh"].sum()
    .sort_values("consumption_kwh", ascending=False)
)

chart_col_one, chart_col_two = st.columns(2)

with chart_col_one:
    st.subheader("Daily Consumption by Region")
    st.line_chart(
        daily_totals.pivot(index="usage_date", columns="region", values="total_kwh"),
        use_container_width=True,
    )

with chart_col_two:
    st.subheader("Hourly Consumption Profile")
    st.area_chart(
        hourly_profile.set_index("reading_timestamp")["consumption_kwh"],
        use_container_width=True,
    )

table_col_one, table_col_two = st.columns(2)

with table_col_one:
    st.subheader("Consumption by Household Type")
    st.bar_chart(
        household_mix.set_index("household_type")["consumption_kwh"],
        use_container_width=True,
    )

with table_col_two:
    st.subheader("Curated Daily Summary")
    st.dataframe(filtered_processed_df, use_container_width=True, hide_index=True)

with st.expander("View raw smart-meter records"):
    st.dataframe(filtered_raw_df, use_container_width=True, hide_index=True)
