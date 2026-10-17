# Architecture

<img alt="image" src="https://github.com/user-attachments/assets/51087d97-21e7-4fc1-bb08-0714885bfb48" />

# Concepts

## Virtual Private Cloud

VPC (Virtual Private Cloud) is a logically isolated virtual network inside the AWS cloud dedicated to your AWS account. It mimics a traditional physical network operating in a data center, but gives you complete control over your cloud networking environment.

<img alt="image" src="https://github.com/user-attachments/assets/d7fb7505-5f70-4cd1-979f-c3b457244567" />

## Public Subnet

Public Subnet is a designated segment of an AWS Virtual Private Cloud (VPC) where resources are directly accessible from and can directly communicate with the public internet.

## Private Subnet

Private Subnet is a segment of an AWS Virtual Private Cloud (VPC) where resources are completely isolated from direct internet access.

## Internet Gateway

Internet Gateway (IGW) is a horizontally scaled, highly available AWS VPC component that acts as the front door between your Virtual Private Cloud and the public internet.
* Without an Internet Gateway, resources in your VPC are completely isolated from the internet.

## NAT Gateway

NAT Gateway (Network Address Translation Gateway) is an AWS VPC service that allows instances in a Private Subnet to connect to the internet or other AWS services, while preventing the internet from initiating an inbound connection with those private instances.
* It acts as a one-way security boundary and proxy for outbound internet traffic.

## IAM Group

IAM Group is a collection of IAM (Identity and Access Management) users within an AWS account. It allows you to specify permissions for multiple users at once, making permissions management vastly simpler and more scalable.
* Instead of attaching permissions to individual users one by one, you assign policies to a group. Any user added to that group automatically inherits all of the group's permissions.

## IAM User

IAM User is an identity created within an AWS account that represents a specific person, application, or service interacting with your AWS resources.
* Unlike a root account, an IAM User has long-term credentials and custom permissions defined by IAM policies.

## Secrets Manager
Secrets Manager is a fully managed service designed to store, manage, retrieve, and automatically rotate sensitive credentials—such as database passwords, API keys, OAuth tokens, and SSH keys—throughout their lifecycle.
* Instead of hardcoding credentials in source code or storing them in plain-text configuration files, applications fetch secrets at runtime via programmatic API calls.

# Prerequisites

## Create AWS IAM group and user

**Create group**

IAM > IAM user groups > Create group

* User group name: group_1

**Create user**

IAM > IAM users > Create user

* User name: user_1

**Create access key**

IAM > IAM users > user_1 > Security credentials > Create access key

* Access key: •••••••••••••••
* Secret access key: •••••••••••••••

**Add permissions to IAM group**

group_1 > Permissions > Policy "AmazonS3FullAccess"

group_1 > Permissions > Inline Policy > KMSKeyManagementPolicy

> {
>   "Version": "2012-10-17",
>   "Statement": [
>     {
>       "Sid": "AllowKMSRotationAndManagement",
>       "Effect": "Allow",
>       "Action": [
>         "kms:CreateKey",
>         "kms:TagResource",
>         "kms:EnableKeyRotation",
>         "kms:GetKeyRotationStatus",
>         "kms:DescribeKey"
>       ],
>       "Resource": "*"
>     }
>   ]
> }

group_1 > Permissions > Inline Policy > KMSKeyManagementPolicy

> {
>   "Version": "2012-10-17",
>   "Statement": [
>     {
>       "Sid": "AllowFullKMSAccess",
>       "Effect": "Allow",
>       "Action": "kms:*",
>       "Resource": "*"
>     }
>   ]
> }

## Create AWS VPC

**Create VPC**

VPC > Your VPCs > Create VPC

* Create VPC: vpc-0c4e638bc3187bdd7 
* Enable DNS hostnames
* Enable DNS resolution
* Verifying VPC creation: vpc-0c4e638bc3187bdd7 
* Create S3 endpoint: vpce-0c03fdc73fb78f235 
* Create subnet: subnet-0573ec4560cf691e4 
* Create subnet: subnet-04e2957dec309de3f 
* Create internet gateway: igw-09a8310e661507c08 
* Attach internet gateway to the VPC
* Create route table: rtb-00f4f7a9f3f3ad6ef 
* Create route
* Associate route table
* Create route table: rtb-0a24f07be01c615f3 
* Associate route table
* Verifying route table creation
* Associate S3 endpoint with private subnet route tables: vpce-0c03fdc73fb78f235 

**Create NAT Gateway**

VPC > NAT gateways > Create NAT gateway

* nat-1e030c6a87d56717f

**Add route from Private Subnet to NAT Gateway**

VPC > Route tables > rtb-0a24f07be01c615f3 > Routes > Edit routes

