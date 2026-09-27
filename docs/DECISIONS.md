# westeros-foodflow Engineering Decisions

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


---

# Phase 3A Decisions — 2026-09-26

## Decision 012 — Standard Bronze source metadata

**Status:** Accepted / Locked

Every Bronze table uses `_ingested_at`, `_ingestion_date`, `_source_system`, `_source_file`, and `_batch_id`. SQL/JDBC uses `azure_sql` and NULL `_source_file`.

## Decision 013 — Preserve existing Bronze source history

**Status:** Accepted / Locked

The existing `restaurants` Bronze history is not overwritten. SQL reconciliation uses explicit `restaurant_id` matching. Historical `_source_file` lineage remains explainable.

## Decision 014 — Explicit table-existence guard for first-load Bronze tables

**Status:** Accepted / Locked

Before a first-load write, check `spark.catalog.tableExists()`. Stop rather than overwrite an existing table. Do not rely on unsupported `errorifexists`.

## Decision 015 — No fabricated SQL file lineage

**Status:** Accepted / Locked

JDBC ingestion has no source file. `_source_file` remains NULL.

## Decision 016 — Treat Serverless/firewall failures as operational dependencies

**Status:** Accepted / Locked

Azure SQL Serverless auto-resume and changing Databricks egress IPs can cause transient connectivity failures. Diagnose these separately from authentication, schema, and data errors. Do not enable broad Azure-services access as a shortcut.

## Decision 017 — Explicit Silver canonicalization gate

**Status:** Accepted / Locked

Before Bronze → Silver, define source precedence/canonicalization for mixed-source Bronze data, especially `restaurants`.

## Decision 018 — Stage progression remains locked

**Status:** Accepted / Locked

Stage A → deterministic ~5K → AI-assisted ~15K → ADF → 250K workload. Do not jump directly to the 250K dataset or introduce AI before the deterministic stage.


---

# Architecture Decisions — 2026-09-26

> **Naming note:** Existing Project Decisions 001–018 are historical/implementation decisions and are preserved unchanged. The architecture checkpoint uses namespaced decision IDs below to avoid renumbering or overwriting the historical decision record.

## Silver Architecture Decisions S-06 through S-22 — LOCKED

### S-06 — Silver physical organization
Silver is entity/domain-oriented and source-neutral. Logical organization follows canonical business entities/domains rather than source systems.

### S-07 — Silver history strategy
Use current-state tables separately from historical/versioned data where history is required. SCD-2 is selective, not universal.

### S-08 — Invalid record handling
Never physically remove evidence because a record is invalid. Use `_record_status` such as `VALID`/`INVALID` and preserve diagnostics. Unrepresentable technical corruption remains upstream.

### S-09 — Silver write/update strategy
Current-state and mutable transactional datasets use MERGE/upsert; event/history datasets use append plus replay detection; CDC follows CDC semantics; SCD-2/history uses versioned merge/insert. Overwrite is not the default Silver strategy.

### S-10 — Silver table classification
Current-state: `customers`, `restaurants`, `menu_items`, `delivery_partners`. Mutable transactional: `orders`, `payments`. Event/history: `order_status_history`, `restaurant_reviews`, `delivery_partner_reviews`. Transaction detail: `order_items`.

### S-11 — Canonical keys and record identity
Use trustworthy business keys as canonical identity. Retain source-specific IDs for provenance where appropriate. Events use event identity. `_record_hash` is generated after canonicalization and supports change/duplicate detection; it does not replace business/event keys.

### S-12 — Source conflict resolution
No source system has permanent precedence. Use trustworthy business/source update timestamps, then ingestion/extraction timing, then deterministic tie-breakers. `_ingested_at` is not business `updated_at`. Unresolvable conflicts remain flagged with evidence preserved.

### S-13 — Silver schema enforcement/evolution
Silver owns the controlled canonical schema. New source columns remain upstream until explicitly approved. Removed source columns do not automatically disappear. Unsafe changes/missing required fields are schema violations.

### S-14 — Silver DQ framework
DQ covers business, relationship, identity/deduplication, and schema-related rules. `_record_status` is the primary record-level state. DQ determines validity, not deletion.

### S-15 — Silver relationship integrity
Validate relationships against canonical Silver entities. Missing parents do not delete children; unresolved children are retained and can be reprocessed when parents arrive.

### S-16 — Silver incremental state
Keep extraction watermark, Bronze processing state, Silver processing state, and business record version separate. Watermarks belong in the Control Plane.

### S-17 — Silver replay/idempotency
Reprocessing the same batch must not create duplicate business records. Current state uses business-key/version MERGE; events use event identity/replay detection.

### S-18 — Silver late-arriving data
Retain unresolved records and reprocess when evidence arrives. Late records are evaluated by business version/time, not arrival time alone.

