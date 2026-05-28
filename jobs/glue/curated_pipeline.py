import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import ApplyMapping, ResolveChoice
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F


args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "SOURCE_PATH", "TARGET_PATH"],
)

glue_context = GlueContext(SparkContext())
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

raw_frame = glue_context.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [args["SOURCE_PATH"]], "recurse": True},
    format="csv",
    format_options={"withHeader": True},
)

resolved_frame = ResolveChoice.apply(raw_frame, choice="make_cols")
mapped_frame = ApplyMapping.apply(
    frame=resolved_frame,
    mappings=[
        ("meter_id", "string", "meter_id", "string"),
        ("reading_timestamp", "string", "reading_timestamp", "string"),
        ("region", "string", "region", "string"),
        ("household_type", "string", "household_type", "string"),
        ("consumption_kwh", "string", "consumption_kwh", "double"),
        ("temperature_f", "string", "temperature_f", "double"),
        ("tariff_band", "string", "tariff_band", "string"),
    ],
)

curated_df = (
    mapped_frame.toDF()
    .dropna(subset=["meter_id", "reading_timestamp", "consumption_kwh"])
    .dropDuplicates(["meter_id", "reading_timestamp"])
    .withColumn("reading_ts", F.to_timestamp("reading_timestamp"))
    .withColumn("usage_date", F.to_date("reading_ts"))
    .withColumn("usage_hour", F.hour("reading_ts"))
    .drop("reading_ts")
)

(
    curated_df.write.mode("overwrite")
    .partitionBy("usage_date", "region")
    .format("parquet")
    .save(args["TARGET_PATH"])
)

job.commit()

