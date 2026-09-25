# westeros-foodflow — Project Plan

## 1. Project Overview

`westeros-foodflow` is a hands-on, end-to-end Azure Data Engineering learning project designed to simulate a production-style modern data platform.

The project progressively integrates batch ingestion, relational databases, cloud storage, distributed processing, Delta Lake, orchestration, streaming, data quality, security, testing, CI/CD, analytics, and AI-assisted/agentic data engineering.

The goal is not only to build the platform, but to understand the engineering concepts behind each component and document design decisions, problems, solutions, and lessons learned.

---

## 2. Primary Learning Objectives

The project provides practical experience with:

- Python
- SQL
- PySpark
- Databricks
- Delta Lake
- Unity Catalog
- Medallion Architecture
- Incremental processing
- `MERGE` and upsert patterns
- Relational SQL ingestion
- Watermark-based incremental extraction
- Data quality and validation
- Data contracts and schema evolution
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
- Performance and cost optimization
- Security and IAM
- Terraform
- Git and GitHub
- CI/CD
- Power BI
- AI-assisted data engineering
- Governed agentic AI for data engineering operations

---

## 3. Learning Strategy

Every major capability follows this progression:

```text
Understand the concept
        ↓
Small manual implementation
        ↓
Validate with controlled scenarios
        ↓
Document the learning
        ↓
Deterministic automation
        ↓
AI-assisted automation
        ↓
Governed agentic workflow
```

AI-generated code must be reviewed, tested, understood, and approved by the human developer before it becomes part of the project.

---

## 4. Target Architecture

```text
                         westeros-foodflow
                                  |
             +--------------------+--------------------+
             |                    |                    |
           BATCH                DATABASE             STREAM
             |                    |                    |
       CSV / JSON / API       Azure SQL / CDC    Event Hubs / Kafka
             |                    |                    |
             +--------------------+--------------------+
                                  |
                         ADF / Airflow
                           orchestration
                                  |
                       +----------+----------+
                       |                     |
                      ADLS                  S3
                       |                     |
                       +----------+----------+
                                  |
                             Databricks
                                  |
                             Bronze Delta
                                  |
                             Silver Delta
                                  |
                         +--------+--------+
                         |                 |
                      PySpark             dbt
                         |                 |
                         +--------+--------+
                                  |
                            Gold / Marts
                                  |
                         +--------+--------+
                         |                 |
                      Power BI         Analytics
```

---

## 5. Current Platform

The current learning environment uses:

- Databricks Free Edition
- Unity Catalog
- Databricks-managed storage
- Databricks-managed volumes
- Managed Delta tables
- PySpark

The attempted direct Azure Storage integration is deferred in the Free Edition environment because of environment-specific authentication/configuration limitations.

Azure SQL is a separate relational-source integration and is now provisioned for Phase 3.

---

# 6. Master Project Tracker

The authoritative whole-project roadmap and stage/task tracker is maintained in [`PROJECT_TRACKER.md`](PROJECT_TRACKER.md).

It intentionally preserves the full learning scope agreed for `westeros-foodflow`, including the current relational SQL work and later stages such as ADF, large-scale engineering, APIs/JSON, dbt, dimensional modeling, streaming, Kafka, Airflow, data quality/observability, data contracts, testing, performance/cost engineering, security/IAM, Terraform/IaC, CI/CD, AWS/multi-cloud, analytics/serving, AI-assisted engineering, and governed agentic data engineering.

The tracker is the source of truth for stage sequencing and completion status. This project plan provides the architectural and learning context; detailed task-level progress belongs in `PROJECT_TRACKER.md`.

### Current execution sequence

```text
Azure SQL
   ↓
10-table schema
   ↓
Stage A — 10 restaurants / 100 customers / 500 orders
   ↓
Relationship + business-rule validation
   ↓
JDBC
   ↓
SQL → Bronze
   ↓
Bronze → Silver
   ↓
Deterministic 5K
   ↓
AI-assisted ~15K
   ↓
ADF
   ↓
250K orders / ~2.9M relational rows
```

# 7. Phase 0 — Project Foundation

Completed:

- Local project structure
- Python virtual environment
- Git repository
- GitHub remote
- Feature-branch workflow
- Initial project documentation
- Learning-first engineering approach

---

# 8. Phase 1 — Databricks / Medallion Foundation

