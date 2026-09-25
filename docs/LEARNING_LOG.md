# westeros-foodflow — Learning Log

## 2026-09-24 — Project Foundation

Established the westeros-foodflow project repository and development environment.

### Topics covered

- Python virtual environment
- Git repository setup
- GitHub remote
- Feature-branch workflow
- Project documentation structure
- Databricks-managed storage in Free Edition
- Manual implementation before AI automation

---

## 2026-09-24 — Incremental CSV Ingestion

Implemented a complete small-batch incremental ingestion exercise.

### Concepts practiced

- Business keys
- Duplicate detection
- Source-batch deduplication
- Audit metadata
- Batch identifiers
- Delta Lake `MERGE`
- Insert handling
- Update handling
- Unchanged-record handling
- Null-safe comparison using Spark SQL `<=>`
- Idempotent replay
- Delta transaction history
- Historical metadata migration/backfill
- Derived Gold-table refresh

### Batch design

Batch 2 intentionally contained:

- One updated record
- One new record
- One unchanged record
- One exact duplicate

The business key was `restaurant_id`.

The 4 source rows were reduced to 3 unique business keys before the Silver `MERGE`.

### MERGE behavior

- The Silver table uses the business key to determine whether a record already exists.
- A record is updated only when business attributes differ.
- The `_batch_id` column is excluded from change detection so replaying the same business data with a different processing batch identifier does not cause an unnecessary business-row update.

### Idempotency

The same batch was replayed.

The replay produced:

- 3 source rows
- 0 inserted rows
- 0 updated rows
- 0 additional data changes

This demonstrates data-level idempotency for the implemented `MERGE` pattern.

Delta transaction history can still contain a `MERGE` operation even when that `MERGE` changes zero target rows.

### Historical metadata migration

The original historical Silver records initially had `NULL` `_batch_id` values.

A controlled migration/backfill populated:

- `20260923_01`

for historical records originating from the original source file.

The migration was deliberately scoped to:

- `_batch_id IS NULL`
- `_source_file = 'restaurants_20262309_01.csv'`

This prevented later incremental records from being modified.

### `_batch_id` semantics

The current design uses `_batch_id` to represent the batch that last modified the current Silver row.

It is therefore not a first-ingestion identifier.

If future requirements need both meanings, separate fields can be introduced, for example:

- `_first_batch_id`
- `_last_batch_id`

### Silver vs. Gold update strategy

- Silver contains current-state row-level data and therefore uses Delta `MERGE`.
- Gold contains derived aggregate state and is recomputed from current Silver data.

This avoids incorrectly treating an aggregate table as if it were a source-system row-level table.

### Validation

- Final Silver state: 11 rows
- Final Gold state: 9 aggregate groups
- The sum of Gold `restaurant_count` equals 11, which reconciles with Silver.

### File naming convention

New local synthetic source files use:

`YYYYMMDD_<file-sequence-of-day>.csv`

Example:

- `restaurants_20260923_01.csv`
- `restaurants_20260923_02.csv`

Historical Databricks volume filenames from the earlier exercise are intentionally left unchanged to preserve lineage.


---

## 2026-09-25 — Phase 3 Relational SQL Design and Azure SQL Foundation

Phase 3 introduced the relational source-system learning path.

### Concepts locked

- Relational entity modeling
- Primary and foreign keys
- Business keys versus surrogate keys
- Transactional versus derived data
- Historical transaction snapshots
- Order lifecycle modeling
- Review/event history
- Watermark-based incremental extraction
- SQL source metadata
- Controlled data-quality scenarios

### Relational model

The source model contains ten tables:

- `customers`
- `restaurants`
- `menu_items`
- `orders`
- `order_items`
- `payments`
- `delivery_partners`
- `order_status_history`
- `restaurant_reviews`
- `delivery_partner_reviews`

### Dataset learning progression

The project intentionally avoids jumping directly to a large dataset:

```text
Manual Stage A
10 restaurants / 100 customers / 500 orders
        ↓
Deterministic Stage A2
5K dataset
        ↓
AI-assisted Stage B
~15K orders
        ↓
ADF
250K orders / ~2.9M relational rows
```

This progression separates foundational engineering, ordinary automation, AI-assisted automation, and orchestration at meaningful learning boundaries.

### Azure SQL foundation

Provisioned:

- `rg-westeros-foodflow-dev`
- `sql-westeros-foodflow-dev`
- `westeros-foodflow`

The database uses the Azure SQL Free Offer with serverless General Purpose / Standard-series (Gen5), 2 vCores, and 32 GB.

### Current state

Azure SQL provisioning is complete.

The next learning step is to create the locked relational schema and manually build the Stage A dataset before introducing JDBC ingestion.
