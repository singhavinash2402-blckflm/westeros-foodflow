# westeros-foodflow — Project Plan

## 1. Project Overview

westeros-foodflow is a hands-on, end-to-end data engineering learning project designed to simulate a production-style modern data platform.

The project will progressively integrate batch ingestion, databases, cloud storage, distributed processing, Delta Lake, orchestration, streaming, data quality, security, testing, CI/CD, analytics, and AI-assisted data engineering.

The goal is not only to build the platform, but to understand the engineering concepts behind each component and document the design decisions, problems, solutions, and lessons learned.

---

## 2. Primary Learning Objectives

westeros-foodflow will provide practical experience with:

- Python
- SQL
- PySpark
- Databricks
- Delta Lake
- Unity Catalog
- Medallion Architecture
- Incremental processing
- `MERGE` and upsert patterns
- Data quality
- Data contracts
- Schema evolution
- Azure Data Factory
- Azure Data Lake Storage Gen2
- SQL Server / Azure SQL
- CDC
- REST APIs and JSON
- AWS S3
- dbt
- Dimensional modeling
- Streaming
- Airflow
- Testing
- Performance optimization
- Security and IAM
- Terraform
- Git and GitHub
- CI/CD
- Power BI
- AI-assisted data engineering
- Agentic AI for data engineering operations

---

## 3. Target Architecture

The long-term FoodFlow architecture will include:

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
                    +-------+-------+
                    |               |
                 PySpark           dbt
                    |               |
                    +-------+-------+
                            |
                       Gold / Marts
                            |
                    +-------+-------+
                    |               |
                 Power BI       Analytics
```

Cross-cutting capabilities:

- Unity Catalog
- Data quality
- Data contracts
- Schema evolution
- Idempotency
- Lineage
- Observability
- Testing
- Security
- IAM/RBAC
- Secrets management
- Performance optimization
- Cost optimization
- Terraform
- Git
- CI/CD
- AI automation

---

## 4. Development Strategy

westeros-foodflow will follow a progressive learning approach:

1. Learn the concept.
2. Implement a small example manually.
3. Validate the result.
4. Document what was learned.
5. Introduce realistic failure cases.
6. Optimize the implementation.
7. Automate repetitive work.
8. Use AI assistance only after understanding the underlying implementation.

AI-generated code must be reviewed, tested, and understood before being incorporated into the project.

---

## 5. Current Platform

The initial implementation uses:

- Databricks Free Edition
- Unity Catalog
- Databricks-managed storage
- Managed volumes
- Delta Lake
- PySpark

Azure ADLS Gen2 integration is intentionally deferred until the appropriate Azure Databricks environment is available.

---

## 6. Major Project Phases

### Phase 1 — Databricks Foundation

- Unity Catalog
- Catalogs and schemas
- Managed volumes
- Raw CSV ingestion
- Bronze Delta
- Silver Delta
- Gold Delta
- Data quality
- Delta history
- Execution plan analysis

### Phase 2 — Incremental Processing

- Multiple source files
- New records
- Updated records
- Duplicate records
- Deduplication
- Business keys
- Delta `MERGE`
- Idempotency
- Batch identifiers
- Audit columns
- Validation

### Phase 3 — Relational Sources

- SQL Server / Azure SQL
- Full loads
- Watermark-based incremental ingestion
- Source metadata
- Incremental extraction

### Phase 4 — Azure Data Factory

- Linked services
- Datasets
- Pipelines
- Parameters
- Variables
- Copy Activity
- Lookup
- ForEach
- Metadata-driven pipelines
- Triggers
- Retry handling
- Monitoring
- Databricks orchestration

### Phase 5 — CDC

- Inserts
- Updates
- Deletes
- CDC versus watermarking
- CDC ingestion
- Delta `MERGE`

### Phase 6 — Azure Data Lake

- ADLS Gen2
- Hierarchical namespace
- RBAC
- Managed identity
- Secure Databricks access

### Phase 7 — APIs and JSON

- REST APIs
- Authentication
- Pagination
- Rate limits
- Nested JSON
- Schema evolution
- Incremental API ingestion

### Phase 8 — AWS and Multi-Cloud

- Amazon S3
- IAM
- Cross-cloud access
- S3 ingestion
- ADLS ingestion
- Multi-cloud architecture

### Phase 9 — dbt and Dimensional Modeling

- dbt models
- Tests
- Documentation
- Lineage
- Incremental models
- Facts
- Dimensions
- Star schema
- SCD Type 1
- SCD Type 2

### Phase 10 — Streaming

- Event Hubs
- Structured Streaming
- Streaming Bronze/Silver/Gold
- Kafka concepts
- Event time
- Processing time
- Watermarks
- Late data
- Stateful processing
- Checkpoints
- Deduplication

### Phase 11 — Airflow

* DAGs
* Tasks
* Dependencies
* Scheduling
* Sensors
* Retries
* Backfills
* Parameters
* Connections
* Variables
* Databricks orchestration
* Monitoring

### Phase 12 — Quality and Observability

* Freshness
* Volume
* Null checks
* Duplicate checks
* Schema changes
* Failed records
* Pipeline duration
* Late data
* Throughput
* Data drift

### Phase 13 — Engineering Practices

* Unit testing
* Integration testing
* Data quality testing
* dbt testing
* CI/CD
* Terraform
* Security
* Secrets management
* Performance optimization
* Cost optimization

### Phase 14 — Analytics and AI

* Power BI
* Gold-layer analytics
* Data engineering assistants
* Data-quality assistants
* Documentation assistants
* PySpark assistants
* Operational AI agents


---

# Phase 3A Current-State Addendum — 2026-09-26

This addendum supersedes any earlier Phase 3 text that says Azure SQL schema validation is the immediate next task. SQL schema, Stage A data, validation, JDBC, and SQL → Bronze are now complete.

## Current sequence

```text
Azure SQL schema
   ↓
