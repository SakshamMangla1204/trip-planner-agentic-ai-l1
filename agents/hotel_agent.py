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


def search_hotel(state: State):
    """Search the hotel options from the web."""
    query = f"""the best possible hotel for the trip from {state["source"]} to {state["destination"]} for a budget of {state["budget"]} and the travel date is {state["travel_date"]}

Include the following constraints in your search:
hotel_options
hotel_prices
hotel_location
hotel_reviews
"""
    response = tavily.search(query=query, max_results=10)
    return response


def build_prompt(state: State, search_results):
    """Build a prompt for the llm model."""
    prompt = f"""You are an expert travel agent. You have been given the user details, now kindly find the best possible hotel option.

Source:
{state["source"]}

destination:
{state["destination"]}

travel_date:
{state["travel_date"]}

Search_results:
{search_results}

Choose the best possible hotel option for the user according to the details which are provided to you.
return only JSON results

Format:
{{
  "hotel": [],
  "hotel_cost": 0
}}
"""
    return prompt


def ask_llm(prompt):
    """Send the prompt to the llm."""
    response = llm.invoke(prompt)
    return response.content


def parse_response(response):
    """Convert JSON into python dictionary."""
    try:
        return json.loads(response)
    except Exception as exc:
        raise ValueError("Invalid format recieved") from exc


def hotel_agent(state: State):
    search_results = search_hotel(state)
    prompt = build_prompt(state, search_results)
    response = ask_llm(prompt)

    hotel = parse_response(response)
    state["hotel"] = hotel["hotel"]
    state["hotel_cost"] = hotel["hotel_cost"]
    return state
