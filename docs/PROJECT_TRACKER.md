# westeros-foodflow — Master Project Tracker

This is the authoritative whole-project roadmap. Future phases are retained for learning continuity but must not be implemented ahead of the current locked sequence.

## Learning progression

```text
Understand manually
      ↓
Validate
      ↓
Deterministic automation
      ↓
Scale
      ↓
AI-assisted automation
      ↓
Governed agentic workflows
```

## Master status

| Phase / Stage | Objective | Status |
|---|---|---|
| Phase 0 | Foundation | ✅ Complete |
| Phase 1 | Databricks / Medallion | ✅ Complete |
| Phase 2 | Incremental CSV | ✅ Complete / merged |
| Phase 3 | Relational SQL | 🔵 Current |
| 3A | SQL Foundation + Stage A + JDBC + SQL→Bronze | 🟢 Complete through Bronze |
| 3E | Bronze → Silver | 🔴 Current / blocked — resume implementation |
| 3F | Deterministic ~5K | ⏳ Future |
| 3G | AI-assisted ~15K | ⏳ Future |
| 3H | Azure Data Factory / orchestration | ⏳ Future |
| 3I | 250K-order workload | ⏳ Future |
| 5 | Advanced data engineering | ⏳ Future |
| 6 | APIs / JSON | ⏳ Future |
| 7 | dbt + dimensional modeling | ⏳ Future |
| 8 | Streaming fundamentals | ⏳ Future |
| 9 | Kafka / streaming engineering | ⏳ Future |
| 10 | Airflow | ⏳ Future |
| 11 | Data quality / observability | ⏳ Future |
| 12 | Data contracts / schema evolution | ⏳ Future |
| 13 | Testing / CI/CD | ⏳ Future |
| 14 | Security / IAM / secrets | ⏳ Future |
| 15 | Terraform / IaC | ⏳ Future |
| 16 | AWS / multi-cloud | ⏳ Future |
| 17 | Power BI / serving | ⏳ Future |
| 18 | Governed AI / agentic data engineering | ⏳ Future |

## Phase 3A completed gates

- [x] Azure SQL environment
- [x] Ten-table normalized schema
- [x] Schema validation
- [x] Stage A deterministic data
- [x] Relationship/business validation
- [x] Local ODBC connectivity
- [x] Databricks JDBC connectivity
- [x] SQL source schema discovery
- [x] SQL → Bronze all ten tables
- [x] Standard Bronze metadata
- [x] Existing restaurants source-history preservation
- [x] Source/Bronze row-count validation

## Stage A counts

| Table | Rows |
|---|---:|
| restaurants | 10 |
| customers | 100 |
| menu_items | 78 |
| orders | 500 |
| order_items | 1,515 |
| payments | 500 |
| delivery_partners | 20 |
| order_status_history | 2,808 |
| restaurant_reviews | 66 |
| delivery_partner_reviews | 23 |

## SQL → Bronze rules — locked

```text
_ingested_at
_ingestion_date
_source_system
_source_file
_batch_id
```

SQL/JDBC: `_source_system=azure_sql`, `_source_file=NULL`, `_batch_id=stage3a_sql_full_20260926`.

The existing Bronze `restaurants` table contains 9 historical CSV-only records. The SQL Stage A set contains 10 rows, with one overlap on `REST-SHJ-001`. Explicit `restaurant_id` reconciliation preserves the 9 historical records and adds/updates the 10 SQL-originated rows, resulting in 19 Bronze restaurant rows.

First-load tables require an explicit `spark.catalog.tableExists()` guard. Source and Bronze counts must be compared.

## Reliability rules — locked

- Azure SQL Serverless can auto-resume and produce transient availability errors.
- Databricks Free Edition public egress IP can change and require a firewall update.
- Diagnose firewall, serverless resume, authentication, and query/schema failures separately.
- Do not use broad Azure-services access as a shortcut.
- Add explicit JDBC retry/resiliency settings to the maintained implementation.

## Current resume point — 3E

The Silver architecture and implementation rules are already locked. Do not reopen or redefine source precedence/canonicalization before implementation.

```text
Existing 3D Bronze
      ↓
3E — Bronze → Silver
      ↓
Table-by-table implementation of locked Silver contract
      ↓
Silver validation / idempotency / lineage / observability
      ↓
3F — deterministic ~5K
      ↓
3G — AI-assisted ~15K
      ↓
3H — ADF introduction
      ↓
3I — 250K workload
```

### 3E implementation gates

- [ ] Map the locked Silver contract to all 10 entities
- [ ] Implement canonical identity and deduplication
- [ ] Implement evidence-based source conflict resolution
- [ ] Implement business/relationship/schema DQ handling
- [ ] Implement current-state/event-specific write semantics
- [ ] Implement late-arriving and unresolved-parent handling
- [ ] Implement idempotent replay behavior
- [ ] Preserve lineage from Silver → Bronze → Landing
- [ ] Record Control Plane processing metrics
- [ ] Validate Silver outputs and reruns
- [ ] Create 3E completion checkpoint

## Documentation gate

Every completed meaningful stage must update the plan, tracker, progress, learning log, affected architecture/data dictionary/decisions/runbook/AI roadmap, and the relevant checkpoint before the agreed Git checkpoint is considered complete.


## Architecture checkpoint — 2026-09-26

**Authoritative checkpoint:** `FOODFLOW-2026-09-26-PHASE3-3E-ARCHITECTURE-LOCKED`

Locked architecture:

```text
Landing → Bronze → Silver → Gold

Control / Observability / Orchestration
```

Silver Decisions 6–22, Gold Decisions 23–33, and Control Plane/Orchestration Decisions 34–43 are locked. The checkpoint was created because the first 3E implementation exposed source provenance/source-resolution problems. Earlier Phase 3 stages 3A–3D are complete and must not be repeated.
