from fastapi import FastAPI
from pydantic import BaseModel
from app.faq import faq_data
from app.utils import get_best_match

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat(message: Message):
    print("msg", message)
    print("Msg", Message)
    user_input = message.message
    print("User input", user_input)
    reply = get_best_match(user_input, faq_data)
    return {"reply": reply}
