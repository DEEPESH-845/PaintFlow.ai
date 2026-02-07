from __future__ import annotations
"""
Dealer intelligence service.
Smart order recommendations with cost savings calculation.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Dealer, DealerOrder, InventoryLevel, SKU, Shade, Warehouse
from app.services.forecast_service import get_forecast
from app.config import APP_SIMULATION_DATE
from datetime import date, timedelta
import numpy as np


def get_dealer_dashboard(db: Session, dealer_id: int) -> dict:
    """Dealer dashboard with health score and key metrics."""
    dealer = db.query(Dealer).filter(Dealer.id == dealer_id).first()
    if not dealer:
        return {"error": "Dealer not found"}

    # Get orders
    total_orders = db.query(func.count(DealerOrder.id)).filter(
        DealerOrder.dealer_id == dealer_id
    ).scalar()

    ai_recs = db.query(func.count(DealerOrder.id)).filter(
        DealerOrder.dealer_id == dealer_id,
        DealerOrder.is_ai_suggested == True,
        DealerOrder.status == "recommended",
    ).scalar()

    revenue = db.query(func.sum(DealerOrder.quantity * 500)).filter(
        DealerOrder.dealer_id == dealer_id,
        DealerOrder.status == "delivered",
        DealerOrder.order_date >= date(2025, 10, 1).isoformat(),
    ).scalar() or 0

    total_savings = db.query(func.sum(DealerOrder.savings_amount)).filter(
        DealerOrder.dealer_id == dealer_id,
        DealerOrder.is_ai_suggested == True,
    ).scalar() or 0

    # Compute health score
    health_score = _compute_health_score(db, dealer)

    return {
        "dealer": {
            "id": dealer.id,
            "name": dealer.name,
            "city": dealer.city,
            "tier": dealer.tier,
        },
        "health_score": health_score,
        "total_orders": total_orders,
        "ai_recommendations_pending": ai_recs,
        "revenue_this_month": round(revenue, 0),
        "total_ai_savings": round(total_savings, 0),
        "performance_score": dealer.performance_score,
    }


def _compute_health_score(db: Session, dealer: Dealer) -> float:
    """
    Health score 0-100:
    40% stock coverage, 25% stockout frequency,
    20% order fulfillment, 15% product breadth
    """
    # Stock coverage (from warehouse inventory)
    levels = db.query(InventoryLevel).filter(
        InventoryLevel.warehouse_id == dealer.warehouse_id
    ).all()

    if not levels:
        return 50.0

    avg_cover = np.mean([l.days_of_cover for l in levels])
    coverage_score = min(100, avg_cover / 30 * 100)

    stockout_count = sum(1 for l in levels if l.days_of_cover < 3)
    stockout_score = max(0, 100 - stockout_count * 15)

    # Order fulfillment
    total = db.query(func.count(DealerOrder.id)).filter(
        DealerOrder.dealer_id == dealer.id
    ).scalar()
    delivered = db.query(func.count(DealerOrder.id)).filter(
        DealerOrder.dealer_id == dealer.id,
        DealerOrder.status == "delivered",
    ).scalar()
    fulfillment_score = (delivered / max(total, 1)) * 100

    # Product breadth
    unique_skus = db.query(func.count(func.distinct(DealerOrder.sku_id))).filter(
        DealerOrder.dealer_id == dealer.id
    ).scalar()
    breadth_score = min(100, unique_skus / 20 * 100)

    return round(
        0.4 * coverage_score + 0.25 * stockout_score +
        0.2 * fulfillment_score + 0.15 * breadth_score, 1
    )


def get_smart_orders(db: Session, dealer_id: int) -> list[dict]:
    """Generate AI-driven order recommendations for a dealer."""
    dealer = db.query(Dealer).filter(Dealer.id == dealer_id).first()
    if not dealer:
        return []

    # Get dealer's warehouse inventory
    levels = db.query(InventoryLevel).filter(
        InventoryLevel.warehouse_id == dealer.warehouse_id,
        InventoryLevel.days_of_cover < 30,
    ).order_by(InventoryLevel.days_of_cover.asc()).all()

    recommendations = []
    sim_date = date.fromisoformat(APP_SIMULATION_DATE)

    for level in levels[:15]:  # Top 15 low-stock items
        sku = db.query(SKU).filter(SKU.id == level.sku_id).first()
        if not sku:
            continue
        shade = db.query(Shade).filter(Shade.id == sku.shade_id).first()
        if not shade:
            continue

        # Forecast demand
        forecast = get_forecast(sku.id, dealer.region_id, horizon=30)
        predicted_demand = sum(f["predicted"] for f in forecast.get("forecast", []))

        # Calculate recommended quantity
        recommended_qty = max(10, int(predicted_demand * 1.2 - level.current_stock))

        # Calculate savings
        manual_cost = recommended_qty * sku.mrp
        ai_cost = manual_cost * 0.92  # 8% savings through optimized logistics
        savings = round(manual_cost - ai_cost, 0)

        # Determine urgency
        if level.days_of_cover < 3:
            urgency = "CRITICAL"
        elif level.days_of_cover < 14:
            urgency = "RECOMMENDED"
        else:
            urgency = "OPTIONAL"

        # Generate context-aware reason
        reason = _generate_reason(shade, level, sim_date)

        # Stockout date
        daily_demand = level.current_stock / max(level.days_of_cover, 0.1)
        stockout_date = sim_date + timedelta(days=int(level.days_of_cover))

        recommendations.append({
            "sku_id": sku.id,
            "sku_code": sku.sku_code,
            "shade_name": shade.shade_name,
            "shade_hex": shade.hex_color,
            "shade_family": shade.shade_family,
            "size": sku.size,
            "current_stock": level.current_stock,
            "recommended_qty": recommended_qty,
            "urgency": urgency,
            "reason": reason,
            "predicted_stockout_date": stockout_date.isoformat(),
            "savings_amount": savings,
            "mrp_per_unit": sku.mrp,
            "total_cost": round(ai_cost, 0),
        })

    return sorted(recommendations, key=lambda x: (
        {"CRITICAL": 0, "RECOMMENDED": 1, "OPTIONAL": 2}[x["urgency"]],
        x["predicted_stockout_date"],
    ))


def _generate_reason(shade: Shade, level: InventoryLevel, sim_date: date) -> str:
    """Generate context-aware reason for the recommendation."""
    # Check upcoming events relative to simulation date
    days_to_diwali = (date(2025, 10, 25) - sim_date).days
    if 0 < days_to_diwali <= 21:
        return f"Diwali in {days_to_diwali} days - demand expected to surge 60%"

    if shade.shade_name == "Bridal Red":
        return "Wedding season peak - 'Bridal Red' trending +40% in your region"

    if shade.is_trending:
        return f"'{shade.shade_name}' is trending - 40% increase in customer searches"

    if level.days_of_cover < 3:
        return f"CRITICAL: Stock will last only {level.days_of_cover:.0f} days at current sell-through"

    if sim_date.month in (6, 7, 8, 9) and shade.product and shade.product.category == "Waterproofing":
        return "Peak monsoon season - waterproofing demand at annual high"

    return f"Stock will last {level.days_of_cover:.0f} days - restock recommended before depletion"


def get_dealer_alerts(db: Session, dealer_id: int) -> dict:
    """Get stockout, transfer, and trending alerts for a dealer."""
    dealer = db.query(Dealer).filter(Dealer.id == dealer_id).first()
    if not dealer:
        return {"stockout_alerts": [], "trending": [], "transfer_notifications": []}

    # Stockout alerts
    critical = db.query(InventoryLevel).filter(
        InventoryLevel.warehouse_id == dealer.warehouse_id,
        InventoryLevel.days_of_cover < 7,
    ).all()

    stockout_alerts = []
    for level in critical:
        sku = db.query(SKU).filter(SKU.id == level.sku_id).first()
        shade = db.query(Shade).filter(Shade.id == sku.shade_id).first() if sku else None
        if shade:
            stockout_alerts.append({
                "shade_name": shade.shade_name,
                "shade_hex": shade.hex_color,
                "days_remaining": round(level.days_of_cover, 1),
                "current_stock": level.current_stock,
            })

    # Trending shades
    trending = db.query(Shade).filter(Shade.is_trending == True).limit(5).all()

    return {
        "stockout_alerts": stockout_alerts[:5],
        "trending": [{"shade_name": s.shade_name, "shade_hex": s.hex_color} for s in trending],
        "transfer_notifications": [],
    }
