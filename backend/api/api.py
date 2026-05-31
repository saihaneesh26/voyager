from fastapi import FastAPI
import main
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

@app.get("/")
def home():
    return "HI"

@app.get("/query")
def invokeAI(query: str, model: str, session_id:str):
    result = main.getResult(query, model, session_id)
    return PlainTextResponse(result)

    