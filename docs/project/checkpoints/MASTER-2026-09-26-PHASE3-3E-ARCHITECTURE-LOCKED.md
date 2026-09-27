# westeros-foodflow — Master Checkpoint

**Checkpoint ID:** `FOODFLOW-2026-09-26-PHASE3-3E-ARCHITECTURE-LOCKED`
**Date:** 2026-09-26
**Project:** `westeros-foodflow`
**Branch:** `feature/phase-3-relational-sql`
**Repository:** `https://github.com/singhavinash2402-blckflm/westeros-foodflow.git`

## 1. Authoritative current position

Phase 3 — Relational SQL has been completed through **Stage 3D**.

| Stage | Status | Meaning |
|---|---|---|
| 3A — SQL Foundation | COMPLETE | Azure SQL environment and normalized 10-table schema validated |
| 3B — Stage A dataset | COMPLETE | Small relational dataset generated/loaded and validated |
| 3C — JDBC connectivity | COMPLETE | Databricks ↔ Azure SQL connectivity established |
| 3D — SQL → Landing → Bronze | COMPLETE | SQL extraction landed as immutable artifacts and Bronze ingestion completed |
| 3E — Bronze → Silver | BLOCKED | Implementation failed and exposed architecture/source-resolution problems |
| Architecture review | COMPLETE / LOCKED | Landing/Bronze/Silver/Gold + Control Plane contracts revisited and locked |
| Next implementation | **3E — Bronze → Silver** | Resume implementation using the locked Silver contract |

**Critical correction:** Do not redo 3A, 3B, 3C, or 3D. The project is not waiting for SQL data generation, JDBC, or SQL→Bronze. The current work resumes at 3E.

## 2. Why the architecture was revisited

The 3E failure exposed a concrete provenance/source-resolution problem in the existing Bronze implementation.

Observed evidence included the `restaurants` Bronze data containing both CSV and Azure SQL records. A problematic record showed SQL ingestion metadata while retaining the old CSV `_source_file`, demonstrating that source metadata could become contaminated/overwritten during processing.

This was not treated as a reason to patch one merge statement blindly. It demonstrated that Bronze→Silver needed an explicit canonicalization and source-resolution contract.

Therefore the architecture was revisited before continuing implementation.

## 3. Locked layer architecture

```text
Landing → Bronze → Silver → Gold
                         \
                          → BI / Analytics / ML

Control / Observability / Orchestration plane
        └─ run state, batches, watermarks, metrics, retries, reconciliation
```

### Landing
Exact source-faithful raw artifacts.

- CSV remains original CSV.
- JSON remains original JSON.
- Parquet remains original Parquet.
- Database extraction artifacts are immutable Parquet.
- No source-payload modification.
- No DQ, deduplication, source resolution, or business logic.
- Physical organization is entity → source system → ingestion date → artifact.
- Extraction state belongs to the Control Plane.

### Bronze
Source-faithful records plus minimal technical/audit metadata.

Universal metadata:

```text
_source_path
_ingested_at
_ingestion_date
_batch_id
```

Bronze does not perform canonicalization, business transformations, source conflict resolution, business DQ, relationship validation, or latest-state selection.

Technical DQ observations are allowed. Evidence is preserved.

### Silver
Canonical, integrated, business-aware layer.

Silver owns:

- canonical schema
- controlled schema evolution
- type normalization
- column standardization/renaming
- nested flattening where applicable
- deduplication
- canonical identity
- source conflict resolution
- current-state selection
- event/replay handling
- business DQ
- relationship validation
- late-arriving data handling
- CDC/state processing
- record hashing
- lineage

### Gold
Business-facing analytical consumption layer.

- dimensions
- facts
- marts
- explicit grain
- dimensional relationships
- analytical aggregations
- BI/analytics/ML serving

### Control Plane
Operational state only.

- runs
- batches
- extraction state
- processing state
- watermarks
- counts
- quality metrics
- errors
- retries
- reconciliation
- observability

