# westeros-foodflow — Progress Tracker

This document tracks implementation progress. The authoritative whole-project lifecycle plan is in `docs/PROJECT_PLAN.md`.

## Master tracker

| Phase | Stage | Major objective | Status | Dependency |
|---|---|---|---|---|
| 0 | Foundation | Local environment, Git, project structure | ✅ Complete | — |
| 1 | Databricks / Medallion | Unity Catalog, managed storage, Bronze/Silver/Gold, Delta, DQ, execution plans | ✅ Complete | Phase 0 |
| 2 | Incremental CSV | Incremental ingestion, `MERGE`, deduplication, idempotency, audit metadata | ✅ Complete / merged | Phase 1 |
| 3 | Relational SQL | Azure SQL + relational ingestion | 🔵 Current | Phase 2 |
| 3A | SQL Foundation + Stage A | SQL schema + 10/100/500 dataset + validation + JDBC + Bronze/Silver | 🔵 Current — Azure SQL provisioned; schema next | Phase 2 |
| 3A2 | Deterministic scaling | Scale to 5K | ⏳ Future | 3A |
| 3B | AI-assisted generation | Scale to ~15K orders | ⏳ Future | 3A2 |
| 4 | Azure Data Factory | Orchestration and Databricks integration | ⏳ Future | 3B |
| 4D | Large-scale dataset | 250K orders / ~2.9M relational rows | ⏳ Future | ADF |
| 5 | Advanced Data Engineering | Performance, optimization, large-volume engineering | ⏳ Future | Phase 4 |
| 6 | Governed Agentic Data Engineering | Specialized agents, bounded execution, validation, monitoring | ⏳ Future | Foundational engineering |

---

## Phase 0 — Project Foundation

- [x] Create local project structure
- [x] Initialize Git repository
- [x] Create initial Git commit
- [x] Create GitHub remote
- [x] Establish feature-branch workflow
- [x] Establish project documentation structure

---

## Phase 1 — Databricks / Medallion Foundation

- [x] Databricks Free Edition
- [x] Unity Catalog
- [x] Catalog/schema design
- [x] Managed volume
- [x] Raw restaurant CSV ingestion
- [x] Bronze Delta
- [x] Silver Delta
- [x] Gold aggregate
- [x] Data-quality checks
- [x] Execution-plan analysis
- [x] Delta table details/history

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
- [x] Recompute Gold aggregate from current Silver state
- [x] Validate Gold row counts against Silver
- [x] Merge feature branch to `main`

Result:

- Batch 2 source rows: 4
- Unique business keys after deduplication: 3
- Silver updates: 1
- Silver inserts: 1
- Silver unchanged: 1
- Final Silver row count: 11
- Replay produced zero additional data changes
- Gold groups: 9
- Gold `restaurant_count` reconciles to Silver row count: 11

---

# Phase 3 — Relational SQL

## Stage 3A — SQL Foundation + Stage A

### Azure SQL foundation

- [x] Create resource group `rg-westeros-foodflow-dev`
- [x] Create SQL logical server `sql-westeros-foodflow-dev`
- [x] Create database `westeros-foodflow`
- [x] Apply Azure SQL Free Offer
- [x] Use serverless General Purpose / Standard-series (Gen5) / 2 vCores / 32 GB
- [x] Disable overage billing
- [x] Keep zone redundancy disabled
- [x] Use locally redundant backup storage
- [x] Keep private endpoint disabled for the learning setup
- [x] Keep identity disabled for the initial setup
- [x] Use service-managed TDE
- [x] Keep minimum TLS at 1.2

### Relational schema

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
- [ ] Add PK/FK/domain constraints
- [ ] Add unique customer email constraint
- [ ] Add FK/access-pattern indexes
- [ ] Add `updated_at` indexes for incremental extraction

### Stage A dataset

- [ ] Generate 10 restaurants
- [ ] Generate 100 customers
- [ ] Generate supporting menu/delivery/payment/review data
- [ ] Generate 500 orders
- [ ] Generate order items
- [ ] Generate order status history
- [ ] Validate all relationships
- [ ] Validate business-rule scenarios
- [ ] Validate order/payment lifecycle consistency

### JDBC and ingestion

