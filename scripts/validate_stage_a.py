from src.synthetic_data.database import get_connection


checks = {
    "orphan_order_customers": """
        SELECT COUNT(*)
        FROM dbo.orders o
        LEFT JOIN dbo.customers c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """,

    "orphan_order_restaurants": """
        SELECT COUNT(*)
        FROM dbo.orders o
        LEFT JOIN dbo.restaurants r
            ON o.restaurant_id = r.restaurant_id
        WHERE r.restaurant_id IS NULL
    """,

    "orphan_order_delivery_partners": """
        SELECT COUNT(*)
        FROM dbo.orders o
        LEFT JOIN dbo.delivery_partners d
            ON o.delivery_partner_id = d.delivery_partner_id
        WHERE o.delivery_partner_id IS NOT NULL
          AND d.delivery_partner_id IS NULL
    """,

    "orphan_order_items_orders": """
        SELECT COUNT(*)
        FROM dbo.order_items oi
        LEFT JOIN dbo.orders o
            ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """,

    "orphan_order_items_menu_items": """
        SELECT COUNT(*)
        FROM dbo.order_items oi
        LEFT JOIN dbo.menu_items m
            ON oi.menu_item_id = m.menu_item_id
        WHERE m.menu_item_id IS NULL
    """,

    "orphan_payments": """
        SELECT COUNT(*)
        FROM dbo.payments p
        LEFT JOIN dbo.orders o
            ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
    """,

    "orphan_status_history": """
        SELECT COUNT(*)
        FROM dbo.order_status_history h
        LEFT JOIN dbo.orders o
            ON h.order_id = o.order_id
        WHERE o.order_id IS NULL
    """,

    "orphan_restaurant_reviews": """
        SELECT COUNT(*)
        FROM dbo.restaurant_reviews rr
        LEFT JOIN dbo.orders o
            ON rr.order_id = o.order_id
        WHERE o.order_id IS NULL
    """,

    "orphan_delivery_reviews": """
        SELECT COUNT(*)
        FROM dbo.delivery_partner_reviews dr
        LEFT JOIN dbo.orders o
            ON dr.order_id = o.order_id
        WHERE o.order_id IS NULL
    """,

    "invalid_delivery_partner_usage": """
        SELECT COUNT(*)
        FROM dbo.orders
        WHERE order_type = 'DELIVERY'
          AND delivery_partner_id IS NULL
    """,

    "unexpected_partner_non_delivery": """
        SELECT COUNT(*)
        FROM dbo.orders
        WHERE order_type IN ('DINE_IN', 'TAKE_AWAY')
          AND delivery_partner_id IS NOT NULL
    """,
}


conn = get_connection()

try:
    cursor = conn.cursor()

    print("Stage A relational validation")
    print("=" * 40)

    for name, sql in checks.items():
        cursor.execute(sql)
        row = cursor.fetchone()
        result = row[0] if row is not None else 0
        status = "PASS" if result == 0 else "FAIL"
        print(f"{name}: {result} [{status}]")

finally:
    conn.close()