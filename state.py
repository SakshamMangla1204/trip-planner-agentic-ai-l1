from typing import TypedDict

class State(TypedDict):
    destination:str
    budget:float
    source:str
    travel_date:str
    preferences:list[str]

    hotel:list[str]
    hotel_cost:float

    travel_mode:list[str]
    travel_expense:float

    food:list[str]
    food_cost:float

    activities:list[str]
    activities_cost:float

    total_cost:float
    within_budget:bool

    final_plan:dict[str, any]



