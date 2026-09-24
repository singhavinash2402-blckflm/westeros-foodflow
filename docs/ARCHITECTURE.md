# FoodFlow — Architecture

## 1. Architecture Overview

FoodFlow is designed as a modern data engineering platform using a layered Medallion architecture.

The initial implementation is being developed in Databricks Free Edition. Cloud-native storage, orchestration, streaming, and multi-cloud capabilities will be introduced progressively.

The target architecture is:

```text
                         FOODFLOW
                            |
       +--------------------+--------------------+
       |                    |                    |
     BATCH                DATABASE             STREAM
       |                    |                    |
 CSV / JSON / API       SQL / CDC        Event Hubs / Kafka
       |                    |                    |
       +--------------------+--------------------+
                            |
                     ADF / Airflow
                       orchestration
                            |
                  +---------+---------+
                  |                   |
                 ADLS                 S3
                  |                   |
                  +---------+---------+
                            |
                       Databricks
                            |
                       Bronze Delta
                            |
                       Silver Delta
                            |
                  +---------+---------+
                  |                   |
                PySpark              dbt
                  |                   |
                  +---------+---------+
                            |
                       Gold / Marts
                            |
                  +---------+---------+
                  |                   |
               Power BI           Analytics
```

---

## 2. Current Architecture

The current hands-on implementation is intentionally smaller:

```text
CSV Files
    |
    v
Databricks Managed Volume
    |
    v
Bronze Delta
    |
    v
Silver Delta
    |
    v
Gold Delta
    |
    v
Analytics / Validation
```

Current platform components:

- Databricks Free Edition
- Unity Catalog
- FoodFlow catalog
- FoodFlow schemas
- Databricks-managed volume
- Delta Lake
- PySpark
- Managed Delta tables

---

## 3. Medallion Architecture

### Bronze

Bronze represents the raw ingestion layer.

Responsibilities:

- Preserve source data
- Maintain source-level structure
- Support replay/reprocessing
- Provide an ingestion boundary

Current source:

- CSV files

---

### Silver

Silver represents the cleaned and standardized layer.

Responsibilities:

- Data type normalization
- Data cleaning
- Validation
- Deduplication where appropriate
- Business-rule transformations
- Standardized schema

---

### Gold

Gold represents business-ready analytical data.

Responsibilities:

- Aggregations
- Business metrics
- Analytical datasets
- Reporting-ready structures

---

## 4. Unity Catalog

Unity Catalog provides the governance hierarchy:

```text
Catalog
  |
  +-- Schema
       |
       +-- Tables
       |
       +-- Volumes
```

FoodFlow uses a dedicated catalog and schemas to keep the project logically isolated.

---

## 5. Incremental Processing Architecture

The next implementation will extend the current architecture:

```text
CSV Batch 1
     |
     v
Bronze
     |
     v
Silver
     |
     v
Gold

CSV Batch 2
     |
     v
Bronze
     |
     v
Deduplication
     |
     v
MERGE
     |
     v
Silver
     |
     v
Gold
```

The second batch will contain:

- New records
- Updated records
- Duplicate records

The business key will be used to identify existing entities.

Delta `MERGE` will be used to apply inserts and updates.

---

## 6. Long-Term Batch Architecture

The planned cloud architecture is:

```text
Sources
   |
   +-- CSV
   +-- SQL
   +-- REST APIs
   +-- S3
   +-- Other sources
   |
   v
Orchestration
   |
   +-- Azure Data Factory
   +-- Airflow
   |
   v
Cloud Storage
   |
   +-- ADLS Gen2
   +-- Amazon S3
   |
   v
Databricks
   |
   +-- Bronze
   +-- Silver
   +-- Gold
   |
   +-- PySpark
   +-- dbt
   |
   v
Serving
   |
   +-- Power BI
   +-- Analytics
```

---

## 7. Streaming Architecture

The planned streaming architecture is:

```text
Event Producer
      |
      v
Event Hubs / Kafka
```
      |
      v
Databricks Structured Streaming
      |
      v
Streaming Bronze
      |
      v
Streaming Silver
      |
      v
Streaming Gold

Important streaming concepts to be implemented:

* Event time
* Processing time
* Watermarks
* Late-arriving events
* Out-of-order events
* Stateful processing
* Checkpoints
* Deduplication
* Delivery guarantees

---

## 8. Cross-Cutting Engineering Capabilities

The architecture will eventually include:

### Governance

* Unity Catalog
* Data lineage
* Access control

### Data Quality

* Null validation
* Duplicate detection
* Volume checks
* Freshness checks
* Schema checks
* Business-rule validation

### Reliability

* Idempotency
* Retry handling
* Checkpointing
* Failure recovery

### Security

* Azure RBAC
* Managed identity
* AWS IAM
* Secrets management
* No credentials in Git

### Engineering

* Automated testing
* CI/CD
* Infrastructure as Code
* Performance monitoring
* Cost optimization

### AI

* Coding assistance
* Documentation assistance
* Data-quality analysis
* Pipeline diagnostics
* Operational agents
