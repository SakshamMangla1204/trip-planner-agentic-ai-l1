from config.settings import MAX_BUDGET_PERCENT
from logger import budget_logger
from state import State


def calculate_total_cost(state: State) -> float:
    budget_logger.info("Cost Calculation Started")

    travel_cost = state["travel_expense"]
    food_cost = state["food_cost"]
    activity_cost = state["activities_cost"]
    hotel_cost = state["hotel_cost"]

    total_cost = hotel_cost + travel_cost + activity_cost + food_cost

    budget_logger.info(f"Cost Calculation Completed - Total: {total_cost}")
    return total_cost


def check_budget_constraint(total_cost: float, budget: float) -> bool:
    budget_logger.info("Budget Check Started")
    budget_logger.info(f"Comparing total cost {total_cost} with budget {budget}")

    is_within_budget = total_cost <= (budget * MAX_BUDGET_PERCENT)

    if is_within_budget:
        budget_logger.info(f"Budget Check Passed - Total cost {total_cost} is within budget {budget}")
    else:
        budget_logger.warning(f"Budget Check Failed - Total cost {total_cost} exceeds budget {budget}")

    budget_logger.info("Budget Check Completed")
    return is_within_budget


def budget_agent(state: State) -> State:
    try:
        budget_logger.info("=" * 50)
        budget_logger.info("Budget Agent Started")
        budget_logger.info("=" * 50)
        budget_logger.info(f"Reading state - Travel expense: {state['travel_expense']}, Hotel cost: {state['hotel_cost']}, Food cost: {state['food_cost']}, Activities cost: {state['activities_cost']}")

        total_cost = calculate_total_cost(state)

        within_budget = check_budget_constraint(total_cost, state["budget"])

        state["total_cost"] = total_cost
        state["within_budget"] = within_budget

        budget_logger.info(f"State Updated - Total cost: {state['total_cost']}, Within budget: {state['within_budget']}")
        budget_logger.info("Budget Agent Completed Successfully")
        budget_logger.info("=" * 50)

        return state
    except Exception as e:
        budget_logger.exception(f"Error in budget_agent: {str(e)}")
        raise