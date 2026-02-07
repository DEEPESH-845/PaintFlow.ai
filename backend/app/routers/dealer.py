from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services.dealer_service import (
    get_dealer_dashboard, get_smart_orders, get_dealer_alerts,
)
from app.models import Dealer, DealerOrder
from datetime import datetime

router = APIRouter()


class OrderCreate(BaseModel):
    sku_id: int
    quantity: int


@router.get("/{dealer_id}/dashboard")
def dealer_dashboard(dealer_id: int, db: Session = Depends(get_db)):
    return get_dealer_dashboard(db, dealer_id)


@router.get("/{dealer_id}/smart-orders")
def smart_orders(dealer_id: int, db: Session = Depends(get_db)):
    return get_smart_orders(db, dealer_id)


@router.post("/{dealer_id}/orders")
def place_order(dealer_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    new_order = DealerOrder(
        dealer_id=dealer_id,
        sku_id=order.sku_id,
        quantity=order.quantity,
        order_date=datetime.utcnow(),
        status="placed",
        is_ai_suggested=False,
        order_source="manual",
        savings_amount=0.0,
    )
    db.add(new_order)
    db.commit()
    return {"success": True, "order_id": new_order.id, "status": "placed"}


@router.post("/{dealer_id}/orders/bundle")
def accept_bundle(dealer_id: int, db: Session = Depends(get_db)):
    """Accept all AI-recommended orders at once."""
    recs = get_smart_orders(db, dealer_id)
    total_savings = 0
    orders_placed = 0

    for rec in recs:
        if rec["urgency"] in ("CRITICAL", "RECOMMENDED"):
            order = DealerOrder(
                dealer_id=dealer_id,
                sku_id=rec["sku_id"],
                quantity=rec["recommended_qty"],
                order_date=datetime.utcnow(),
                status="placed",
                is_ai_suggested=True,
                order_source="ai_recommendation",
                savings_amount=rec["savings_amount"],
            )
            db.add(order)
            total_savings += rec["savings_amount"]
            orders_placed += 1

    db.commit()
    return {
        "success": True,
        "orders_placed": orders_placed,
        "total_savings": round(total_savings, 0),
        "message": f"Bundle accepted! {orders_placed} orders placed. You saved ₹{total_savings:,.0f}!",
    }


@router.get("/{dealer_id}/orders")
def order_history(dealer_id: int, db: Session = Depends(get_db)):
    orders = db.query(DealerOrder).filter(
        DealerOrder.dealer_id == dealer_id
    ).order_by(DealerOrder.order_date.desc()).limit(50).all()

    return [
        {
            "id": o.id,
            "sku_id": o.sku_id,
            "quantity": o.quantity,
            "order_date": o.order_date.isoformat() if o.order_date else None,
            "status": o.status,
            "is_ai_suggested": o.is_ai_suggested,
            "savings_amount": o.savings_amount,
        }
        for o in orders
    ]


@router.get("/{dealer_id}/alerts")
def dealer_alerts(dealer_id: int, db: Session = Depends(get_db)):
    return get_dealer_alerts(db, dealer_id)
