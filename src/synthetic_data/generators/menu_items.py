from datetime import datetime


CATEGORIES = {
    "North Indian": ["Paneer Tikka", "Dal Makhani", "Butter Chicken", "Jeera Rice"],
    "South Indian": ["Masala Dosa", "Idli Sambar", "Vada", "Lemon Rice"],
    "Chinese": ["Hakka Noodles", "Fried Rice", "Manchurian", "Chilli Paneer"],
    "Italian": ["Margherita Pizza", "Pasta Alfredo", "Lasagna", "Garlic Bread"],
    "Continental": ["Grilled Sandwich", "Pasta Bowl", "Veg Burger", "Chicken Burger"],
    "Mughlai": ["Chicken Korma", "Seekh Kebab", "Biryani", "Roomali Roti"],
    "Biryani": ["Chicken Biryani", "Mutton Biryani", "Veg Biryani", "Raita"],
    "Street Food": ["Pav Bhaji", "Chole Bhature", "Samosa", "Aloo Tikki"],
    "Cafe": ["Cold Coffee", "Cappuccino", "Club Sandwich", "Brownie"],
    "Asian": ["Thai Curry", "Ramen", "Sushi Roll", "Teriyaki Bowl"],
}


def generate_menu_items(restaurants, cfg, rng):
    rows = []
    now = datetime.now()

    for restaurant in restaurants:
        names = CATEGORIES.get(restaurant["cuisine"], ["House Special", "Chef Bowl", "Classic Meal"])
        count = rng.randint(*cfg.menu_items_per_restaurant)
        for j in range(1, count + 1):
            name = f"{names[(j - 1) % len(names)]} {j}"
            rows.append({
                "restaurant_id": restaurant["restaurant_id"],
                "item_name": name,
                "category": restaurant["cuisine"],
                "description": f"Signature {restaurant['cuisine']} item at {restaurant['restaurant_name']}",
                "price": round(rng.uniform(90, 650), 2),
                "is_available": rng.random() > 0.05,
                "created_at": now,
                "updated_at": now,
            })
    return rows
