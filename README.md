# PaintFlow.ai — AI-Powered Supply Chain Intelligence for Paint Manufacturing

PaintFlow.ai is a full-stack supply chain intelligence platform for paint manufacturing and distribution. It features three role-based portals (Admin, Dealer, Customer) with AI-powered demand forecasting, inventory optimization, smart order recommendations, and a conversational AI copilot.

## Tech Stack

| Layer      | Technology                                                  |
| ---------- | ----------------------------------------------------------- |
| Backend    | Python 3.10+, FastAPI, SQLAlchemy, SQLite                   |
| Frontend   | React 19, Vite, TailwindCSS 4, Recharts, React Router DOM  |
| ML         | Prophet (time-series forecasting)                           |
| AI         | Google Gemini 1.5 Flash (conversational copilot)            |
| Maps       | react-simple-maps (India warehouse network visualization)   |

## Prerequisites

- **Python 3.10+** (tested on 3.13)
- **Node.js 18+** and **npm**
- **Google Gemini API Key** (optional — copilot falls back to heuristics without it)

## Run on Localhost

### 1. Clone the repository

```bash
git clone https://github.com/Arijit2772-dev/hacktu7.0.git
cd hacktu7.0
```

### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install Python dependencies
pip install -r requirements.txt

# (Optional) Set your Gemini API key for the AI copilot
export GEMINI_API_KEY="your-google-gemini-api-key"
# On Windows: set GEMINI_API_KEY=your-google-gemini-api-key

# Seed the database and train Prophet forecasting models
python seed_and_train.py

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at **http://localhost:8000**
Interactive API docs at **http://localhost:8000/docs**

### 3. Frontend Setup

Open a **new terminal** window:

```bash
# Navigate to the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the dev server
npm run dev
```

The frontend will be available at **http://localhost:5173**

> Vite automatically proxies `/api` requests to the backend at `http://localhost:8000`.

### 4. Open the App

Visit **http://localhost:5173** in your browser. From the landing page, select a portal:

- **Admin Portal** — Supply chain dashboard, inventory management, demand forecasting, dealer analytics
- **Dealer Portal** — Smart order recommendations, order tracking, health score
- **Customer Portal** — Shade catalog, nearby dealer finder, snap & find color matcher

## Project Structure

```
hacktu7.0/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── config.py              # App configuration
│   │   ├── database.py            # SQLAlchemy setup
│   │   ├── models/                # Database models (Product, Shade, SKU, Warehouse, Dealer, etc.)
│   │   ├── routers/               # API endpoints (admin, dealer, customer, forecast, copilot, simulate)
│   │   ├── services/              # Business logic (analytics, forecast, inventory, dealer, copilot)
│   │   ├── ml/                    # Prophet model training & saved models
│   │   └── simulations/           # Supply chain scenario engine (truck strike, heatwave, monsoon)
│   ├── seed/                      # Database seeding scripts
│   ├── seed_and_train.py          # One-command setup: seed DB + train ML models
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # React Router configuration
│   │   ├── pages/                 # Admin, Dealer, Customer portal pages
│   │   ├── components/            # Reusable UI components (charts, maps, copilot, paint swatches)
│   │   ├── contexts/              # React context (Simulation scenarios)
│   │   ├── api/                   # Axios API client layer
│   │   └── layouts/               # Portal layouts (Admin, Dealer, Customer)
│   ├── vite.config.js
│   └── package.json
│
└── README.md
```

## Key Features

- **Demand Forecasting** — Prophet-based time-series prediction with Diwali surge detection
- **Inventory Optimization** — Days-of-cover analysis, stockout alerts, dead stock identification
- **Smart Transfers** — AI-recommended warehouse-to-warehouse inventory rebalancing
- **Smart Orders** — ML-driven order recommendations for dealers with cost savings calculation
- **AI Copilot** — Gemini-powered conversational assistant with generative UI widgets
- **Scenario Simulation** — What-if analysis for truck strikes, heatwaves, and early monsoons
- **Snap & Find** — Color matching from photos or hex codes to find the closest paint shade
- **India Warehouse Map** — Geographic visualization of warehouse network with transfer arcs

## Environment Variables

| Variable        | Required | Description                          |
| --------------- | -------- | ------------------------------------ |
| `GEMINI_API_KEY` | No       | Google Gemini API key for AI copilot. Falls back to heuristic responses if not set. |

## API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Build for Production

```bash
# Build the frontend
cd frontend
npm run build
# Output will be in frontend/dist/
```
