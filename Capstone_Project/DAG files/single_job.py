from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Default arguments for the dag
default_args = {
    "owner": "krishnapriya_capstone",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Helper function to log the databricks run_id via xcom
def log_run_id(ti):
    run_id = ti.xcom_pull(
        task_ids="trigger_databricks_census_job",
        key="run_id"
    )
    print(f"Databricks job triggered successfully. run_id = {run_id}")

with DAG(
    dag_id="population_census_single_job",   
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["census", "databricks", "capstone"],
) as dag:

    trigger_census_pipeline = DatabricksRunNowOperator(
        task_id="trigger_databricks_census_job",
        databricks_conn_id="databricksDefault",  
        job_id=969233964957203,
        wait_for_termination=False
    )

    log_runid = PythonOperator(
        task_id="log_databricks_run_id",
        python_callable=log_run_id
    )

    trigger_census_pipeline >> log_runid
