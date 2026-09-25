# westeros-foodflow — Data Dictionary

## Purpose

This document defines the structure, meaning, and business semantics of the datasets used in the westeros-foodflow project.

The dictionary will evolve as new ingestion patterns, transformations, data quality rules, dimensional models, streaming datasets, and serving layers are introduced.

---

## 1. Current Data Architecture

westeros-foodflow currently uses a Medallion-style architecture:

```text
Source Files
    │
    ▼
Bronze Delta
    │
    ▼
Silver Delta
    │
    ▼
Gold Delta
```

Current implemented datasets:

```text
foodflow_dev.bronze.restaurants
        │
        ▼
foodflow_dev.silver.restaurants
        │
        ├── Data quality checks
        │
        ▼
foodflow_dev.gold.restaurant_performance
```

---

## 2. Source Dataset

### Restaurant Source CSV

Current synthetic source files:

- `restaurants_20260923_01.csv`
- `restaurants_20260923_02.csv`

Future source files follow the naming convention:

```text
YYYYMMDD_<file-sequence-of-day>.csv
```

Example:

- `restaurants_20260924_01.csv`
- `restaurants_20260924_02.csv`

### Source Columns

| Column | Data Type | Description | Business Meaning |
| --- | --- | --- | --- |
| `restaurant_id` | STRING | Unique restaurant identifier | Business key for a restaurant |
| `restaurant_name` | STRING | Restaurant name | Display/business name |
| `city` | STRING | City where restaurant operates | Geographic attribute |
| `state` | STRING | State/province/region | Geographic attribute |
| `country` | STRING | Country | Geographic attribute |
| `address` | STRING | Restaurant address/location description | Location detail |
| `cuisine` | STRING | Cuisine type | Restaurant classification |
| `opening_date` | DATE | Restaurant opening date | Business lifecycle attribute |
| `phone` | STRING | Restaurant phone number | Contact information |
| `rating` | DOUBLE | Restaurant rating | Customer/business rating |

---

## 3. Bronze Layer

### Table

`foodflow_dev.bronze.restaurants`

### Purpose

The Bronze layer represents the raw-ingestion layer.

It preserves source data while adding ingestion metadata required for traceability and operational analysis.

Bronze is intended to remain close to the source representation and should not contain business-level transformations unless required for ingestion or technical processing.

### Current Columns

| Column | Data Type | Description |
| --- | --- | --- |
| `restaurant_id` | STRING | Source restaurant identifier |
| `restaurant_name` | STRING | Restaurant name |
| `city` | STRING | Restaurant city |
| `state` | STRING | State/province/region |
| `country` | STRING | Country |
| `address` | STRING | Restaurant address/location |
| `cuisine` | STRING | Cuisine type |
| `opening_date` | DATE | Restaurant opening date |
| `phone` | STRING | Restaurant phone number |
| `rating` | DOUBLE | Restaurant rating |
| `_ingested_at` | TIMESTAMP | Timestamp when the record was ingested |
| `_ingestion_date` | DATE | Calendar date on which the record was ingested |
| `_source_file` | STRING | Source file from which the record originated |

### Bronze Design Notes

- Bronze retains source-oriented data.
- Technical ingestion metadata is added for traceability.
- Source files are treated as immutable inputs.
- Bronze ingestion and Silver processing are separate concerns.
- Incremental processing uses source files as batches.

---

## 4. Silver Layer

### Table

`foodflow_dev.silver.restaurants`

### Purpose

The Silver layer contains cleaned, validated, deduplicated, and incrementally maintained restaurant records.

Silver represents the current operational state of each restaurant based on its business key.

### Current Columns

| Column | Data Type | Description | Notes |
| --- | --- | --- | --- |
| `restaurant_id` | STRING | Unique restaurant identifier | Business key |
| `restaurant_name` | STRING | Restaurant name | Current value |
| `city` | STRING | Restaurant city | Current value |
| `state` | STRING | State/province/region | Current value |
| `country` | STRING | Country | Current value |
| `address` | STRING | Restaurant address/location | Current value |
| `cuisine` | STRING | Cuisine type | Current value |
| `opening_date` | DATE | Restaurant opening date | Current value |
| `phone` | STRING | Restaurant phone number | Current value |
| `rating` | DOUBLE | Restaurant rating | Current value |
| `_ingested_at` | TIMESTAMP | Timestamp associated with the ingestion that last modified the record | Updated when the record changes |
| `_ingestion_date` | DATE | Ingestion date associated with the ingestion that last modified the record | Updated when the record changes |
| `_source_file` | STRING | Source file associated with the ingestion that last modified the record | Updated when the record changes |
| `_batch_id` | STRING | Identifier of the ingestion batch that last modified the record | Incremental processing metadata |

