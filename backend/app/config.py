from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv  # Import this to load the .env file

BASE_DIR = Path(__file__).resolve().parent.parent

# --- NEW: Force load the .env file ---
# This tells Python to look for .env in the backend folder (BASE_DIR)
load_dotenv(BASE_DIR / ".env")
# -------------------------------------

DB_PATH = BASE_DIR / "paintflow.db"
MODEL_DIR = BASE_DIR / "app" / "ml" / "models"
SCENARIO_DIR = BASE_DIR / "app" / "simulations" / "data"

DATABASE_URL = f"sqlite:///{DB_PATH}"

# The narrative date for the demo - all logic uses this as "today"
APP_SIMULATION_DATE = "2025-10-10"

# Gemini API key (Now it will actually find it)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Copilot timeout in seconds
COPILOT_TIMEOUT = 3.0