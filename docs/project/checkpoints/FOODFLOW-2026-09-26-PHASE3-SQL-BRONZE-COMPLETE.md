> **HISTORICAL CHECKPOINT — SUPERSEDED FOR CURRENT ARCHITECTURE**
>
> This checkpoint records the completed 3D SQL → Bronze state before the 3E architecture review. The current authoritative checkpoint is `FOODFLOW-2026-09-26-PHASE3-3E-ARCHITECTURE-LOCKED`.
>
---

# westeros-foodflow Master Checkpoint

**Checkpoint ID:** `FOODFLOW-2026-09-26-PHASE3-SQL-BRONZE-COMPLETE`  
**Date:** 2026-09-26  
**Phase:** Phase 3 — Relational SQL  
**Stage:** Stage 3A — SQL Foundation + Stage A  
**Execution point:** SQL → Bronze complete; Bronze → Silver next.

## Repository

- Repository: `westeros-foodflow`
- Workspace: `C:\Work\westeros_foodflow_workspace`
- Branch: `feature/phase-3-relational-sql`
- Phase 2 Incremental CSV Ingestion: merged to `main`
- Phase 3 push: deferred until the agreed Phase 3 completion milestone

## Azure SQL

```text
Resource group: rg-westeros-foodflow-dev
Server:         sql-westeros-foodflow-dev
Database:       westeros-foodflow
Region:         Central India
Compute:        General Purpose / Serverless / Standard-series Gen5
2 vCores / 32 GB
Free offer:     Applied
```

Authentication is SQL + Microsoft Entra. Broad Azure-services access is disabled. No private endpoint. TLS 1.2. Service-managed TDE. Overage billing disabled.

## Relational schema — locked

Ten tables: `customers`, `restaurants`, `menu_items`, `orders`, `order_items`, `payments`, `delivery_partners`, `order_status_history`, `restaurant_reviews`, `delivery_partner_reviews`.

The physical design uses BIGINT IDENTITY keys where appropriate, `restaurants.restaurant_id` as the business key, `DATETIME2(3)`, monetary DECIMAL types, relational constraints, and access-pattern/`updated_at` indexes.

## Stage A — validated

```text
restaurants                 10
customers                  100
menu_items                  78
orders                     500
order_items              1,515
payments                   500
delivery_partners           20
order_status_history     2,808
restaurant_reviews          66
delivery_partner_reviews    23
```

Relationship/business validation passed. Controlled invalid cases are isolated in `controlled_dq_fixtures.csv`.

## JDBC — validated

Local ODBC and Databricks JDBC connectivity succeeded. Databricks public egress IP changes caused firewall authorization failures during testing; the current IP was explicitly authorized. A separate transient database-unavailable condition was consistent with Serverless auto-resume.

## SQL → Bronze — complete

Standard metadata is:

```text
_ingested_at
_ingestion_date
_source_system
_source_file
_batch_id
```

SQL/JDBC values:

```text
_source_system = azure_sql
_source_file   = NULL
_batch_id      = stage3a_sql_full_20260926
```

### Customers

100 rows loaded and validated.

### Restaurants — special history-preservation rule

Existing Bronze contained 9 historical CSV-only rows. Current SQL contains 10 rows. One business key overlaps: `REST-SHJ-001`. Explicit `restaurant_id` reconciliation produced 19 Bronze rows: 9 historical CSV-only + 10 SQL-originated. Historical `_source_file` lineage is preserved; historical CSV-only rows are not relabeled as SQL.

### Other SQL tables

Full loads completed and validated: menu_items 78; orders 500; order_items 1,515; payments 500; delivery_partners 20; order_status_history 2,808; restaurant_reviews 66; delivery_partner_reviews 23.

First-load operations used an explicit `spark.catalog.tableExists()` guard. `errorifexists` is not used.

## Locked rules

1. Preserve existing Bronze history.
2. Use explicit merge keys when source reconciliation is required.
3. Standardize Bronze metadata.
4. Keep `_source_file=NULL` for JDBC sources.
5. Use `_source_system` for source-system identity.
6. Use `_batch_id` for ingestion-run identity.
7. Validate source/Bronze row counts.
8. Keep credentials/secrets out of Git.
9. Diagnose Serverless/firewall/auth/query failures separately.
10. Add explicit JDBC retry/resiliency settings to the maintained implementation.

## Locked stage progression

```text
Stage A small/manual-deterministic
        ↓
Stage A2 deterministic ~5K
        ↓
Stage B AI-assisted ~15K
        ↓
ADF
        ↓
250K-order workload
```

Do not generate 250K now. Do not introduce AI-assisted generation before Stage A2.

## Documentation protocol

At every completed meaningful stage update `PROJECT_PLAN.md`, `PROJECT_TRACKER.md`, `PROGRESS.md`, `LEARNING_LOG.md`, affected architecture/data dictionary/decisions/runbook/AI roadmap, and the relevant checkpoint. Review Git diff/status, then commit/push according to the agreed Phase 3 workflow.

## Next action

**Bronze → Silver.** Define canonical/source-precedence behavior for mixed-source Bronze data, especially `restaurants`, before transformation code.

## Continuation instruction

> Continue `westeros-foodflow` from checkpoint `FOODFLOW-2026-09-26-PHASE3-SQL-BRONZE-COMPLETE`. Phase 3A SQL schema, Stage A data, relational validation, JDBC connectivity, and SQL → Bronze are complete. Standard SQL Bronze metadata and source-history preservation are locked. Start Bronze → Silver by defining source precedence/canonicalization before writing transformation code.

**Security:** no credentials, passwords, tokens, or secret-bearing connection strings are stored in this checkpoint.
