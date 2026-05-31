from langchain.agents import create_agent
from dotenv import load_dotenv
from backend.tools.attractions import getNearByAttractions
from backend.tools.flights import *
from backend.tools.currency import exchageRate

load_dotenv()

agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    tools=[exchageRate,getNearByAttractions,getFlightsBetweenAirports,getAirportsInCityOfCountry,getAirportsInCity,getAirportsInCountry],
    system_prompt="You are a super helpful, intelligent travel assistant and provide details on exchange rates, attractions in a place, travel options.")

def getResult(input:str):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": input}]}
    )
    # return (result["messages"][-1])
    return "dev"