# westeros-foodflow — AI / Agentic Engineering Roadmap

## Locked principle

AI must follow understanding, not replace it. The project sequence is:

```text
Manual understanding
      ↓
Deterministic automation
      ↓
AI-assisted automation
      ↓
Governed agents
```

## Stage A — manual/deterministic foundation

The learner must understand SQL DDL, relationships, synthetic-data generation, validation, JDBC, Bronze, Silver, lineage, and data-quality behavior before delegating the work to AI or agents.

## Stage A2 — deterministic scaling

Target: approximately 5K orders.

Focus: repeatable generation, larger-volume validation, performance, and operational reliability without hiding the control flow behind AI.

## Stage B — AI-assisted scaling

Target: approximately 15K orders.

AI can assist with repetitive generation code, SQL, validation queries, test expansion, documentation, and scaling. Human review remains mandatory.

## Future governed agents

Potential specialized agents:

- Data Agent
- Ingestion Agent
- Curation / Transformation / Analytics Agent
- Monitoring and Reporting Agent
- Prediction / ML / Analytical Agent

## Required agent governance

Future agents must have explicit tools and permissions, bounded execution, validation gates, bounded retries, auditable outputs, clear failure reporting, and human approval where appropriate. No unrestricted destructive actions.

## Current status

No governed agent is part of the current Phase 3A execution path. Current work is Bronze → Silver. AI-assisted dataset generation remains a later Stage B activity after deterministic ~5K scaling.
