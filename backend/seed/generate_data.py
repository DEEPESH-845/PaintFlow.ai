from __future__ import annotations
"""
Master data generator: seeds the entire PaintFlow.ai database.
Creates products, shades, SKUs, regions, warehouses, dealers,
sales history, inventory levels, transfers, and dealer orders.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app.models import (
    Product, Shade, SKU, Region, Warehouse,
    InventoryLevel, InventoryTransfer, Dealer, DealerOrder, SalesHistory,
    CustomerOrderRequest,
)
from seed.paint_catalog import (
    PRODUCTS, SHADES, SIZE_MULTIPLIERS, hex_to_rgb, get_shade_code, get_sku_code,
)
from seed.geography import REGIONS, WAREHOUSES, DEALER_NAMES, DEALER_LOCATIONS
from seed.time_series import generate_daily_sales, TOP_SKU_REGION_CONFIGS


rng = np.random.default_rng(42)


def create_tables():
    print("Creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created.")


def seed_products(db: Session) -> list[Product]:
    print("Seeding products...")
    products = []
    for p_data in PRODUCTS:
        product = Product(**p_data)
        db.add(product)
        products.append(product)
    db.flush()
    print(f"  Created {len(products)} products.")
    return products


def seed_shades(db: Session, products: list[Product]) -> list[Shade]:
    print("Seeding shades...")
    shades = []
    for family, shade_list in SHADES.items():
        for idx, (name, hex_color, prod_idx, is_trending) in enumerate(shade_list):
            r, g, b = hex_to_rgb(hex_color)
            shade = Shade(
                product_id=products[prod_idx].id,
                shade_code=get_shade_code(family, idx),
                shade_name=name,
                hex_color=hex_color,
                rgb_r=r, rgb_g=g, rgb_b=b,
                shade_family=family,
                is_trending=is_trending,
            )
            db.add(shade)
            shades.append(shade)
    db.flush()
    print(f"  Created {len(shades)} shades.")
    return shades


def seed_skus(db: Session, shades: list[Shade], products: list[Product]) -> list[SKU]:
    print("Seeding SKUs...")
    skus = []
    for shade in shades:
        product = next(p for p in products if p.id == shade.product_id)
        for size, mults in SIZE_MULTIPLIERS.items():
            sku = SKU(
                shade_id=shade.id,
                size=size,
                sku_code=get_sku_code(product.name, shade.shade_code, size),
                unit_cost=round(product.price_per_litre * mults["cost_mult"] * 0.65, 2),
                mrp=round(product.price_per_litre * mults["mrp_mult"], 2),
            )
            db.add(sku)
            skus.append(sku)
    db.flush()
    print(f"  Created {len(skus)} SKUs.")
    return skus


def seed_regions(db: Session) -> list[Region]:
    print("Seeding regions...")
    regions = []
    for r_data in REGIONS:
        region = Region(**r_data)
        db.add(region)
        regions.append(region)
    db.flush()
    print(f"  Created {len(regions)} regions.")
    return regions


def seed_warehouses(db: Session, regions: list[Region]) -> list[Warehouse]:
    print("Seeding warehouses...")
    warehouses = []
    for wh_data in WAREHOUSES:
        warehouse = Warehouse(
            name=wh_data["name"],
            code=wh_data["code"],
            region_id=regions[wh_data["region_idx"]].id,
            city=wh_data["city"],
            state=wh_data["state"],
            latitude=wh_data["lat"],
            longitude=wh_data["lng"],
            capacity_litres=wh_data["capacity"],
        )
        db.add(warehouse)
        warehouses.append(warehouse)
    db.flush()
    print(f"  Created {len(warehouses)} warehouses.")
    return warehouses


def seed_dealers(db: Session, regions: list[Region], warehouses: list[Warehouse]) -> list[Dealer]:
    print("Seeding dealers...")
    dealers = []
    tiers = ["Platinum"] * 10 + ["Gold"] * 15 + ["Silver"] * 25
    rng.shuffle(tiers)

    for i, (name, loc) in enumerate(zip(DEALER_NAMES, DEALER_LOCATIONS)):
        wh = warehouses[loc["wh_idx"]]
        dealer = Dealer(
            name=name,
            code=f"DLR-{wh.city[:3].upper()}-{i + 1:03d}",
            region_id=wh.region_id,
            warehouse_id=wh.id,
            city=loc["city"],
            state=loc["state"],
            latitude=loc["lat"],
            longitude=loc["lng"],
            tier=tiers[i],
            credit_limit=float(rng.choice([300000, 500000, 750000, 1000000])),
            performance_score=round(float(rng.uniform(35, 95)), 1),
        )
        db.add(dealer)
        dealers.append(dealer)
    db.flush()
    print(f"  Created {len(dealers)} dealers.")
    return dealers


def seed_sales_history(db: Session, shades: list[Shade], skus: list[SKU], products: list[Product]):
    print("Seeding sales history (2 years)...")
    start_date = date(2023, 10, 1)
    end_date = date(2025, 10, 10)  # Up to APP_SIMULATION_DATE

    total_records = 0
    shade_lookup = {s.shade_name: s for s in shades}
    sku_lookup = {}
    for sku in skus:
        shade = next(s for s in shades if s.id == sku.shade_id)
        key = (shade.shade_name, sku.size)
        sku_lookup[key] = sku

    for config in TOP_SKU_REGION_CONFIGS:
        shade_name, product_category, region_ids, base_demand, is_premium = config

        # Find the 4L SKU for this shade (most popular size)
        shade = shade_lookup.get(shade_name)
        if not shade:
            continue

        sku = sku_lookup.get((shade.shade_name, "4L"))
        if not sku:
            continue

        for region_id in region_ids:
            records = generate_daily_sales(
                sku_id=sku.id,
                region_id=region_id,
                product_category=product_category,
                shade_name=shade.shade_name,
                is_premium=is_premium,
                base_daily_demand=base_demand,
                start_date=start_date,
                end_date=end_date,
                rng=rng,
            )

            for rec in records:
                rec["revenue"] = round(rec["quantity_sold"] * sku.mrp / 4, 2)  # per-unit revenue
                sale = SalesHistory(**rec)
                db.add(sale)
                total_records += 1

            if total_records % 5000 == 0:
                db.flush()

    db.flush()
    print(f"  Created {total_records} sales records.")


def seed_inventory_levels(db: Session, warehouses: list[Warehouse], skus: list[SKU], shades: list[Shade]):
    print("Seeding inventory levels with deliberate imbalances...")
    shade_lookup = {s.id: s for s in shades}
    levels_created = 0

    # Pick subset of SKUs for each warehouse (top 30 SKUs per warehouse)
    top_skus = skus[:120]  # First 120 SKUs (30 shades x 4 sizes)

    for wh in warehouses:
        for sku in top_skus:
            shade = shade_lookup[sku.shade_id]
            base_stock = int(rng.uniform(50, 2000))
            avg_daily = rng.uniform(5, 30)

            # --- Deliberate imbalances ---

            # Bridal Red: OVERSTOCKED in Mumbai (WH-MUM-01), CRITICAL in Pune (WH-PUN-01)
            if shade.shade_name == "Bridal Red":
                if wh.code == "WH-MUM-01":
                    base_stock = 3200  # Overstocked (Blue marker)
                    avg_daily = 22
                elif wh.code == "WH-PUN-01":
                    base_stock = 20  # Critical stockout (Red pulsing marker)
                    avg_daily = 35

            # Create some other stockouts
            if shade.shade_name == "Pacific Breeze" and wh.code == "WH-CHE-01":
                base_stock = 8
                avg_daily = 25
            if shade.shade_name == "Terracotta Dream" and wh.code == "WH-DEL-01":
                base_stock = 12
                avg_daily = 30

            # Create some overstock (dead stock)
            if shade.shade_name == "Cobalt Dream" and wh.code == "WH-KOL-01":
                base_stock = 4500
                avg_daily = 3
            if shade.shade_name == "Graphite" and wh.code == "WH-BPL-01":
                base_stock = 3800
                avg_daily = 2

            days_of_cover = round(base_stock / max(avg_daily, 0.1), 1)

            level = InventoryLevel(
                warehouse_id=wh.id,
                sku_id=sku.id,
                current_stock=base_stock,
                reorder_point=int(avg_daily * 14),
                max_capacity=int(avg_daily * 120),
                days_of_cover=days_of_cover,
                last_updated=datetime(2025, 10, 10),
            )
            db.add(level)
            levels_created += 1

    db.flush()
    print(f"  Created {levels_created} inventory levels.")


def seed_transfers(db: Session, warehouses: list[Warehouse], skus: list[SKU], shades: list[Shade]):
    print("Seeding transfer recommendations...")
    shade_lookup = {s.id: s for s in shades}

    transfers = [
        # Bridal Red: Mumbai -> Pune (the hero demo transfer)
        {
            "from_code": "WH-MUM-01", "to_code": "WH-PUN-01",
            "shade_name": "Bridal Red", "qty": 500,
            "reason": "Critical stockout in Pune. Wedding season demand surge. Mumbai overstocked.",
        },
        # Pacific Breeze: Bangalore -> Chennai
        {
            "from_code": "WH-BLR-01", "to_code": "WH-CHE-01",
            "shade_name": "Pacific Breeze", "qty": 300,
            "reason": "Low stock in Chennai. Trending shade with rising demand.",
        },
        # Terracotta Dream: Jaipur -> Delhi
        {
            "from_code": "WH-JAI-01", "to_code": "WH-DEL-01",
            "shade_name": "Terracotta Dream", "qty": 250,
            "reason": "Exterior paint demand rising in Delhi NCR. Jaipur has excess.",
        },
    ]

    wh_lookup = {w.code: w for w in warehouses}
    sku_by_shade = {}
    for sku in skus:
        shade = shade_lookup[sku.shade_id]
        if sku.size == "4L":
            sku_by_shade[shade.shade_name] = sku

    for t in transfers:
        sku = sku_by_shade.get(t["shade_name"])
        if not sku:
            continue
        transfer = InventoryTransfer(
            from_warehouse_id=wh_lookup[t["from_code"]].id,
            to_warehouse_id=wh_lookup[t["to_code"]].id,
            sku_id=sku.id,
            quantity=t["qty"],
            status="PENDING",
            reason=t["reason"],
            recommended_at=datetime(2025, 10, 10, 9, 0, 0),
        )
        db.add(transfer)

    db.flush()
    print(f"  Created {len(transfers)} transfer recommendations.")


def seed_dealer_orders(db: Session, dealers: list[Dealer], skus: list[SKU]):
    print("Seeding dealer orders (last 6 months)...")
    orders_created = 0
    start = date(2025, 4, 1)
    end = date(2025, 10, 10)

    top_skus = skus[:60]  # First 60 SKUs

    for dealer in dealers:
        num_orders = int(rng.uniform(10, 40))
        for _ in range(num_orders):
            sku = rng.choice(top_skus)
            order_date = start + timedelta(days=int(rng.uniform(0, (end - start).days)))
            is_ai = bool(rng.random() > 0.6)
            savings = round(float(rng.uniform(500, 5000)), 0) if is_ai else 0.0

            statuses = ["delivered", "delivered", "delivered", "shipped", "confirmed", "placed"]
            status = rng.choice(statuses)

            order = DealerOrder(
                dealer_id=dealer.id,
                sku_id=sku.id,
                quantity=int(rng.choice([10, 20, 50, 100, 200, 500])),
                order_date=datetime.combine(order_date, datetime.min.time()),
                status=status,
                is_ai_suggested=is_ai,
                order_source="ai_recommendation" if is_ai else "manual",
                savings_amount=savings,
            )
            db.add(order)
            orders_created += 1

    db.flush()
    print(f"  Created {orders_created} dealer orders.")


def run_seed():
    create_tables()
    db = SessionLocal()

    try:
        products = seed_products(db)
        shades = seed_shades(db, products)
        skus = seed_skus(db, shades, products)
        regions = seed_regions(db)
        warehouses = seed_warehouses(db, regions)
        dealers = seed_dealers(db, regions, warehouses)
        seed_sales_history(db, shades, skus, products)
        seed_inventory_levels(db, warehouses, skus, shades)
        seed_transfers(db, warehouses, skus, shades)
        seed_dealer_orders(db, dealers, skus)
        db.commit()
        print("\nDatabase seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"\nError seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
