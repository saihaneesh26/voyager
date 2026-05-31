from fastapi import FastAPI
import cache
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

modelCache = cache()

@app.get("/")
def home():
    return "HI"

@app.get("/query")
def invokeAI(query: str, model: str, session_id:str):
    if query == None or query == "":
        return "NO query requested"
    if model not in modelCache :
        return "NO MODEL AVAILABLE"

    result = modelCache[model].invoke({"messages": [{"role": "user","content": query}]}, config={"configurable": {"thread_id": session_id}})

    message = result["messages"][-1]

    if isinstance(message.content, list):
        return PlainTextResponse(message.content[0]["text"])

    return PlainTextResponse(str(message.content))

    