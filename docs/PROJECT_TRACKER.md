# Westeros FoodFlow — Master Project Tracker

**Project:** `westeros-foodflow`
**Purpose:** Authoritative whole-project implementation and learning tracker.

This document is the master roadmap for the entire Westeros FoodFlow learning project. It deliberately includes both the **current implementation stages** and the **later learning stages** already agreed for the project. A phase being listed does not mean it should be implemented immediately.

## How to use this tracker

The project follows this progression:

```text
Understand manually
      ↓
Deterministic automation
      ↓
AI-assisted automation
      ↓
Governed agentic workflows
```

For every stage:

1. Learn the underlying concept.
2. Implement a small, understandable example.
3. Validate the result.
4. Introduce realistic edge/failure cases.
5. Test and document the behavior.
6. Optimize where appropriate.
7. Automate repetitive work.
8. Introduce AI assistance only after the underlying engineering is understood.

When a stage is completed, update the relevant project documentation, update this tracker, create/update the appropriate checkpoint, review the Git diff, commit the work, and push according to the current phase Git workflow.

---

## Master roadmap

| Phase | Stage | Major objective | Status | Dependency |
|---|---|---|---|---|
| 0 | Foundation | Local environment, Git, project structure, engineering workflow | ✅ Complete | — |
| 1 | Databricks / Medallion | Unity Catalog, managed storage, Bronze/Silver/Gold, Delta, DQ, execution plans | ✅ Complete | Phase 0 |
| 2 | Incremental CSV | Incremental ingestion, MERGE, deduplication, idempotency, audit metadata | ✅ Complete / merged | Phase 1 |
| 3 | Relational SQL | Azure SQL + relational source ingestion | 🔵 Current | Phase 2 |
| 3A | SQL Foundation + Stage A | Schema + 10 restaurants / 100 customers / 500 orders + validation + JDBC + Bronze/Silver | 🔵 Current | Phase 2 |
| 3A2 | Deterministic scaling | Scale the validated design to approximately 5K orders | ⏳ Future | 3A |
| 3B | AI-assisted generation | AI-assisted generation and validation to approximately 15K orders | ⏳ Future | 3A2 |
| 4 | Azure Data Factory | Orchestration, parameters, metadata-driven pipelines, monitoring | ⏳ Future | 3B |
| 4D | Large-scale dataset | Introduce the 250K-order / ~2.9M-row relational workload | ⏳ Future | ADF implementation |
| 5 | Advanced Data Engineering | Spark/Delta performance, optimization, scale, operational engineering | ⏳ Future | Phase 4 |
| 6 | APIs / JSON | REST APIs, pagination, rate limits, nested JSON, incremental API ingestion | ⏳ Future | Foundational batch engineering |
| 7 | dbt + Dimensional Modeling | dbt, marts, facts/dimensions, star schema, SCD | ⏳ Future | Phase 5 |
| 8 | Streaming Fundamentals | Event Hubs, Structured Streaming, streaming Medallion architecture | ⏳ Future | Phase 5 |
| 9 | Kafka + Streaming Engineering | Kafka, event semantics, watermarks, state, checkpoints, delivery guarantees | ⏳ Future | Phase 8 |
| 10 | Airflow | DAGs, scheduling, sensors, retries, backfills, external orchestration | ⏳ Future | Core orchestration knowledge |
| 11 | Data Quality / Observability | Freshness, volume, drift, pipeline health, operational monitoring | ⏳ Future | Phases 4–10 progressively |
| 12 | Data Contracts / Schema Evolution | Contracts, compatibility, schema enforcement/evolution | ⏳ Future | Data quality foundations |
| 13 | Testing | Unit, integration, data-quality, pipeline and dbt testing | ⏳ Future | Progressive |
| 14 | Performance / Cost Engineering | Shuffle, AQE, skew, partitioning, small files, Delta optimization, cost tradeoffs | ⏳ Future | Phase 5 + larger workloads |
| 15 | Security / IAM | Entra ID, RBAC, managed identity, Key Vault, AWS IAM, secrets | ⏳ Future | Cloud services |
| 16 | Terraform / Infrastructure as Code | Providers, resources, variables, state, modules, plan/apply | ⏳ Future | Azure/cloud resources |
| 17 | Git / CI/CD | Feature branches, PRs, automated tests, build/deployment validation | ⏳ Future | Git foundation + project maturity |
| 18 | AWS / Multi-cloud | S3, IAM, cross-cloud ingestion, architecture portability | ⏳ Future | Cloud fundamentals |
| 19 | Analytics / Serving | Power BI and business-facing analytical datasets | ⏳ Future | Gold/marts |
| 20 | AI-assisted Data Engineering | SQL, PySpark, DQ, documentation, repetitive engineering assistance | ⏳ Future | Foundational engineering |
| 21 | Governed Agentic Data Engineering | Planning, tools, validation, bounded execution, retry, monitoring, human governance | ⏳ Future | Foundational + AI-assisted stages |

