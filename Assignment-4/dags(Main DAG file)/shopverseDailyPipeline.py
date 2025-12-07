from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import datetime, timedelta
import pandas as pd
import json
import os

dataBasePath = Variable.get("dataBasePath")
minOrderThreshold = int(Variable.get("minOrderThreshold"))

defaultArgs = {
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def checkFiles(ds, **kwargs):
    customerFile = os.path.join(dataBasePath,"landing/customers/customers_20250101.csv")
    productFile = os.path.join(dataBasePath,"landing/products/products_20250101.csv")
    orderFile = os.path.join(dataBasePath,"landing/orders/orders_20250101.json")
    filesExist = all([os.path.exists(f) for f in [customerFile, productFile, orderFile]])
    if not filesExist:
        raise FileNotFoundError("One or more input files are missing")
    return True

def loadStagingTables(ds, **kwargs):
    pg = PostgresHook(postgres_conn_id="postgresDwh")
    conn = pg.get_conn()
    cursor = conn.cursor()

    # Load customers
    dfCustomers = pd.read_csv(os.path.join(dataBasePath,"landing/customers/customers_20250101.csv"))
    for index,row in dfCustomers.iterrows():
        cursor.execute("""
        INSERT INTO stg_customers(customer_id, first_name, last_name, email, signup_date, country)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (row.customer_id, row.first_name, row.last_name, row.email, row.signup_date, row.country))

    # Load products
    dfProducts = pd.read_csv(os.path.join(dataBasePath,"landing/products/products_20250101.csv"))
    for index,row in dfProducts.iterrows():
        cursor.execute("""
        INSERT INTO stg_products(product_id, product_name, category, unit_price)
        VALUES (%s,%s,%s,%s)
        """, (row.product_id, row.product_name, row.category, row.unit_price))

    # Load orders
    with open(os.path.join(dataBasePath,"landing/orders/orders_20250101.json")) as f:
        orders = json.load(f)
        for row in orders:
            cursor.execute("""
            INSERT INTO stg_orders(order_id, order_timestamp, customer_id, product_id, quantity, total_amount, currency, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (row["order_id"], row["order_timestamp"], row["customer_id"], row["product_id"], row["quantity"], row["total_amount"], row["currency"], row["status"]))
    conn.commit()

def branchMinOrders(ds, **kwargs):
    pg = PostgresHook(postgres_conn_id="postgresDwh")
    conn = pg.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM stg_orders")
    count = cursor.fetchone()[0]
    if count < minOrderThreshold:
        return "lowVolumeWarning"
    else:
        return "normalFlow"

def lowVolumeWarning(ds, **kwargs):
    print("Orders below threshold. Alert sent or anomaly logged.")

def normalFlow(ds, **kwargs):
    print("Normal flow: continue ETL to warehouse")

with DAG(
    "shopverseDailyPipeline",
    default_args=defaultArgs,
    description="Shopverse daily ETL pipeline",
    schedule_interval=None,
    start_date=datetime(2025,1,1),
    catchup=False,
    tags=["shopverse"],
) as dag:

    checkFilesTask = PythonOperator(
        task_id="checkFilesExistence",
        python_callable=checkFiles
    )

    loadStagingTask = PythonOperator(
        task_id="loadStagingTables",
        python_callable=loadStagingTables
    )

    branchTask = BranchPythonOperator(
        task_id="branchMinOrders",
        python_callable=branchMinOrders
    )

    lowVolumeTask = PythonOperator(
        task_id="lowVolumeWarning",
        python_callable=lowVolumeWarning
    )

    normalFlowTask = PythonOperator(
        task_id="normalFlow",
        python_callable=normalFlow
    )

    checkFilesTask >> loadStagingTask >> branchTask
    branchTask >> [lowVolumeTask, normalFlowTask]

