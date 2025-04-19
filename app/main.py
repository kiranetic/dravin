from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.vector import create_collection, index_faq, search_faq
from app.fallback import gpt_fallback_response
from app.logger import log_response
from app.meta import APP_METADATA
from app.config import TEMPLATE_DIR


app = FastAPI()

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

class Message(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/info")
def app_info():
    return APP_METADATA


@app.on_event("startup")
def startup_event():
    create_collection()
    index_faq()


@app.post("/chat")
def chat(message: Message):
    user_input = message.message
    print(f"🔹 Incoming query: {user_input}")

    reply, score = search_faq(user_input)

    if reply == "__fallback__":
        print("⚠️ No FAQ match found. Using GPT fallback.")
        reply = gpt_fallback_response(user_input)
        source = "gpt"
        fallback_reason = "no_match_above_threshold"
    else:
        print("✅ FAQ match found.")
        source = "faq"
        fallback_reason = None
    
    print(f"📝 Reply: {reply}")

    log_response(user_query=user_input, response=reply, source=source, score=score, fallback_reason=fallback_reason)

    return {"reply": reply}