* Destination: 0.0.0.0/0
* Target: NAT Gateway > nat-1e030c6a87d56717f

## Create AWS Secrets

**Create Azure SQL secret**

AWS Secrets Manager > Secrets > Store a new secret > /nonprod/product-1/sub-product-1/sqlserver_secret

* db_username: serveradmin2902
* db_password: ••••••••
* driver_name: com.microsoft.sqlserver.jdbc.SQLServerDriver
* host: azureserver2902.database.windows.net

**Create Snowflake secret**

AWS Secrets Manager > Secrets > Store a new secret > /nonprod/product-1/sub-product-1/snowflake_secret

* ACCOUNT: GWEKWZX-CZ48845
* USER: BAO2902
* ROLE: ACCOUNTADMIN

# Use Terraform to deploy AWS infrastructures

https://github.com/bao2902/terraform/wiki/Use-Terraform-to-deploy-AWS-infrastructures

# Use Glue to load data from Azure SQL Database to Snowflake

## Create Data Access Layer table

> CREATE OR REPLACE TABLE GLUE_DAL_TABLES ( 
> ROW_ID NUMBER(38,0) NOT NULL COMMENT 'The primary key.', 
> SOURCE_DATABASE VARCHAR(16777216) NOT NULL COMMENT 'The name of the source database.', 
> SOURCE_DB_TYPE VARCHAR(16777216) NOT NULL COMMENT 'The type of the source database.', 
> SOURCE_SCHEMA VARCHAR(16777216) NOT NULL COMMENT 'The name of the schema from the source database.', 
> SOURCE_TABLE VARCHAR(16777216) NOT NULL COMMENT 'The name of the table from the source database.', 
> SOURCE_COLUMN VARCHAR(16777216) NOT NULL COMMENT 'The column names from the source table.', 
> SOURCE_KEY VARCHAR(16777216) COMMENT 'The source-table columns that make this row''s merge key.', 
> DELTA_COLUMN VARCHAR(16777216) COMMENT 'The name of the column in the source table', 
> DELTA_DATATYPE VARCHAR(16777216) COMMENT 'Stores the delta column''s data type because it can vary between tables.', 
> DELTA_LAST_RUN VARCHAR(16777216) COMMENT 'The value of the delta column on the last run.', 
> DELTA_MODE VARCHAR(1) NOT NULL DEFAULT 'F' COMMENT '''F'' = Full Load, ''D'' = Delta Load', 
> ACTIVE BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'The active indicator, used to turn on/off the ETL for each table.', 
> SNOWFLAKE_SCHEMA VARCHAR(16777216) NOT NULL COMMENT 'The name of the Snowflake schema.', 
> SNOWFLAKE_TABLE VARCHAR(16777216) NOT NULL COMMENT 'The name of the Snowflake table.', 
> primary key (ROW_ID) 
> )COMMENT='Metadata about source tables used in AWS Glue ETL jobs to load data into Snowflake.' 
> ;

## Add ETL table

> INSERT INTO GLUE_DAL_TABLES (
> ROW_ID,
> SOURCE_DATABASE,
> SOURCE_DB_TYPE,
> SOURCE_SCHEMA,
> SOURCE_TABLE,
> SOURCE_COLUMN,
> DELTA_COLUMN,
> DELTA_DATATYPE,
> DELTA_LAST_RUN,
> DELTA_MODE,
> ACTIVE,
> SNOWFLAKE_SCHEMA,
> SNOWFLAKE_TABLE
> )
> SELECT
> '1' ROW_ID,
> 'AzureSQLDatabase2902' SOURCE_DATABASE,
> 'sqlserver' SOURCE_DB_TYPE,
> 'titan' SOURCE_SCHEMA,
> 'Dim_PurchaseOrderStatus' SOURCE_TABLE,
> 'DimPurchaseOrderStatusSID, Code, Description' SOURCE_COLUMN,
> 'DimPurchaseOrderStatusSID' SOURCE_KEY,
> 'Code' DELTA_COLUMN,
> 'INT' DELTA_DATATYPE,
> NULL DELTA_LAST_RUN,
> 'D' DELTA_MODE,
> 'TRUE' ACTIVE,
> 'SRC_NHE_INSIGHTS' SNOWFLAKE_SCHEMA,
> 'TITAN_DIM_PURCHASEORDERSTATUS' SNOWFLAKE_TABLE

## Create ETL Metrics table

> CREATE OR REPLACE TABLE GLUE_ETL_METRICS (
> ROW_ID NUMBER(38,0) NOT NULL COMMENT 'The foreign key used to refer to the GLUE_DAL_TABLES table.',
> LAST_RUN VARCHAR(16777216) COMMENT 'The value of the delta column at the end of this run.',
> DELTA_MODE VARCHAR(1) NOT NULL COMMENT 'Has the same meaning as GLUE_DAL_TABLES.DELTA_MODE.',
> START_TIME TIMESTAMP_NTZ(9) NOT NULL COMMENT 'The timestamp when the ETL of a specific table started.',
> END_TIME TIMESTAMP_NTZ(9) NOT NULL COMMENT 'The timestamp when the ETL of a specific table ended.',
> ELAPSED_TIME_MILLIS NUMBER(38,0) NOT NULL COMMENT 'END_TIME - START_TIME in milliseconds.',
> RECORD_COUNT NUMBER(38,0) NOT NULL COMMENT 'Number of records processed (inserted/updated/deleted) in the ETL of a specific table.'
> )COMMENT='Metrics about AWS Glue ETL runs.'
> ;

## Read the table list from the DAL table

> glue_metadata_query = """
> SELECT 
> row_id,
> source_database,
> source_db_type,
> source_schema, 
> source_table, 
> source_column, 
> source_key,
> delta_column,
> delta_datatype, 
> delta_last_run, 
> delta_mode, 
> snowflake_schema, 
> snowflake_table
> FROM 
> %s 
> WHERE 
> active 
> ORDER BY 
> row_id """ % (glue_metadata_table)

> df_table_list = spark.read.format(SNOWFLAKE_SOURCE_NAME).options(**sfOptions) \
> .option("query", glue_metadata_query).load().toPandas()

## Use asyncio to run ETL for all tables asynchronously

> tasks = [process_etl_from_source_to_target(sfOptions, row_id, source_db_type, source_database, source_schema,
>     source_table, source_column, snowflake_table, delta_column, delta_datatype, delta_last_run, delta_mode,
>     snowflake_schema, source_key, target_columns_by_table.get((snowflake_schema, snowflake_table), []))
>     for index, row_id, source_database, source_db_type, source_schema, source_table, source_column, source_key, delta_column, delta_datatype, delta_last_run, delta_mode, snowflake_schema, snowflake_table
>     in df_table_list.itertuples()]
> asyncio.run(main(tasks))

## Extract data from Azure SQL Database to Spark Data Frame

> df = glueContext.read.format("jdbc").option("driver", source_jdbc_driver_name).option("url", source_db_url) \
>             .option("dbtable", query).option("user", source_db_username).option("password", source_db_password) \
>             .option("partitionColumn", partition_column) \
>             .option("numPartitions", num_partitions) \
>             .option("lowerBound", str(lower_bound)) \
>             .option("upperBound", str(upper_bound)) \
>             .load()

## Load data from Spark Data Frame to Snowflake Staging

> df.write.format(SNOWFLAKE_SOURCE_NAME).options(**sfOptions) \
>             .option("parallelism", parallelism).option("dbtable", snowflake_table + '_DELTA') \
>             .option("use_parquet_in_write", "true").mode("overwrite").save()

## Merge data from Snowflake Staging to Snowflake Final Table

> merge_table_sql = """
> MERGE INTO %s.%s.%s AS T
> USING (
>   SELECT * FROM %s.%s.%s_DELTA AS S
>   QUALIFY ROW_NUMBER() OVER (PARTITION BY %s ORDER BY %s DESC NULLS LAST) = 1
> ) AS S
> ON %s
> """ % (snowflake_database, snowflake_schema, snowflake_table, snowflake_database, snowflake_schema, snowflake_table,
> concat_key, delta_column, key_predicate)

> update_columns_values = ''
> insert_columns = ''
> insert_values = ''
> for column_name in column_names:
> 	update_columns_values = update_columns_values + "T." + \
> 		column_name + ' = ' + "S." + column_name + ','
> 	insert_columns = insert_columns + column_name + ','
> 	insert_values = insert_values + 'S.' + column_name + ','
> update_columns_values = update_columns_values.rstrip(',')
> insert_columns = insert_columns.rstrip(',')
> insert_values = insert_values.rstrip(',')

> query = merge_table_sql + " WHEN MATCHED THEN UPDATE SET " + update_columns_values \
> 	+ ' WHEN NOT MATCHED THEN INSERT ( ' + insert_columns + ') VALUES (' + insert_values + ');'

> cur.execute(query)

## Log ETL Metrics

> query = """
> INSERT INTO GLUE_ETL_METRICS (
> ROW_ID,
> LAST_RUN,
> DELTA_MODE,
> START_TIME,
> END_TIME,
> ELAPSED_TIME_MILLIS,
> RECORD_COUNT
> )
> VALUES (%s, %s, %s, %s, %s, %s, %s) """
> params = (row_id, resolve_last_run(max_run_value, watermark_advanced), delta_mode, start_time, end_time,
> 	elapsed_millis, record_count)
> 		
> cur.execute(query, params)










