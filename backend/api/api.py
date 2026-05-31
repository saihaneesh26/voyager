from fastapi import FastAPI
from backend import main
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "HI"

@app.get("/query")
def invokeAI(query: str, model: str, session:str):
    result = main.getResult(query, model, session)

    message = result["messages"][-1]

    if isinstance(message.content, list):
        text = message.content[0]["text"]
    else:
        text = str(message.content)

    return PlainTextResponse(text)

    