Completed:

- Unity Catalog
- Catalog/schema design
- Managed volume
- Raw CSV ingestion
- Bronze Delta
- Silver Delta
- Gold aggregate
- Data-quality checks
- Delta history
- Execution-plan analysis

---

# 9. Phase 2 — Incremental CSV Ingestion

Completed and merged to `main`.

Key learning:

- Business keys
- Duplicate detection
- Batch deduplication
- Audit metadata
- Delta `MERGE`
- Insert/update/unchanged handling
- Null-safe change detection
- Idempotent replay
- Historical metadata backfill
- Gold recomputation from current Silver state

---

# 10. Phase 3 — Relational SQL Source

## 10.1 Stage 3A — SQL Foundation + Stage A

Current status: **Azure SQL provisioned; schema creation is next.**

Azure resources:

- Resource group: `rg-westeros-foodflow-dev`
- SQL logical server: `sql-westeros-foodflow-dev`
- Database: `westeros-foodflow`
- Region: Central India
- Compute: General Purpose, Serverless, Standard-series (Gen5), 2 vCores, 32 GB
- Azure SQL Free Offer applied
- Zone redundancy: disabled
- Backup storage redundancy: locally redundant
- Overage billing: disabled
- Azure services/resources access: disabled
- Private endpoint: none
- Minimum TLS: 1.2
- Identity: not enabled
- TDE: service-managed key

### Stage A dataset

Create manually:

| Table/domain | Target records |
|---|---:|
| restaurants | 10 |
| customers | 100 |
| orders | 500 |

The supporting relational tables are populated only as required to maintain valid relationships and realistic order lifecycle data.

### Stage 3A sequence

1. Create the 10-table SQL schema.
2. Insert the Stage A data.
3. Validate primary/foreign-key relationships and business rules.
4. Verify JDBC connectivity from Databricks.
5. Implement SQL → Bronze ingestion.
6. Implement Bronze → Silver transformations.
7. Validate data-quality scenarios.
8. Mark Stage 3A complete.

## 10.2 Stage 3A2 — Deterministic Scaling

Scale the validated Stage A design to approximately 5K orders using ordinary deterministic automation.

This stage focuses on:

- parameterized generation
- reusable SQL/templates
- configurable row counts
- repeatable validation
- repeatable test scenarios
- scripted execution

No AI dependency is introduced at this stage.

## 10.3 Stage 3B — AI-assisted Generation

Scale toward the approximately 15K-order dataset.

AI may assist with:

- repetitive data-generation code
- SQL
- validation queries
- scaling
- test-case generation
- documentation

Human review, validation, execution approval, and diagnosis remain mandatory.

Target 15K dataset:

| Table | Target records |
|---|---:|
| customers | 5,000 |
| restaurants | 100 |
| menu_items | 3,000 |
| delivery_partners | 500 |
| orders | ~15,000 |
| order_items | ~2–5 per order |
| payments | ~15,000 |
| order_status_history | multiple events per applicable order |
| restaurant_reviews | ~1,000 |
| delivery_partner_reviews | ~500 |

Orders represent approximately 60 days of naturally varying activity. Master entities may predate the order window.

---

# 11. Phase 4 — Azure Data Factory

ADF is introduced after the 15K dataset has been implemented and validated.

Learning scope:

- Linked services
- Datasets
- Parameters
- Variables
- Copy Activity
- Lookup
- ForEach
- Metadata-driven ingestion
- Triggers
- Retry handling
- Monitoring
- Databricks notebook orchestration

## 11.1 Large-scale dataset

During the ADF phase, introduce the larger relational dataset:

| Table | Initial records |
|---|---:|
| customers | 25,000 |
| restaurants | 500 |
| menu_items | 15,000 |
| delivery_partners | 1,000 |
| orders | 250,000 |
| order_items | ~750,000 |
| payments | ~250,000 |
| order_status_history | ~1,500,000 |
| restaurant_reviews | ~75,000 |
| delivery_partner_reviews | ~40,000 |

This is approximately 2.9 million relational rows.

The large dataset is deliberately deferred until the ADF phase rather than being created immediately after Azure SQL provisioning.

---

# 12. Phase 5 — Advanced Data Engineering

Planned areas:

