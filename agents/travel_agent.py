import json
from typing import Any

from config.settings import (
    MAX_TRAVEL_OPTIONS,
    TAVILY_MAX_RESULTS,
)
from logger import travel_logger
from prompts.travel_prompt import build_travel_prompt
from state import State
from utils.parsers import parse_json_response


def search_travel(state: State) -> dict[str, Any]:
    from clients import get_tavily_client

    travel_logger.info("=" * 50)
    travel_logger.info("Travel Agent Started")
    travel_logger.info("=" * 50)
    travel_logger.info(f"Reading state - Source: {state['source']}, Destination: {state['destination']}, Budget: {state['budget']}")
    travel_logger.info("Search Started")

    tavily_client = get_tavily_client()

    query = f"""the best possible travel options to travel from {state["source"]} to {state["destination"]} for a budget of {state["budget"]} and a travel date of {state["travel_date"]}

Include the following constraints in your search:
travel_mode
approximation_price
travel_duration
"""
    response = tavily_client.search(query=query, max_results=TAVILY_MAX_RESULTS)

    travel_logger.info("Search Completed")
    travel_logger.info(f"Search returned {len(response.get('results', []))} results")

    return response


def build_prompt(state: State, search_results: dict[str, Any]) -> str:
    travel_logger.info("Prompt Building Started")

    prompt = build_travel_prompt(
        source=state["source"],
        destination=state["destination"],
        travel_date=state["travel_date"],
        budget=state["budget"],
        preferences=state["preferences"],
        search_results=search_results
    )

    travel_logger.info("Prompt Building Completed")
    return prompt


def ask_llm(prompt: str) -> str:
    from clients import get_llm

    travel_logger.info("LLM Call Started")
    llm = get_llm()
    response = llm.invoke(prompt)
    travel_logger.info("LLM Call Completed")

    print("=" * 50)
    print("RAW LLM RESPONSE START")
    print("=" * 50)
    print(response.content)
    print("=" * 50)
    print("RAW LLM RESPONSE END")
    print("=" * 50)

    return response.content


def travel_agent(state: State) -> State:
    try:
        travel_logger.info("=" * 50)
        travel_logger.info("Travel Agent Started")
        travel_logger.info("=" * 50)
        travel_logger.info(f"Reading state - Source: {state['source']}, Destination: {state['destination']}, Budget: {state['budget']}")

        search_results = search_travel(state)

        prompt = build_prompt(state, search_results)

        response = ask_llm(prompt)

        travel_logger.info("Parsing Started")
        travel_options = parse_json_response(response)
        travel_logger.info("Parsing Completed")

        state["travel_options"] = travel_options[:MAX_TRAVEL_OPTIONS]
        state["travel_expense"] = travel_options[0].get("estimated_cost", 0.0) if travel_options else 0.0

        travel_logger.info(f"State Updated - Travel options count: {len(state['travel_options'])}, Travel expense: {state['travel_expense']}")
        travel_logger.info("Travel Agent Completed Successfully")
        travel_logger.info("=" * 50)

        return state
    except Exception as e:
        travel_logger.exception(f"Error in travel_agent: {str(e)}")
        raise