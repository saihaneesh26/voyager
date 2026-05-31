from fastapi import FastAPI
from api.cache import Cache
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://voyager-8tjk.onrender.com"],
    allow_credentials=True,
    allow_methods=["GET","OPTIONS"],
    allow_headers=["*"],
)

modelCache = Cache()

@app.get("/")
def home():
    return "HI"

@app.get("/query")
def invokeAI(query: str, model: str, session_id:str):
    if query == None or query == "":
        return PlainTextResponse("NO AGENT SELECTED",status_code=400)
    
    agent = modelCache.getAgent(model)

    if agent is None:
        return PlainTextResponse("NO MODEL AVAILABLE",status_code=400)
    result = agent.invoke({"messages": [{"role": "user","content": query}]}, config={"configurable": {"thread_id": session_id}})

    message = result["messages"][-1]

    if isinstance(message.content, list):
        return PlainTextResponse(message.content[0]["text"])

    return PlainTextResponse(str(message.content))

    