from __future__ import annotations
#!/usr/bin/env python3
"""
One-shot setup: Seed database + Train Prophet models.
Run this once before starting the app.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seed.generate_data import run_seed


def main():
    print("=" * 60)
    print("  PaintFlow.ai - Setup")
    print("=" * 60)

    # Step 1: Seed database
    print("\n[Step 1/2] Seeding database...")
    run_seed()

    # Step 2: Train Prophet models
    print("\n[Step 2/2] Training Prophet models...")
    try:
        from app.ml.train_prophet import train_all_models
        train_all_models()
    except ImportError as e:
        print(f"  Warning: Prophet not installed. Skipping model training. ({e})")
        print("  Install with: pip install prophet")
    except Exception as e:
        print(f"  Warning: Model training failed: {e}")
        print("  The app will still work but forecasts will use fallback data.")

    print("\n" + "=" * 60)
    print("  Setup complete!")
    print("  Start the server: uvicorn app.main:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    main()