- [ ] Verify Databricks → Azure SQL JDBC connectivity
- [ ] Implement SQL → Bronze full load
- [ ] Add SQL ingestion metadata
- [ ] Implement Bronze → Silver
- [ ] Implement data-quality checks
- [ ] Validate Silver state
- [ ] Validate Gold/analytics output
- [ ] Test SQL watermark extraction
- [ ] Test lower/upper watermark boundaries

### Stage 3A completion gate

Stage 3A is complete only when:

- 10-table schema exists and validates
- Stage A data is relationally consistent
- JDBC connectivity is verified
- SQL → Bronze works
- Bronze → Silver works
- Data-quality scenarios are tested
- Watermark extraction is understood and tested
- Required documentation and checkpoint updates are committed

---

## Stage 3A2 — Deterministic scaling to 5K

- [ ] Parameterize dataset sizes
- [ ] Build repeatable deterministic generators
- [ ] Build reusable validation
- [ ] Generate 5K-order dataset
- [ ] Validate relationships at scale
- [ ] Validate data-quality scenarios at scale
- [ ] Document scaling lessons

---

## Stage 3B — AI-assisted generation to ~15K

- [ ] Use AI to assist repetitive generation work
- [ ] Review generated code
- [ ] Generate approximately 15K orders
- [ ] Validate approximately 60 days of natural activity variation
- [ ] Validate master entities that predate the order window
- [ ] Validate all relationships and business rules
- [ ] Document AI-assisted workflow and human approval points

Target:

- 5,000 customers
- 100 restaurants
- 3,000 menu items
- 500 delivery partners
- ~15,000 orders
- ~2–5 order items per order
- ~15,000 payments
- multiple status-history events per applicable order
- ~1,000 restaurant reviews
- ~500 delivery-partner reviews

---

# Phase 4 — Azure Data Factory

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

## Large-scale dataset — ADF phase

- [ ] Generate 25,000 customers
- [ ] Generate 500 restaurants
- [ ] Generate 15,000 menu items
- [ ] Generate 1,000 delivery partners
- [ ] Generate 250,000 orders
- [ ] Generate ~750,000 order items
- [ ] Generate ~250,000 payments
- [ ] Generate ~1,500,000 order-status history rows
- [ ] Generate ~75,000 restaurant reviews
- [ ] Generate ~40,000 delivery-partner reviews
- [ ] Validate approximately 2.9M relational rows
- [ ] Use the large dataset for ADF/orchestration learning

---

# Phase 5 — Advanced Data Engineering

- [ ] Execution plans
- [ ] Shuffle
- [ ] Broadcast joins
- [ ] AQE
- [ ] Data skew
- [ ] Partitioning
- [ ] Small-file problem
- [ ] Predicate pushdown
- [ ] File sizing
- [ ] Delta optimization/clustering concepts
- [ ] Caching
- [ ] Cost/performance trade-offs
- [ ] Operational reliability

---

# Phase 6 — Governed Agentic Data Engineering

- [ ] westeros-foodflow Data Agent
- [ ] westeros-foodflow Ingestion Agent
- [ ] westeros-foodflow Curation/Transformation/Analytics Agent
- [ ] westeros-foodflow Monitoring and Reporting Agent
- [ ] westeros-foodflow Prediction/ML/Analytical Agent
- [ ] Tool permissions
- [ ] Planning boundaries
- [ ] Validation gates
- [ ] Bounded retries
- [ ] Human approval/governance
- [ ] Operational reporting

---

## Documentation workflow

Whenever a stage is completed:

- [ ] Update `docs/PROJECT_PLAN.md`
- [ ] Update `docs/PROGRESS.md`
- [ ] Update `docs/LEARNING_LOG.md`
- [ ] Update `docs/ARCHITECTURE.md` if architecture/state changed
- [ ] Update `docs/DATA_DICTIONARY.md` if schema/data contracts changed
- [ ] Update `docs/DECISIONS.md` if a decision changed or was added
- [ ] Update `docs/RUNBOOK.md` if operating procedures changed
- [ ] Update `docs/AI_AGENT_ROADMAP.md` for AI/agentic scope changes
- [ ] Update the relevant phase checkpoint
- [ ] Review `git diff` and `git status`
- [ ] Commit
- [ ] Push at the agreed milestone

Current milestone decision: Phase 3 checkpoint work is committed locally but is intentionally not pushed until Phase 3 is complete.
