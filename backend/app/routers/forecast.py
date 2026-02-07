from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.forecast_service import get_forecast
from app.models import SKU, Shade, SalesHistory, Region
from sqlalchemy import func

router = APIRouter()


@router.get("/{sku_id}")
def get_sku_forecast(
    sku_id: int, region_id: int = 1, horizon: int = 30,
    db: Session = Depends(get_db),
):
    """Get forecast for a specific SKU with event annotations."""
    forecast_data = get_forecast(sku_id, region_id, horizon)

    # Add event annotations
    annotations = [
        {"date": "2025-10-25", "label": "Diwali Start", "color": "#FF6B35"},
        {"date": "2025-11-10", "label": "Diwali End", "color": "#FF6B35"},
        {"date": "2025-10-10", "label": "Today", "color": "#3B82F6"},
    ]

    # Get actual sales data for this SKU-region
    actuals = db.query(SalesHistory).filter(
        SalesHistory.sku_id == sku_id,
        SalesHistory.region_id == region_id,
    ).order_by(SalesHistory.date.desc()).limit(90).all()

    actual_data = [
        {"date": s.date.isoformat(), "actual": s.quantity_sold}
        for s in reversed(actuals)
    ]

    # SKU info
    sku = db.query(SKU).filter(SKU.id == sku_id).first()
    shade = db.query(Shade).filter(Shade.id == sku.shade_id).first() if sku else None

    return {
        "sku_id": sku_id,
        "sku_code": sku.sku_code if sku else "",
        "shade_name": shade.shade_name if shade else "",
        "shade_hex": shade.hex_color if shade else "#000",
        "region_id": region_id,
        "actual": actual_data,
        "forecast": forecast_data.get("forecast", []),
        "annotations": annotations,
    }


@router.get("/regional/summary")
def regional_forecast_summary(db: Session = Depends(get_db)):
    """Aggregated forecast summary by region."""
    regions = db.query(Region).all()
    result = []

    for region in regions:
        total_sales = db.query(func.sum(SalesHistory.revenue)).filter(
            SalesHistory.region_id == region.id,
        ).scalar() or 0

        result.append({
            "region_id": region.id,
            "region_name": region.name,
            "total_revenue": round(total_sales, 0),
        })

    return result
