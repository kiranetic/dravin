from fastapi import FastAPI
from pydantic import BaseModel
from app.vector import create_collection, index_faq, search_faq

app = FastAPI()

class Message(BaseModel):
    message: str

@app.on_event("startup")
def startup_event():
    create_collection()
    index_faq()

@app.post("/chat")
def chat(message: Message):
    reply = search_faq(message.message)
    return {"reply": reply}
