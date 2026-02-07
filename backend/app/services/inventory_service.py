from __future__ import annotations
"""
Inventory orchestration service.
Transfer recommendations, auto-balance, inventory health.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import InventoryLevel, InventoryTransfer, Warehouse, SKU, Shade
from datetime import datetime


def get_warehouse_map_data(db: Session) -> list[dict]:
    """Get all warehouses with inventory status for the map."""
    warehouses = db.query(Warehouse).all()
    result = []

    for wh in warehouses:
        levels = db.query(InventoryLevel).filter(
            InventoryLevel.warehouse_id == wh.id
        ).all()

        total_stock = sum(l.current_stock for l in levels)
        critical_count = sum(1 for l in levels if l.days_of_cover < 3)
        low_count = sum(1 for l in levels if 3 <= l.days_of_cover < 14)
        overstock_count = sum(1 for l in levels if l.days_of_cover > 90)

        if critical_count > 0:
            status = "critical"
        elif low_count > 2:
            status = "low"
        elif overstock_count > 2:
            status = "overstocked"
        else:
            status = "healthy"

        # Revenue at risk calculation
        revenue_at_risk = 0
        for l in levels:
            if l.days_of_cover < 7:
                sku = db.query(SKU).filter(SKU.id == l.sku_id).first()
                if sku:
                    daily_demand = l.current_stock / max(l.days_of_cover, 0.1)
                    days_out = max(0, 7 - l.days_of_cover)
                    revenue_at_risk += daily_demand * days_out * sku.mrp

        result.append({
            "id": wh.id,
            "name": wh.name,
            "code": wh.code,
            "city": wh.city,
            "state": wh.state,
            "latitude": wh.latitude,
            "longitude": wh.longitude,
            "capacity": wh.capacity_litres,
            "total_stock": total_stock,
            "capacity_pct": round(total_stock / max(wh.capacity_litres, 1) * 100, 1),
            "critical_skus": critical_count,
            "low_skus": low_count,
            "overstock_skus": overstock_count,
            "status": status,
            "revenue_at_risk": round(revenue_at_risk, 0),
        })

    return result


def get_warehouse_inventory(db: Session, warehouse_id: int) -> list[dict]:
    """Get detailed inventory for a specific warehouse."""
    levels = db.query(InventoryLevel).filter(
        InventoryLevel.warehouse_id == warehouse_id
    ).all()

    result = []
    for level in levels:
        sku = db.query(SKU).filter(SKU.id == level.sku_id).first()
        shade = db.query(Shade).filter(Shade.id == sku.shade_id).first() if sku else None

        if level.days_of_cover < 3:
            status = "critical"
        elif level.days_of_cover < 14:
            status = "low"
        elif level.days_of_cover > 90:
            status = "overstocked"
        else:
            status = "healthy"

        result.append({
            "id": level.id,
            "sku_id": sku.id if sku else None,
            "sku_code": sku.sku_code if sku else "",
            "shade_name": shade.shade_name if shade else "",
            "shade_hex": shade.hex_color if shade else "#000",
            "size": sku.size if sku else "",
            "current_stock": level.current_stock,
            "reorder_point": level.reorder_point,
            "days_of_cover": level.days_of_cover,
            "status": status,
        })

    return sorted(result, key=lambda x: x["days_of_cover"])


def get_recommended_transfers(db: Session) -> list[dict]:
    """Get all pending transfer recommendations."""
    transfers = db.query(InventoryTransfer).filter(
        InventoryTransfer.status.in_(["PENDING", "APPROVED", "IN_TRANSIT"])
    ).all()

    result = []
    for t in transfers:
        from_wh = db.query(Warehouse).filter(Warehouse.id == t.from_warehouse_id).first()
        to_wh = db.query(Warehouse).filter(Warehouse.id == t.to_warehouse_id).first()
        sku = db.query(SKU).filter(SKU.id == t.sku_id).first()
        shade = db.query(Shade).filter(Shade.id == sku.shade_id).first() if sku else None

        result.append({
            "id": t.id,
            "from_warehouse": {"id": from_wh.id, "name": from_wh.name, "city": from_wh.city,
                               "lat": from_wh.latitude, "lng": from_wh.longitude} if from_wh else None,
            "to_warehouse": {"id": to_wh.id, "name": to_wh.name, "city": to_wh.city,
                             "lat": to_wh.latitude, "lng": to_wh.longitude} if to_wh else None,
            "sku_code": sku.sku_code if sku else "",
            "shade_name": shade.shade_name if shade else "",
            "shade_hex": shade.hex_color if shade else "#000",
            "quantity": t.quantity,
            "status": t.status,
            "reason": t.reason,
            "recommended_at": t.recommended_at.isoformat() if t.recommended_at else None,
        })

    return result


def approve_transfer(db: Session, transfer_id: int) -> dict:
    """Approve a transfer and optimistically update inventory."""
    transfer = db.query(InventoryTransfer).filter(InventoryTransfer.id == transfer_id).first()
    if not transfer:
        return {"success": False, "message": "Transfer not found"}

    transfer.status = "IN_TRANSIT"

    # Optimistic update: reduce source, increase destination
    from_level = db.query(InventoryLevel).filter(
        InventoryLevel.warehouse_id == transfer.from_warehouse_id,
        InventoryLevel.sku_id == transfer.sku_id,
    ).first()

    to_level = db.query(InventoryLevel).filter(
        InventoryLevel.warehouse_id == transfer.to_warehouse_id,
        InventoryLevel.sku_id == transfer.sku_id,
    ).first()

    if from_level:
        from_level.current_stock = max(0, from_level.current_stock - transfer.quantity)
        from_level.days_of_cover = round(from_level.current_stock / max(transfer.quantity / 30, 1), 1)

    if to_level:
        to_level.current_stock += transfer.quantity
        to_level.days_of_cover = round(to_level.current_stock / max(transfer.quantity / 30, 1), 1)

    db.commit()

    to_wh = db.query(Warehouse).filter(Warehouse.id == transfer.to_warehouse_id).first()
    from_wh = db.query(Warehouse).filter(Warehouse.id == transfer.from_warehouse_id).first()
    sku = db.query(SKU).filter(SKU.id == transfer.sku_id).first()
    shade = db.query(Shade).filter(Shade.id == sku.shade_id).first() if sku else None

    return {
        "success": True,
        "message": f"Transfer approved. {transfer.quantity} units of {shade.shade_name if shade else 'product'} "
                   f"moving from {from_wh.city if from_wh else '?'} to {to_wh.city if to_wh else '?'}. ETA: 2 days.",
        "transfer_id": transfer.id,
    }


def get_dead_stock(db: Session) -> list[dict]:
    """Get SKUs with > 90 days of cover (dead stock)."""
    levels = db.query(InventoryLevel).filter(
        InventoryLevel.days_of_cover > 90
    ).all()

    result = []
    for level in levels:
        wh = db.query(Warehouse).filter(Warehouse.id == level.warehouse_id).first()
        sku = db.query(SKU).filter(SKU.id == level.sku_id).first()
        shade = db.query(Shade).filter(Shade.id == sku.shade_id).first() if sku else None

        result.append({
            "warehouse": wh.name if wh else "",
            "warehouse_city": wh.city if wh else "",
            "sku_code": sku.sku_code if sku else "",
            "shade_name": shade.shade_name if shade else "",
            "shade_hex": shade.hex_color if shade else "#000",
            "size": sku.size if sku else "",
            "current_stock": level.current_stock,
            "days_of_cover": level.days_of_cover,
            "capital_locked": round(level.current_stock * (sku.unit_cost if sku else 0), 0),
            "recommendation": "Transfer to high-demand warehouse" if level.days_of_cover > 120 else "Run promotion",
        })

    return sorted(result, key=lambda x: -x["days_of_cover"])