### Silver Business Key

The current Silver business key is:

```text
restaurant_id
```

Example:

```text
REST-DXB-001
```

The business key is used by the Delta `MERGE` operation to determine whether an incoming record represents:

- an existing restaurant
- a new restaurant

### `MERGE` Logic

Conceptually:

1. If `restaurant_id` exists and business attributes changed, then update the existing record.
2. If `restaurant_id` exists and business attributes are unchanged, then do nothing.
3. If `restaurant_id` does not exist, then insert a new record.

This makes the Silver layer idempotent for replayed source batches.

---

## 5. Incremental Processing Metadata

### `_batch_id`

- Data type: `STRING`
- Purpose: identifies the incremental ingestion batch that last modified the current Silver record.
- Example: `20260924_02`

Important semantic:

`_batch_id` does not represent the first batch in which a restaurant was ever observed.

It represents the batch associated with the most recent change to the current Silver record.

Example:

```text
Batch 20260923_01
    REST-DXB-001 rating = 4.9

Batch 20260924_02
    REST-DXB-001 rating = 4.7

Final Silver record:
    restaurant_id = REST-DXB-001
    rating        = 4.7
    _batch_id     = 20260924_02
```

### Historical Backfill

Historical records created before `_batch_id` existed were backfilled using the following rule:

```sql
WHERE _batch_id IS NULL
  AND _source_file = 'restaurants_20262309_01.csv'
```

They were assigned:

```text
_batch_id = '20260923_01'
```

This was treated as a historical metadata migration/backfill rather than a new ingestion.

### `_source_file`

Identifies the source file associated with the ingestion that last modified the current record.

Example:

```text
restaurants_20262309_02.csv
```

This field provides source-level lineage from the current Silver record back to the source batch.

### `_ingested_at`

- Data type: `TIMESTAMP`
- Purpose: records when the corresponding ingestion operation processed the record.

For updated records, this value is refreshed when the record is modified by a later batch.

### `_ingestion_date`

- Data type: `DATE`
- Purpose: stores the calendar date associated with the ingestion operation.

This field is useful for:

- operational monitoring
- partitioning strategies where appropriate
- batch-level analysis
- troubleshooting
- data freshness analysis

---

## 6. Incremental Batch Example

Batch 2 contained four source rows:

```text
REST-DXB-001
REST-HYD-001
REST-DEL-001
REST-DXB-001
```

After deduplication by `restaurant_id`:

```text
REST-DXB-001
REST-HYD-001
REST-DEL-001
```

The processing outcome was:

| Restaurant | Result |
| --- | --- |
| `REST-DXB-001` | Existing record updated |
| `REST-HYD-001` | New record inserted |
| `REST-DEL-001` | Existing record unchanged |
| Duplicate `REST-DXB-001` | Removed during batch deduplication |

Final Silver row count:

```text
11
```

---

## 7. Current Silver Batch Distribution

After the historical metadata backfill:

| `_batch_id` | Record Count | Meaning |
| --- | ---: | --- |
| `20260923_01` | 9 | Historical records from the initial source batch |
| `20260924_02` | 2 | Records currently associated with the incremental batch |
| `NULL` | 0 | Records without a batch identifier |

Total:

```text
11
```

---

## 8. Gold Layer

### Table

`foodflow_dev.gold.restaurant_performance`

### Purpose

The Gold layer contains business-oriented analytical aggregates derived from Silver.

Current Gold data is grouped by:

- `country`
- `city`
- `cuisine`

### Current Columns

| Column | Data Type | Description |
| --- | --- | --- |
| `country` | STRING | Country grouping |
| `city` | STRING | City grouping |
| `cuisine` | STRING | Cuisine grouping |
| `restaurant_count` | BIGINT | Number of restaurants in the group |
| `average_rating` | DOUBLE | Average restaurant rating |
| `minimum_rating` | DOUBLE | Minimum restaurant rating |
| `maximum_rating` | DOUBLE | Maximum restaurant rating |

