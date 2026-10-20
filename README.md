# westeros-foodflow

`westeros-foodflow` is a hands-on end-to-end Azure Data Engineering learning project designed to simulate a production-style modern data platform.

## Goals

The project progressively covers:

- Python
- SQL
- PySpark
- Databricks
- Delta Lake
- Unity Catalog
- Medallion Architecture
- Incremental Data Processing
- Relational SQL ingestion
- Azure Data Factory
- Azure Data Lake Storage Gen2
- CDC
- REST APIs and JSON
- AWS S3
- dbt
- Dimensional Modeling
- Streaming
- Airflow
- Data Quality and Observability
- Data Contracts and Schema Evolution
- Testing
- Performance and Cost Optimization
- Security and IAM
- Terraform
- Git and CI/CD
- Power BI
- AI-assisted Data Engineering
- Governed Agentic AI for Data Engineering Operations

## Learning approach

The project follows this progression:

```text
Manual
  ↓
Deterministic automation
  ↓
AI-assisted automation
  ↓
Governed agentic workflows
```

Core engineering concepts are learned and validated before they are automated with AI.

## Current platform

The initial hands-on implementation uses:

- Databricks Free Edition
- Unity Catalog
- Databricks-managed storage
- Managed volumes
- Delta Lake
- PySpark

Direct Azure Storage integration is deferred in the Free Edition environment. Azure SQL/JDBC is introduced as a separate relational-source integration pattern.

## Current phase

**Phase 3 — Relational SQL Source / Stage 3A**

Azure SQL has been provisioned. The next implementation step is to create the locked 10-table relational schema and then build the small Stage A dataset:

- 10 restaurants
- 100 customers
- 500 orders

The implementation sequence is:

```text
Azure SQL
   ↓
Create schema
   ↓
Stage A — 10 restaurants / 100 customers / 500 orders
   ↓
Validate relationships and business rules
   ↓
JDBC connectivity
   ↓
SQL → Bronze
   ↓
Bronze → Silver
   ↓
Stage A2 — deterministic scaling to 5K
   ↓
Stage B — AI-assisted generation to ~15K
   ↓
ADF
   ↓
250K-order / ~2.9M-row dataset
```

## Repository structure

```text
docs/        Project documentation
notebooks/   Databricks notebooks
src/         Python source code
tests/       Automated tests
scripts/     Utility scripts
00_synthetic_data/  Synthetic source datasets
artifacts/   Databricks export/backup artifacts
```

The authoritative master project tracker is maintained in `docs/PROJECT_TRACKER.md`.
