from langchain.agents import create_agent
from dotenv import load_dotenv

from tools.currency import exchageRate

load_dotenv()

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[exchageRate],
    system_prompt="You are a super helpful, intelligent travel assistant")

def getResult(input:str):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": input}]}
    )
    return (result["messages"][-1])

print(getResult("What is the value of 1 Indian Rupee in Japanese currency"))