### Gold Grain

The current Gold table has the following grain:

One row per `country + city + cuisine`.

Example:

```text
India + Delhi + North Indian
```

This represents one analytical group.

The Gold table is an aggregate and therefore does not have the same row-level grain as the Silver restaurant table.

### Gold Refresh Strategy

The current Gold table is recomputed from Silver rather than incrementally merged.

Reason:

```text
Gold = derived analytical state
```

When Silver changes, the aggregate can be recalculated from the current Silver state.

Current validation:

- Silver row count = 11
- Gold group count = 9
- `SUM(Gold.restaurant_count) = 11`

This confirms that every current Silver restaurant is represented in the Gold aggregation.

---

## 9. Data Quality Expectations

Current data quality checks include validation of:

- row counts
- null values
- duplicate business keys
- expected columns
- rating values
- business key uniqueness
- Silver-to-Gold reconciliation

The following concepts are part of the westeros-foodflow data quality strategy and will expand in later phases:

- freshness
- volume anomalies
- schema changes
- failed records
- late-arriving data
- data drift
- pipeline duration
- throughput
- completeness
- referential integrity

---

## 10. Idempotency

Incremental Silver processing is designed to be idempotent.

Reprocessing the same batch should not create duplicate business records or repeatedly update unchanged records.

The current implementation uses:

- business key
- deduplication
- change detection
- Delta `MERGE`

A replay of the completed Batch 2 produced:

- 0 inserted
- 0 updated
- 0 deleted

This is an important property for reliable batch ingestion and future orchestration.

---

## 11. Future Data Dictionary Expansion

This document will be expanded as westeros-foodflow introduces additional data sources and architecture components.

Planned additions include:

### Relational Sources

- SQL Server
- Azure SQL
- watermark columns
- CDC metadata

### APIs

- JSON structures
- pagination metadata
- API ingestion timestamps
- request/batch identifiers

### Streaming

- event IDs
- event timestamps
- processing timestamps
- watermarks
- partition/offset metadata

### Dimensional Modeling

- `dim_restaurant`
- `dim_customer`
- `dim_date`
- `dim_delivery`
- `fact_orders`

### Slowly Changing Dimensions

- natural keys
- surrogate keys
- effective dates
- expiration dates
- current-record indicators

### Data Contracts

- schema versions
- compatibility rules
- required fields
- breaking changes
- non-breaking changes

### Observability

- pipeline run IDs
- execution IDs
- data quality results
- processing duration
- record counts
- failure information

---

## 12. Naming Conventions

### Source Files

Current convention:

```text
YYYYMMDD_<file-sequence-of-day>.csv
```

### Technical Metadata

Technical metadata columns use a leading underscore:

- `_ingested_at`
- `_ingestion_date`
- `_source_file`
- `_batch_id`

### Tables

Tables follow the Unity Catalog three-level naming pattern:

```text
catalog.schema.table
```

Example:

```text
foodflow_dev.silver.restaurants
```

---

## 13. Data Dictionary Maintenance Rules

When a new dataset or column is introduced:

1. Define its purpose.
2. Document its data type.
3. Document its business meaning.
4. Identify whether it is a business or technical field.
5. Document its grain where applicable.
6. Document the business key where applicable.
7. Document lineage or source information.
8. Update this file in the same feature/phase where the schema changes.
9. Commit the documentation alongside the implementation.

The data dictionary should remain aligned with the actual westeros-foodflow implementation.

18. Naming Conventions
Source Files

Current convention:

YYYYMMDD_<file-sequence-of-day>.csv
Technical Metadata

Technical metadata columns use a leading underscore:

_ingested_at
_ingestion_date
_source_file
_batch_id
Tables

Tables follow the Unity Catalog three-level naming pattern:

catalog.schema.table

Example:

foodflow_dev.silver.restaurants
19. Data Dictionary Maintenance Rules

When a new dataset or column is introduced:

Define its purpose.
Document its data type.
Document its business meaning.
Identify whether it is a business or technical field.
Document its grain where applicable.
Document the business key where applicable.
Document lineage or source information.
Update this file in the same feature/phase where the schema changes.
Commit the documentation alongside the implementation.

