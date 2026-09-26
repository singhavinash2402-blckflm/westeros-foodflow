from datetime import datetime, timedelta


ORDER_TYPES = ["DINE_IN", "TAKE_AWAY", "DELIVERY"]


def generate_orders(cfg, rng, customers, restaurants, delivery_partners, menu_items):
    now = datetime.now()
    start = now - timedelta(days=cfg.order_window_days)

    menus_by_restaurant = {}
    for item in menu_items:
        menus_by_restaurant.setdefault(item["restaurant_id"], []).append(item)

    rows = []
    item_rows = []

    for n in range(1, cfg.order_count + 1):
        restaurant = rng.choice(restaurants)
        customer = rng.choice(customers)
        order_type = rng.choices(ORDER_TYPES, weights=[20, 20, 60], k=1)[0]
        order_date = start + timedelta(
            days=rng.randint(0, cfg.order_window_days - 1),
            minutes=rng.randint(0, 1439),
        )

        # Stage A is a clean baseline dataset. Business-rule violations are
        # maintained separately in controlled_dq_fixtures.csv so they can be
        # tested intentionally without contaminating the normal load.
        delivery_partner = (
            rng.choice(delivery_partners) if order_type == "DELIVERY" else None
        )

        status = rng.choices(
            [
                "DELIVERED", "CONFIRMED", "PREPARING", "READY_FOR_PICKUP",
                "PICKED_UP", "ON_THE_WAY", "CANCELLED_BY_CUSTOMER",
                "CANCELLED_PAYMENT_FAILURE"
            ],
            weights=[62, 8, 5, 4, 4, 5, 8, 4],
            k=1,
        )[0]

        selected_items = rng.sample(
            menus_by_restaurant[restaurant["restaurant_id"]],
            k=min(
                rng.randint(cfg.min_order_items, cfg.max_order_items),
                len(menus_by_restaurant[restaurant["restaurant_id"]]),
            ),
        )

        order_items = []
        subtotal = 0.0
        for menu_item in selected_items:
            quantity = rng.randint(1, 3)
            unit_price = menu_item["price"]
            subtotal += quantity * unit_price
            order_items.append((menu_item, quantity, unit_price))

        delivery_fee = round(rng.uniform(20, 80), 2) if order_type == "DELIVERY" else 0.0
        tax_amount = round(subtotal * 0.05, 2)
        order_total = round(subtotal + delivery_fee + tax_amount, 2)

        rows.append({
            "customer_id_ref": customer["email"],
            "restaurant_id": restaurant["restaurant_id"],
            "delivery_partner_ref": delivery_partner["partner_name"] if delivery_partner else None,
            "order_type": order_type,
            "order_status": status,
            "order_total": order_total,
            "delivery_fee": delivery_fee,
            "tax_amount": tax_amount,
            "order_date": order_date,
            "created_at": order_date,
            "updated_at": order_date + timedelta(minutes=rng.randint(1, 30)),
        })

        item_rows.append({
            "order_index": n,
            "items": order_items,
        })

    return rows, item_rows
