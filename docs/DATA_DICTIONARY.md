# FoodFlow — Data Dictionary

This document defines the datasets, entities, fields, keys, and business meanings used throughout FoodFlow.

The dictionary will evolve as new source systems and analytical models are introduced.

---

## 1. Data Layer Definitions

| Layer  | Purpose                                        |
| ------ | ---------------------------------------------- |
| Raw    | Original source files before processing        |
| Bronze | Ingested source data persisted in Delta format |
| Silver | Cleaned and standardized data                  |
| Gold   | Business-ready analytical data                 |

---

## 2. Current Source

### Restaurant Dataset

The initial FoodFlow dataset represents restaurant information.

The dataset is used to demonstrate:

* File ingestion
* Data quality
* Data transformation
* Aggregation
* Incremental processing
* Updates
* Duplicate handling
* Delta MERGE

---

## 3. Business Key

The restaurant identifier is used as the business key for incremental processing.

Example:

REST-DXB-001

The business key will be used to identify whether an incoming restaurant record represents:

* A new restaurant
* An existing restaurant requiring an update
* A duplicate record

---

## 4. Incremental Test Scenario

The second restaurant source file will contain a test update for:

Restaurant ID: REST-DXB-001

Expected rating change:

4.9 → 4.7

This test case will be used to validate Delta MERGE behavior.

---

## 5. Future Dimensional Model

The planned analytical model includes:

dim_restaurant
dim_customer
dim_date
dim_delivery
fact_orders

The detailed column definitions will be added when these models are implemented.

---

## 6. Data Dictionary Rules

For each production-style dataset, document:

* Column name
* Data type
* Nullable/non-nullable
* Business definition
* Source
* Business key
* Surrogate key
* Transformation logic
* Allowed values where applicable
* Data quality rules
* Sensitivity classification where applicable

The dictionary should be updated whenever the schema changes.
