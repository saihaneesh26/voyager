from fastapi import FastAPI
from backend import main

app = FastAPI()

@app.get("/")
def home():
    return "HI"

@app.get("/query")
def invokeAI(q:str) -> str:
    return main.getResult(q)