Stage A data
   ↓
Relationship/business validation
   ↓
JDBC
   ↓
SQL → Bronze   [COMPLETE]
   ↓
Bronze → Silver [NEXT]
   ↓
Stage A2 — deterministic ~5K
   ↓
Stage B — AI-assisted ~15K
   ↓
ADF
   ↓
250K-order workload
```

## Locked SQL → Bronze rules

- Standard Bronze metadata: `_ingested_at`, `_ingestion_date`, `_source_system`, `_source_file`, `_batch_id`.
- SQL/JDBC rows use `_source_system = azure_sql`.
- SQL/JDBC rows use `_source_file = NULL`; never invent file lineage for a database source.
- Current SQL batch: `stage3a_sql_full_20260926`.
- Existing Bronze `restaurants` history is preserved. SQL reconciliation uses explicit `restaurant_id` matching rather than overwrite.
- Existing historical `_source_file` lineage on restaurant records is preserved.
- Historical CSV-only restaurant rows are not relabeled as Azure SQL.
- First-load SQL tables require an explicit `spark.catalog.tableExists()` safety check before writing.
- Source and Bronze row counts are compared after each full load.
- Databricks `errorifexists` is not used as the safety mechanism because it was unsupported in this environment.

## Current Stage A counts

- restaurants: 10
- customers: 100
- menu_items: 78
- orders: 500
- order_items: 1,515
- payments: 500
- delivery_partners: 20
- order_status_history: 2,808
- restaurant_reviews: 66
- delivery_partner_reviews: 23

## Bronze restaurants result

The pre-existing Bronze `restaurants` table contained 9 historical CSV-only rows. Current Azure SQL Stage A contributes 10 rows. One business key overlaps (`REST-SHJ-001`). The final Bronze state contains 19 restaurant rows: 9 historical CSV-only + 10 SQL-originated.

## JDBC/serverless reliability rule

Azure SQL General Purpose Serverless may auto-pause/resume and produce transient connection failures during resume. Databricks Free Edition public egress IPs can also change and cause firewall authorization failures. Troubleshooting must distinguish transient availability, firewall/IP, authentication, and query/schema errors. Do not enable broad Azure-services access as a shortcut. Add explicit JDBC retry/resiliency properties to the maintained ingestion implementation.

## Next task

Bronze → Silver. The canonical/source-resolution contract is already locked by the 2026-09-26 architecture checkpoint. Implementation now translates those locked rules into executable Silver processing without silently destroying historical lineage.


## 2026-09-26 authoritative Phase 3 state

Phase 3 is complete through **3D — SQL → Landing → Bronze**. The current implementation point is **3E — Bronze → Silver**.

The first 3E implementation exposed source metadata/provenance contamination in mixed-source Bronze data. The project deliberately paused implementation and completed an architecture review rather than applying a narrow patch.

The resulting architecture is locked as:

```text
Landing → Bronze → Silver → Gold
Control / Observability / Orchestration
```

Silver Decisions 6–22, Gold Decisions 23–33, and Control Plane/Orchestration Decisions 34–43 are authoritative. No redesign is required before 3E implementation.

### 3E resume rule

Implement the locked Silver contract against the existing 3D Bronze data. Reopen an architecture decision only if concrete implementation evidence demonstrates a defect or contradiction.
