# westeros-foodflow — Learning Roadmap

## Learning Philosophy

The project follows a build-first learning approach:

```text
Concept
   ↓
Small manual exercise
   ↓
Realistic implementation
   ↓
Failure / edge cases
   ↓
Testing
   ↓
Optimization
   ↓
Deterministic automation
   ↓
AI assistance
   ↓
Governed agentic workflows
```

AI is used to accelerate repetitive work only after the underlying engineering concepts are understood.

---

## Completed foundations

### Foundation

- [x] Python installation
- [x] Project-local Python virtual environment
- [x] VS Code Python interpreter configuration
- [x] Git installation/configuration
- [x] Git repository initialization
- [x] `.gitignore`

### Databricks and Delta

- [x] Databricks Free Edition
- [x] Unity Catalog
- [x] Catalog and schema design
- [x] Managed volume
- [x] Raw CSV ingestion
- [x] Bronze Delta
- [x] Silver Delta
- [x] Data quality checks
- [x] Gold aggregation
- [x] Delta history
- [x] Execution plan analysis

### Incremental CSV

- [x] Multiple source batches
- [x] New records
- [x] Updated records
- [x] Duplicate records
- [x] Deduplication
- [x] Business keys
- [x] Delta `MERGE`
- [x] Idempotency
- [x] Batch/audit columns
- [x] Historical metadata backfill
- [x] Validation
- [x] Delta history

---

# Current — Relational SQL

## Stage 3A

- [x] Azure SQL resource group
- [x] Azure SQL logical server
- [x] Azure SQL database
- [x] Free Offer configuration
- [ ] 10-table relational schema
- [ ] Stage A dataset
- [ ] Relationship validation
- [ ] Business-rule validation
- [ ] JDBC connectivity
- [ ] SQL → Bronze
- [ ] Bronze → Silver
- [ ] SQL watermark extraction
- [ ] Lower/upper watermark boundary testing

## Stage A2 — Deterministic scaling

- [ ] Parameterized data generation
- [ ] Repeatable validation
- [ ] Repeatable test scenarios
- [ ] 5K dataset
- [ ] Scale validation

## Stage B — AI-assisted generation

- [ ] AI-assisted repetitive generation
- [ ] Human review/approval
- [ ] ~15K dataset
- [ ] ~60-day order activity
- [ ] Scale validation
- [ ] Document AI assistance

---

# Future — Azure Data Factory

- [ ] Linked services
- [ ] Datasets
- [ ] Parameters
- [ ] Variables
- [ ] Copy Activity
- [ ] Lookup
- [ ] ForEach
- [ ] Metadata-driven ingestion
- [ ] Triggers
- [ ] Retries
- [ ] Monitoring
- [ ] Databricks orchestration

## Large-scale dataset

- [ ] 250K orders
- [ ] ~2.9M relational rows
- [ ] ADF ingestion/orchestration against the large dataset

---

# Future — CDC

- [ ] Insert handling
- [ ] Update handling
- [ ] Delete handling
- [ ] Watermark versus Change Tracking
- [ ] Watermark versus CDC
- [ ] CDC to Delta
- [ ] MERGE-based CDC processing

---

# Future — Cloud Storage

- [ ] ADLS Gen2
- [ ] Azure RBAC
- [ ] Managed identity
- [ ] Secure Databricks access
- [ ] AWS S3
- [ ] AWS IAM
- [ ] Multi-cloud ingestion

---

# Future — APIs and JSON

- [ ] REST API fundamentals
- [ ] Authentication
- [ ] Pagination
- [ ] Rate limits
- [ ] JSON
- [ ] Nested JSON
- [ ] Schema evolution
- [ ] Incremental API ingestion

---

# Future — dbt and Modeling

- [ ] dbt setup
- [ ] Staging models
- [ ] Intermediate models
- [ ] Mart models
- [ ] `ref()`
- [ ] Incremental models
- [ ] Tests
- [ ] Documentation
- [ ] Lineage
- [ ] Star schema
- [ ] SCD Type 1
- [ ] SCD Type 2

---

# Future — Streaming

- [ ] Event Hubs
- [ ] Structured Streaming
- [ ] Streaming Bronze
- [ ] Streaming Silver
- [ ] Streaming Gold
- [ ] Event time
- [ ] Processing time
- [ ] Watermarks
- [ ] Late events
- [ ] Stateful processing
- [ ] Checkpoints
- [ ] Deduplication
- [ ] Kafka concepts

---

# Future — Production Engineering

- [ ] Data quality
- [ ] Data contracts
- [ ] Schema evolution
- [ ] Unit testing
- [ ] Integration testing
- [ ] Observability
- [ ] Performance optimization
- [ ] Cost optimization
- [ ] Security
- [ ] Secrets management
- [ ] Terraform
- [ ] GitHub Actions
- [ ] CI/CD
- [ ] Power BI

---

# AI / Agentic AI progression

## AI-assisted automation

- [ ] SQL generation assistance
- [ ] PySpark generation assistance
- [ ] Synthetic data generation assistance
- [ ] Data-quality test generation
- [ ] Documentation assistance
- [ ] Validation assistance

## Governed agentic workflows

- [ ] Data Agent
- [ ] Ingestion Agent
- [ ] Curation/Transformation/Analytics Agent
- [ ] Monitoring/Reporting Agent
- [ ] Prediction/ML/Analytics Agent
- [ ] Tool permission boundaries
- [ ] Planning constraints
- [ ] Validation gates
- [ ] Bounded retry/recovery
- [ ] Human approval
- [ ] Audit/reporting
