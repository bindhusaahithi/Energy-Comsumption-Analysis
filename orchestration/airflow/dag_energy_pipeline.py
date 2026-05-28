from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="energy_consumption_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["energy", "aws", "analytics"],
) as dag:
    validate_raw = BashOperator(
        task_id="validate_raw_dataset",
        bash_command="echo 'Validating raw smart-meter files'",
    )

    run_glue_job = BashOperator(
        task_id="run_glue_job",
        bash_command="echo 'Triggering AWS Glue curated transformation job'",
    )

    refresh_athena_views = BashOperator(
        task_id="refresh_athena_views",
        bash_command="echo 'Refreshing Athena reporting views'",
    )

    publish_metrics = BashOperator(
        task_id="publish_quality_metrics",
        bash_command="echo 'Publishing operational metrics to monitoring'",
    )

    validate_raw >> run_glue_job >> refresh_athena_views >> publish_metrics

