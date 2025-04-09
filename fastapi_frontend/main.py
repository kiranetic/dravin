from fastapi import FastAPI, Body
import requests
from .chatbot import init_chatbot

app = FastAPI()
chatbot = init_chatbot()

@app.post("/chat")
async def chat(query: str = Body(...)):
    response = chatbot.get_response(query)
    django_response = requests.post(
        "http://127.0.0.1:8000/api/queries/",
        json={"text": query},
        headers={"Content-Type": "application/json"}
    )
    return {"response": response, "django_data": django_response.json()}