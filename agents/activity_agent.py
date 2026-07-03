import os 
import json
from langchain_ollama import ChatOllama
from tavily import TavilyClient
from dotenv import load_dotenv

from state import State

llm= ChatOllama(model="qwen3:8b", temperature=0,)

tavily= TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY"),    
)
def search_actvity(state:State):
    """Search the web for th best possible activity one can perform in the destination city as mentioned by the user """
    query=f"""Find the high rated and best possible,commonly done activities by the the visitors the destination entered by the user{state['destination]}']}
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
    response=tavily.search(query=query,max_results=10)
    return response
    
def build_prompt(state:State,search_results):
    """Build a prompt for the llm model"""
    prompt=f"""You are an expert travel agent you need to find out the best possible activities a user can perfrom in the destination he is visiting to kindly fetch me some valuable places where the user can spend his worthy time and money according to the details which are mentioned below:
    Source:
    {state["source"]}

    destination:
    {state['destination']}
  
    travel_date:
    {state["travel_date"]}
   
    search_results:
    {state['search_results']}

 Choose the best poosible activtiy which has a good value to investmenet ration ffilter thoroughly thorught the entire web and give me out the best possble activities which a user can perform while he is visiting accrding to the details which have been share
 Return only Json output
 Format:
 activity_options=[]
 activity_loaction=[]
 actiity_time=[]
 activity_price[]
"""
    
    return prompt

def ask_llm(state:State,prompt):
    """give the above prompt to llm to process the. results"""
    response=llm.invoke(prompt)
    return response.content 

def parse_response(response):
    """convert json into python dictionary"""
       
    try:
        return json.loads(response)
    except Exception as exc:
        raise ValueError("Invalid format recived ") from exc


def activity_agent(state: State):
    """Main activity agent function."""
    search_results = search_actvity(state)
    prompt = build_prompt(state, search_results)
    response = ask_llm(state, prompt)
    
    activity = parse_response(response)
    state["activities"] = activity.get("activities", activity.get("activity_options", []))
    state["activities_cost"] = activity.get("activities_cost", activity.get("activity_price", 0))
    return state





     

    


     
 




     
