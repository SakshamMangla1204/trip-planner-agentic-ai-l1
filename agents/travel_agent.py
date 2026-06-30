import json
import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from tavily import TavilyClient

from state import State

load_dotenv()



TEMPERATURE = 0.2
TOP_P = 0.9
MAX_OUTPUT_TOKENS = 500

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY"),
)

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)


def search_travel(state: State):
    """Search the travel options from the web."""
    query = f"""the best possible travel options to travel from {state["source"]} to {state["destination"]} for a budget of {state["budget"]} and a travel date of {state["travel_date"]}

Include the following constraints in your search:
travel_mode
approximation_price
travel_duration
"""
    response = tavily.search(query=query, max_results=10)
    return response


def build_prompt(state: State, search_results):
    """Build a prompt for the LLM."""
    prompt = f"""You are a travel agent. You have been given the user details kindly find the best possible trip for the user.
User Details:

Source:
{state["source"]}

destination:
{state["destination"]}

budget:
{state["budget"]}

travel_date:
{state["travel_date"]}

Search_Results:
{search_results}

Choose the best travel options according to the details which are provided to you above.
return only JSON results

Format:
{{
  "travel_mode": [],
  "travel_expense": 0
}}
"""
    return prompt


def ask_llm(prompt):
    """Send prompt to the llm."""
    response = llm.invoke(prompt)
    return response.content


def parse_response(response):
    """Convert JSON into python dictionary."""
    try:
        return json.loads(response)
    except Exception as exc:
        raise ValueError("invalid format recieved") from exc


def travel_agent(state: State):
    search_results = search_travel(state)
    prompt = build_prompt(state, search_results)
    response = ask_llm(prompt)

    travel = parse_response(response)
    state["travel_mode"] = travel["travel_mode"]
    state["travel_expense"] = travel["travel_expense"]
    return state