---

# Phase 3 — Relational SQL: detailed execution tracker

This is the current implementation path. Do not skip ahead to the larger datasets or ADF until the preceding stage is validated.

## Stage 3A — SQL Foundation + Stage A

### 3A.1 Azure SQL foundation

- [x] Create resource group `rg-westeros-foodflow-dev`
- [x] Create Azure SQL logical server `sql-westeros-foodflow-dev`
- [x] Create database `westeros-foodflow`
- [x] Apply Azure SQL Free Offer
- [x] Configure server/database for the cost-conscious learning environment

### 3A.2 Relational schema

- [ ] Create `customers`
- [ ] Create `restaurants`
- [ ] Create `menu_items`
- [ ] Create `orders`
- [ ] Create `order_items`
- [ ] Create `payments`
- [ ] Create `delivery_partners`
- [ ] Create `order_status_history`
- [ ] Create `restaurant_reviews`
- [ ] Create `delivery_partner_reviews`
- [ ] Add primary keys
- [ ] Add foreign keys
- [ ] Add uniqueness/domain constraints
- [ ] Add access-pattern indexes
- [ ] Add `updated_at` indexes for incremental extraction

### 3A.3 Stage A dataset

- [ ] Create 10 restaurants
- [ ] Create 100 customers
- [ ] Create menu items
- [ ] Create delivery partners
- [ ] Create 500 orders
- [ ] Create order items
- [ ] Create payments
- [ ] Create order status history
- [ ] Create restaurant reviews
- [ ] Create delivery partner reviews

### 3A.4 Relationship and business-rule validation

- [ ] Validate customer → order relationships
- [ ] Validate restaurant → menu item relationships
- [ ] Validate restaurant → order relationships
- [ ] Validate order → order item relationships
- [ ] Validate order → payment relationships
- [ ] Validate order → status history relationships
- [ ] Validate review relationships
- [ ] Validate DELIVERY / delivery-partner rules
- [ ] Validate DINE_IN / TAKE_AWAY delivery-partner rules
- [ ] Validate rating range
- [ ] Validate positive quantities and monetary values
- [ ] Validate controlled bad-data scenarios

### 3A.5 JDBC connectivity

- [ ] Establish Databricks → Azure SQL JDBC connectivity
- [ ] Validate authentication approach used by the learning environment
- [ ] Read a source table through JDBC
- [ ] Document connection configuration without committing secrets

### 3A.6 SQL → Bronze

- [ ] Define SQL ingestion metadata
- [ ] Implement initial/full extraction
- [ ] Preserve source relational structure
- [ ] Add `_ingested_at`
- [ ] Add `_ingestion_date`
- [ ] Add `_source_system`
- [ ] Add `_batch_id`
- [ ] Validate Bronze counts against SQL

### 3A.7 Bronze → Silver

- [ ] Standardize types
- [ ] Apply relational/business validation
- [ ] Handle controlled bad records
- [ ] Validate referential integrity in the curated layer
- [ ] Establish Silver tables for the relational domain

### 3A.8 Stage 3A completion gate

Stage 3A is complete only when:

- [ ] Stage A dataset is loaded and validated
- [ ] JDBC is repeatably working
- [ ] SQL → Bronze is validated
- [ ] Bronze → Silver is validated
- [ ] Incremental strategy is documented
- [ ] Project documentation/checkpoint is updated
- [ ] Git changes are committed

---

## Stage 3A2 — Deterministic scaling to 5K

- [ ] Design deterministic scaling rules from Stage A
- [ ] Preserve referential integrity
- [ ] Preserve realistic distributions
- [ ] Generate approximately 5K orders
- [ ] Scale related entities consistently
- [ ] Validate row counts and relationships
- [ ] Validate duplicate/key constraints
- [ ] Validate business-rule distributions
- [ ] Document deterministic generation approach

**Important:** This stage is ordinary deterministic automation. AI is not required for the core generation logic.

