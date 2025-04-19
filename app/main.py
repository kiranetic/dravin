from fastapi import FastAPI
from pydantic import BaseModel

from app.vector import create_collection, index_faq, search_faq
from app.fallback import gpt_fallback_response


app = FastAPI()

class Message(BaseModel):
    message: str

@app.on_event("startup")
def startup_event():
    create_collection()
    index_faq()

@app.post("/chat")
def chat(message: Message):
    user_input = message.message
    reply = search_faq(user_input)

    if reply == "__fallback__":
        reply = gpt_fallback_response(user_input)
    
    return {"reply": reply}
