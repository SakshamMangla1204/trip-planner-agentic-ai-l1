from typing import TypedDict, List, Any

class State(TypedDict):
    destination: str
    budget: float
    source: str
    travel_date: str
    preferences: List[str]

    hotel_options: List[dict[str, Any]]
    hotel_cost: float

    travel_options: List[dict[str, Any]]
    travel_expense: float

    food_options: List[dict[str, Any]]
    food_cost: float

    activity_options: List[dict[str, Any]]
    activities_cost: float

    total_cost: float
    within_budget: bool

    final_plan: dict[str, Any]



