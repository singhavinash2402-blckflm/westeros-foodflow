import argparse
import csv
import random
from pathlib import Path

from .config import StageAConfig
from .generators.customers import generate_customers
from .generators.delivery_partners import generate_delivery_partners
from .generators.menu_items import generate_menu_items
from .generators.orders import generate_orders
from .generators.payments import generate_payment
from .generators.restaurants import generate_restaurants
from .generators.reviews import generate_reviews
from .generators.order_status_history import generate_status_history
from .dq_fixtures import write_controlled_dq_fixtures


def build_dataset(cfg):
    rng = random.Random(cfg.seed)

    restaurants = generate_restaurants(cfg, rng)
    customers = generate_customers(cfg, rng)
    delivery_partners = generate_delivery_partners(cfg, rng)
    menu_items = generate_menu_items(restaurants, cfg, rng)
    orders, order_item_plan = generate_orders(
        cfg, rng, customers, restaurants, delivery_partners, menu_items
    )

    restaurant_reviews, delivery_reviews = generate_reviews(cfg, rng, orders)

    # Use separate deterministic RNG streams for child datasets so adding or
    # changing one generator does not silently reshuffle another dataset.
    rng_payment = random.Random(cfg.seed + 1)
    payments = [
        {"order_index": idx, **generate_payment(order, rng_payment)}
        for idx, order in enumerate(orders, start=1)
    ]

    rng_status = random.Random(cfg.seed + 2)
    status_history = []
    for idx, order in enumerate(orders, start=1):
        for history in generate_status_history(order, rng_status):
            status_history.append({"order_index": idx, **history})

    # Flatten relational child collections for CSV inspection. The database
    # loader later resolves order_index/menu-item references to SQL identities.
    order_items = []
    for plan in order_item_plan:
        for menu_item, quantity, unit_price in plan["items"]:
            order_items.append({
                "order_index": plan["order_index"],
                "restaurant_id": menu_item["restaurant_id"],
                "item_name": menu_item["item_name"],
                "quantity": quantity,
                "unit_price": unit_price,
            })

    return {
        "restaurants": restaurants,
        "customers": customers,
        "delivery_partners": delivery_partners,
        "menu_items": menu_items,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "status_history": status_history,
        "restaurant_reviews": restaurant_reviews,
        "delivery_reviews": delivery_reviews,
    }


def write_csv(rows, path):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def dry_run(cfg, output_dir):
    data = build_dataset(cfg)

    output_dir.mkdir(parents=True, exist_ok=True)

    for name in [
        "restaurants",
        "customers",
        "delivery_partners",
        "menu_items",
        "orders",
        "order_items",
        "payments",
        "status_history",
        "restaurant_reviews",
        "delivery_reviews",
    ]:
        write_csv(data[name], output_dir / f"{name}.csv")

    # DQ fixtures are deliberately separate from the clean Stage A dataset.
    write_controlled_dq_fixtures(output_dir)

    print("Stage A dry-run generated:")
    print(f"  restaurants:          {len(data['restaurants'])}")
    print(f"  customers:            {len(data['customers'])}")
    print(f"  menu_items:           {len(data['menu_items'])}")
    print(f"  delivery_partners:    {len(data['delivery_partners'])}")
    print(f"  orders:               {len(data['orders'])}")
    print(f"  order_items:          {len(data['order_items'])}")
    print(f"  payments:             {len(data['payments'])}")
    print(f"  status_history:       {len(data['status_history'])}")
    print(f"  restaurant_reviews:   {len(data['restaurant_reviews'])}")
    print(f"  delivery_reviews:     {len(data['delivery_reviews'])}")
    print(f"  output:               {output_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default="artifacts/stage_a")
    args = parser.parse_args()

    cfg = StageAConfig()

    # Stage A starts with dry-run generation. The database loader is deliberately
    # a separate next step so generated data can be inspected before INSERT.
    if args.dry_run:
        dry_run(cfg, Path(args.output))
    else:
        raise SystemExit(
            "Database loading is intentionally a separate step. "
            "Run with --dry-run first, inspect the generated dataset, "
            "then use the reviewed loader."
        )


if __name__ == "__main__":
    main()