---

## Stage 3B — AI-assisted generation to ~15K

- [ ] Define generation requirements and constraints
- [ ] Use AI assistance to accelerate repetitive generation-code development
- [ ] Review generated code manually
- [ ] Generate approximately 15K orders
- [ ] Generate related records consistently
- [ ] Run automated validation
- [ ] Introduce controlled invalid scenarios
- [ ] Compare generated output against business rules
- [ ] Document where AI helped and where human validation remained necessary

**Important:** AI assistance does not replace deterministic validation or human review.

---

# Phase 4 — ADF and large-scale relational engineering

## ADF fundamentals

- [ ] Linked services
- [ ] Datasets
- [ ] Pipelines
- [ ] Parameters
- [ ] Variables
- [ ] Copy Activity
- [ ] Lookup
- [ ] ForEach
- [ ] Metadata-driven ingestion
- [ ] Triggers
- [ ] Retry handling
- [ ] Monitoring
- [ ] Databricks orchestration

## Large-scale dataset

Introduce the large workload during the ADF phase, not during initial SQL provisioning:

| Table | Target initial records |
|---|---:|
| `customers` | 25,000 |
| `restaurants` | 500 |
| `menu_items` | 15,000 |
| `delivery_partners` | 1,000 |
| `orders` | 250,000 |
| `order_items` | ~750,000 |
| `payments` | ~250,000 |
| `order_status_history` | ~1,500,000 |
| `restaurant_reviews` | ~75,000 |
| `delivery_partner_reviews` | ~40,000 |

Approximate total: **~2.9 million relational rows**.

---

# Phase 5 — Advanced Data Engineering

- [ ] Execution-plan analysis at larger scale
- [ ] Spark partitioning
- [ ] Shuffle analysis
- [ ] Broadcast joins
- [ ] AQE
- [ ] Data skew
- [ ] Small-file problem
- [ ] Predicate pushdown
- [ ] File sizing
- [ ] Delta optimization / clustering concepts
- [ ] Caching
- [ ] Cost/performance trade-offs
- [ ] Large-volume operational patterns

---

# Phase 6 — APIs / JSON

- [ ] REST API fundamentals
- [ ] Authentication
- [ ] Pagination
- [ ] Rate limits
- [ ] Nested JSON
- [ ] Schema evolution
- [ ] Incremental API ingestion
- [ ] API failure/retry handling

---

# Phase 7 — dbt + Dimensional Modeling

- [ ] dbt setup
- [ ] Staging models
- [ ] Intermediate models
- [ ] Mart models
- [ ] `ref()`
- [ ] Incremental models
- [ ] dbt tests
- [ ] Documentation
- [ ] Lineage
- [ ] Fact tables
- [ ] Dimension tables
- [ ] Grain
- [ ] Natural vs surrogate keys
- [ ] Star schema
- [ ] SCD Type 1
- [ ] SCD Type 2

---

# Phase 8 — Streaming Fundamentals

- [ ] Event Hubs concepts
- [ ] Structured Streaming concepts
- [ ] Streaming Bronze
- [ ] Streaming Silver
- [ ] Streaming Gold
- [ ] Batch vs streaming architecture
- [ ] Event time
- [ ] Processing time
- [ ] Basic checkpointing

---

# Phase 9 — Kafka + Streaming Engineering

- [ ] Kafka architecture
- [ ] Topics
- [ ] Partitions
- [ ] Producers
- [ ] Consumers
- [ ] Consumer groups
- [ ] Offsets
- [ ] Kafka → Spark ingestion
- [ ] Watermarks
- [ ] Late/out-of-order events
- [ ] Windows
- [ ] Stateful processing
- [ ] Streaming deduplication
- [ ] Delivery guarantees / semantics
- [ ] Checkpoint/recovery behavior
- [ ] Near-real-time FoodFlow analytics

---

# Phase 10 — Airflow

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
- [ ] Compare Airflow vs ADF vs Databricks Workflows

---

# Phase 11 — Data Quality / Observability

- [ ] Freshness checks
- [ ] Volume checks
- [ ] Null checks
- [ ] Duplicate checks
- [ ] Referential-integrity checks
- [ ] Schema-change detection
- [ ] Failed-record handling
- [ ] Pipeline duration
- [ ] Throughput
- [ ] Data drift
- [ ] Operational dashboards/alerts
- [ ] Lineage and run metadata

---

# Phase 12 — Data Contracts / Schema Evolution

