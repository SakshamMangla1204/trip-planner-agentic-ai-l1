import os

from dotenv import load_dotenv

load_dotenv()

from phoenix.otel import register
from opentelemetry import trace

from config.settings import (
    APP_NAME,
    APP_VERSION,
    PHOENIX_COLLECTOR_ENDPOINT,
    PHOENIX_PROJECT_NAME,
)

os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = PHOENIX_COLLECTOR_ENDPOINT
tracer_provider = register(project_name=PHOENIX_PROJECT_NAME)

from openinference.instrumentation.langchain import LangChainInstrumentor
LangChainInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

from logger import main_logger
from graph import build_graph
from state import State


def create_initial_state() -> State:
    main_logger.info("Creating initial state from user inputs")

    source = input("Enter Source City: ").strip()
    destination = input("Enter Destination City: ").strip()
    travel_date = input("Enter Travel Date (DD-MM-YYYY): ").strip()
    budget = float(input("Enter Budget (INR): "))

    preferences = input("Enter Preferences (comma separated): ").split(",")
    preferences = [pref.strip() for pref in preferences]

    main_logger.info(f"User inputs collected - Source: {source}, Destination: {destination}, Date: {travel_date}, Budget: {budget}")

    return {
        "source": source,
        "destination": destination,
        "travel_date": travel_date,
        "budget": budget,
        "preferences": preferences,
        "travel_options": [],
        "travel_expense": 0.0,
        "hotel_options": [],
        "hotel_cost": 0.0,
        "food_options": [],
        "food_cost": 0.0,
        "activity_options": [],
        "activities_cost": 0.0,
        "total_cost": 0.0,
        "within_budget": False,
        "final_plan": {}
    }


def main() -> None:
    main_logger.info("=" * 50)
    main_logger.info(f"{APP_NAME} v{APP_VERSION} Started")
    main_logger.info("=" * 50)

    print("\n==============================")
    print("      AI TRIP PLANNER")
    print("==============================\n")

    main_logger.info("Building graph")
    graph = build_graph()
    main_logger.info("Graph built successfully")

    main_logger.info("Creating initial state")
    initial_state = create_initial_state()

    main_logger.info("Starting graph execution")
    final_state = graph.invoke(initial_state)
    main_logger.info("Graph execution completed")

    main_logger.info("Displaying final itinerary")
    print("\n==============================")
    print("      FINAL ITINERARY")
    print("==============================\n")

    print(final_state["final_plan"])

    main_logger.info("=" * 50)
    main_logger.info(f"{APP_NAME} Finished")
    main_logger.info("=" * 50)


if __name__ == "__main__":
    main()