The data dictionary should remain aligned with the actual westeros-foodflow implementation.

---

# 9. Phase 3 Relational SQL Source

## Relational source database

The Phase 3 source database is:

```text
Azure SQL
  Server: sql-westeros-foodflow-dev
  Database: westeros-foodflow
```

The relational domain contains ten tables.

### 9.1 `customers`

| Column | Type | Key / Rule |
|---|---|---|
| `customer_id` | BIGINT | PK / IDENTITY |
| `customer_name` | VARCHAR(150) | NOT NULL |
| `email` | VARCHAR(255) | NOT NULL; unique |
| `phone` | VARCHAR(20) | Nullable |
| `city` | VARCHAR(100) | Nullable |
| `state` | VARCHAR(100) | Nullable |
| `created_at` | DATETIME2 | NOT NULL |
| `updated_at` | DATETIME2 | NOT NULL; incremental extraction candidate |
| `is_active` | BIT | NOT NULL |

### 9.2 `restaurants`

| Column | Type | Key / Rule |
|---|---|---|
| `restaurant_id` | VARCHAR(20) | PK / business key |
| `restaurant_name` | VARCHAR(150) | NOT NULL |
| `city` | VARCHAR(100) | NOT NULL |
| `state` | VARCHAR(100) | NOT NULL |
| `country` | VARCHAR(100) | NOT NULL |
| `address` | VARCHAR(300) | Nullable |
| `cuisine` | VARCHAR(100) | NOT NULL |
| `opening_date` | DATE | NOT NULL |
| `phone` | VARCHAR(20) | Nullable |
| `rating` | DECIMAL(3,2) | Nullable |
| `created_at` | DATETIME2 | NOT NULL |
| `updated_at` | DATETIME2 | NOT NULL |
| `is_active` | BIT | NOT NULL |

Restaurant identifiers use business values such as:

```text
REST-SHJ-001
REST-SHJ-002
REST-DEL-001
REST-BLR-001
```

### 9.3 `menu_items`

| Column | Type | Key / Rule |
|---|---|---|
| `menu_item_id` | BIGINT | PK / IDENTITY / globally unique |
| `restaurant_id` | VARCHAR(20) | FK to `restaurants` |
| `item_name` | VARCHAR(150) | NOT NULL |
| `category` | VARCHAR(100) | Nullable |
| `description` | VARCHAR(500) | Nullable |
| `price` | DECIMAL(10,2) | Positive |
| `is_available` | BIT | NOT NULL |
| `created_at` | DATETIME2 | NOT NULL |
| `updated_at` | DATETIME2 | NOT NULL |

`menu_item_id` is the sole primary key. No composite `(menu_item_id, restaurant_id)` key is used.

### 9.4 `orders`

| Column | Type | Key / Rule |
|---|---|---|
| `order_id` | BIGINT | PK / IDENTITY |
| `customer_id` | BIGINT | FK |
| `restaurant_id` | VARCHAR(20) | FK |
| `delivery_partner_id` | BIGINT | Nullable FK |
| `order_type` | VARCHAR(20) | `DINE_IN`, `TAKE_AWAY`, `DELIVERY` |
| `order_status` | VARCHAR(30) | Lifecycle status |
| `order_total` | DECIMAL(12,2) | Positive |
| `delivery_fee` | DECIMAL(10,2) | Positive/non-negative as defined by validation |
| `tax_amount` | DECIMAL(10,2) | Positive/non-negative as defined by validation |
| `order_date` | DATETIME2(3) | NOT NULL |
| `created_at` | DATETIME2(3) | NOT NULL |
| `updated_at` | DATETIME2(3) | NOT NULL; watermark candidate |

Order lifecycle values include:

```text
PLACED
CONFIRMED
PREPARING
READY_FOR_PICKUP
PICKED_UP
ON_THE_WAY
DELIVERED
CANCELLED_BY_CUSTOMER
CANCELLED_PAYMENT_FAILURE
```

### 9.5 `order_items`