## 4. Silver Decisions 6–22 — LOCKED

### Decision 6 — Silver physical organization
Silver is entity/domain-oriented and source-neutral. Logical organization follows canonical business entities/domains, not source systems.

### Decision 7 — Silver history strategy
Use current-state tables separately from historical/versioned data where history is required. Use SCD-2 selectively; do not force SCD-2 on every table.

### Decision 8 — Invalid record handling
Never physically remove evidence because a record is invalid. Represent successfully processed records with `_record_status` such as `VALID` or `INVALID`; retain diagnostics. Technical corruption that cannot be represented remains preserved upstream.

### Decision 9 — Silver write/update strategy
Choose processing semantics by dataset behavior:
- current-state entities → MERGE/upsert
- mutable transactional state → MERGE/upsert
- append/event history → append plus replay/duplicate detection
- CDC → CDC semantics
- SCD-2/history → versioned merge/insert

Overwrite is not the default Silver strategy.

### Decision 10 — Silver table classification
- Current-state: `customers`, `restaurants`, `menu_items`, `delivery_partners`
- Mutable transactional: `orders`, `payments`
- Event/history: `order_status_history`, `restaurant_reviews`, `delivery_partner_reviews`
- Transaction detail/relationship: `order_items`

### Decision 11 — Silver canonical keys and record identity
Business-key-first identity. Stable trustworthy business keys remain canonical. Source IDs may be retained for provenance. Event/history datasets use event identity. `_record_hash` is generated only after canonicalization and supports change/duplicate detection; it does not replace business/event keys.

Same source IDs across systems do not automatically mean the same real-world entity. Where identity cannot be safely established, retain competing candidate evidence and flag the identity conflict rather than silently merging.

### Decision 12 — Source conflict resolution
No source system has permanent precedence.

Resolution order is evidence-based:
1. trustworthy business/source update timestamp
2. ingestion/extraction timing
3. deterministic tie-breakers

`_ingested_at` is not a business `updated_at`. Late-arriving data must not overwrite newer business state merely because it arrived later. Unresolvable conflicts remain flagged with competing evidence preserved.

### Decision 13 — Silver schema enforcement/evolution
Silver owns a controlled canonical schema.

- New source columns are preserved upstream but are not automatically added to Silver.
- Removed source columns do not automatically disappear from Silver.
- Safe datatype changes may be normalized.
- Unsafe changes/missing required fields are schema violations.
- Breaking changes require an explicit, version-controlled Silver decision.

### Decision 14 — Silver DQ framework
DQ categories:
- business
- relationship
- identity/deduplication
- schema-related

`_record_status` is the primary record-level state. Detailed rule outcomes are retained for diagnostics. DQ determines validity; it does not delete evidence.

### Decision 15 — Silver relationship/referential integrity
Validate relationships against canonical Silver entities.

A missing parent does not delete a child. The child is retained and flagged unresolved. It can be reprocessed when the parent arrives.

### Decision 16 — Silver incremental processing/watermarks
Keep these concepts separate:
- extraction watermark
- Bronze batch-processing state
- Silver processing state
- business record version

Watermarks belong in the Control Plane.

### Decision 17 — Silver replay/idempotency
Silver processing must be idempotent.

- Current state: business key + version logic + MERGE
- Events: event identity + replay detection
- Batch identity is tracked separately

### Decision 18 — Silver late-arriving data
Retain unresolved records. Reprocess when missing evidence arrives. Late business records must be compared using business timestamps/version semantics rather than arrival time alone.

### Decision 19 — Silver deletes
Absence is not automatically deletion.

Explicit delete semantics are required. Current-state deletes follow the approved soft-delete approach. Historical/event evidence is preserved. CDC DELETE later follows the soft-delete policy.

### Decision 20 — Silver schema/table versioning
Canonical Silver contract changes are controlled, documented, version-controlled in Git, and deliberately deployed. Do not create physical `v1`, `v2`, etc. tables for every small change.

