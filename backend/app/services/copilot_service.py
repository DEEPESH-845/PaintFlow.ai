from __future__ import annotations
import json
import asyncio
import logging
from typing import Optional, Dict, Any

# --- CHANGED: Use the Stable SDK ---
import google.generativeai as genai
# -----------------------------------

from app.config import GEMINI_API_KEY, COPILOT_TIMEOUT, APP_SIMULATION_DATE

# Configure structured logging
logger = logging.getLogger(__name__)

# --- 1. THE SYSTEM PROMPT DEFINITION ---
BASE_SYSTEM_PROMPT = f"""
You are the "PaintFlow Supply Chain Copilot", an expert logistics AI assistant.
Your goal is to help warehouse managers optimize inventory, predict risks, and handle disruptions.

CURRENT SYSTEM TIME: {APP_SIMULATION_DATE}

GUIDELINES:
1. **Be Action-Oriented:** Don't just report data; suggest transfers or reordering.
2. **Roleplay the Scenario:** If a "Truck Strike" is active, acknowledge delays.
3. **Structured Data:** You MUST return responses in the specified JSON format.
4. **Data Fidelity:** Never hallucinate inventory numbers. Use ONLY the provided context.

OUTPUT FORMAT (JSON ONLY):
{{
  "text": "Your helpful, natural language response here.",
  "ui_widget": {{
      "type": "TRANSFER_CARD" | "INSIGHT_CARD" | null,
      "props": {{ ... }}
  }}
}}
"""

async def get_chat_response(message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Orchestrator function: Decides whether to use Real AI or Heuristic Fallback.
    """
    context = context or {}
    scenario_id = context.get("scenario_id", "NORMAL")

    if not GEMINI_API_KEY:
        return _heuristic_response(message, scenario_id)

    try:
        # Run Gemini logic with a timeout safety net
        return await asyncio.wait_for(
            _call_gemini_api(message, context, scenario_id),
            timeout=COPILOT_TIMEOUT
        )
    except (asyncio.TimeoutError, Exception) as e:
        logger.error(f"Gemini API Error: {e}")
        return _heuristic_response(message, scenario_id)


async def _call_gemini_api(user_message: str, context: Dict[str, Any], scenario_id: str) -> Dict[str, Any]:
    """
    Constructs the prompt and calls Google Gemini (Stable Version).
    """
    # --- CONFIGURE STABLE CLIENT ---
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Use the stable model name that always works
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash", 
        generation_config={"response_mime_type": "application/json", "temperature": 0.4},
        system_instruction=f"""
        {BASE_SYSTEM_PROMPT}

        CURRENT SIMULATION SCENARIO: {scenario_id}

        REAL-TIME INVENTORY SNAPSHOT:
        {context.get("inventory_snapshot", "No current inventory data available.")}
        """
    )

    # --- CALL API ---
    response = model.generate_content(user_message)

    # --- PARSE RESPONSE ---
    try:
        return json.loads(response.text)
    except Exception:
        # Fallback parsing if JSON mode glitches
        return {
            "text": response.text, 
            "ui_widget": None
        }


def _heuristic_response(message: str, scenario_id: str) -> Dict[str, Any]:
    """
    Fallback logic (Kept strictly as backup).
    """
    msg = message.lower()
    prefix = f"(Offline Mode - {scenario_id}) "

    if "bridal" in msg or "pune" in msg:
        return {
            "text": prefix + "Critical shortage of Bridal Red in Pune detected. 20 units left. Recommend transfer from Mumbai.",
            "ui_widget": {"type": "TRANSFER_CARD", "props": {"from": "Mumbai", "to": "Pune", "sku": "Bridal Red", "qty": 500, "eta": "2 days", "savings": "₹15,000"}}
        }
    
    return {
        "text": prefix + "I'm having trouble connecting to the AI brain. However, I can still see your inventory data. Try asking about 'stockouts' or specific cities.",
        "ui_widget": None
    }