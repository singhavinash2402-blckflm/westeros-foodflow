# FoodFlow Engineering Decisions

## Decision 001 — Use Databricks Free Edition for Initial Learning

**Status:** Accepted

Databricks Free Edition is used for the initial FoodFlow implementation.

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

This keeps the FoodFlow development environment reproducible and prevents global package conflicts.

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

For the current FoodFlow design, Gold is recomputed and overwritten from Silver after incremental changes.

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
