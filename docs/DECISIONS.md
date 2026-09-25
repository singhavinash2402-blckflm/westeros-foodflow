# westeros-foodflow — Engineering Decisions

## Decision 001 — Use Databricks Free Edition for Initial Learning

**Status:** Accepted

Databricks Free Edition is used for the initial westeros-foodflow implementation.

Azure ADLS integration is deferred until the project reaches the appropriate Azure infrastructure phase.

---

## Decision 002 — Use Databricks-Managed Storage Initially

**Status:** Accepted

Initial Bronze, Silver, and Gold Delta tables use Databricks-managed storage and managed volumes.

External ADLS and AWS S3 storage will be introduced later as part of the multi-cloud architecture.

---

## Decision 003 — Use a Project-local Python Virtual Environment

**Status:** Accepted

Python dependencies are isolated in the project-local `.venv`.

This keeps the westeros-foodflow development environment reproducible and prevents global package conflicts.

---

## Decision 004 — GitHub Is the Project Source of Truth

**Status:** Accepted

Project code, documentation, synthetic test data, and development artifacts are version controlled in Git and pushed to GitHub.

The repository is the backup and source of truth for the learning project.

---

## Decision 005 — Learn Manually Before Automating with AI

**Status:** Accepted

Core data-engineering concepts will first be implemented manually.

AI tools and agents will later be introduced to automate repetitive work, generate boilerplate, and assist with diagnosis and documentation.

Generated code must still be reviewed and tested.

---

## Decision 006 — Use Delta `MERGE` for Incremental Silver Updates

**Status:** Accepted

Silver is treated as current-state row-level data.

The business key is:

```text
restaurant_id
```

Incoming records are deduplicated before the `MERGE`.

The `MERGE`:

- updates existing rows when business attributes change
- inserts new rows
- leaves unchanged rows untouched

Null-safe comparisons using `<=>` are used to avoid incorrect change detection when nullable fields are involved.

---

## Decision 007 — `_batch_id` Represents the Last Modifying Batch

**Status:** Accepted

The current `_batch_id` design identifies the batch that last modified the current Silver row.

It is not a first-ingestion identifier.

Historical rows were migrated with:

```text
20260923_01
```

while the incremental batch used:

```text
20260924_02
```

If first-ingestion lineage is required later, a separate field will be introduced.

---

## Decision 008 — Historical Metadata Is Migrated with a Scoped Backfill

**Status:** Accepted

Historical `_batch_id` values were populated through a controlled migration/backfill rather than treating the operation as a new ingestion batch.

The migration was restricted to rows where:

```text
_batch_id IS NULL
```

and:

```text
_source_file = 'restaurants_20262309_01.csv'
```

This prevented later incremental records from being modified.

The migration was validated after execution.

---

## Decision 009 — Recompute Gold Aggregates from Current Silver State

**Status:** Accepted

Gold aggregate tables are derived state.

For the current westeros-foodflow design, Gold is recomputed and overwritten from Silver after incremental changes.

Silver uses `MERGE` because it represents current row-level entities.

Gold is recomputed because it represents an aggregate projection of Silver.

---

## Decision 010 — Use Date-based Synthetic File Naming

**Status:** Accepted

New local synthetic source files use:

```text
YYYYMMDD_<file-sequence-of-day>.csv
```

Example:

```text
restaurants_20260923_01.csv
restaurants_20260923_02.csv
```

Existing Databricks historical filenames are not renamed because they are already part of the executed lineage.

---

## Decision 011 — Python Notebook Source Is the Primary Databricks Artifact

**Status:** Accepted

Databricks notebooks are exported as Python source for Git version control.

Python source is the primary editable and reviewable artifact.

DBC exports are retained as Databricks-native backup/import artifacts.

Current structure:

```text
notebooks/
└── dev/
    └── 01_Bronze/

artifacts/
└── databricks/
    └── dev/
        └── 01_Bronze/
```

The Python notebook and the corresponding DBC backup are maintained together for important Databricks development work.


---

## Decision 012 — Project and Azure SQL Resource Naming

**Status:** Accepted

The project/repository name is:

```text
westeros-foodflow
```

Phase 3 Azure resource naming uses:

```text
rg-westeros-foodflow-dev
sql-westeros-foodflow-dev
westeros-foodflow
```

Existing executed Databricks objects are not renamed solely for documentation consistency when doing so would alter historical lineage.

---

## Decision 013 — Phase 3 Dataset Implementation Sequence

**Status:** Accepted

The relational dataset is implemented progressively:

```text
Azure SQL
   ↓
Create schema
   ↓
Stage A — 10 restaurants / 100 customers / 500 orders
   ↓
Relationship + business-rule validation
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
250K orders / ~2.9M relational rows
```

The large 250K-order dataset is deliberately deferred until the ADF phase.

---

## Decision 014 — Azure SQL as a Separate Relational Integration Pattern

**Status:** Accepted

Azure SQL is introduced as a separate source-system integration pattern from the Databricks-managed storage used in the current Free Edition environment.

The initial SQL ingestion pattern is JDBC-based and uses SQL-specific ingestion metadata:

- `_ingested_at`
- `_ingestion_date`
- `_source_system`
- `_batch_id`

The CSV-specific `_source_file` field is not required for SQL ingestion.

---

## Decision 015 — Watermark-based Incremental SQL Extraction Before CDC

**Status:** Accepted

The initial incremental SQL pattern uses `updated_at` watermarks:

```sql
SELECT *
FROM dbo.orders
WHERE updated_at > @last_watermark
  AND updated_at <= @current_watermark;
```

This captures inserts and updates but does not capture hard deletes.

The project will later compare this pattern with soft deletes, Change Tracking, and CDC.

---

## Decision 016 — Large Dataset Deferred to ADF Phase

**Status:** Accepted

The eventual large relational dataset is:

- customers: 25,000
- restaurants: 500
- menu_items: 15,000
- delivery_partners: 1,000
- orders: 250,000
- order_items: ~750,000
- payments: ~250,000
- order_status_history: ~1,500,000
- restaurant_reviews: ~75,000
- delivery_partner_reviews: ~40,000

Approximately 2.9 million relational rows are expected.

This dataset is not created immediately after Azure SQL provisioning. It is introduced during the ADF learning/implementation phase.
