from datetime import timedelta


LIFECYCLE = [
    "PLACED",
    "CONFIRMED",
    "PREPARING",
    "READY_FOR_PICKUP",
    "PICKED_UP",
    "ON_THE_WAY",
    "DELIVERED",
]


def generate_status_history(order, rng):
    order_status = order["order_status"]

    if order_status == "CANCELLED_BY_CUSTOMER":
        statuses = ["PLACED", "CONFIRMED", "CANCELLED_BY_CUSTOMER"]
    elif order_status == "CANCELLED_PAYMENT_FAILURE":
        statuses = ["PLACED", "CANCELLED_PAYMENT_FAILURE"]
    elif order_status in LIFECYCLE:
        end = LIFECYCLE.index(order_status)
        statuses = LIFECYCLE[: end + 1]
    else:
        statuses = ["PLACED"]

    rows = []
    for i, status in enumerate(statuses):
        rows.append({
            "status": status,
            "status_timestamp": order["order_date"] + timedelta(minutes=i * rng.randint(3, 15)),
            "changed_by": rng.choice(["SYSTEM", "RESTAURANT", "CUSTOMER", "DELIVERY_APP"]),
        })
    return rows
