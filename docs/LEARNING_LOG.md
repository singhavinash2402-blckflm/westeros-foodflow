# westeros-foodflow Learning Log

## 2026-09-24 — Project Foundation

Established the FoodFlow project repository and development environment.

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

# 2026-09-26 — SQL → Bronze learning checkpoint

## Lessons learned

- JDBC makes Azure SQL a direct relational source for Databricks.
- Azure SQL Serverless can create transient resume-time availability failures.
- Databricks Free Edition public egress IP changes can independently cause SQL firewall failures.
- Source system and source file are different lineage concepts. SQL/JDBC has no source file, so `_source_file` must remain NULL.
- Existing Bronze source history must be preserved rather than blindly overwritten.
- First-load safety is best expressed as an explicit table-existence guard plus source/Bronze count validation.
- Bronze can contain multiple source histories; Silver needs an explicit canonicalization/source-precedence decision.

## Current result

All ten Stage A SQL tables are loaded into Bronze. The special `restaurants` table retains its 9 historical CSV-only rows in addition to 10 SQL-originated rows.

## Next learning target

Design Bronze → Silver canonicalization and validation before implementing transformations.


---

## 2026-09-26 — Bronze → Silver architecture lesson

The first 3E implementation exposed an important distinction: **preserving source evidence is not the same as defining canonical business state**.

Bronze preserves source records and technical provenance. Silver interprets that evidence using explicit identity, deduplication, source conflict resolution, DQ, relationship, versioning, late-arrival, replay, and lineage rules.

The `restaurants` Bronze evidence demonstrated why source metadata must not be mixed or overwritten during cross-source processing. The project therefore paused implementation and locked the layer contracts before continuing 3E.

### Current learning sequence

```text
Understand manually
      ↓
Implement deterministically
      ↓
Validate correctness/idempotency
      ↓
Automate repetitive work
      ↓
AI-assisted automation
      ↓
Governed agentic workflows
```

ADF and agentic automation remain later learning stages.
