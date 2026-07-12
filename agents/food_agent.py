from typing import Any

from config.settings import (
    MAX_FOOD_OPTIONS,
    TAVILY_MAX_RESULTS,
)
from logger import food_logger
from prompts.food_prompt import build_food_prompt
from state import State
from utils.parsers import parse_json_response


def search_food(state: State) -> dict[str, Any]:
    from clients import get_tavily_client

    food_logger.info("=" * 50)
    food_logger.info("Food Agent Started")
    food_logger.info("=" * 50)
    food_logger.info(f"Reading state - Destination: {state['destination']}, Preferences: {state['preferences']}")
    food_logger.info("Search Started")

    tavily_client = get_tavily_client()

    query = f"""Find the best possible food place for the user who is travelling from {state["source"]} to {state["destination"]} on {state["travel_date"]}.

It is mandatory to include the checkpoints mentioned below:
food_price
food_place
food_type (veg/non-veg)
food_quantity_to_quality_ratio
food_place_review
"""
    response = tavily_client.search(query=query, max_results=TAVILY_MAX_RESULTS)

    food_logger.info("Search Completed")
    food_logger.info(f"Search returned {len(response.get('results', []))} results")

    return response


def build_prompt(state: State, search_results: dict[str, Any]) -> str:
    food_logger.info("Prompt Building Started")

    prompt = build_food_prompt(
        source=state["source"],
        destination=state["destination"],
        travel_date=state["travel_date"],
        preferences=state["preferences"],
        search_results=search_results
    )

    food_logger.info("Prompt Building Completed")
    return prompt


def ask_llm(prompt: str) -> str:
    from clients import get_llm

    food_logger.info("LLM Call Started")
    llm = get_llm()
    response = llm.invoke(prompt)
    food_logger.info("LLM Call Completed")

    print("=" * 50)
    print("RAW LLM RESPONSE START")
    print("=" * 50)
    print(response.content)
    print("=" * 50)
    print("RAW LLM RESPONSE END")
    print("=" * 50)

    return response.content


def food_agent(state: State) -> State:
    try:
        food_logger.info("=" * 50)
        food_logger.info("Food Agent Started")
        food_logger.info("=" * 50)
        food_logger.info(f"Reading state - Destination: {state['destination']}, Preferences: {state['preferences']}")

        search_results = search_food(state)

        prompt = build_prompt(state, search_results)

        response = ask_llm(prompt)

        food_logger.info("Parsing Started")
        food_options = parse_json_response(response)
        food_logger.info("Parsing Completed")

        state["food_options"] = food_options[:MAX_FOOD_OPTIONS]
        state["food_cost"] = food_options[0].get("food_price", 0.0) if food_options else 0.0

        food_logger.info(f"State Updated - Food options count: {len(state['food_options'])}, Food cost: {state['food_cost']}")
        food_logger.info("Food Agent Completed Successfully")
        food_logger.info("=" * 50)

        return state
    except Exception as e:
        food_logger.exception(f"Error in food_agent: {str(e)}")
        raise