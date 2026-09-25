# westeros-foodflow — Runbook

## 1. Purpose

This runbook contains practical procedures for developing, validating, troubleshooting, and operating westeros-foodflow.

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

## 6. Historical Incremental CSV Processing Workflow

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

The following sections will be added as westeros-foodflow grows:

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

## 12. Phase 3 — Azure SQL Foundation

Current Azure SQL resources:

```text
Resource Group:
rg-westeros-foodflow-dev

SQL Server:
sql-westeros-foodflow-dev

Database:
westeros-foodflow
```

Current configuration:

- Azure SQL Free Offer
- General Purpose / Serverless / Standard-series (Gen5)
- 2 vCores
- 32 GB
- Central India
- Zone redundancy disabled
- Locally redundant backup storage
- Overage billing disabled
- Azure services/resources access disabled
- Private endpoint none
- Minimum TLS 1.2
- Identity not enabled
- Service-managed TDE

### Current Phase 3 sequence

```text
Azure SQL
   ↓
Create 10-table schema
   ↓
Stage A — 10 restaurants / 100 customers / 500 orders
   ↓
Validate relationships and business rules
   ↓
JDBC
   ↓
SQL → Bronze
   ↓
Bronze → Silver
   ↓
Stage A2 — 5K deterministic dataset
   ↓
Stage B — ~15K AI-assisted dataset
   ↓
ADF
   ↓
250K orders / ~2.9M relational rows
```

Do not create the 250K-order dataset during initial SQL setup.

---

## 13. Phase 3 — Relational Schema Validation

Before inserting Stage A data:

1. Execute the schema DDL.
2. Confirm all ten tables exist.
3. Confirm primary keys.
4. Confirm foreign keys.
5. Confirm domain constraints.
6. Confirm customer email uniqueness.
7. Confirm indexes, especially `updated_at` indexes.
8. Confirm `IDENTITY` behavior for surrogate keys.

After Stage A data is loaded:

1. Validate all foreign-key relationships.
2. Validate order-item references.
3. Validate payment references.
4. Validate status-history references.
5. Validate review references.
6. Validate `DELIVERY` partner rules.
7. Validate review ratings.
8. Validate positive quantities and monetary values.

---

## 14. Phase 3 — JDBC Connectivity

The SQL source will be accessed from Databricks through JDBC.

Do not place credentials directly in notebooks or Git.

The initial connectivity test should prove:

```text
Databricks
   ↓
JDBC
   ↓
Azure SQL
   ↓
SELECT against a known table
```

Only after connectivity is verified should the SQL → Bronze ingestion implementation begin.

---

## 15. Phase 3 — SQL Watermark Extraction

Full extraction example:

```sql
SELECT * FROM dbo.orders;
```

Incremental extraction:

```sql
SELECT *
FROM dbo.orders
WHERE updated_at > @last_watermark
  AND updated_at <= @current_watermark;
```

Validation must include:

- record exactly at `last_watermark`;
- record just after `last_watermark`;
- record exactly at `current_watermark`;
- record just after `current_watermark`.

Expected rule:

- lower boundary is exclusive;
- upper boundary is inclusive.

This pattern captures inserts and updates represented by `updated_at`, but not hard deletes.

---

## 16. Documentation After Each Completed Stage

At every completed stage:

1. Update `docs/PROJECT_PLAN.md`.
2. Update `docs/PROGRESS.md`.
3. Update `docs/LEARNING_LOG.md`.
4. Update architecture/data dictionary/decisions as applicable.
5. Update the relevant checkpoint.
6. Update `docs/AI_AGENT_ROADMAP.md` if AI/agentic scope changes.
7. Review `git diff`.
8. Review `git status`.
9. Commit.
10. Push only at the agreed milestone.

Current decision: Phase 3 checkpoint commits remain local until Phase 3 is complete.
