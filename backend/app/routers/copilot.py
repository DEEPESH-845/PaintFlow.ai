from __future__ import annotations
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db

# Import your services
from app.services.copilot_service import get_chat_response
from app.services.inventory_service import get_warehouse_map_data

router = APIRouter()

# --- Step 2: Define the Request Model ---
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

# --- Step 3: Define the Chat Endpoint ---
@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    AI Copilot chat endpoint with Generative UI support.
    
    1. Fetches real-time warehouse data.
    2. Injects critical/overstock alerts into the AI's context.
    3. Returns a structured JSON response (text + optional UI widget).
    """
    
    # Initialize context from request or empty dict
    context = request.context or {}

    # --- Context Injection Logic ---
    try:
        # Fetch real-time data from the database
        map_data = get_warehouse_map_data(db)
        
        # Filter for warehouses that need attention
        critical = [w for w in map_data if w.get("status") == "critical"]
        overstocked = [w for w in map_data if w.get("status") == "overstocked"]

        snapshot_lines = []
        
        # Format Critical Alerts clearly for the AI
        if critical:
            snapshot_lines.append("⚠️ CRITICAL ALERTS (High Priority):")
            for w in critical:
                # Safe access to keys with defaults
                city = w.get('city', 'Unknown')
                code = w.get('code', 'N/A')
                crit_count = w.get('critical_skus', 0)
                rev_risk = w.get('revenue_at_risk', 0)
                
                snapshot_lines.append(
                    f"- {city} ({code}): {crit_count} SKUs at risk. Revenue impact: ₹{rev_risk:,.0f}"
                )
        
        # Format Overstock Alerts
        if overstocked:
            snapshot_lines.append("📦 OVERSTOCK ALERTS:")
            for w in overstocked:
                city = w.get('city', 'Unknown')
                code = w.get('code', 'N/A')
                over_count = w.get('overstock_skus', 0)
                
                snapshot_lines.append(
                    f"- {city} ({code}): {over_count} excess SKUs."
                )

        # Finalize the snapshot string
        if not snapshot_lines:
            context["inventory_snapshot"] = "✅ All warehouses are currently healthy. No critical issues."
        else:
            context["inventory_snapshot"] = "\n".join(snapshot_lines)

    except Exception as e:
        # Fallback if DB fetch fails, so chat doesn't crash
        print(f"Error building copilot context: {e}")
        context["inventory_snapshot"] = "Error: Unable to fetch real-time inventory data."

    # --- Call the AI Service ---
    # This function (in copilot_service.py) handles the Gemini API call
    response = await get_chat_response(request.message, context)
    
    return response