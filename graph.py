from logger import graph_logger
from langgraph.graph import StateGraph, START, END
from state import State
from agents.travel_agent import travel_agent
from agents.hotel_agent import hotel_agent
from agents.activity_agent import activity_agent
from agents.food_agent import food_agent
from agents.budget_agent import budget_agent

def build_graph():
    graph_logger.info("Creating StateGraph")
    workflow = StateGraph(State)
    
    graph_logger.info("Registering nodes: travel, hotel, food, activity, budget")
    workflow.add_node("travel", travel_agent)
    workflow.add_node("hotel", hotel_agent)
    workflow.add_node("food", food_agent)
    workflow.add_node("activity", activity_agent)
    workflow.add_node("budget", budget_agent)

    graph_logger.info("Registering edges")
    workflow.add_edge(START, "travel")
    workflow.add_edge("travel", "hotel")
    workflow.add_edge("hotel", "food")
    workflow.add_edge("food", "activity")
    workflow.add_edge("activity", "budget")
    workflow.add_edge("budget", END)

    graph_logger.info("Compiling graph")
    compiled_graph = workflow.compile()
    graph_logger.info("Graph compilation successful")
    
    return compiled_graph
