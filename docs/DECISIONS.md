# FoodFlow — Architecture Decisions

This document records important technical and architectural decisions made during the FoodFlow project.

The purpose is to preserve the reasoning behind decisions so they can be revisited when the architecture evolves.

---

## Decision 001 — Use Databricks Free Edition for Initial Learning

**Date:** 2026-09-24

**Status:** Accepted

### Context

The initial objective is to learn Databricks, Unity Catalog, Delta Lake, PySpark, Medallion architecture, data quality, and incremental processing through hands-on exercises.

### Decision

Use Databricks Free Edition for the initial implementation.

### Reason

It provides an accessible environment for learning the core Databricks and Delta concepts without immediately introducing additional cloud infrastructure.

### Consequence

Some production Azure capabilities will not be available or appropriate in the current environment and will be introduced later.

---

## Decision 002 — Use Databricks-Managed Storage During the Initial Phase

**Date:** 2026-09-24

**Status:** Accepted

### Context

The project initially attempted to work with Azure ADLS authentication from the current Databricks Free Edition environment.

The environment encountered authentication/configuration limitations, including authorization failures.

### Decision

Use Databricks-managed storage and managed volumes for the current learning phase.

### Reason

This allows the project to continue learning:

* File ingestion
* Delta Lake
* Unity Catalog
* Medallion architecture
* Incremental processing
* MERGE
* Data quality

without blocking progress on external storage authentication.

### Consequence

The current implementation is not yet representative of the final ADLS-based production architecture.

### Future

ADLS Gen2 will be introduced when the appropriate Azure Databricks environment and authentication model are available.

---

## Decision 003 — Use Project-Local Python Virtual Environment

**Date:** 2026-09-24

**Status:** Accepted

### Context

FoodFlow will eventually use multiple Python-based tools and frameworks.

### Decision

Maintain a `.venv` inside the FoodFlow workspace.

westeros_foodflow_workspace/
└── .venv/

### Reason

Project-local environments provide dependency isolation and make the project easier to reproduce.

### Consequence

`.venv/` must never be committed to Git.

---

## Decision 004 — Use GitHub as Project Source of Truth

**Date:** 2026-09-24

**Status:** Accepted

### Context

FoodFlow is a long-running learning and engineering project.

The project will evolve across many technologies and development phases.

### Decision

Use Git and GitHub to maintain the project source code, documentation, architecture decisions, learning history, tests, and configuration templates.

### Reason

Git provides:

* Version history
* Change tracking
* Rollback
* Collaboration
* Backup
* Project evolution history

GitHub provides remote persistence so the project does not depend on a single local machine.

### Consequence

Secrets must never be committed.

---

## Decision 005 — Learn Manually Before Automating With AI

**Date:** 2026-09-24

**Status:** Accepted

### Context

FoodFlow will eventually include AI-assisted engineering and agentic AI.

### Decision

Understand and manually implement important engineering concepts before using AI to automate them.

### Reason

The project is intended to develop engineering understanding rather than simply generate working code.

### Approach

Understand
    ↓
Implement manually
    ↓
Test
    ↓
Document
    ↓
Automate
    ↓
Use AI assistance

AI-generated code must be reviewed and tested before being incorporated.
