from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from backend.tools.attractions import getNearByAttractions
from backend.tools.flights import *
from backend.tools.currency import exchageRate

load_dotenv()

def getResult(input:str, model:str, session:str):
    if input ==None or input == "":
        return "NO query requested"
    if model ==None or model == "":
        return "No Model selected"

    agent = create_agent(
    model="google_genai:"+model,
    tools=[exchageRate,getNearByAttractions,getFlightsBetweenAirports,getAirportsInCityOfCountry,getAirportsInCity,getAirportsInCountry],
    system_prompt="You are a super helpful, intelligent travel assistant and provide details on exchange rates, attractions in a place, travel options." \
    "Format the response in clean markdown.Use headings, bullet lists, bold text and tables where appropriate. Do not return JSON.")

    result = agent.invoke(
        {"messages": [{"role": "user", "content": input}]}
    )
    message = result["messages"][-1]

    if isinstance(message.content, list):
        return message.content[0]["text"]

    return str(message.content)