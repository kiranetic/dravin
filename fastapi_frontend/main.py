from fastapi import FastAPI, Body
import requests
from .chatbot import init_chatbot, get_response

app = FastAPI()
chatbot = init_chatbot()

@app.post("/chat")
async def chat(query: str = Body(...)):
    intent = get_response(chatbot, query)
    django_response = requests.post(
        "http://127.0.0.1:8000/api/queries/",
        json={"text": query},
        headers={"Content-Type": "application/json"}
    )
    return {"intent": intent, "django_data": django_response.json()}