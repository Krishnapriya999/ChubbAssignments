1. Overview

This project implements a daily ETL pipeline for the Shopverse dataset using Apache Airflow.
The pipeline performs the following:
Checks for input files in the landing folder.
Loads data into staging tables (stg_customers, stg_products, stg_orders).
Branches based on minimum order threshold (minOrderThreshold).
Loads data into data warehouse tables (dim_customers, dim_products, fact_orders).
Performs basic data quality checks (row counts, nulls, duplicates, foreign key integrity).

2. Airflow Setup
Variables
Set the following Airflow Variables:

Name	            Value
dataBasePath	    /opt/airflow/data
minOrderThreshold	10

Go to Airflow UI ->Admin -> Variables -> Create.

Connections

Set up a Postgres connection for the warehouse:
Field	        Value
Conn Id	        postgresDwh
Conn Type	Postgres
Host	        postgres
Database        dwh_shopverse
Login	        airflow
Password        enter your airflow password
Port	        5432

Go to Airflow UI - Admin -> Connections-> Create.

3. Input Files
Place the daily files in the landing folder:

/opt/airflow/data/landing/customers/customers_<YYYYMMDD>.csv
/opt/airflow/data/landing/products/products_<YYYYMMDD>.csv
/opt/airflow/data/landing/orders/orders_<YYYYMMDD>.json
customers_20250101.csv
products_20250101.csv
orders_20250101.json
The DAG checks for file existence before loading.
The DAG File is in /airflow-docker/dags/shopverseDailyPipeline.py
The sql files are in /airflow-docker/sql
4. Triggering the DAG

Manual Trigger: 
Go to Airflow UI->DAGs ->shopverseDailyPipeline
Click Trigger DAG
Backfill Older Dates:
docker exec -it airflow-docker-airflow-webserver-1 airflow dags backfill shopverseDailyPipeline -s 2025-01-01 -e 2025-01-05
This will execute the DAG for all dates from start (-s) to end (-e).

5. Data Quality Checks

The DAG ensures:
Minimum orders check: If stg_orders count < minOrderThreshold, branch to lowVolumeWarning.
Primary key checks: Ensures customer_id, product_id, order_id are unique and not null.
Foreign key checks: All orders reference valid customers and products.
Numeric constraints: unit_price, quantity, and total_amount are non-negative.
