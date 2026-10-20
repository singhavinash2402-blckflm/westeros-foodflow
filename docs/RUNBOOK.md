# westeros-foodflow — Runbook

## 1. Purpose

This runbook contains practical procedures for developing, validating, troubleshooting, and operating FoodFlow.

The document will evolve as new technologies and pipeline components are introduced.

---

## 2. Local Development Environment

### Workspace

```text
C:\Work\westeros_foodflow_workspace
```

### Python Environment

```text
.venv\
```

Activate the environment from PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Expected prompt:

```text
(.venv) PS C:\Work\westeros_foodflow_workspace>
```

Verify Python:

```powershell
python --version
```

Verify the active interpreter:

```powershell
where.exe python
```

Expected first result:

```text
C:\Work\westeros_foodflow_workspace\.venv\Scripts\python.exe
```

Verify pip:

```powershell
python -m pip --version
```

---

## 3. Git Operations

Check repository status:

```bash
git status
```

View repository history:

```bash
git log --oneline
```

View changes:

```bash
git diff
```

Stage changes:

```bash
git add .
```

Create a commit:

```bash
git commit -m "descriptive message"
```

Review recent commits:

```bash
git log --oneline --decorate
```

---

## 4. Git Safety Rules

Never commit:

- Passwords
- API keys
- Access tokens
- Cloud credentials
- Private keys
- Connection strings containing credentials
- `.env` files
- `.venv`
- Generated caches

Before committing:

```bash
git status
```

Review staged files:

```bash
git diff --cached
```

---

## 5. Databricks Workflow

Current environment:

- Databricks Free Edition

Current storage approach:

- Databricks-managed storage
- Databricks-managed volume

Current processing pattern:

```text
Source File
    ↓
Bronze
    ↓
Silver
    ↓
Gold
```

---

## 6. Current Incremental Processing Workflow

The next implementation uses:

```text
restaurants_20262309_02.csv
```

Expected test scenarios:

- New restaurant records
- Updated restaurant records
- Duplicate records

Known update test:

```text
REST-DXB-001
rating: 4.9 → 4.7
```

Expected processing:

```text
Incoming Batch
      ↓
Bronze
      ↓
Validate
      ↓
Deduplicate
      ↓
MERGE
      ↓
Silver
      ↓
Gold
      ↓
Validate Results
      ↓
Inspect Delta History
```

---

## 7. Incremental Validation Checklist

After an incremental load, validate:

### New records

Confirm that new business keys were inserted.

### Updated records

Confirm that existing business keys received the expected updates.

### Duplicate records

Confirm that duplicate source records do not create duplicate target records.

### Idempotency

Run the same batch again.

The second execution should not create unintended additional records or changes.

### Data quality

Repeat relevant data-quality checks.

### Delta history

Inspect the Delta table history to understand the operations performed.

---

## 8. Future Azure Workflow

When ADLS Gen2 is introduced:

```text
Source
  ↓
ADLS Gen2
  ↓
ADF / Airflow
  ↓
Databricks
  ↓
Bronze
  ↓
Silver
  ↓
Gold
```

Authentication and authorization will use appropriate Azure identity and access-control mechanisms.

Credentials must never be embedded in notebooks or committed to Git.

---

## 9. Future AWS Workflow

The planned AWS ingestion path is:

Source
  ↓
Amazon S3
  ↓
Orchestration
  ↓
Databricks
  ↓
Bronze
  ↓
Silver
  ↓
Gold

AWS IAM will be used for access control.

---

# 10. Troubleshooting Principles

When a pipeline fails:

1. Identify the exact failing layer.
2. Check the error message.
3. Check input data.
4. Check schema.
5. Check permissions.
6. Check recent pipeline/table history.
7. Check data-quality results.
8. Check execution plan where performance is involved.
9. Reproduce with the smallest possible dataset.
10. Document the problem and solution.

Do not immediately rewrite the entire pipeline.

---

# 11. Documentation After Significant Changes

After completing a meaningful feature:

1. Update `PROGRESS.md`.
2. Update `LEARNING_LOG.md`.
3. Update `DATA_DICTIONARY.md` if the schema changed.
4. Update `ARCHITECTURE.md` if the architecture changed.
5. Add a decision to `DECISIONS.md` when an important architectural choice was made.
6. Update this runbook when operational procedures change.
7. Commit the changes to Git.

---

# 12. Future Production Runbook Areas

The following sections will be added as FoodFlow grows:

* ADF pipeline execution
* ADF failure recovery
* Databricks job recovery
* Airflow DAG troubleshooting
* Streaming checkpoint recovery
* Event Hubs troubleshooting
* S3 ingestion troubleshooting
* ADLS access troubleshooting
* dbt execution
* dbt test failures
* Data-quality failures
* Schema evolution
* CDC failures
* Backfills
* Reprocessing
* Performance troubleshooting
* CI/CD deployment failures


---

# Phase 3A SQL → Bronze Runbook Addendum — 2026-09-26

## SQL Bronze metadata

```text
_source_system = azure_sql
_source_file   = NULL
_batch_id      = stage3a_sql_full_20260926
```

## First-load safety

1. Check `spark.catalog.tableExists(bronze_table)`.
2. Stop if the table exists and the operation is intended as a first load.
3. Read the SQL source through JDBC.
4. Compare source count to Bronze count after writing.

Do not use unsupported `errorifexists` as the guard.

## Existing restaurants Bronze

Do not overwrite. Use explicit `restaurant_id` reconciliation. Preserve historical `_source_file` lineage. Confirm that SQL-originated rows carry SQL metadata while historical CSV-only rows remain historical.

## JDBC troubleshooting

- Firewall/IP rejection: identify the current Databricks egress IP and authorize it explicitly.
- Serverless database-unavailable/transient error: allow auto-resume time and retry; distinguish from query/schema errors.
- Authentication failure: verify credentials outside notebooks/Git.
- Query/schema failure: investigate only after connectivity is established.

Do not enable broad Azure-services access as a troubleshooting shortcut.

## Bronze → Silver gate

Before Silver code, define source precedence, canonicalization, lineage preservation, and relationship/data-quality rules for mixed-source Bronze tables.


---

## 2026-09-26 — Current Phase 3 resume point

### Phase 3 state

```text
3A SQL Foundation       COMPLETE
3B Stage A              COMPLETE
3C JDBC                 COMPLETE
3D SQL → Landing→Bronze COMPLETE
3E Bronze → Silver      CURRENT
```

### 3E operating rule

The Silver architecture is already locked. Do not redefine source precedence, canonicalization, DQ, relationship handling, replay semantics, or layer boundaries during implementation unless concrete evidence proves a defect.

The implementation should proceed table-by-table using the locked Silver decisions and validate:

- canonical identity
- deduplication
- source conflict resolution
- business/relationship/schema DQ
- current-state vs event semantics
- late-arriving records
- idempotent replay
- lineage
- processing metrics

Reference checkpoint: `docs/project/checkpoints/MASTER-2026-09-26-PHASE3-3E-ARCHITECTURE-LOCKED.md`.

### Superseded 3E preparation wording

Earlier runbook text that says Silver source precedence/canonicalization must first be defined is superseded. Those architecture rules were locked on 2026-09-26; the remaining task is implementation and validation.
