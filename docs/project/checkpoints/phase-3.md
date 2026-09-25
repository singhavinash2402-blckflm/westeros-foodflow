# FoodFlow Phase 3 Checkpoint — Relational SQL Source

**Status:** Design locked; implementation next  
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

## 5. Initial dataset — LOCKED

Full initial target:
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

## 6. Learning and automation progression — LOCKED

### Stage A — Manual
Small foundational dataset:
- 10 restaurants
- 100 customers
- 500 orders

Purpose:
- understand SQL DDL;
- relationships;
- data generation;
- validation;
- JDBC extraction;
- Bronze;
- Silver;
- data quality.

### Stage A2 — Simple deterministic automation
Before AI is introduced:
- parameterized/scripted data generation;
- reusable SQL/templates;
- configurable row counts;
- repeatable validation;
- repeatable test scenarios;
- scripted execution.

Purpose: learn how ordinary engineering automation scales a process that is already understood.

### Stage B — AI-assisted automation
Scale toward the ~15,000-order dataset.

AI may assist with:
- repetitive data-generation code;
- SQL;
- validation queries;
- scaling;
- test-case generation;
- documentation.

Human remains responsible for architecture, review, validation, execution approval, and diagnosis.

### Stage C — Governed agentic workflows
Specialized agents are planned for:
- Data;
- Ingestion;
- Curation/Transformation/Analytics;
- Monitoring/Reporting;
- Prediction/ML/Analytics.

Agents must have bounded planning, tool use, validation, bounded retry, reporting, and human governance.

## 7. Controlled data-quality scenarios — LOCKED

Examples:
- DELIVERY + NULL `delivery_partner_id`
- DINE_IN/TAKE_AWAY + populated delivery partner
- rating outside 1–5
- negative quantity
- unknown restaurant ID
- other documented business-rule violations

## 8. Analytics — LOCKED

Monthly historical rating aggregation:
- restaurant average rating and review count;
- delivery-partner average rating and review count;
- useful rating distributions/trends.

Order lifecycle analytics distinguish:
- successful/completed deliveries;
- customer cancellations;
- payment-failure cancellations.

## 9. Databricks / storage decision

Current environment is Databricks Free Edition. The project uses Databricks-managed storage/managed volumes/managed Delta tables for this environment because the attempted direct Azure Storage integration encountered Free Edition authentication/configuration limitations.

Direct Azure SQL/JDBC remains a separate integration pattern to verify.

## 10. Next implementation step

Verify current Azure SQL pricing/free allowances before provisioning.

Then:
1. choose the smallest suitable Azure SQL configuration;
2. provision Azure SQL;
3. execute Stage A manually;
4. implement Stage A2 deterministic automation;
5. move to Stage B AI-assisted scaling;
6. implement SQL → Bronze → Silver → Gold flows and downstream orchestration/performance work.

## Current master checkpoint

`FOODFLOW-2026-09-25-PHASE3-PHYSICAL-DESIGN-AI-AUTOMATION-LINEAGE-LOCKED`
