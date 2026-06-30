import json
import os

from langchain import ollama
from state import State
from dotenv import dotenv 

TEMPERATURE=0.1
TOKENS=500
TOP_P=0,9

tavily=tavily_client(spi_key=os.getev("Tavily_api_key"))

llm=ChatOllama(model=qwen3:8b,temperature=0)

def search_food(state:State):
    """Search the web for the best food options for the trip according to the user details which are mentioned:
    """
    query=f""" Find the best possible food place for the user who is travelling from {state['source']} to {state['destination']} on {state['travel_date']}
      It is mandatory to include the checkpoints am going to mention below which may include:
      Food_price
      Food_place
      Food_type(veg/non-veg)
      Food_quntity to qualityratio
      Food_place_reveiw 
      """
    
    response = tavily.search(query=query, max_results=10)
    return response 

def build_prompt()