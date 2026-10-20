# westeros-foodflow Progress Tracker

## Phase 0 — Project Foundation

- [x] Create local project structure
- [x] Initialize Git repository
- [x] Create initial Git commit
- [x] Create GitHub remote
- [x] Push `main` branch
- [x] Create feature branch for incremental ingestion

---

## Phase 1 — Databricks / Delta Lake / Unity Catalog Foundations

- [x] Create FoodFlow catalog
- [x] Create Bronze, Silver, and Gold schemas
- [x] Create managed volume
- [x] Upload raw restaurant CSV
- [x] Create Bronze Delta table
- [x] Create Silver Delta table
- [x] Create Gold aggregate
- [x] Perform data-quality checks
- [x] Inspect execution plan
- [x] Inspect Delta table details
- [x] Inspect Delta history

---

## Phase 2 — Incremental CSV Ingestion

- [x] Create second synthetic CSV batch
- [x] Introduce new records
- [x] Introduce updated records
- [x] Introduce unchanged records
- [x] Introduce duplicate records
- [x] Identify `restaurant_id` as business key
- [x] Detect duplicate business keys
- [x] Deduplicate incoming batch
- [x] Add `_batch_id`
- [x] Add ingestion audit metadata
- [x] Implement Delta `MERGE`
- [x] Implement null-safe change detection
- [x] Validate update behavior
- [x] Validate insert behavior
- [x] Validate unchanged-record behavior
- [x] Validate duplicate handling
- [x] Replay the same batch
- [x] Validate data-level idempotency
- [x] Inspect Delta transaction history
- [x] Perform historical `_batch_id` backfill
- [x] Validate migrated batch metadata
- [x] Recompute Gold aggregate from current Silver state
- [x] Validate Gold row counts against Silver

### Incremental ingestion result

Batch 2 contained 4 source rows:

- 1 updated record
- 1 new record
- 1 unchanged record
- 1 exact duplicate

After deduplication:

- Source rows: 4
- Unique business keys: 3
- Silver updates: 1
- Silver inserts: 1
- Silver unchanged: 1
- Silver final row count: 11

The replay produced zero additional data changes, demonstrating data-level idempotency.

### Batch metadata result

- `20260923_01`: 9 historical records
- `20260924_02`: 2 records last changed by the incremental batch
- `NULL`: 0 records

`_batch_id` currently represents the batch that last modified the current Silver row.

### Gold result

- Silver current-state rows: 11
- Gold groups: 9
- Sum of Gold `restaurant_count`: 11

Gold is recomputed from Silver because it represents derived aggregate state rather than row-level source state.

---

## Phase 3 — Relational SQL Source

- [ ] Set up SQL Server / Azure SQL
- [ ] Create source restaurant tables
- [ ] Implement full load
- [ ] Implement watermark-based incremental ingestion
- [ ] Compare watermarking with CDC

## Phase 4 — Azure Data Factory

- [ ] Linked services
- [ ] Datasets
- [ ] Parameters
- [ ] Variables
- [ ] Copy Activity
- [ ] Lookup
- [ ] ForEach
- [ ] Metadata-driven ingestion
- [ ] Triggers
- [ ] Retry handling
- [ ] Monitoring
- [ ] Databricks notebook orchestration

## Phase 5 — CDC

- [ ] Insert handling
- [ ] Update handling
- [ ] Delete handling
- [ ] CDC ingestion to ADLS / Delta
- [ ] CDC MERGE patterns

## Phase 6 — Azure ADLS Gen2

- [ ] Storage account
- [ ] Container
- [ ] Hierarchical namespace
- [ ] RBAC
- [ ] Managed identity / access connector
- [ ] Databricks to ADLS integration

## Phase 7 — REST API / JSON

- [ ] API authentication
- [ ] Pagination
- [ ] Rate limits
- [ ] Nested JSON
- [ ] Schema evolution
- [ ] Incremental API ingestion

## Phase 8 — AWS S3 / Multi-cloud

- [ ] S3
- [ ] IAM
- [ ] Cross-cloud access
- [ ] S3 to Databricks
- [ ] ADLS to Databricks

## Phase 9 — dbt

- [ ] dbt setup
- [ ] Staging models
- [ ] Intermediate models
- [ ] Mart models
- [ ] `ref()`
- [ ] Incremental models
- [ ] Tests
- [ ] Documentation
- [ ] Lineage

## Phase 10 — Dimensional Modeling

- [ ] Fact tables
- [ ] Dimension tables
- [ ] Grain
- [ ] Natural keys
- [ ] Surrogate keys
- [ ] SCD Type 1
- [ ] SCD Type 2
- [ ] FoodFlow star schema

## Phase 11 — Streaming

- [ ] Azure Event Hubs
- [ ] Databricks Structured Streaming
- [ ] Streaming Bronze
- [ ] Streaming Silver
- [ ] Streaming Gold
- [ ] Kafka concepts
- [ ] Kafka implementation

## Phase 12 — Streaming Engineering

- [ ] Event time
- [ ] Processing time
- [ ] Watermarks
- [ ] Late data
- [ ] Out-of-order events
- [ ] Windows
- [ ] Stateful processing
- [ ] Checkpoints
- [ ] Streaming deduplication
- [ ] Delivery guarantees

## Phase 13 — Airflow

