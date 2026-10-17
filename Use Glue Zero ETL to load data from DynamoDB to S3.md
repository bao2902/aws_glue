# Architecture

<img alt="image" src="https://github.com/user-attachments/assets/7fc3b5df-ee0d-4263-bac6-032852c6724e" />

# Concepts

## DynamoDB table

DynamoDB is AWS’s fully managed, serverless, NoSQL database service built to deliver single-digit millisecond performance at any scale. Unlike traditional relational databases (like PostgreSQL or SQL Server), DynamoDB abstracts away infrastructure management, server provisioning, software patching, and cluster maintenance.

table is the primary organizational container for your data in Amazon DynamoDB—similar to a table in a relational SQL database, but with fundamental structural and architectural differences.

## Glue Zero-ETL

Zero-ETL is a fully managed, serverless capability within AWS designed to replicate data continuously from operational databases and SaaS applications directly into AWS analytics targets—without requiring custom ETL scripts, manual scheduling, or managing Spark clusters.

# Use Glue Zero-ETL to load data from DynamoDB to S3

## Create DynamoDB source

**Create table**

DynamoDB > Tables > Create table > test_orders_data

* Partition key: order_id (String)
* Capacity mode: On-demand
* Point-in-time recovery (PITR): On

**Grant permissions to table**

Permissions > Resource-based policy for table

> {
>   "Version": "2012-10-17",
>   "Statement": [
>     {
>       "Sid": "AllowFullGlueZeroETLAccess",
>       "Effect": "Allow",
>       "Principal": {
>         "Service": "glue.amazonaws.com"
>       },
>       "Action": "dynamodb:*",
>       "Resource": [
>         "arn:aws:dynamodb:us-east-1:481742614791:table/test_orders_data",
>         "arn:aws:dynamodb:us-east-1:481742614791:table/test_orders_data/*"
>       ]
>     }
>   ]
> }

**Create item**

DynamoDB > Explore items > test_orders_data > Create item

> {
>   "order_id": {
>     "S": "ORD-1001"
>   },
>   "amount": {
>     "N": "249.99"
>   },
>   "customer_id": {
>     "S": "CUST-88"
>   },
>   "status": {
>     "S": "COMPLETED"
>   }
> }

<img alt="image" src="https://github.com/user-attachments/assets/6051d4fb-6c3e-47bb-b2eb-4e0bb3e40f92" />

## Configure Glue Data Catalog target

Glue > Zero-ETL integrations > Configure target

Target details
* Data warehouse or catalog: 481742614791
* Target database: src_nhe_insights
* Target IAM role: MyGlueExecutionRole
Source details
* Source principal ARN: arn:aws:iam::481742614791:role/MyGlueExecutionRole
Configure target
* Update resource policy to authorize AWS Glue for inbound integrations on target src_nhe_insights
* Update resource policy to allow arn:aws:iam::481742614791:root to create inbound integrations on target 
* Create S3 bucket glue-zetl-target-481742614791-us-east-1
* Set the S3 Location URI of target src_nhe_insights to s3://glue-zetl-target-481742614791-us-east-1/
* Check for IAM role association with the target
* Check for KMS key
* Check for VPC connection
Target configured successfully
* The selected target now has valid configurations to support zero-ETL integrations. To copy the target ARN and send it to the integration creator, choose the "Copy target ARN" button.

## Create zero-ETL integration

**Create zero-ETL integration**

Glue > Zero-ETL integrations > Create zero-ETL integration

Source details
* Source type: Amazon DynamoDB
* Source connection: test_orders_data 
* Source ARN: arn:aws:glue:us-east-1:481742614791:connection/test_orders_data
Target details
* Target resource: src_nhe_insights 
* Target ARN: arn:aws:glue:us-east-1:481742614791:database/src_nhe_insights
Output settings
* Schema unnesting options: Unnest all fields
* Data partitioning: Use primary keys from DynamoDB tables
* Configure target table name: test_orders_data
Replication settings
* Refresh Interval: 0 days 0 hours 15 minutes (MINIMUM)
Integration details
* Name: dynamodb-test-orders-zeroetl

## Check Athena

<img alt="image" src="https://github.com/user-attachments/assets/c4dce899-13f2-48de-a8dc-db2169bda91e" />
