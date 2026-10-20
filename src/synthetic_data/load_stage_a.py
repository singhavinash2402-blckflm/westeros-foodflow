import argparse
import random

from .config import StageAConfig
from .database import get_connection
from .dq_fixtures import write_controlled_dq_fixtures
from .generators.customers import generate_customers
from .generators.delivery_partners import generate_delivery_partners
from .generators.menu_items import generate_menu_items
from .generators.orders import generate_orders
from .generators.order_status_history import generate_status_history
from .generators.restaurants import generate_restaurants
from .generators.reviews import generate_reviews


TABLES = [
    "customers", "restaurants", "menu_items", "orders", "order_items",
    "payments", "delivery_partners", "order_status_history",
    "restaurant_reviews", "delivery_partner_reviews"
]


def assert_empty(cursor):
    for table in TABLES:
        cursor.execute(f"SELECT TOP 1 1 FROM dbo.{table}")
        if cursor.fetchone():
            raise RuntimeError(
                f"dbo.{table} is not empty. "
                "Use --reset with --confirm-reset RESET_STAGE_A only if this is the intended learning database."
            )


def reset_tables(cursor):
    # Child -> parent order. This is intentionally explicit for learning.
    for table in [
        "delivery_partner_reviews", "restaurant_reviews", "order_status_history",
        "payments", "order_items", "orders", "menu_items",
        "delivery_partners", "customers", "restaurants"
    ]:
        cursor.execute(f"DELETE FROM dbo.{table}")


