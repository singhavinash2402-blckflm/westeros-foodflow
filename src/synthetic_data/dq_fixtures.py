from pathlib import Path
import csv


def write_controlled_dq_fixtures(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = [
        {
            "scenario_id": "DQ-001",
            "table_name": "orders",
            "scenario": "DELIVERY_WITH_NULL_PARTNER",
            "description": "DELIVERY order without delivery_partner_id",
        },
        {
            "scenario_id": "DQ-002",
            "table_name": "orders",
            "scenario": "NON_DELIVERY_WITH_PARTNER",
            "description": "DINE_IN/TAKE_AWAY order with delivery_partner_id",
        },
        {
            "scenario_id": "DQ-003",
            "table_name": "restaurant_reviews",
            "scenario": "RATING_OUTSIDE_RANGE",
            "description": "Rating outside 1-5; do not load into constrained production table",
        },
        {
            "scenario_id": "DQ-004",
            "table_name": "order_items",
            "scenario": "NEGATIVE_QUANTITY",
            "description": "Negative quantity; do not load into constrained production table",
        },
        {
            "scenario_id": "DQ-005",
            "table_name": "orders",
            "scenario": "UNKNOWN_RESTAURANT_ID",
            "description": "Unknown restaurant business key; FK rejection scenario",
        },
    ]

    path = output_dir / "controlled_dq_fixtures.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return path