| Column | Type | Key / Rule |
|---|---|---|
| `order_item_id` | BIGINT | PK / IDENTITY |
| `order_id` | BIGINT | FK |
| `menu_item_id` | BIGINT | FK |
| `quantity` | INT | Positive |
| `unit_price` | DECIMAL(10,2) | Historical transaction snapshot |
| `created_at` | DATETIME2(3) | NOT NULL |
| `updated_at` | DATETIME2(3) | NOT NULL |

`unit_price` records the transaction-time price and is intentionally independent from the current `menu_items.price`.

### 9.6 `payments`

| Column | Type | Key / Rule |
|---|---|---|
| `payment_id` | BIGINT | PK / IDENTITY |
| `order_id` | BIGINT | FK |
| `payment_method` | VARCHAR(30) | `UPI`, `CARD`, `NET_BANKING`, `CASH`, `WALLET` |
| `payment_status` | VARCHAR(30) | `PENDING`, `AUTHORIZED`, `SUCCESS`, `FAILED`, `REFUNDED` |
| `amount` | DECIMAL(12,2) | Positive |
| `transaction_reference` | VARCHAR(100) | Nullable |
| `created_at` | DATETIME2(3) | NOT NULL |
| `updated_at` | DATETIME2(3) | NOT NULL |

### 9.7 `delivery_partners`

| Column | Type | Key / Rule |
|---|---|---|
| `delivery_partner_id` | BIGINT | PK / IDENTITY |
| `partner_name` | VARCHAR(150) | NOT NULL |
| `phone` | VARCHAR(20) | Nullable |
| `vehicle_type` | VARCHAR(30) | Nullable |
| `city` | VARCHAR(100) | NOT NULL |
| `status` | VARCHAR(30) | `AVAILABLE`, `BUSY`, `OFFLINE` |
| `created_at` | DATETIME2(3) | NOT NULL |
| `updated_at` | DATETIME2(3) | NOT NULL |

### 9.8 `order_status_history`

| Column | Type | Key / Rule |
|---|---|---|
| `status_history_id` | BIGINT | PK / IDENTITY |
| `order_id` | BIGINT | FK |
| `status` | VARCHAR(30) | Lifecycle status |
| `status_timestamp` | DATETIME2(3) | NOT NULL |
| `changed_by` | VARCHAR(50) | Nullable |

This table stores lifecycle events; `orders.order_status` represents current state.

### 9.9 `restaurant_reviews`

| Column | Type | Key / Rule |
|---|---|---|
| `review_id` | BIGINT | PK / IDENTITY |
| `order_id` | BIGINT | FK |
| `customer_id` | BIGINT | FK |
| `restaurant_id` | VARCHAR(20) | FK |
| `rating` | DECIMAL(2,1) | 1–5 |
| `review_text` | VARCHAR(1000) | Nullable |
| `created_at` | DATETIME2(3) | NOT NULL |
| `updated_at` | DATETIME2(3) | NOT NULL |

### 9.10 `delivery_partner_reviews`

| Column | Type | Key / Rule |
|---|---|---|
| `review_id` | BIGINT | PK / IDENTITY |
| `order_id` | BIGINT | FK |
| `customer_id` | BIGINT | FK |
| `delivery_partner_id` | BIGINT | FK |
| `rating` | DECIMAL(2,1) | 1–5 |
| `review_text` | VARCHAR(1000) | Nullable |
| `created_at` | DATETIME2(3) | NOT NULL |
| `updated_at` | DATETIME2(3) | NOT NULL |

---

## 10. SQL ingestion metadata

SQL ingestion uses source-system/batch metadata rather than `_source_file`:

| Metadata field | Purpose |
|---|---|
| `_ingested_at` | Timestamp of ingestion |
| `_ingestion_date` | Calendar date of ingestion |
| `_source_system` | Identifies Azure SQL as the source |
| `_batch_id` | Identifies the ingestion batch |

The existing CSV-specific `_source_file` lineage remains unchanged for historical CSV processing.

---

## 11. Dataset implementation sequence

The relational dataset is intentionally staged:

1. Stage A: 10 restaurants, 100 customers, 500 orders.
2. Stage A2: deterministic scaling to approximately 5K orders.
3. Stage B: AI-assisted generation to approximately 15K orders.
4. ADF phase: approximately 250K orders and approximately 2.9M relational rows.

The 250K-order dataset is not created during initial Azure SQL provisioning.
