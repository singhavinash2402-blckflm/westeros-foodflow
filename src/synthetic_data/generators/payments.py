from datetime import timedelta


def generate_payment(order, rng):
    if order["order_status"] == "CANCELLED_PAYMENT_FAILURE":
        status = "FAILED"
    elif order["order_status"] == "CANCELLED_BY_CUSTOMER":
        status = rng.choice(["FAILED", "REFUNDED"])
    else:
        status = rng.choices(["SUCCESS", "AUTHORIZED", "PENDING"], [85, 10, 5], k=1)[0]

    method = rng.choice(["UPI", "CARD", "NET_BANKING", "CASH", "WALLET"])
    reference = None if method == "CASH" else f"TXN-{rng.randint(10000000, 99999999)}"

    return {
        "payment_method": method,
        "payment_status": status,
        "amount": order["order_total"],
        "transaction_reference": reference,
        "created_at": order["order_date"] + timedelta(minutes=2),
        "updated_at": order["updated_at"],
    }
