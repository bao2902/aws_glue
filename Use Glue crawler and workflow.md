# Architecture

<img alt="image" src="https://github.com/user-attachments/assets/da684057-4c6c-4999-b819-3397576ce1f8" />

# Concepts

## Data Catalog

Data Catalog is a centralized, fully managed metadata repository that acts as an index for all your data assets across AWS storage services and on-premises databases.
* Instead of storing actual raw data (like CSVs, Parquet files, or SQL rows), the Glue Catalog stores metadata—table schemas, column data types, partition details, file formats, and source locations in Amazon S3 or relational databases.

## Database

Database is a logical container and namespace inside the AWS Glue Data Catalog used to organize and manage related metadata tables.
* It does not hold actual physical data or store files itself; instead, it acts as a catalog grouping mechanism—similar to a standard relational database schema—that points to datasets stored elsewhere, such as in Amazon S3, Amazon Redshift, or external relational databases.

## Table
	
Table is a metadata definition in the AWS Glue Data Catalog that represents a specific dataset. It does not store actual records or raw files; instead, it acts as a schema layer and pointer that tells query engines (like Amazon Athena, Redshift Spectrum, EMR, and Glue Spark jobs) how to read and interpret raw files stored in Amazon S3 or external data sources.

## Crawler

Crawler is an automated, serverless program in AWS Glue that connects to a data store (like Amazon S3, Redshift, or relational databases), inspects the raw data, infers its structure and format, and automatically populates or updates table definitions in the AWS Glue Data Catalog.
* Instead of manually defining schemas, data types, and file formats, a Crawler automates data discovery so analytics engines like Amazon Athena or AWS Glue ETL can instantly query the data.

## Python Shell ETL job

Python Shell ETL job in AWS Glue is a lightweight, cost-effective runtime environment designed to run standard Python scripts that do not require the heavy distributed processing power of Apache Spark.
* While Spark jobs spin up multi-node clusters suited for gigabytes or terabytes of data, a Python Shell job runs on a single compute node (a portion of a Data Processing Unit, or DPU), making it much faster to start and significantly cheaper to run.

## Workflow

Workflow is a serverless graph-based orchestration tool used to visually link, schedule, and execute multi-step ETL pipelines involving Glue Crawlers, Jobs, and Triggers.
* Instead of writing custom scripts or managing external orchestration servers (like Apache Airflow) to chain tasks together, Glue Workflows provide a native DAG (Directed Acyclic Graph) view inside AWS.

# Create Glue crawler

## Create Data Catalog database

Glue > Data Catalog > Databases > Add database

* Database type: Glue Database
* Name: src_nhe_insights

## Upload S3 file

Data\DIMDELIVERY_DBT_FIVETRAN_DATASET_09-28-26_full.parquet

<img alt="image" src="https://github.com/user-attachments/assets/dc92b0c5-f1c1-4e3d-ab2c-e642443b0485" />

## Create crawler

Glue > Data Catalog > Crawlers > Create crawler

* Name: s3_delivery_metrics_crawler
* Data source: S3
* S3 path: s3://bucket29022902/fivetran/snowflake/
* Subsequent crawler runs: Crawl all sub-folders
* IAM role: MyGlueExecutionRole
* Target database: src_nhe_insights
* S3 schema grouping: Create a single schema for each S3 path
* When the crawler detects schema changes in the data store, how should AWS Glue handle table updates in the data catalog? Update the table definition in the data catalog

## Run crawler and check Athena

<img alt="image" src="https://github.com/user-attachments/assets/26bfebc8-f470-4107-b4a0-d36a0cd1e831" />

# Create Python Shell ETL job

Python\test_workflow_dummy_job.py

ETL jobs > Visual ETL > Script editor

* Engine: Python shell
* Name: test_workflow_dummy_job
* IAM Role: MyGlueExecutionRole
* Data processing units: 1/16 DPU

# Create Glue workflow

Glue > Workflows > Add workflow

* Workflow name: Daily_Delivery_Data_Pipeline

**Orchestrate graph**

Daily_Delivery_Data_Pipeline > Graph

Trigger details
* Name: trigger_1
* Trigger type: ON_DEMAND
Crawler details
* Name: s3_delivery_metrics_crawler
Trigger details
* Name: On_Crawler_Success
* Trigger type: CONDITIONAL
* Trigger state: ACTIVATED
* Starts: test_workflow_dummy_job
* Trigger logic: Start after ANY watched event
* Watching: s3_delivery_metrics_crawler - SUCCEEDED
Job details
* Name: test_workflow_dummy_job
* Triggered by: On_Crawler_Success

<img alt="image" src="https://github.com/user-attachments/assets/5e55a31f-ce07-40d6-8fee-b2e63ed025c1" />

