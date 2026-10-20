/*
    westeros-foodflow — Stage A validation
    Run after the Stage A dataset is loaded.

    Structural PK/FK integrity is enforced by Azure SQL.
    These checks focus on business rules and source-data sanity.
*/

-- 1. Row counts
SELECT 'customers' AS table_name, COUNT_BIG(*) AS row_count FROM dbo.customers
UNION ALL SELECT 'restaurants', COUNT_BIG(*) FROM dbo.restaurants
UNION ALL SELECT 'menu_items', COUNT_BIG(*) FROM dbo.menu_items
UNION ALL SELECT 'delivery_partners', COUNT_BIG(*) FROM dbo.delivery_partners
UNION ALL SELECT 'orders', COUNT_BIG(*) FROM dbo.orders
UNION ALL SELECT 'order_items', COUNT_BIG(*) FROM dbo.order_items
UNION ALL SELECT 'payments', COUNT_BIG(*) FROM dbo.payments
UNION ALL SELECT 'order_status_history', COUNT_BIG(*) FROM dbo.order_status_history
UNION ALL SELECT 'restaurant_reviews', COUNT_BIG(*) FROM dbo.restaurant_reviews
UNION ALL SELECT 'delivery_partner_reviews', COUNT_BIG(*) FROM dbo.delivery_partner_reviews;

-- 2. Orders with missing customer / restaurant references
SELECT COUNT_BIG(*) AS orphan_customer_orders
FROM dbo.orders o
LEFT JOIN dbo.customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;

SELECT COUNT_BIG(*) AS orphan_restaurant_orders
FROM dbo.orders o
LEFT JOIN dbo.restaurants r ON r.restaurant_id = o.restaurant_id
WHERE r.restaurant_id IS NULL;

-- 3. Menu item belongs to the restaurant referenced by the order
SELECT COUNT_BIG(*) AS restaurant_menu_mismatch
FROM dbo.order_items oi
JOIN dbo.orders o ON o.order_id = oi.order_id
JOIN dbo.menu_items mi ON mi.menu_item_id = oi.menu_item_id
WHERE mi.restaurant_id <> o.restaurant_id;

-- 4. Delivery business-rule scenarios
SELECT COUNT_BIG(*) AS delivery_without_partner
FROM dbo.orders
WHERE order_type = 'DELIVERY'
  AND delivery_partner_id IS NULL;

SELECT COUNT_BIG(*) AS non_delivery_with_partner
FROM dbo.orders
WHERE order_type IN ('DINE_IN', 'TAKE_AWAY')
  AND delivery_partner_id IS NOT NULL;

-- 5. Ratings
SELECT COUNT_BIG(*) AS invalid_restaurant_ratings
FROM dbo.restaurant_reviews
WHERE rating < 1 OR rating > 5;

SELECT COUNT_BIG(*) AS invalid_delivery_ratings
FROM dbo.delivery_partner_reviews
WHERE rating < 1 OR rating > 5;

-- 6. Positive quantities and amounts
SELECT COUNT_BIG(*) AS invalid_quantities
FROM dbo.order_items
WHERE quantity <= 0;

SELECT COUNT_BIG(*) AS invalid_order_totals
FROM dbo.orders
WHERE order_total <= 0;

SELECT COUNT_BIG(*) AS invalid_payment_amounts
FROM dbo.payments
WHERE amount <= 0;

-- 7. Payment/order amount reconciliation
SELECT COUNT_BIG(*) AS payment_amount_mismatches
FROM dbo.payments p
JOIN dbo.orders o ON o.order_id = p.order_id
WHERE ABS(p.amount - o.order_total) > 0.01;

-- 8. Status history final state should agree with orders.current status
WITH latest_status AS (
    SELECT
        order_id,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY status_timestamp DESC, status_history_id DESC
        ) AS rn
    FROM dbo.order_status_history
)
SELECT COUNT_BIG(*) AS current_status_mismatches
FROM dbo.orders o
JOIN latest_status s
  ON s.order_id = o.order_id
 AND s.rn = 1
WHERE s.status <> o.order_status;
