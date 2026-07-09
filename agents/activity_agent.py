from typing import Any

from config.settings import (
    MAX_ACTIVITY_OPTIONS,
    TAVILY_MAX_RESULTS,
)
from logger import activity_logger
from prompts.activity_prompt import build_activity_prompt
from state import State
from utils.parsers import parse_json_response


def search_activity(state: State) -> dict[str, Any]:
    from clients import get_tavily_client

    activity_logger.info("=" * 50)
    activity_logger.info("Activity Agent Started")
    activity_logger.info("=" * 50)
    activity_logger.info(f"Reading state - Destination: {state['destination']}, Travel date: {state['travel_date']}")
    activity_logger.info("Search Started")

    tavily_client = get_tavily_client()

    query = f"""Find the high rated and best possible,commonly done activities by the the visitors the destination entered by the user{state['destination']}
     It is mandoatory to take care of the check points which are mentioned belo:
     activity_name
     activity_time
     activity_type
     activity_reveiw
     activity_cost
     activity_location
     activity_duration
     activity_safety
     activity_tickets_availability
    """
    response = tavily_client.search(query=query, max_results=TAVILY_MAX_RESULTS)

    activity_logger.info("Search Completed")
    activity_logger.info(f"Search returned {len(response.get('results', []))} results")

    return response


def build_prompt(state: State, search_results: dict[str, Any]) -> str:
    activity_logger.info("Prompt Building Started")

    prompt = build_activity_prompt(
        source=state["source"],
        destination=state["destination"],
        travel_date=state["travel_date"],
        search_results=search_results
    )

    activity_logger.info("Prompt Building Completed")
    return prompt


def ask_llm(prompt: str) -> str:
    from clients import get_llm

    activity_logger.info("LLM Call Started")
    llm = get_llm()
    response = llm.invoke(prompt)
    activity_logger.info("LLM Call Completed")

    return response.content


def activity_agent(state: State) -> State:
    try:
        activity_logger.info("=" * 50)
        activity_logger.info("Activity Agent Started")
        activity_logger.info("=" * 50)
        activity_logger.info(f"Reading state - Destination: {state['destination']}, Travel date: {state['travel_date']}")

        search_results = search_activity(state)

        prompt = build_prompt(state, search_results)

        response = ask_llm(prompt)

        activity_logger.info("Parsing Started")
        activity_options = parse_json_response(response)
        activity_logger.info("Parsing Completed")

        state["activity_options"] = activity_options[:MAX_ACTIVITY_OPTIONS]
        state["activities_cost"] = activity_options[0].get("activities_cost", activity_options[0].get("activity_price", 0.0)) if activity_options else 0.0

        activity_logger.info(f"State Updated - Activity options count: {len(state['activity_options'])}, Activities cost: {state['activities_cost']}")
        activity_logger.info("Activity Agent Completed Successfully")
        activity_logger.info("=" * 50)

        return state
    except Exception as e:
        activity_logger.exception(f"Error in activity_agent: {str(e)}")
        raise