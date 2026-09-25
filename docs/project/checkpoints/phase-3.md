# westeros-foodflow Phase 3 Checkpoint — Relational SQL Source

**Status:** Stage 3A in progress — Azure SQL provisioned; schema creation next
**Current master checkpoint:** `FOODFLOW-2026-09-25-PHASE3-PHYSICAL-DESIGN-AI-AUTOMATION-LINEAGE-LOCKED`

## 1. Relational domain — LOCKED

Tables:
1. `customers`
2. `restaurants`
3. `menu_items`
4. `orders`
5. `order_items`
6. `payments`
7. `delivery_partners`
8. `order_status_history`
9. `restaurant_reviews`
10. `delivery_partner_reviews`

Restaurant IDs use business identifiers such as:
- `REST-SHJ-001`
- `REST-SHJ-002`
- `REST-DEL-001`
- `REST-BLR-001`

`restaurants.restaurant_id` is the business PK and is `VARCHAR(20)`.

## 2. Physical design — LOCKED

- Transactional/entity PKs: `BIGINT IDENTITY`.
- `restaurants.restaurant_id`: `VARCHAR(20)` business PK.
- `menu_items.menu_item_id`: globally unique `BIGINT IDENTITY` sole PK.
- `menu_items.restaurant_id`: FK to `restaurants`.
- `order_items.menu_item_id`: FK to `menu_items` only.
- No composite menu-item PK.
- Operational timestamps: `DATETIME2(3)`.
- Order/payment totals: `DECIMAL(12,2)`.
- Menu/unit prices: `DECIMAL(10,2)`.
- Boolean flags: `BIT`.
- PK/FK/domain/access-pattern constraints and indexes are part of the design.
- `created_at` / `updated_at` are used where appropriate.
- No CDC initially.

## 3. Order design

`order_type`:
- `DINE_IN`
- `TAKE_AWAY`
- `DELIVERY`

Order lifecycle:
- `PLACED`
- `CONFIRMED`
- `PREPARING`
- `READY_FOR_PICKUP`
- `PICKED_UP`
- `ON_THE_WAY`
- `DELIVERED`
- `CANCELLED_BY_CUSTOMER`
- `CANCELLED_PAYMENT_FAILURE`

## 4. Incremental SQL ingestion — LOCKED

Full load:

```sql
SELECT * FROM dbo.orders;
```

Watermark pattern:

```sql
SELECT *
FROM dbo.orders
WHERE updated_at > @last_watermark
  AND updated_at <= @current_watermark;
```

Initial watermark ingestion captures inserts/updates but not hard deletes. Boundary testing includes records exactly at the lower and upper watermark timestamps.

Later topics:
- soft deletes;
- Change Tracking;
- CDC;
- production-grade incremental patterns.

## 5. Azure SQL foundation — COMPLETED

Provisioned:

- Resource group: `rg-westeros-foodflow-dev`
- SQL server: `sql-westeros-foodflow-dev`
- Database: `westeros-foodflow`
- Region: Central India
- Azure SQL Free Offer
- General Purpose / Serverless / Standard-series (Gen5)
- 2 vCores
- 32 GB
- Zone redundancy disabled
- Locally redundant backup storage
- Overage billing disabled
- Azure services/resources access disabled
- Private endpoint none
- Minimum TLS 1.2
- Identity not enabled
- Service-managed TDE

## 6. Dataset implementation sequence — LOCKED

```text
Azure SQL
   ↓
Create schema
   ↓
Stage A
10 restaurants
100 customers
500 orders
   ↓
Validate relationships
   ↓
JDBC connectivity
   ↓
SQL → Bronze
   ↓
Bronze → Silver
   ↓
Stage A2 — deterministic scaling to 5K
   ↓
Stage B — AI-assisted generation to ~15K
   ↓
ADF
   ↓
250K orders / ~2.9M relational rows
```

### Stage A — Manual

Purpose:
- understand SQL DDL;
- relationships;
- data generation;
- validation;
- JDBC extraction;
- Bronze;
- Silver;
- data quality.

### Stage A2 — Deterministic automation

Purpose:
- parameterized/scripted data generation;
- reusable SQL/templates;
- configurable row counts;
- repeatable validation;
- repeatable test scenarios.

AI is not required for this stage.

### Stage B — AI-assisted automation

Target approximately 15K orders.

AI may assist with:
- repetitive data-generation code;
- SQL;
- validation queries;
- scaling;
- test-case generation;
- documentation.

Human remains responsible for architecture, review, validation, execution approval, and diagnosis.

## 7. 15K dataset target — LOCKED

- 5,000 customers
- 100 restaurants
- 3,000 menu items
- 500 delivery partners
- ~15,000 orders
- ~2–5 order items per order
- ~15,000 payments
- multiple status-history events per applicable order
- ~1,000 restaurant reviews
- ~500 delivery-partner reviews

Orders represent approximately 60 days of naturally varying activity. Master entities may predate the 60-day order period.

## 8. ADF-scale dataset — LOCKED

Introduced during the ADF phase:

| Table | Initial records |
|---|---:|
| customers | 25,000 |
| restaurants | 500 |
| menu_items | 15,000 |
| delivery_partners | 1,000 |
| orders | 250,000 |
| order_items | ~750,000 |
| payments | ~250,000 |
| order_status_history | ~1,500,000 |
| restaurant_reviews | ~75,000 |
| delivery_partner_reviews | ~40,000 |

Approximately 2.9M relational rows.

The large dataset is deliberately **not** created immediately after Azure SQL provisioning.

## 9. Controlled data-quality scenarios — LOCKED

Examples:
- DELIVERY + NULL `delivery_partner_id`
- DINE_IN/TAKE_AWAY + populated delivery partner
- rating outside 1–5
- negative quantity
- unknown restaurant ID
- other documented business-rule violations

## 10. Analytics — LOCKED

Monthly historical rating aggregation:
- restaurant average rating and review count;
- delivery-partner average rating and review count;
- useful rating distributions/trends.

Order lifecycle analytics distinguish:
- successful/completed deliveries;
- customer cancellations;
- payment-failure cancellations.

## 11. Databricks / storage decision

Current environment is Databricks Free Edition. The project uses Databricks-managed storage/managed volumes/managed Delta tables for this environment because the attempted direct Azure Storage integration encountered Free Edition authentication/configuration limitations.

Direct Azure SQL/JDBC remains a separate integration pattern.

## 12. Current next implementation step

**Create and validate the locked 10-table Azure SQL schema.**

After schema creation:

1. populate Stage A;
2. validate relationships and business rules;
3. verify JDBC;
4. implement SQL → Bronze;
5. implement Bronze → Silver;
6. validate the ingestion and data-quality patterns.
