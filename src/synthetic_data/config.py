from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class StageAConfig:
    seed: int = 20260926
    restaurant_count: int = 10
    customer_count: int = 100
    menu_items_per_restaurant: tuple[int, int] = (6, 10)
    delivery_partner_count: int = 20
    order_count: int = 500
    min_order_items: int = 1
    max_order_items: int = 5
    restaurant_review_rate: float = 0.20
    delivery_review_rate: float = 0.12

    # Approximately 60 days of order activity.
    order_window_days: int = 60

    @property
    def run_timestamp(self) -> datetime:
        return datetime.now(timezone.utc)