- [ ] Local Airflow setup
- [ ] DAGs
- [ ] Tasks
- [ ] Dependencies
- [ ] Scheduling
- [ ] Sensors
- [ ] Retries
- [ ] Backfills
- [ ] Parameters
- [ ] Connections
- [ ] Variables
- [ ] Databricks orchestration
- [ ] Monitoring

## Phase 14 — Data Quality / Observability

- [ ] Freshness
- [ ] Volume
- [ ] Null checks
- [ ] Duplicate checks
- [ ] Schema changes
- [ ] Failed-record handling
- [ ] Pipeline duration
- [ ] Late data
- [ ] Throughput
- [ ] Data drift

## Phase 15 — Data Contracts / Schema Evolution

- [ ] Schema enforcement
- [ ] Schema evolution
- [ ] Backward compatibility
- [ ] Breaking changes
- [ ] Non-breaking changes

## Phase 16 — Testing

- [ ] Pytest unit tests
- [ ] Integration tests
- [ ] Data-quality tests
- [ ] dbt tests
- [ ] Pipeline tests

## Phase 17 — Performance / Cost

- [ ] Execution plans
- [ ] Shuffle
- [ ] Broadcast joins
- [ ] AQE
- [ ] Data skew
- [ ] Partitioning
- [ ] Small-file problem
- [ ] Predicate pushdown
- [ ] File sizing
- [ ] Delta optimization / clustering concepts
- [ ] Caching
- [ ] Cost/performance tradeoffs

## Phase 18 — Security

- [ ] Entra ID
- [ ] RBAC
- [ ] Managed identity
- [ ] Key Vault
- [ ] AWS IAM
- [ ] Roles and policies
- [ ] STS
- [ ] Secret management

## Phase 19 — Terraform / IaC

- [ ] Providers
- [ ] Resources
- [ ] Variables
- [ ] Outputs
- [ ] State
- [ ] Modules
- [ ] Plan
- [ ] Apply

## Phase 20 — Git / CI/CD

- [ ] Feature branches
- [ ] Pull requests
- [ ] GitHub Actions
- [ ] Automated tests
- [ ] dbt tests
- [ ] Build validation
- [ ] Deployment automation

## Phase 21 — Power BI / Serving

- [ ] Gold to Power BI
- [ ] Restaurant analytics
- [ ] Customer analytics
- [ ] Order analytics
- [ ] Delivery analytics
- [ ] Rating trends

## Phase 22 — AI / Agentic AI

- [ ] SQL assistant
- [ ] Data-quality assistant
- [ ] Pipeline documentation assistant
- [ ] PySpark coding assistant
- [ ] Pipeline monitoring agent
- [ ] Delta history/log analysis agent
- [ ] Automated diagnosis/recommendation workflow


---

# Phase 3A — SQL → Bronze Completion Addendum — 2026-09-26

## Completed

- [x] Azure SQL environment
- [x] Ten-table normalized schema
- [x] Schema validation: tables, columns/types, PKs, FKs, indexes, constraints
- [x] Stage A deterministic relational dataset
- [x] Relationship/business validation
- [x] Local Python/ODBC connectivity
- [x] Databricks JDBC connectivity
- [x] SQL source schema discovery
- [x] SQL → Bronze for all ten tables
- [x] Standard SQL Bronze metadata
- [x] Restaurant historical-source preservation
- [x] Source/Bronze row-count validation

## SQL → Bronze batch

`stage3a_sql_full_20260926`

| Table | SQL rows | Bronze SQL rows |
|---|---:|---:|
| customers | 100 | 100 |
| restaurants | 10 | 10 SQL-originated rows; 9 historical CSV-only rows retained |
| menu_items | 78 | 78 |
| orders | 500 | 500 |
| order_items | 1,515 | 1,515 |
| payments | 500 | 500 |
| delivery_partners | 20 | 20 |
| order_status_history | 2,808 | 2,808 |
| restaurant_reviews | 66 | 66 |
| delivery_partner_reviews | 23 | 23 |

## Locked metadata

```text
_ingested_at
_ingestion_date
_source_system
_source_file
_batch_id
```

For SQL/JDBC: `_source_system=azure_sql`, `_source_file=NULL`, `_batch_id=stage3a_sql_full_20260926`.

## Next

**Bronze → Silver.** First define source precedence/canonicalization for the mixed-source `restaurants` Bronze state.


---

## Phase 3 — Relational SQL — 2026-09-26 architecture checkpoint

### Completed

- [x] 3A — Azure SQL foundation and normalized 10-table schema
- [x] 3B — Stage A relational dataset
- [x] 3C — Databricks/JDBC connectivity
- [x] 3D — SQL → Landing → Bronze
- [x] Architecture review after 3E failure
- [x] Landing → Bronze → Silver → Gold architecture locked
- [x] Silver Decisions 6–22 locked
- [x] Gold Decisions 23–33 locked
- [x] Control Plane/Orchestration Decisions 34–43 locked

### Current

- [ ] 3E — Bronze → Silver implementation and validation

### Future

- [ ] 3F — deterministic Stage A2 scaling (~5K)
- [ ] 3G — AI-assisted Stage B scaling (~15K)
- [ ] 3H — ADF introduction
- [ ] 3I — large-scale workload (~250K orders)

**Resume checkpoint:** `FOODFLOW-2026-09-26-PHASE3-3E-ARCHITECTURE-LOCKED`

Do not repeat 3A–3D. Do not begin ADF design before the planned ADF learning stage.
