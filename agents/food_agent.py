import json
import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from tavily import TavilyClient

from state import State

load_dotenv()

TEMPERATURE = 0.1
TOP_P = 0.9
MAX_OUTPUT_TOKENS = 500

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY"),
)

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)


def search_food(state: State):
    """Search the web for the best food options for the trip."""
    query = f"""Find the best possible food place for the user who is travelling from {state["source"]} to {state["destination"]} on {state["travel_date"]}.

It is mandatory to include the checkpoints mentioned below:
food_price
food_place
food_type (veg/non-veg)
food_quantity_to_quality_ratio
food_place_review
"""
    response = tavily.search(query=query, max_results=10)
    return response


def build_prompt(state: State, search_results):
    """Build a prompt for the llm model."""
    prompt = f"""You are an expert travel agent and a food vlogger. Kindly find the best possible food places from the web for the trip whose details are shared below.

Source:
{state["source"]}

Destination:
{state["destination"]}

Travel date:
{state["travel_date"]}

Preferences:
{state["preferences"]}

Search results:
{search_results}

Choose the best possible food places according to the request of the user and help them find the best food options.
Return only JSON.

Format:
{{
  "food_options": [],
  "food_budget": 0
}}
"""
    return prompt


def ask_llm(prompt):
    """Send the prompt to the llm."""
    response = llm.invoke(prompt)
    return response.content


def parse_response(response):
    """Convert JSON into a python dictionary."""
    try:
        return json.loads(response)
    except Exception as exc:
        raise ValueError("Invalid format received") from exc


def food_agent(state: State):
    search_results = search_food(state)
    prompt = build_prompt(state, search_results)
    response = ask_llm(prompt)

    food = parse_response(response)
    state["food"] = food.get("food", food.get("food_options", []))
    state["food_cost"] = food.get("food_cost", food.get("food_budget", 0))
    return state