### Decision 21 — Silver lineage/auditability
Every canonical Silver record must be traceable:

```text
Gold → Silver → Bronze record/batch → Landing artifact → source
```

### Decision 22 — Silver observability/processing metrics
The Control Plane tracks, as applicable:

`batch_id`, entity, input records, valid/invalid records, new/updated/unchanged records, duplicates, identity conflicts, relationship failures, schema failures, processing start/end, status.

## 5. Locked Silver table behavior

| Silver entity | Behavior |
|---|---|
| `customers` | Current-state MERGE; optional history |
| `restaurants` | Current-state MERGE; source conflict resolution required; optional history |
| `menu_items` | Current-state MERGE; optional history |
| `delivery_partners` | Current-state MERGE; optional history |
| `orders` | Mutable transactional state; MERGE; status history separate |
| `order_items` | Transaction detail/relationship; controlled MERGE/upsert |
| `payments` | Mutable transactional state; MERGE |
| `order_status_history` | Event/history; append + replay dedup; preserve legitimate events |
| `restaurant_reviews` | Review identity/chronology aware; preserve legitimate reviews |
| `delivery_partner_reviews` | Review identity/chronology aware; preserve legitimate reviews |

## 6. Gold Decisions 23–33 — LOCKED

### Decision 23 — Gold architecture
Gold is business-facing and uses a hybrid dimensional model: dimensions + facts + marts. Every fact/mart has an explicit grain.

### Decision 24 — Selective dimensions
Initial candidates:
`dim_customer`, `dim_restaurant`, `dim_menu_item`, `dim_delivery_partner`, `dim_date`.

Use SCD-1/SCD-2 selectively according to analytical history needs.

### Decision 25 — Gold surrogate keys
Use warehouse surrogate keys in Gold dimensions where appropriate. Preserve Silver/business keys for traceability. Facts reference dimension surrogate keys.

### Decision 26 — Gold facts
Initial facts:
- `fact_orders` — one row/order
- `fact_order_items` — one row/order-item
- `fact_payments` — one row/payment transaction
- `fact_restaurant_reviews` — one row/review
- `fact_delivery_partner_reviews` — one row/review

A status-event fact may be added later.

### Decision 27 — Gold grain protection
Every Gold table documents grain and key. Aggregate at the correct grain before joins. Protect against row multiplication and double counting.

### Decision 28 — Gold dimensional relationships
Use dimensional/star-schema relationships rather than repeatedly joining Silver for consumers. Preserve original business identifiers.

### Decision 29 — Gold marts
Marts answer business questions and are not Silver copies. Candidate marts include daily sales, restaurant performance, customer behavior, delivery performance, payment performance, and review analytics.

### Decision 30 — Gold aggregation/refresh
Support incremental Gold processing where practical. Identify affected records/dates/entities and update relevant aggregates. Correctness comes before premature optimization.

### Decision 31 — Gold historical consistency
Preserve historical events. Where historical dimension tracking is required, facts use the dimension version applicable at fact time.

### Decision 32 — Gold invalid/null/unmatched dimensions
Do not lose facts because a dimension is late. Use an unknown/unmatched dimension member, such as surrogate key `0`, and reconcile later.

### Decision 33 — Gold serving contracts
Consumers include Power BI, SQL/analysts, dashboards, analytics, ML/feature preparation, and downstream applications. Create separate Gold products only for genuinely different needs.

## 7. Control Plane / Orchestration Decisions 34–43 — LOCKED

### Decision 34 — Control Plane purpose
Own execution state and operational metadata, not business/source payload.

### Decision 35 — Control Plane metadata model
Track run-level and batch/extraction-level metadata including run ID, pipeline name/version, timestamps, status, trigger type, errors, batch ID, entity, source system, extraction boundaries, watermarks, counts, and status.

### Decision 36 — Watermark ownership
Extraction watermark, Bronze processing state, Silver processing state, and business record version remain separate. Watermarks belong in Control Plane.

