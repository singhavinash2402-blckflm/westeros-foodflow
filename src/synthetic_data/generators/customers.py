from datetime import datetime, timedelta


FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Kabir", "Ishaan", "Rohan",
    "Ananya", "Diya", "Ira", "Meera", "Priya", "Neha", "Kavya", "Aisha"
]
LAST_NAMES = [
    "Sharma", "Singh", "Verma", "Gupta", "Patel", "Khan", "Mehta",
    "Kapoor", "Joshi", "Malhotra"
]


def generate_customers(cfg, rng):
    rows = []
    base = datetime.now() - timedelta(days=420)

    for i in range(1, cfg.customer_count + 1):
        first = FIRST_NAMES[(i - 1) % len(FIRST_NAMES)]
        last = LAST_NAMES[((i - 1) // len(FIRST_NAMES)) % len(LAST_NAMES)]
        rows.append({
            "customer_name": f"{first} {last} {i:03d}",
            "email": f"customer{i:03d}@westeros-foodflow.local",
            "phone": f"+91-91000{i:05d}",
            "city": rng.choice(["Delhi", "Bengaluru", "Mumbai", "Hyderabad", "Sharjah"]),
            "state": rng.choice(["Delhi", "Karnataka", "Maharashtra", "Telangana", "Sharjah"]),
            "created_at": base + timedelta(days=rng.randint(0, 300)),
            "updated_at": base + timedelta(days=rng.randint(301, 420)),
            "is_active": True,
        })
    return rows
