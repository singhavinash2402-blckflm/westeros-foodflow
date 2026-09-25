# westeros-foodflow — Architecture

## 1. Architecture Overview

`westeros-foodflow` is designed as a modern data engineering learning platform using a layered Medallion architecture.

The project is intentionally built progressively. The current implementation uses Databricks Free Edition with Databricks-managed storage. Relational SQL is now introduced as a separate source integration pattern.

Target architecture:

```text
                         westeros-foodflow
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
     BATCH                     DATABASE                   STREAM
       |                          |                          |
 CSV / JSON / API            Azure SQL / CDC          Event Hubs / Kafka
       |                          |                          |
       +--------------------------+--------------------------+
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
                       +----------+----------+
                       |                     |
                    PySpark                 dbt
                       |                     |
                       +----------+----------+
                                  |
                            Gold / Marts
                                  |
                       +----------+----------+
                       |                     |
                    Power BI              Analytics
```

---

## 2. Current Architecture

The current hands-on implementation remains:

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
```

Current platform components:

- Databricks Free Edition
- Unity Catalog
- Databricks-managed storage
- Managed volumes
- Managed Delta tables
- PySpark

The earlier direct Azure Storage integration attempt is deferred in the Free Edition environment because of environment-specific authentication/configuration limitations.

---

## 3. Phase 3 Relational Architecture

Azure SQL is a separate source system:

```text
Azure SQL
    |
    +-- customers
    +-- restaurants
    +-- menu_items
    +-- orders
    +-- order_items
    +-- payments
    +-- delivery_partners
    +-- order_status_history
    +-- restaurant_reviews
    +-- delivery_partner_reviews
    |
    v
JDBC
    |
    v
Databricks Bronze
    |
    v
Silver
    |
    v
Gold / Analytics
```

SQL-specific ingestion metadata is used for the relational source, such as:

- `_ingested_at`
- `_ingestion_date`
- `_source_system`
- `_batch_id`

`_source_file` remains a CSV-specific lineage field and is not required for SQL ingestion.

---

## 4. Medallion Architecture

### Bronze

Bronze represents the ingestion boundary.

Responsibilities:

- Preserve source-oriented data
- Maintain replay/reprocessing capability
- Add technical ingestion metadata
- Preserve source lineage
- Avoid unnecessary business transformations

### Silver

Silver represents cleaned and standardized current-state data.

Responsibilities:

- Data type normalization
- Validation
- Deduplication where appropriate
- Business-rule checks
- Standardized schema
- Incremental maintenance

### Gold

Gold represents business-ready analytical data.

Responsibilities:

- Aggregations
- Business metrics
- Analytical datasets
- Reporting-ready structures

---

## 5. Unity Catalog

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

The existing Databricks objects from earlier phases remain part of the executed lineage. Historical object names are not renamed merely for documentation naming changes.

---

## 6. Phase 3 Dataset Progression

The relational dataset grows deliberately:

```text
Stage A — Manual
10 restaurants
100 customers
500 orders
        |
        v
Relationship + business-rule validation
        |
        v
JDBC + SQL → Bronze → Silver
        |
        v
Stage A2 — Deterministic automation
5K dataset
        |
        v
Stage B — AI-assisted generation
~15K orders
        |
        v
ADF
        |
        v
250K orders / ~2.9M relational rows
```

The large dataset is intentionally deferred until the ADF phase.

---

## 7. Incremental SQL Architecture

Full extraction:

```sql
SELECT * FROM dbo.orders;
```

Watermark-based extraction:

```sql
SELECT *
FROM dbo.orders
WHERE updated_at > @last_watermark
  AND updated_at <= @current_watermark;
```

The initial pattern captures inserts and updates but not hard deletes.

The design explicitly includes boundary testing at the lower and upper watermark timestamps.

Later work compares watermarking with soft deletes, Change Tracking, and CDC.

---

## 8. Long-Term Batch Architecture

```text
Sources
   |
   +-- CSV
   +-- Azure SQL
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

## 9. Streaming Architecture

Planned streaming architecture:

```text
Event Producer
      |
      v
Event Hubs / Kafka
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
```

Important concepts:

- Event time
- Processing time
- Watermarks
- Late-arriving events
- Out-of-order events
- Stateful processing
- Checkpoints
- Deduplication
- Delivery guarantees

---

## 10. Cross-Cutting Engineering Capabilities

### Governance

- Unity Catalog
- Data lineage
- Access control

### Data Quality

- Null validation
- Duplicate detection
- Volume checks
- Freshness checks
- Schema checks
- Business-rule validation

### Reliability

- Idempotency
- Retry handling
- Checkpointing
- Failure recovery

### Security

- Azure RBAC
- Managed identity
- AWS IAM
- Secrets management
- No credentials in Git

### Engineering

- Automated testing
- CI/CD
- Infrastructure as Code
- Performance monitoring
- Cost optimization

### AI

- Coding assistance
- Documentation assistance
- Data-quality analysis
- Pipeline diagnostics
- Governed operational agents
