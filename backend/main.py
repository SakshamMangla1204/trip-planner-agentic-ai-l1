"""
backend/main.py — FastAPI backend for AI Trip Planner

Exposes the LangGraph pipeline as a REST API endpoint.
"""

import os
import sys
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Add project root to path so we can import project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from graph import build_graph
from state import State

# Paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

app = FastAPI(title="Cosmic Navigator — AI Trip Planner", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    source: str
    destination: str
    travel_date: str
    budget: float
    preferences: list[str]


class TripResponse(BaseModel):
    travel_options: list[dict[str, Any]]
    travel_expense: float
    hotel_options: list[dict[str, Any]]
    hotel_cost: float
    food_options: list[dict[str, Any]]
    food_cost: float
    activity_options: list[dict[str, Any]]
    activities_cost: float
    total_cost: float
    within_budget: bool
    final_plan: dict[str, Any]


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/plan", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    try:
        graph = build_graph()

        initial_state: State = {
            "source": request.source,
            "destination": request.destination,
            "travel_date": request.travel_date,
            "budget": request.budget,
            "preferences": request.preferences,
            "travel_options": [],
            "travel_expense": 0.0,
            "hotel_options": [],
            "hotel_cost": 0.0,
            "food_options": [],
            "food_cost": 0.0,
            "activity_options": [],
            "activities_cost": 0.0,
            "total_cost": 0.0,
            "within_budget": False,
            "final_plan": {},
        }

        result = graph.invoke(initial_state)

        return TripResponse(
            travel_options=result.get("travel_options", []),
            travel_expense=result.get("travel_expense", 0.0),
            hotel_options=result.get("hotel_options", []),
            hotel_cost=result.get("hotel_cost", 0.0),
            food_options=result.get("food_options", []),
            food_cost=result.get("food_cost", 0.0),
            activity_options=result.get("activity_options", []),
            activities_cost=result.get("activities_cost", 0.0),
            total_cost=result.get("total_cost", 0.0),
            within_budget=result.get("within_budget", False),
            final_plan=result.get("final_plan", {}),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve frontend — catch-all route (only for non-API paths)
@app.api_route("/{full_path:path}", methods=["GET"])
async def serve_frontend(full_path: str):
    # Don't interfere with API routes
    if full_path.startswith("health") or full_path.startswith("plan") or full_path.startswith("openapi") or full_path.startswith("docs") or full_path.startswith("redoc"):
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    if not os.path.isdir(FRONTEND_DIR):
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"error": "Frontend not found"})

    # Serve exact file if it exists, otherwise fall back to index.html
    file_path = os.path.join(FRONTEND_DIR, full_path or "index.html")
    if not full_path or not os.path.isfile(file_path):
        file_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(file_path)