- Performance engineering
- Execution plans
- Spark optimization
- Shuffle and partitioning
- Broadcast joins
- AQE
- Data skew
- Small-file management
- Predicate pushdown
- Delta optimization/clustering concepts
- Cost/performance trade-offs
- Operational reliability

---

# 13. Phase 6 — Governed Agentic Data Engineering

The eventual agentic layer will be built only after the underlying data-engineering workflows are understood.

Planned specialized agents:

- westeros-foodflow Data Agent
- westeros-foodflow Ingestion Agent
- westeros-foodflow Curation/Transformation/Analytics Agent
- westeros-foodflow Monitoring and Reporting Agent
- westeros-foodflow Prediction/ML/Analytical Agent

Each agent must use:

```text
Goal
  ↓
Plan
  ↓
Tool use
  ↓
Inspect intermediate results
  ↓
Validate
  ↓
Bounded retry/recovery
  ↓
Report
  ↓
Human governance
```

Agents must not receive unrestricted authority over production-like resources.

---

# 14. Dataset and Domain Design

Phase 3 uses ten relational tables:

1. `customers`
2. `restaurants`
3. `menu_items`
4. `orders`
5. `order_items`
6. `payments`
7. `delivery_partners`
8. `order_status_history`
9. `restaurant_reviews`
10. `delivery_partner_reviews`

Important locked design decisions:

- Transactional/entity PKs use `BIGINT IDENTITY`.
- `restaurants.restaurant_id` is a `VARCHAR(20)` business PK.
- `menu_items.menu_item_id` is a globally unique `BIGINT IDENTITY` sole PK.
- `order_items.menu_item_id` references `menu_items` directly.
- Operational timestamps use `DATETIME2(3)`.
- Order/payment totals use `DECIMAL(12,2)`.
- Menu/unit prices use `DECIMAL(10,2)`.
- Boolean flags use `BIT`.
- PK/FK/domain/access-pattern constraints and indexes are part of the design.
- Mutable tables use `created_at` / `updated_at` where appropriate.
- CDC is not introduced initially.

---

# 15. Incremental SQL Strategy

Full load:

```sql
SELECT * FROM dbo.orders;
```

Incremental watermark pattern:

```sql
SELECT *
FROM dbo.orders
WHERE updated_at > @last_watermark
  AND updated_at <= @current_watermark;
```

This captures inserts and updates but does not detect hard deletes.

Boundary tests will include records exactly at the lower and upper watermark timestamps.

Later phases will compare this pattern with soft deletes, Change Tracking, and CDC.

---

# 16. Controlled Data-Quality Scenarios

Phase 3 intentionally includes test cases such as:

- `DELIVERY` with a null `delivery_partner_id`
- `DINE_IN` or `TAKE_AWAY` with a populated delivery partner
- rating outside 1–5
- negative quantity
- unknown `restaurant_id`
- other documented business-rule violations

Business rules are validated in the appropriate data layer rather than over-constraining the source system unnecessarily.

---

# 17. Analytics Design

Restaurant and delivery-partner reviews support monthly historical aggregation:

- average rating
- review count
- rating distribution/trends

Historical monthly metrics are retained.

Order lifecycle history supports distinguishing:

- completed deliveries
- customer cancellations
- payment-failure cancellations

---

# 18. Documentation and Git Workflow

The master tracker in this document is authoritative for project progression.

Whenever a stage is completed:

1. Update `docs/PROJECT_PLAN.md`.
2. Update `docs/PROGRESS.md`.
3. Update `docs/LEARNING_LOG.md`.
4. Update `docs/ARCHITECTURE.md` when architecture/state changes.
5. Update `docs/DATA_DICTIONARY.md` when schemas/data contracts change.
6. Update `docs/DECISIONS.md` when an architectural decision is added or changed.
7. Update `docs/RUNBOOK.md` when operational procedures change.
8. Update `docs/AI_AGENT_ROADMAP.md` when AI/agentic scope or governance changes.
9. Update the relevant phase checkpoint.
10. Review `git diff` and `git status`.
11. Commit the completed stage.
12. Push at the agreed project milestone.

For the current Phase 3 work, the existing decision remains: **Phase 3 checkpoint commits are intentionally not pushed until Phase 3 is complete.**

---

# 19. Current Next Step

**Stage 3A — Create and validate the locked 10-table Azure SQL schema.**

Do not create the 250K-order dataset at this point.
