from datetime import date, datetime, timedelta
import random


CITIES = [
    ("SHJ", "Sharjah", "Sharjah", "UAE"),
    ("DEL", "Delhi", "Delhi", "India"),
    ("BLR", "Bengaluru", "Karnataka", "India"),
    ("MUM", "Mumbai", "Maharashtra", "India"),
    ("HYD", "Hyderabad", "Telangana", "India"),
]

CUISINES = [
    "North Indian", "South Indian", "Chinese", "Italian", "Continental",
    "Mughlai", "Biryani", "Street Food", "Cafe", "Asian"
]


def generate_restaurants(cfg, rng):
    rows = []
    base_date = date.today() - timedelta(days=240)

    for i in range(1, cfg.restaurant_count + 1):
        code, city, state, country = CITIES[(i - 1) % len(CITIES)]
        rows.append({
            "restaurant_id": f"REST-{code}-{i:03d}",
            "restaurant_name": f"{city} Kitchen {i:02d}",
            "city": city,
            "state": state,
            "country": country,
            "address": f"{i * 11} Food Street, {city}",
            "cuisine": CUISINES[(i - 1) % len(CUISINES)],
            "opening_date": base_date + timedelta(days=i * 7),
            "phone": f"+91-90000{i:05d}",
            "rating": round(rng.uniform(3.4, 4.8), 2),
            "created_at": datetime.combine(base_date + timedelta(days=i * 3), datetime.min.time()),
            "updated_at": datetime.combine(base_date + timedelta(days=i * 3), datetime.min.time()),
            "is_active": True,
        })
    return rows
