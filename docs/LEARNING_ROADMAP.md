# FoodFlow — Learning Roadmap

## Learning Philosophy

FoodFlow follows a build-first learning approach.

For each technology:

```text
Concept
   ↓
Small manual exercise
   ↓
Realistic FoodFlow implementation
   ↓
Failure / edge cases
   ↓
Testing
   ↓
Optimization
   ↓
Automation
   ↓
AI assistance
```

AI is used to accelerate repetitive work only after the underlying engineering concepts are understood.

---

## Roadmap

### Foundation

- [x] Python installation
- [x] Project-local Python virtual environment
- [x] VS Code Python interpreter configuration
- [x] Git installation
- [x] Git configuration
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

### Incremental Processing — Current

- [ ] Second source file
- [ ] New records
- [ ] Updated records
- [ ] Duplicate records
- [ ] Deduplication
- [ ] Business keys
- [ ] Delta `MERGE`
- [ ] Idempotency
- [ ] Batch/audit columns
- [ ] Validation
- [ ] Delta history after incremental processing

### Relational Data

- [ ] SQL Server / Azure SQL
- [ ] Source table design
- [ ] Full ingestion
- [ ] Watermarking
- [ ] Incremental ingestion
- [ ] Incremental validation

### Azure Data Factory

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

### CDC

- [ ] Insert handling
- [ ] Update handling
- [ ] Delete handling
- [ ] CDC versus watermarking
- [ ] CDC to Delta
- [ ] MERGE-based processing

### Cloud Storage

- [ ] ADLS Gen2
- [ ] Azure RBAC
- [ ] Managed identity
- [ ] Secure Databricks access
- [ ] AWS S3
- [ ] AWS IAM
- [ ] Multi-cloud ingestion

### APIs

- [ ] REST API fundamentals
- [ ] Authentication
- [ ] Pagination
- [ ] Rate limits
- [ ] JSON
- [ ] Nested JSON
- [ ] Schema evolution
- [ ] Incremental API ingestion

### dbt and Modeling

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

### Streaming

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

### Airflow

- [ ] Local Airflow
- [ ] DAGs
- [ ] Tasks
- [ ] Dependencies
- [ ] Scheduling
- [ ] Sensors
- [ ] Retries
- [ ] Backfills
- [ ] Parameters
- [ ] Connections
- [ ] Variables
- [ ] Databricks orchestration
- [ ] Monitoring

### Production Engineering

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

### AI / Agentic AI

- [ ] SQL assistant
- [ ] PySpark assistant
- [ ] Data-quality assistant
- [ ] Pipeline documentation assistant
- [ ] Operational data-engineering agent
- [ ] Agent for pipeline/log/DQ diagnosis
- [ ] AI-generated remediation recommendations
