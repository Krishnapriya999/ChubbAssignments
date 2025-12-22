Project Overview

This project demonstrates the implementation of a modern data lakehouse architecture using Azure Databricks, Spark, and Delta Lake. The platform is designed to ingest, process, and analyze global retail sales data, transforming raw transactional records into high-impact executive insights. By utilizing the medallion architecture, the system ensures data reliability, scalability, and high quality through automated calibration and incremental processing.
1. Data Ingestion Phase:

The project begins in the landing zone, where legacy source systems deposit raw retail data in CSV format. These files include sales transactions, product master data, and store location details.

The ingestion notebook utilizes spark to read these files into the bronze layer of the lakehouse. During this phase, the data is stored in its rawest form to preserve a full audit history. Mandatory metadata, including ingestion timestamps and source system identifiers, are appended to every record to establish a clear line of data lineage.

2. Silver Layer: Processing and Standardization

The silver layer serves as the core transformation engine where raw data is converted into clean, standardized, and reliable information. This phase implements several critical enterprise-grade data engineering patterns.

Data Quality and Quarantine

Before data is integrated into the silver tables, it passes through a quality gate. Records with missing identifiers or invalid metrics are automatically diverted to a quarantine table. This ensures the main analytics pipeline remains unpolluted while providing a log for data troubleshooting.

### Calibration and Normalization

A data calibration routine validates the mathematical accuracy of every sale, correcting any discrepancies between quantity, unit price, and total amount. Furthermore, all timestamps are standardized to utc, and currencies are normalized to usd using a fixed exchange rate to allow for accurate global comparison.

Incremental UPSERT Logic

To optimize performance, the silver layer uses delta lake merge operations. This allows the system to perform incremental updates, only processing new or changed records since the last run. This ensures the platform can scale efficiently as data volumes grow.

3. Gold Layer: Analytics and Curated Data

The gold layer contains the final, business-ready datasets. Data in this layer is de-normalized and pre-aggregated to support specific analytical use cases.

By pre-calculating metrics such as daily regional revenue and monthly product rankings, the system removes the computational burden from the visualization layer. These tables are optimized for high-speed access by business intelligence tools, providing a seamless experience for end users.

4. Power BI Integration and Visualization

The final stage of the project is the creation of interactive dashboards in power bi. The tool connects directly to the gold delta tables in databricks using directquery.

Executive Sales Overview:

This dashboard provides leadership with a high-level view of global performance, featuring total revenue trends, regional sales distribution, and key performance indicators.

Product Performance Insights:

This dashboard drills down into inventory success, visualizing category-wise sales, top-performing products, and monthly growth trends. Because of the standardization and calibration performed in the earlier layers, executives can trust that the insights are based on accurate and unified data.