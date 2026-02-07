from __future__ import annotations
"""
AI Copilot service with Gemini integration and heuristic fallback.
Returns structured JSON with text + optional ui_widget for Generative UI.
"""

import re
import json
import asyncio
from app.config import GEMINI_API_KEY, COPILOT_TIMEOUT


def clean_and_parse_json(raw_response: str) -> dict:
    """Safely parse Gemini response that may be wrapped in markdown."""
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except (json.JSONDecodeError, Exception):
                pass
    return {"text": raw_response, "ui_widget": None}


async def get_chat_response(message: str, context: dict = None) -> dict:
    """
    Process a copilot chat message.
    Returns: {"text": str, "ui_widget": {"type": str, "props": dict} | None}
    """
    scenario_id = (context or {}).get("scenario_id", "NORMAL")

    # Try Gemini first, fall back to heuristics
    if GEMINI_API_KEY:
        try:
            return await asyncio.wait_for(
                _gemini_response(message, context, scenario_id),
                timeout=COPILOT_TIMEOUT,
            )
        except (asyncio.TimeoutError, Exception) as e:
            print(f"Gemini failed ({e}), using heuristic fallback.")

    return _heuristic_response(message, scenario_id)


async def _gemini_response(message: str, context: dict, scenario_id: str) -> dict:
    """Get response from Gemini API."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        inventory_context = (context or {}).get("inventory_snapshot", "")

        system_prompt = f"""You are PaintFlow Supply Chain AI assistant.
Current Simulation Mode: {scenario_id}
Current System Date: 2025-10-10

Current Inventory Context:
{inventory_context}

You must respond with valid JSON in this exact format:
{{"text": "your analysis here", "ui_widget": null}}

If you recommend a transfer, use this format:
{{"text": "your analysis", "ui_widget": {{"type": "TRANSFER_CARD", "props": {{"from": "city", "to": "city", "sku": "shade name", "qty": number, "eta": "X days", "savings": "₹X,XXX"}}}}}}

User question: {message}"""

        response = model.generate_content(system_prompt)
        return clean_and_parse_json(response.text)

    except Exception as e:
        raise e


def _heuristic_response(message: str, scenario_id: str) -> dict:
    """Heuristic keyword-matching fallback for when Gemini is unavailable."""
    msg = message.lower()

    # Handle scenario context
    scenario_prefix = ""
    if scenario_id == "TRUCK_STRIKE":
        scenario_prefix = "During the simulated truck strike: "
    elif scenario_id == "HEATWAVE":
        scenario_prefix = "During the simulated heatwave: "
    elif scenario_id == "EARLY_MONSOON":
        scenario_prefix = "During the early monsoon simulation: "

    # Bridal Red + Pune (hero demo query)
    if ("bridal" in msg or "red" in msg) and ("pune" in msg or "low" in msg or "why" in msg):
        eta = "4 days (delayed due to strike)" if scenario_id == "TRUCK_STRIKE" else "2 days"
        return {
            "text": f"{scenario_prefix}I've detected a critical shortage of 'Bridal Red' in Pune. "
                    f"Wedding season demand has surged 40%, depleting stock to just 20 units (1.2 days cover). "
                    f"Mumbai warehouse has 3,200 units overstocked. I recommend an immediate transfer.",
            "ui_widget": {
                "type": "TRANSFER_CARD",
                "props": {
                    "from": "Mumbai",
                    "to": "Pune",
                    "sku": "Bridal Red",
                    "qty": 500,
                    "eta": eta,
                    "savings": "₹15,000",
                },
            },
        }

    # Stockout queries
    if "stockout" in msg or "shortage" in msg or "critical" in msg:
        return {
            "text": f"{scenario_prefix}There are currently 8 critical stockout situations across the network. "
                    f"The most urgent: Bridal Red in Pune (1.2 days), Pacific Breeze in Chennai (0.3 days), "
                    f"and Terracotta Dream in Delhi (0.4 days). Revenue at risk: ₹4,50,000.",
            "ui_widget": {
                "type": "INSIGHT_CARD",
                "props": {
                    "title": "Critical Stockouts",
                    "items": [
                        {"shade": "Bridal Red", "location": "Pune", "days_left": 1.2},
                        {"shade": "Pacific Breeze", "location": "Chennai", "days_left": 0.3},
                        {"shade": "Terracotta Dream", "location": "Delhi", "days_left": 0.4},
                    ],
                },
            },
        }

    # Diwali queries
    if "diwali" in msg or "festival" in msg:
        return {
            "text": f"{scenario_prefix}Diwali is 15 days away. Based on 2 years of historical data, "
                    f"I predict a 60% demand surge across all paint categories. Premium products like "
                    f"Royale Luxury Emulsion will see the highest spike. I recommend pre-positioning "
                    f"stock in North and West warehouses.",
            "ui_widget": None,
        }

    # Monsoon / waterproofing
    if "monsoon" in msg or "rain" in msg or "waterproof" in msg:
        return {
            "text": f"{scenario_prefix}The Great Mumbai Rain event of Oct 2025 caused a 3x spike in "
                    f"waterproofing demand. Our Prophet model detected this pattern and can predict "
                    f"similar events 3 days in advance. Current waterproofing stock in West region "
                    f"is adequate for normal demand but insufficient for another rain event.",
            "ui_widget": None,
        }

    # Default
    return {
        "text": f"{scenario_prefix}I'm analyzing the current supply chain state. "
                f"There are 8 stockout risks, 3 recommended transfers, and Diwali demand surge approaching. "
                f"Would you like me to focus on a specific area? Try asking about 'Bridal Red in Pune', "
                f"'stockouts', 'Diwali preparation', or 'monsoon impact'.",
        "ui_widget": None,
    }
