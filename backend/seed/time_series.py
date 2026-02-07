from __future__ import annotations
"""
Sales history generator: 2 years of daily sales data with:
- Diwali surge (+60%)
- Monsoon dip (-30% exterior, +40% waterproofing)
- Summer peak (+20% interior)
- Wedding season (+25% North)
- "The Great Mumbai Rain of 2025" narrative spike
- "Bridal Red" hero product story
- YoY growth (8%, premium 15%)
- Day-of-week effects
- Random noise
"""

import numpy as np
from datetime import date, timedelta


def is_diwali_period(d: date) -> bool:
    """Diwali falls in Oct-Nov. Main shopping 2 weeks before."""
    return (d.month == 10 and d.day >= 15) or (d.month == 11 and d.day <= 10)


def is_monsoon(d: date) -> bool:
    return d.month in (6, 7, 8, 9)


def is_summer(d: date) -> bool:
    return d.month in (3, 4, 5)


def is_wedding_season(d: date) -> bool:
    return d.month in (11, 12, 1, 2)


def is_holi_period(d: date) -> bool:
    return d.month == 3 and 10 <= d.day <= 20


def is_mumbai_rain_event(d: date) -> bool:
    """The Great Mumbai Rain of 2025: Oct 8-15"""
    return d.year == 2025 and d.month == 10 and 8 <= d.day <= 15


def generate_daily_sales(
    sku_id: int,
    region_id: int,
    product_category: str,
    shade_name: str,
    is_premium: bool,
    base_daily_demand: float,
    start_date: date,
    end_date: date,
    rng: np.random.Generator,
) -> list[dict]:
    """Generate daily sales records for one SKU-region combination."""
    records = []
    current = start_date
    days_from_start = 0

    while current <= end_date:
        # Base demand
        demand = base_daily_demand

        # YoY growth trend
        year_fraction = days_from_start / 365.0
        if is_premium:
            demand *= (1 + 0.15 * year_fraction)  # 15% YoY for premium
        else:
            demand *= (1 + 0.08 * year_fraction)  # 8% YoY for economy

        # --- Seasonal Multipliers ---

        # Diwali surge: +60% for all paints
        if is_diwali_period(current):
            demand *= 1.6

        # Monsoon effects
        if is_monsoon(current):
            if product_category == "Waterproofing":
                demand *= 1.4  # +40% waterproofing
            elif product_category == "Exterior Wall":
                demand *= 0.7  # -30% exterior
            else:
                demand *= 0.9  # slight dip for interior too

        # Summer peak for interior
        if is_summer(current):
            if product_category == "Interior Wall":
                demand *= 1.2  # +20%

        # Wedding season in North
        if is_wedding_season(current) and region_id in (1, 2):  # North region IDs
            demand *= 1.25  # +25%
            # Extra boost for Bridal Red during wedding season
            if shade_name == "Bridal Red":
                demand *= 1.4  # additional 40% for the hero product

        # Holi period
        if is_holi_period(current):
            if product_category == "Exterior Wall":
                demand *= 1.15  # washable exterior paint

        # --- Narrative Events ---

        # The Great Mumbai Rain of 2025
        if is_mumbai_rain_event(current) and product_category == "Waterproofing" and region_id in (4, 5):  # West
            demand *= 3.0  # Massive spike!

        # Trending shade boost (last 6 months of data)
        if shade_name in ("Bridal Red", "Pacific Breeze", "Mint Fresh", "Sunrise Yellow"):
            months_from_end = (end_date - current).days / 30
            if months_from_end < 6:
                demand *= 1.0 + (0.4 * (1 - months_from_end / 6))  # Ramp up

        # --- Day-of-week effect ---
        if current.weekday() == 6:  # Sunday
            demand *= 0.6
        elif current.weekday() == 5:  # Saturday
            demand *= 0.85

        # --- Random noise ---
        noise = rng.normal(1.0, 0.15)
        demand = max(0, demand * noise)

        quantity = max(0, int(round(demand)))

        if quantity > 0:
            records.append({
                "sku_id": sku_id,
                "region_id": region_id,
                "date": current,
                "quantity_sold": quantity,
                "revenue": 0.0,  # Filled later from SKU MRP
                "channel": rng.choice(["dealer", "dealer", "dealer", "online", "institutional"]),
            })

        current += timedelta(days=1)
        days_from_start += 1

    return records


# Top SKU-region combinations to generate detailed time series for
# Format: (shade_name, product_category, region_ids, base_demand, is_premium)
TOP_SKU_REGION_CONFIGS = [
    ("Bridal Red", "Interior Wall", [1, 4], 35, True),           # Hero: North + West
    ("Ivory Dream", "Interior Wall", [1, 2], 45, True),          # Popular white
    ("Pacific Breeze", "Interior Wall", [2, 3], 30, True),       # Trending blue
    ("Terracotta Dream", "Exterior Wall", [1, 4], 25, True),     # Exterior
    ("Forest Canopy", "Exterior Wall", [2, 3], 20, True),        # South exterior
    ("Sunrise Yellow", "Interior Wall", [1, 4], 28, True),       # Snap & Find demo
    ("Monsoon Shield", "Waterproofing", [4, 3], 40, True),       # Mumbai Rain hero
    ("Warm Taupe", "Interior Wall", [1, 3], 55, False),          # Economy-like demand
    ("Desert Sand", "Interior Wall", [1, 2], 22, True),          # Neutral trending
    ("Mint Fresh", "Interior Wall", [2, 4], 18, True),           # Green trending
]
