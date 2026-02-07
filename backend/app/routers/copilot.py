from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.copilot_service import get_chat_response
from app.services.inventory_service import get_warehouse_map_data


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None


@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """AI Copilot chat endpoint with Generative UI support."""
    # Build inventory snapshot for context injection
    context = request.context or {}

    # Get current inventory state for the copilot
    try:
        map_data = get_warehouse_map_data(db)
        critical = [w for w in map_data if w["status"] == "critical"]
        overstocked = [w for w in map_data if w["status"] == "overstocked"]

        snapshot_lines = []
        for w in critical:
            snapshot_lines.append(f"CRITICAL: {w['city']} ({w['code']}) - {w['critical_skus']} SKUs at risk, Revenue at risk: ₹{w['revenue_at_risk']:,.0f}")
        for w in overstocked:
            snapshot_lines.append(f"OVERSTOCKED: {w['city']} ({w['code']}) - {w['overstock_skus']} SKUs excess")

        context["inventory_snapshot"] = "\n".join(snapshot_lines) if snapshot_lines else "All warehouses healthy."
    except Exception:
        context["inventory_snapshot"] = "Unable to fetch inventory data."

    response = await get_chat_response(request.message, context)
    return response
