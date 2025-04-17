from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.faq import faq_data

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat(message: Message):
    user_input = message.message.lower()
    for question, answer in faq_data.items():
        if question.lower() in user_input:
            return {"reply": answer}
    return {"reply": "Sorry, I didn't understand that. Can you please rephrase?"}
