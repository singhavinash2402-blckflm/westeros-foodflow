# westeros-foodflow — AI and Agentic Data Engineering Roadmap

## 1. Purpose

This roadmap defines how AI is introduced into `westeros-foodflow` without replacing foundational data-engineering learning.

The project intentionally progresses:

```text
Manual
   ↓
Deterministic automation
   ↓
AI-assisted automation
   ↓
Governed agentic workflows
```

---

## 2. AI-assisted automation

AI may be used to accelerate repetitive work after the underlying engineering pattern is understood.

Examples:

- SQL generation
- Synthetic-data generation
- PySpark boilerplate
- Validation-query generation
- Data-quality test-case generation
- Documentation drafting
- Test-case expansion
- Scaling scripts

Human responsibilities remain:

- architecture
- design decisions
- code review
- execution approval
- validation
- diagnosis
- security
- cost control

---

## 3. Stage B — AI-assisted dataset generation

The first substantial AI-assisted workflow is Phase 3 Stage B.

Goal:

- scale the validated deterministic design toward approximately 15K orders.

AI can assist with:

1. generating repetitive data-generation code;
2. producing SQL/templates;
3. proposing validation queries;
4. expanding test cases;
5. documenting generated datasets;
6. identifying likely data-quality edge cases.

The generated output must be reviewed and validated before execution.

---

## 4. Governed agentic workflows

Agentic workflows are introduced only after the underlying ingestion, transformation, validation, and orchestration patterns are understood.

Planned agents:

### westeros-foodflow Data Agent

Responsibilities:

- answer governed questions about available datasets;
- inspect approved schemas;
- explain lineage and data definitions.

### westeros-foodflow Ingestion Agent

Responsibilities:

- inspect ingestion status;
- validate expected source availability;
- execute bounded ingestion operations where explicitly authorized;
- verify ingestion results.

### westeros-foodflow Curation / Transformation / Analytics Agent

Responsibilities:

- propose transformations;
- inspect data-quality results;
- run approved transformations;
- validate outputs;
- report analytical findings.

### westeros-foodflow Monitoring and Reporting Agent

Responsibilities:

- inspect pipeline/table health;
- summarize failures;
- inspect logs/history;
- produce operational reports;
- propose remediation.

### westeros-foodflow Prediction / ML / Analytics Agent

Responsibilities:

- prepare approved analytical datasets;
- run bounded analytical workflows;
- report model/analysis outputs;
- surface assumptions and validation results.

---

## 5. Required agent control loop

Every operational agent should follow:

```text
Goal
  ↓
Plan
  ↓
Tool selection
  ↓
Execute bounded action
  ↓
Inspect intermediate result
  ↓
Validate
  ↓
Retry within limits if required
  ↓
Report result and evidence
  ↓
Human governance where required
```

Agents should not receive unrestricted production-like access.

---

## 6. Governance requirements

Agentic workflows must include:

- least-privilege tool access;
- explicit action boundaries;
- validation gates;
- bounded retries;
- observable execution;
- audit-friendly reporting;
- safe failure behavior;
- human approval for consequential actions.

The project will treat an agent as an engineering system, not simply as a chat interface.

---

## 7. Learning checkpoints

AI/agentic work is considered complete only when the user can explain:

- what the agent is doing;
- which tools it can use;
- why each tool is needed;
- what data it can access;
- what validations protect the workflow;
- what happens on failure;
- when human approval is required;
- how execution is audited.
