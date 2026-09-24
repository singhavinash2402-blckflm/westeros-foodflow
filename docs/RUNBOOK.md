# FoodFlow — Runbook

## 1. Purpose

This runbook contains practical procedures for developing, validating, troubleshooting, and operating FoodFlow.

The document will evolve as new technologies and pipeline components are introduced.

---

# 2. Local Development Environment

## Workspace

C:\Work\westeros_foodflow_workspace

## Python Environment

.venv\

Activate the environment from PowerShell:

.venv\Scripts\Activate.ps1

Expected prompt:

(.venv) PS C:\Work\westeros_foodflow_workspace>

Verify Python:

python --version

Verify the active interpreter:

where.exe python

Expected first result:

C:\Work\westeros_foodflow_workspace\.venv\Scripts\python.exe

Verify pip:

python -m pip --version

---

# 3. Git Operations

Check repository status:

git status

View repository history:

git log --oneline

View changes:

git diff

Stage changes:

git add .

Create a commit:

git commit -m "descriptive message"

Review recent commits:

git log --oneline --decorate

---

# 4. Git Safety Rules

Never commit:

* Passwords
* API keys
* Access tokens
* Cloud credentials
* Private keys
* Connection strings containing credentials
* `.env` files
* `.venv`
* Generated caches

Before committing:

git status

Review staged files:

git diff --cached

---

# 5. Databricks Workflow

Current environment:

Databricks Free Edition

Current storage approach:

Databricks-managed storage
Databricks-managed volume

Current processing pattern:

Source File
    ↓
Bronze
    ↓
Silver
    ↓
Gold

---

# 6. Current Incremental Processing Workflow

The next implementation uses:

restaurants_20262309_02.csv

Expected test scenarios:

* New restaurant records
* Updated restaurant records
* Duplicate records

Known update test:

REST-DXB-001
rating: 4.9 → 4.7

Expected processing:

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

---

# 7. Incremental Validation Checklist

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

# 8. Future Azure Workflow

When ADLS Gen2 is introduced:

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

Authentication and authorization will use appropriate Azure identity and access-control mechanisms.

Credentials must never be embedded in notebooks or committed to Git.

---

# 9. Future AWS Workflow

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
