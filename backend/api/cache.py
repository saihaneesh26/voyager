from tools.attractions import getNearByAttractions
from tools.flights import *
from tools.currency import exchageRate
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv


load_dotenv()

class Cache:
    models = ["gemini-2.5-flash","gemini-3.5-flash","gemini-3.1-flash-lite","gemini-2.5-flash-lite","gemini-3.0-flash"    ]
    agents = {}
    def __init__(self):
        for model in self.models:
            self.agents[model] = create_agent(
    model="google_genai:"+model,
    tools=[exchageRate,getNearByAttractions,getFlightsBetweenAirports,getAirportsInCityOfCountry,getAirportsInCity,getAirportsInCountry],
    system_prompt="You are a super helpful, intelligent travel assistant and provide details on exchange rates, attractions in a place, travel options." \
    "Format the response in clean markdown.Use headings, bullet lists, bold text and tables where appropriate. Do not return JSON.",
    checkpointer=InMemorySaver()) 

    def getAgent(self,model):
        return self.agents[model]
        

    