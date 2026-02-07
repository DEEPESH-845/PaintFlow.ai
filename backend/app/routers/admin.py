from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import get_dashboard_summary, get_dealer_performance, get_top_skus
from app.services.inventory_service import (
    get_warehouse_map_data, get_warehouse_inventory,
    get_recommended_transfers, approve_transfer, get_dead_stock,
)

router = APIRouter()


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)


@router.get("/inventory/map")
def inventory_map(db: Session = Depends(get_db)):
    return get_warehouse_map_data(db)


@router.get("/inventory/warehouse/{warehouse_id}")
def warehouse_inventory(warehouse_id: int, db: Session = Depends(get_db)):
    return get_warehouse_inventory(db, warehouse_id)


@router.get("/dead-stock")
def dead_stock(db: Session = Depends(get_db)):
    return get_dead_stock(db)


@router.get("/transfers/recommended")
def recommended_transfers(db: Session = Depends(get_db)):
    return get_recommended_transfers(db)


@router.post("/transfers/{transfer_id}/approve")
def approve_transfer_endpoint(transfer_id: int, db: Session = Depends(get_db)):
    return approve_transfer(db, transfer_id)


@router.post("/transfers/{transfer_id}/auto-balance")
def auto_balance(transfer_id: int, db: Session = Depends(get_db)):
    return approve_transfer(db, transfer_id)


@router.get("/dealers/performance")
def dealer_performance(region_id: int = None, db: Session = Depends(get_db)):
    return get_dealer_performance(db, region_id)


@router.get("/top-skus")
def top_skus(limit: int = 10, db: Session = Depends(get_db)):
    return get_top_skus(db, limit)