def insert_stage_a(cursor, cfg):
    rng = random.Random(cfg.seed)

    restaurants = generate_restaurants(cfg, rng)
    customers = generate_customers(cfg, rng)
    partners = generate_delivery_partners(cfg, rng)
    menu_items = generate_menu_items(restaurants, cfg, rng)
    orders, item_plan = generate_orders(
        cfg, rng, customers, restaurants, partners, menu_items
    )
    restaurant_reviews, delivery_reviews = generate_reviews(cfg, rng, orders)

    # Parent/reference data first.
    for r in restaurants:
        cursor.execute("""
            INSERT INTO dbo.restaurants
            (restaurant_id, restaurant_name, city, state, country, address, cuisine,
             opening_date, phone, rating, created_at, updated_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["restaurant_id"], r["restaurant_name"], r["city"], r["state"], r["country"],
            r["address"], r["cuisine"], r["opening_date"], r["phone"], r["rating"],
            r["created_at"], r["updated_at"], r["is_active"]
        ))

    for c in customers:
        cursor.execute("""
            INSERT INTO dbo.customers
            (customer_name, email, phone, city, state, created_at, updated_at, is_active)
            OUTPUT INSERTED.customer_id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["customer_name"], c["email"], c["phone"], c["city"], c["state"],
            c["created_at"], c["updated_at"], c["is_active"]
        ))

    customer_ids = {}
    cursor.execute("SELECT customer_id, email FROM dbo.customers")
    for row in cursor.fetchall():
        customer_ids[row.email] = row.customer_id

    for p in partners:
        cursor.execute("""
            INSERT INTO dbo.delivery_partners
            (partner_name, phone, vehicle_type, city, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            p["partner_name"], p["phone"], p["vehicle_type"], p["city"], p["status"],
            p["created_at"], p["updated_at"]
        ))

    partner_ids = {}
    cursor.execute("SELECT delivery_partner_id, partner_name FROM dbo.delivery_partners")
    for row in cursor.fetchall():
        partner_ids[row.partner_name] = row.delivery_partner_id

    for m in menu_items:
        cursor.execute("""
            INSERT INTO dbo.menu_items
            (restaurant_id, item_name, category, description, price, is_available, created_at, updated_at)
            OUTPUT INSERTED.menu_item_id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m["restaurant_id"], m["item_name"], m["category"], m["description"],
            m["price"], m["is_available"], m["created_at"], m["updated_at"]
        ))

    menu_ids = {}
    cursor.execute("SELECT menu_item_id, restaurant_id, item_name FROM dbo.menu_items")
    for row in cursor.fetchall():
        menu_ids[(row.restaurant_id, row.item_name)] = row.menu_item_id

    order_ids = {}

    # Orders are inserted one-by-one deliberately in Stage A so the identity mapping is explicit.
    for idx, order in enumerate(orders, start=1):
        delivery_id = (
            partner_ids[order["delivery_partner_ref"]]
            if order["delivery_partner_ref"] else None
        )
        customer_id = customer_ids[order["customer_id_ref"]]

        cursor.execute("""
            INSERT INTO dbo.orders
            (customer_id, restaurant_id, delivery_partner_id, order_type, order_status,
             order_total, delivery_fee, tax_amount, order_date, created_at, updated_at)
            OUTPUT INSERTED.order_id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_id, order["restaurant_id"], delivery_id, order["order_type"],
            order["order_status"], order["order_total"], order["delivery_fee"],
            order["tax_amount"], order["order_date"], order["created_at"], order["updated_at"]
        ))
        order_ids[idx] = cursor.fetchone()[0]

    # Transaction-time item snapshot.
    for plan in item_plan:
        order_id = order_ids[plan["order_index"]]
        for menu_item, quantity, unit_price in plan["items"]:
            menu_id = menu_ids[(menu_item["restaurant_id"], menu_item["item_name"])]
            cursor.execute("""
                INSERT INTO dbo.order_items
                (order_id, menu_item_id, quantity, unit_price, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                order_id, menu_id, quantity, unit_price,
                orders[plan["order_index"] - 1]["created_at"],
                orders[plan["order_index"] - 1]["updated_at"],
            ))

    # One payment per order in Stage A.
    from .generators.payments import generate_payment
    rng_payment = random.Random(cfg.seed + 1)
    for idx, order in enumerate(orders, start=1):
        payment = generate_payment(order, rng_payment)
        cursor.execute("""
            INSERT INTO dbo.payments
            (order_id, payment_method, payment_status, amount, transaction_reference, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            order_ids[idx], payment["payment_method"], payment["payment_status"],
            payment["amount"], payment["transaction_reference"],
            payment["created_at"], payment["updated_at"]
        ))

    # Lifecycle history.
    rng_status = random.Random(cfg.seed + 2)
    for idx, order in enumerate(orders, start=1):
        for h in generate_status_history(order, rng_status):
            cursor.execute("""
                INSERT INTO dbo.order_status_history
                (order_id, status, status_timestamp, changed_by)
                VALUES (?, ?, ?, ?)
            """, (
                order_ids[idx], h["status"], h["status_timestamp"], h["changed_by"]
            ))

    # Reviews are generated from delivered orders only.
    for review in restaurant_reviews:
        idx = review["order_index"]
        order = orders[idx - 1]
        cursor.execute("""
            INSERT INTO dbo.restaurant_reviews
            (order_id, customer_id, restaurant_id, rating, review_text, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            order_ids[idx], customer_ids[order["customer_id_ref"]], order["restaurant_id"],
            review["rating"], review["review_text"], review["created_at"], review["updated_at"]
        ))

    for review in delivery_reviews:
        idx = review["order_index"]
        order = orders[idx - 1]
        cursor.execute("""
            INSERT INTO dbo.delivery_partner_reviews
            (order_id, customer_id, delivery_partner_id, rating, review_text, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            order_ids[idx], customer_ids[order["customer_id_ref"]],
            partner_ids[order["delivery_partner_ref"]], review["rating"],
            review["review_text"], review["created_at"], review["updated_at"]
        ))

    return {
        "restaurants": len(restaurants),
        "customers": len(customers),
        "menu_items": len(menu_items),
        "delivery_partners": len(partners),
        "orders": len(orders),
        "order_items": sum(len(x["items"]) for x in item_plan),
        "restaurant_reviews": len(restaurant_reviews),
        "delivery_reviews": len(delivery_reviews),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--confirm-reset")
    args = parser.parse_args()

    if args.reset and args.confirm_reset != "RESET_STAGE_A":
        raise SystemExit(
            "Reset requires: --reset --confirm-reset RESET_STAGE_A"
        )

    cfg = StageAConfig()
    conn = get_connection()
    try:
        cursor = conn.cursor()

        if args.reset:
            reset_tables(cursor)
            conn.commit()
        else:
            assert_empty(cursor)

        counts = insert_stage_a(cursor, cfg)
        conn.commit()

        print("Stage A loaded successfully.")
        for key, value in counts.items():
            print(f"  {key}: {value}")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
