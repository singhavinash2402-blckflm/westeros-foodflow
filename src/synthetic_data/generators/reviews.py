from datetime import timedelta


REVIEW_TEXTS = [
    "Good food and timely service.",
    "Very tasty and nicely packed.",
    "Food was fresh and enjoyable.",
    "Service was acceptable.",
    "Would order again.",
]


def generate_reviews(cfg, rng, orders):
    restaurant_reviews = []
    delivery_reviews = []

    for idx, order in enumerate(orders, start=1):
        if order["order_status"] != "DELIVERED":
            continue

        if rng.random() < cfg.restaurant_review_rate:
            rating = rng.choice([3.0, 3.5, 4.0, 4.5, 5.0])
            restaurant_reviews.append({
                "order_index": idx,
                "rating": rating,
                "review_text": rng.choice(REVIEW_TEXTS),
                "created_at": order["updated_at"] + timedelta(hours=2),
                "updated_at": order["updated_at"] + timedelta(hours=2),
            })

        if order["order_type"] == "DELIVERY" and order.get("delivery_partner_ref"):
            if rng.random() < cfg.delivery_review_rate:
                delivery_reviews.append({
                    "order_index": idx,
                    "rating": rng.choice([3.0, 3.5, 4.0, 4.5, 5.0]),
                    "review_text": rng.choice(REVIEW_TEXTS),
                    "created_at": order["updated_at"] + timedelta(hours=3),
                    "updated_at": order["updated_at"] + timedelta(hours=3),
                })

    return restaurant_reviews, delivery_reviews
