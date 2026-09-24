# FoodFlow

FoodFlow is a hands-on end-to-end data engineering project designed to simulate a production-style modern data platform.

## Goals

The project covers:

- Python
- SQL
- PySpark
- Databricks
- Delta Lake
- Unity Catalog
- Medallion Architecture
- Incremental Data Processing
- Azure Data Factory
- Azure Data Lake Storage Gen2
- SQL Server / Azure SQL
- CDC
- REST APIs
- AWS S3
- dbt
- Dimensional Modeling
- Streaming
- Airflow
- Data Quality
- Data Contracts
- Testing
- Performance and Cost Optimization
- Security and IAM
- Terraform
- Git and CI/CD
- Power BI
- AI-assisted Data Engineering
- Agentic AI for Data Engineering Operations

## Current Platform

The initial hands-on implementation is being developed using:

- Databricks Free Edition
- Unity Catalog
- Databricks-managed storage
- Delta Lake
- PySpark

Azure ADLS Gen2 and other cloud services will be introduced in later phases.

## Current Phase

**Incremental CSV Processing**

The next implementation will introduce:

- New records
- Updated records
- Duplicate records
- Deduplication
- Business keys
- Delta MERGE
- Idempotency
- Batch/audit metadata
- Validation
- Delta history

## Repository Structure

```text
docs/        Project documentation
notebooks/   Databricks notebooks
src/         Python source code
tests/       Automated tests
scripts/     Utility scripts