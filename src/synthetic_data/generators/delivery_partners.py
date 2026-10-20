from datetime import datetime, timedelta


VEHICLES = ["BIKE", "SCOOTER", "CAR"]


def generate_delivery_partners(cfg, rng):
    rows = []
    base = datetime.now() - timedelta(days=300)

    for i in range(1, cfg.delivery_partner_count + 1):
        rows.append({
            "partner_name": f"Delivery Partner {i:03d}",
            "phone": f"+91-92000{i:05d}",
            "vehicle_type": rng.choice(VEHICLES),
            "city": rng.choice(["Delhi", "Bengaluru", "Mumbai", "Hyderabad", "Sharjah"]),
            "status": rng.choices(
                ["AVAILABLE", "BUSY", "OFFLINE"],
                weights=[65, 25, 10],
                k=1,
            )[0],
            "created_at": base + timedelta(days=rng.randint(0, 240)),
            "updated_at": base + timedelta(days=rng.randint(241, 300)),
        })
    return rows