- [ ] Schema enforcement
- [ ] Schema evolution
- [ ] Backward compatibility
- [ ] Breaking changes
- [ ] Non-breaking changes
- [ ] Contract validation
- [ ] Contract ownership/versioning concepts

---

# Phase 13 — Testing

- [ ] Pytest unit tests
- [ ] Integration tests
- [ ] Data-quality tests
- [ ] Pipeline tests
- [ ] dbt tests
- [ ] Regression testing
- [ ] Test data strategy

---

# Phase 14 — Performance / Cost Engineering

- [ ] Execution plans
- [ ] Shuffle
- [ ] Broadcast joins
- [ ] AQE
- [ ] Data skew
- [ ] Partitioning
- [ ] Small files
- [ ] Predicate pushdown
- [ ] File sizing
- [ ] Delta optimization / clustering concepts
- [ ] Caching
- [ ] Cost/performance trade-offs
- [ ] Workload sizing

---

# Phase 15 — Security / IAM

- [ ] Microsoft Entra ID
- [ ] Azure RBAC
- [ ] Managed identity
- [ ] Key Vault
- [ ] Secret management
- [ ] AWS IAM
- [ ] Roles and policies
- [ ] STS / temporary credentials concepts
- [ ] Least-privilege design

---

# Phase 16 — Terraform / Infrastructure as Code

- [ ] Terraform providers
- [ ] Resources
- [ ] Variables
- [ ] Outputs
- [ ] State
- [ ] Modules
- [ ] Plan
- [ ] Apply
- [ ] Azure infrastructure provisioning
- [ ] Databricks resource management
- [ ] Environment separation
- [ ] CI/CD integration

---

# Phase 17 — Git / CI/CD

- [x] Feature branches
- [x] Pull-request workflow used for Phase 2
- [ ] Automated tests
- [ ] Build validation
- [ ] GitHub Actions
- [ ] Deployment automation
- [ ] Environment promotion concepts

---

# Phase 18 — AWS / Multi-cloud

- [ ] Amazon S3
- [ ] AWS IAM
- [ ] Cross-cloud access concepts
- [ ] S3 → Databricks
- [ ] ADLS → Databricks
- [ ] Databricks across cloud providers
- [ ] Cloud-specific identity/networking differences
- [ ] Portable architecture considerations
- [ ] Multi-cloud operational/cost trade-offs

---

# Phase 19 — Analytics / Serving

- [ ] Gold-layer analytical datasets
- [ ] Power BI integration
- [ ] Restaurant analytics
- [ ] Customer analytics
- [ ] Order analytics
- [ ] Delivery analytics
- [ ] Rating trends
- [ ] Monthly rating aggregation
- [ ] Historical analytical metrics

---

# Phase 20 — AI-assisted Data Engineering

- [ ] SQL assistant workflows
- [ ] PySpark coding assistance
- [ ] Data-quality assistant
- [ ] Pipeline documentation assistant
- [ ] Test-case generation assistance
- [ ] Repetitive data-generation assistance
- [ ] Validation-query generation assistance
- [ ] Human review and governance workflow

---

# Phase 21 — Governed Agentic Data Engineering

The agentic stage is intentionally later than the foundational engineering work.

### Planned agents

- [ ] FoodFlow Data Agent
- [ ] FoodFlow Ingestion Agent
- [ ] FoodFlow Curation / Transformation / Analytics Agent
- [ ] Monitoring and Reporting Agent
- [ ] Prediction / ML / Analytical Agent

### Agent capabilities

- [ ] Goal interpretation
- [ ] Planning
- [ ] Tool selection/use
- [ ] Intermediate-result inspection
- [ ] Validation
- [ ] Bounded execution
- [ ] Retry/recovery within limits
- [ ] Reporting
- [ ] Human approval/governance
- [ ] Auditability

---

## Current execution pointer

**Current phase:** Phase 3 — Relational SQL
**Current stage:** Stage 3A — SQL Foundation + Stage A
**Completed:** Azure SQL environment provisioned
**Next task:** Create the locked 10-table relational schema.

The current dataset sequence is intentionally:

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
Stage 3A complete
   ↓
Stage 3A2 — deterministic 5K
   ↓
Stage 3B — AI-assisted ~15K
   ↓
ADF
   ↓
250K orders / ~2.9M relational rows
```

**Rule:** Later phases are planned and tracked here, but implementation only advances when the dependency chain reaches them.