### Decision 37 — Pipeline idempotency
Retries must not duplicate business data. Run, batch, record, and event identity remain distinct.

### Decision 38 — Failure/retry semantics
Failed runs remain diagnosable and retryable. Failed processing must not incorrectly advance watermarks. Partial processing must be recoverable without uncontrolled duplication.

### Decision 39 — Reconciliation controls
Track reconciliation across:

```text
Source → Landing → Bronze → Silver → Gold
```

including extracted, landed, processed, valid, invalid, new, updated, unchanged, duplicate, relationship-failure, schema-failure, and output metrics.

### Decision 40 — Orchestration responsibility
Orchestration coordinates execution; it does not perform business transformations.

ADF will be introduced later as the Azure orchestration learning stage. Airflow will later become the primary orchestration layer. Databricks remains responsible for Spark/Delta transformation processing.

### Decision 41 — Pipeline boundaries
Use meaningful operational boundaries based on ownership, retryability, monitoring, and learning objectives. Avoid unnecessary fragmentation.

### Decision 42 — Dependency/data-readiness
Downstream stages run only when required upstream state is successfully available. Failed upstream processing must not feed incomplete data downstream.

### Decision 43 — Observability/audit trail
Meaningful executions must be traceable:

```text
run → pipeline → batch → entity → Landing → Bronze → Silver → Gold
```

This supports troubleshooting, replay, lineage, reconciliation, latency/SLA analysis, failure analysis, and learning/performance analysis.

## 8. Implementation rule going forward

The architecture above is **locked**.

Do not reopen Silver, Gold, or Control Plane design merely because implementation is beginning.

For 3E, implementation must translate the existing decisions into executable logic for the 10 current entities.

If implementation exposes a genuine contradiction or defect in a locked decision, stop, document the evidence, and make an explicit architecture change. Otherwise, implement the existing contract.

## 9. Immediate next task — 3E Bronze → Silver

The next work session begins here:

```text
Existing 3D Bronze
      ↓
3E Silver implementation
      ↓
canonicalization
      ↓
identity / deduplication
      ↓
source conflict resolution
      ↓
business + relationship DQ
      ↓
current-state / event semantics
      ↓
idempotent Silver writes
      ↓
lineage + observability
      ↓
Silver validation
```

The first implementation activity should be a **table-by-table Silver implementation contract**, followed by the actual notebook/code changes.

Do not start ADF yet.

## 10. Later Phase 3 sequence

After 3E is successfully implemented and validated:

```text
3F — Stage A2 deterministic scaling (~5K)
3G — Stage B AI-assisted generation/scaling (~15K)
3H — ADF introduction
3I — large-scale dataset (~250K orders)
```

The project deliberately follows:

```text
Understand manually
        ↓
Deterministic automation
        ↓
AI-assisted automation
        ↓
Governed agentic workflows
```

## 11. Git/documentation checkpoint rule

At significant milestones update:

- `docs/PROJECT_PLAN.md`
- `docs/PROJECT_TRACKER.md`
- `docs/PROGRESS.md`
- `docs/LEARNING_LOG.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `docs/project/checkpoints/phase-3.md`
- this master checkpoint

Then perform:

```text
git status
git diff
git add
git commit
git push
```

## 12. Authoritative checkpoint statement

> **As of 2026-09-26, `westeros-foodflow` Phase 3 is complete through 3D (SQL → Landing → Bronze). Stage 3E (Bronze → Silver) is the current blocked implementation point. The 3E failure exposed source metadata/provenance and canonicalization issues, which led to a deliberate architecture review. Landing → Bronze → Silver → Gold and the separate Control/Observability/Orchestration plane are now locked, with Silver Decisions 6–22, Gold Decisions 23–33, and Control Plane/Orchestration Decisions 34–43 finalized. No earlier Phase 3 stage is to be repeated. The next task is to implement 3E according to these locked contracts.**

**Checkpoint status: LOCKED — READY TO RESUME 3E**