### S-19 — Silver deletes
Absence does not imply deletion. Explicit source delete semantics are required. Current-state deletes use the approved soft-delete approach; event/history evidence is preserved.

### S-20 — Silver schema/table versioning
Canonical contract changes are controlled, documented, version-controlled, and deliberately deployed. Do not create physical versioned tables for every small change.

### S-21 — Silver lineage
Every canonical Silver record is traceable through Gold → Silver → Bronze record/batch → Landing artifact → source evidence.

### S-22 — Silver observability
Control Plane metrics include batch/entity, input, valid/invalid, new/updated/unchanged, duplicates, identity conflicts, relationship failures, schema failures, processing timestamps, and status as applicable.

## Gold Architecture Decisions G-23 through G-33 — LOCKED

### G-23 — Gold architecture
Gold is business-facing and uses a hybrid dimensional model: dimensions, facts, and marts. Every fact/mart has explicit grain.

### G-24 — Selective Gold dimensions
Initial dimensions: `dim_customer`, `dim_restaurant`, `dim_menu_item`, `dim_delivery_partner`, `dim_date`. SCD-1/SCD-2 is selective according to analytical need.

### G-25 — Gold surrogate keys
Use warehouse surrogate keys in Gold dimensions where appropriate while preserving Silver/business keys. Facts reference dimension surrogate keys.

### G-26 — Gold facts
Initial facts: `fact_orders`, `fact_order_items`, `fact_payments`, `fact_restaurant_reviews`, `fact_delivery_partner_reviews`. A status-event fact may be added later.

### G-27 — Gold grain protection
Every Gold table documents grain and key. Aggregate at the correct grain before joins and protect against row multiplication/double counting.

### G-28 — Gold dimensional relationships
Use dimensional/star-schema relationships for consumer access rather than repeatedly joining Silver. Preserve business identifiers.

### G-29 — Gold marts
Marts are business-question-oriented products, not Silver copies. Candidate marts include daily sales, restaurant performance, customer behavior, delivery performance, payment performance, and review analytics.

### G-30 — Gold refresh
Use incremental Gold processing where practical. Correctness comes before premature optimization.

### G-31 — Gold historical consistency
Preserve historical events. When historical dimension tracking is required, facts use the dimension version applicable at fact time.

### G-32 — Gold unmatched dimensions
Do not lose facts because dimensions are late. Use an unknown/unmatched dimension member such as surrogate key 0 and reconcile later.

### G-33 — Gold serving contracts
Consumers include Power BI, SQL/analysts, dashboards, analytics, ML/feature preparation, and downstream applications. Create separate products only for genuinely different needs.

## Control Plane / Orchestration Decisions C-34 through C-43 — LOCKED

### C-34 — Control Plane purpose
Own execution state and operational metadata, not business/source payload.

### C-35 — Control Plane metadata model
Track run-level and batch/extraction metadata including run ID, pipeline/version, timestamps, status, trigger, errors, batch ID, entity, source system, extraction boundaries, watermarks, and counts.

### C-36 — Watermark ownership
Extraction watermark, Bronze processing state, Silver processing state, and business record version remain separate. Watermarks belong in the Control Plane.

### C-37 — Pipeline idempotency
Retries must not duplicate business data. Run, batch, record, and event identities remain distinct.

### C-38 — Failure/retry semantics
Failed runs remain diagnosable/retryable. Failed processing must not incorrectly advance watermarks. Partial processing must be recoverable without uncontrolled duplication.

### C-39 — Reconciliation controls
Track reconciliation across Source → Landing → Bronze → Silver → Gold, including extracted, landed, processed, valid, invalid, new, updated, unchanged, duplicate, relationship-failure, schema-failure, and output metrics.

### C-40 — Orchestration responsibility
Orchestration coordinates execution; it does not perform business transformations. ADF is the later Azure orchestration learning stage; Airflow is the later primary orchestrator. Databricks owns Spark/Delta transformations.

### C-41 — Pipeline boundaries
Use meaningful operational boundaries based on ownership, retryability, monitoring, and learning objectives. Avoid unnecessary fragmentation.

### C-42 — Dependency/data readiness
Downstream stages run only when required upstream state is successfully available. Failed upstream processing must not feed incomplete data downstream.

### C-43 — Observability/audit trail
Trace meaningful executions through run → pipeline → batch → entity → Landing → Bronze → Silver → Gold for troubleshooting, replay, lineage, reconciliation, latency, failure, and learning/performance analysis.

## Architecture lock rule

The above architecture decisions are locked by checkpoint `FOODFLOW-2026-09-26-PHASE3-3E-ARCHITECTURE-LOCKED`. They are implemented next; they are not to be redefined during 3E unless concrete implementation evidence proves a contradiction or defect.
