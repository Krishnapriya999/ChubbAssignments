from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# 1. Default arguments
default_args = {
    "owner": "krishnapriya_capstone",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
# 2. DAG Definition
with DAG(
    dag_id="populationCensus_sequentialJobs",   
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,   # Manual trigger (best for Databricks pipelines)
    catchup=False,
    tags=["census", "bronze", "silver", "gold", "databricks"],
) as dag:

    # Start marker
    start_pipeline = EmptyOperator(
        task_id="start_pipeline"
    )

    # Bronze Layer
    bronze_layer = DatabricksRunNowOperator(
        task_id="run_bronze_layer",
        databricks_conn_id="databricksDefault",
        job_id=672530452226296,
        wait_for_termination=True
    )

    # Silver Layer
    silver_layer = DatabricksRunNowOperator(
        task_id="run_silver_layer",
        databricks_conn_id="databricksDefault",
        job_id=1042163527863242,
        wait_for_termination=True
    )

    # Gold Layer
    gold_layer = DatabricksRunNowOperator(
        task_id="run_gold_layer",
        databricks_conn_id="databricksDefault",
        job_id=498960847987735,
        wait_for_termination=True
    )

    # End marker
    end_pipeline = EmptyOperator(
        task_id="end_pipeline"
    )
    # 3. Sequential dependency
    start_pipeline >> bronze_layer >> silver_layer >> gold_layer >> end_pipeline
