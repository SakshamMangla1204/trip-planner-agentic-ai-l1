from state import State


def budget_agent(state: State):

    travel_cost = state["travel_expense"]
    food_cost = state["food_cost"]
    activity_cost = state["activities_cost"]
    hotel_cost = state["hotel_cost"]

    total_cost = (
        hotel_cost
        + travel_cost
        + activity_cost
        + food_cost
    )

    state["total_cost"] = total_cost

    budget = state["budget"]

    if total_cost <= budget:
        state["within_budget"] = True
    else:
        state["within_budget"] = False

    return state
