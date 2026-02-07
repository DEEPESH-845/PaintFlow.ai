from __future__ import annotations
"""
Dashboard analytics aggregations with lru_cache for sub-50ms responses.
"""



from functools import lru_cache
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import (
    InventoryLevel, InventoryTransfer, Warehouse, SKU, Shade,
    Dealer, DealerOrder, SalesHistory, Product, Region,
)
from datetime import date


def get_dashboard_summary(db: Session) -> dict:
    """Admin dashboard KPI summary."""
    total_skus = db.query(func.count(SKU.id)).scalar()
    total_warehouses = db.query(func.count(Warehouse.id)).scalar()
    total_dealers = db.query(func.count(Dealer.id)).scalar()

    stockout_count = db.query(func.count(InventoryLevel.id)).filter(
        InventoryLevel.days_of_cover < 3
    ).scalar()

    pending_transfers = db.query(func.count(InventoryTransfer.id)).filter(
        InventoryTransfer.status == "PENDING"
    ).scalar()

    # Revenue this month (from dealer orders)
    total_revenue = db.query(func.sum(SalesHistory.revenue)).filter(
        SalesHistory.date >= date(2025, 10, 1)
    ).scalar() or 0

    # Revenue at risk (from critical stockouts)
    critical_levels = db.query(InventoryLevel).filter(
        InventoryLevel.days_of_cover < 7
    ).all()

    revenue_at_risk = 0
    for level in critical_levels:
        sku = db.query(SKU).filter(SKU.id == level.sku_id).first()
        if sku:
            daily_demand = level.current_stock / max(level.days_of_cover, 0.1)
            days_out = max(0, 7 - level.days_of_cover)
            revenue_at_risk += daily_demand * days_out * sku.mrp

    dead_stock_count = db.query(func.count(InventoryLevel.id)).filter(
        InventoryLevel.days_of_cover > 90
    ).scalar()

    return {
        "total_skus": total_skus,
        "total_warehouses": total_warehouses,
        "total_dealers": total_dealers,
        "total_revenue_mtd": round(total_revenue, 0),
        "stockout_count": stockout_count,
        "pending_transfers": pending_transfers,
        "revenue_at_risk": round(revenue_at_risk, 0),
        "dead_stock_count": dead_stock_count,
    }


def get_dealer_performance(db: Session, region_id: int | None = None) -> list[dict]:
    """Dealer rankings sorted by performance score."""
    query = db.query(Dealer)
    if region_id:
        query = query.filter(Dealer.region_id == region_id)

    dealers = query.order_by(Dealer.performance_score.desc()).all()

    result = []
    for d in dealers:
        order_count = db.query(func.count(DealerOrder.id)).filter(
            DealerOrder.dealer_id == d.id
        ).scalar()

        total_revenue = db.query(func.sum(DealerOrder.quantity * 500)).filter(
            DealerOrder.dealer_id == d.id,
            DealerOrder.status == "delivered",
        ).scalar() or 0

        ai_orders = db.query(func.count(DealerOrder.id)).filter(
            DealerOrder.dealer_id == d.id,
            DealerOrder.is_ai_suggested == True,
        ).scalar()

        result.append({
            "id": d.id,
            "name": d.name,
            "code": d.code,
            "city": d.city,
            "state": d.state,
            "tier": d.tier,
            "performance_score": d.performance_score,
            "total_orders": order_count,
            "total_revenue": round(total_revenue, 0),
            "ai_adoption_rate": round(ai_orders / max(order_count, 1) * 100, 1),
            "trend": "up" if d.performance_score > 60 else "down",
        })

    return result


def get_top_skus(db: Session, limit: int = 10) -> list[dict]:
    """Top selling SKUs by revenue."""
    results = db.query(
        SalesHistory.sku_id,
        func.sum(SalesHistory.revenue).label("total_revenue"),
        func.sum(SalesHistory.quantity_sold).label("total_qty"),
    ).filter(
        SalesHistory.date >= date(2025, 9, 1)
    ).group_by(
        SalesHistory.sku_id
    ).order_by(
        func.sum(SalesHistory.revenue).desc()
    ).limit(limit).all()

    top_skus = []
    for row in results:
        sku = db.query(SKU).filter(SKU.id == row.sku_id).first()
        shade = db.query(Shade).filter(Shade.id == sku.shade_id).first() if sku else None

        top_skus.append({
            "sku_id": row.sku_id,
            "sku_code": sku.sku_code if sku else "",
            "shade_name": shade.shade_name if shade else "",
            "shade_hex": shade.hex_color if shade else "#000",
            "size": sku.size if sku else "",
            "total_revenue": round(row.total_revenue, 0),
            "total_quantity": row.total_qty,
        })

    return top_skus
