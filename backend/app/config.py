from __future__ import annotations
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "paintflow.db"
MODEL_DIR = BASE_DIR / "app" / "ml" / "models"
SCENARIO_DIR = BASE_DIR / "app" / "simulations" / "data"

DATABASE_URL = f"sqlite:///{DB_PATH}"

# The narrative date for the demo - all logic uses this as "today"
APP_SIMULATION_DATE = "2025-10-10"

# Gemini API key (set via environment variable)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Copilot timeout in seconds
COPILOT_TIMEOUT = 3.0
