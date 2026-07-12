from typing import Any

from config.settings import (
    MAX_HOTEL_OPTIONS,
    TAVILY_MAX_RESULTS,
)
from logger import hotel_logger
from prompts.hotel_prompt import build_hotel_prompt
from state import State
from utils.parsers import parse_json_response


def search_hotel(state: State) -> dict[str, Any]:
    from clients import get_tavily_client

    hotel_logger.info("=" * 50)
    hotel_logger.info("Hotel Agent Started")
    hotel_logger.info("=" * 50)
    hotel_logger.info(f"Reading state - Destination: {state['destination']}, Budget: {state['budget']}")
    hotel_logger.info("Search Started")

    tavily_client = get_tavily_client()

    query = f"""the best possible hotel for the trip from {state["source"]} to {state["destination"]} for a budget of {state["budget"]} and the travel date is {state["travel_date"]}

Include the following constraints in your search:
hotel_options
hotel_prices
hotel_location
hotel_reviews
"""
    response = tavily_client.search(query=query, max_results=TAVILY_MAX_RESULTS)

    hotel_logger.info("Search Completed")
    hotel_logger.info(f"Search returned {len(response.get('results', []))} results")

    return response


def build_prompt(state: State, search_results: dict[str, Any]) -> str:
    hotel_logger.info("Prompt Building Started")

    prompt = build_hotel_prompt(
        source=state["source"],
        destination=state["destination"],
        travel_date=state["travel_date"],
        budget=state["budget"],
        preferences=state["preferences"],
        search_results=search_results
    )

    hotel_logger.info("Prompt Building Completed")
    return prompt


def ask_llm(prompt: str) -> str:
    from clients import get_llm

    hotel_logger.info("LLM Call Started")
    llm = get_llm()
    response = llm.invoke(prompt)
    hotel_logger.info("LLM Call Completed")

    print("=" * 50)
    print("RAW LLM RESPONSE START")
    print("=" * 50)
    print(response.content)
    print("=" * 50)
    print("RAW LLM RESPONSE END")
    print("=" * 50)

    return response.content


def hotel_agent(state: State) -> State:
    try:
        hotel_logger.info("=" * 50)
        hotel_logger.info("Hotel Agent Started")
        hotel_logger.info("=" * 50)
        hotel_logger.info(f"Reading state - Destination: {state['destination']}, Budget: {state['budget']}")

        search_results = search_hotel(state)

        prompt = build_prompt(state, search_results)

        response = ask_llm(prompt)

        hotel_logger.info("Parsing Started")
        hotel_options = parse_json_response(response)
        hotel_logger.info("Parsing Completed")

        state["hotel_options"] = hotel_options[:MAX_HOTEL_OPTIONS]
        state["hotel_cost"] = hotel_options[0].get("hotel_price", 0.0) if hotel_options else 0.0

        hotel_logger.info(f"State Updated - Hotel options count: {len(state['hotel_options'])}, Hotel cost: {state['hotel_cost']}")
        hotel_logger.info("Hotel Agent Completed Successfully")
        hotel_logger.info("=" * 50)

        return state
    except Exception as e:
        hotel_logger.exception(f"Error in hotel_agent: {str(e)}")
        raise