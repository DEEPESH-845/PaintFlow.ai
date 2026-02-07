from __future__ import annotations
"""
What-If simulation scenarios: Truck Strike, Heatwave, Early Monsoon.
Pre-computed data loaded at startup for instant client-side toggling.
"""

import json
from pathlib import Path
from app.config import SCENARIO_DIR
from typing import Optional

_scenarios: dict = {}

SCENARIO_DEFINITIONS = {
    "TRUCK_STRIKE": {
        "name": "Truck Strike",
        "description": "Nationwide trucking strike reduces inbound stock by 50% for 5 days.",
        "impact": "Cascading stockouts across West and Central regions.",
        "affected_regions": ["West", "Central"],
        "inventory_multiplier": 0.5,
        "demand_multiplier": 1.0,
    },
    "HEATWAVE": {
        "name": "Heatwave",
        "description": "Severe heatwave increases exterior paint demand by 35%.",
        "impact": "Exterior paints deplete faster in North and Central regions.",
        "affected_regions": ["North", "Central"],
        "inventory_multiplier": 1.0,
        "demand_multiplier": 1.35,
    },
    "EARLY_MONSOON": {
        "name": "Early Monsoon",
        "description": "Monsoon arrives 2 weeks early, waterproofing demand surges 60%.",
        "impact": "Waterproofing products deplete rapidly in West and South.",
        "affected_regions": ["West", "South"],
        "inventory_multiplier": 1.0,
        "demand_multiplier": 1.6,
    },
}


def preload_scenarios():
    """Load pre-computed scenario data from JSON files."""
    global _scenarios
    scenario_dir = Path(SCENARIO_DIR)
    if not scenario_dir.exists():
        scenario_dir.mkdir(parents=True, exist_ok=True)
        print("  Scenario directory created. Generating scenario data...")
        generate_scenario_data()
        return

    for json_file in scenario_dir.glob("*.json"):
        try:
            with open(json_file, "r") as f:
                _scenarios[json_file.stem.upper()] = json.load(f)
            print(f"  Loaded scenario: {json_file.stem}")
        except Exception as e:
            print(f"  Warning: Failed to load {json_file.name}: {e}")

    if not _scenarios:
        generate_scenario_data()


def generate_scenario_data():
    """Generate scenario data from base inventory data."""
    global _scenarios
    scenario_dir = Path(SCENARIO_DIR)
    scenario_dir.mkdir(parents=True, exist_ok=True)

    for scenario_id, definition in SCENARIO_DEFINITIONS.items():
        scenario_data = {
            "id": scenario_id,
            **definition,
            "dashboard_summary": _compute_scenario_dashboard(definition),
        }
        _scenarios[scenario_id] = scenario_data

        filepath = scenario_dir / f"{scenario_id.lower()}.json"
        with open(filepath, "w") as f:
            json.dump(scenario_data, f, indent=2)
        print(f"  Generated scenario: {scenario_id}")


def _compute_scenario_dashboard(definition: dict) -> dict:
    """Compute modified dashboard metrics for a scenario."""
    inv_mult = definition["inventory_multiplier"]
    demand_mult = definition["demand_multiplier"]

    return {
        "total_revenue_mtd": round(45_00_000 * demand_mult),
        "stockout_count": int(8 + (1 - inv_mult) * 15 + (demand_mult - 1) * 10),
        "pending_transfers": int(3 + (1 - inv_mult) * 5),
        "revenue_at_risk": round(12_50_000 * (1 - inv_mult) + 8_00_000 * (demand_mult - 1)),
        "avg_days_of_cover": round(25 * inv_mult / demand_mult, 1),
    }


def get_scenario_list() -> list[dict]:
    return [
        {"id": k, "name": v["name"], "description": v["description"]}
        for k, v in SCENARIO_DEFINITIONS.items()
    ]


def get_scenario_data(scenario_id: str) -> dict | None:
    return _scenarios.get(scenario_id)
