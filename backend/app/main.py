from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import APP_SIMULATION_DATE



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: preload Prophet models and scenario data
    from app.services.forecast_service import preload_models
    from app.simulations.scenarios import preload_scenarios
    try:
        preload_models()
    except Exception as e:
        print(f"Warning: Could not preload Prophet models: {e}")
    try:
        preload_scenarios()
    except Exception as e:
        print(f"Warning: Could not preload scenarios: {e}")
    yield
    # Shutdown


app = FastAPI(
    title="PaintFlow.ai API",
    description="AI-Powered Supply Chain Intelligence for Paint Manufacturing",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.routers import admin, dealer, customer, forecast, copilot, simulate

app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(dealer.router, prefix="/api/dealer", tags=["Dealer"])
app.include_router(customer.router, prefix="/api/customer", tags=["Customer"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(copilot.router, prefix="/api/copilot", tags=["Copilot"])
app.include_router(simulate.router, prefix="/api/simulate", tags=["Simulate"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "PaintFlow.ai"}


@app.get("/api/meta")
def get_meta():
    return {
        "app_simulation_date": APP_SIMULATION_DATE,
        "scenarios": ["NORMAL", "TRUCK_STRIKE", "HEATWAVE", "EARLY_MONSOON"],
        "model_version": "prophet-1.1.5",
        "demo_mode": False,
    }
