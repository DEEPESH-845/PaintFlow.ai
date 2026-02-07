from __future__ import annotations
from fastapi import APIRouter
from app.simulations.scenarios import get_scenario_list, get_scenario_data

router = APIRouter()


@router.get("/scenarios")
def list_scenarios():
    return get_scenario_list()


@router.get("/scenario/{scenario_id}/data")
def scenario_data(scenario_id: str):
    data = get_scenario_data(scenario_id.upper())
    if not data:
        return {"error": "Scenario not found"}
    return data
