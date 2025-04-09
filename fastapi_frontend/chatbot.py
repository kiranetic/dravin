from transformers import pipeline
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self):
        self.mode = os.getenv("AI_MODE", "local")
        if self.mode == "local":
            self.model = pipeline("sentiment-analysis", model="distilbert-base-uncased", framework="pt", device=-1)
        elif self.mode == "chatgpt":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.mode == "grok":
            self.api_key = os.getenv("XAI_API_KEY")
            if not self.api_key:
                raise ValueError("XAI_API_KEY required for Grok mode")
        elif self.mode == "gemini":
            self.api_key = os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError("GOOGLE_API_KEY required for Gemini mode")
        else:
            raise ValueError(f"Unsupported AI_MODE: {self.mode}")

    def get_response(self, query):
        if self.mode == "local":
            return self.model(query)[0]["label"]
        elif self.mode == "chatgpt":
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}]
            )
            return response.choices[0].message.content
        elif self.mode == "grok":
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",  # Placeholder URL, adjust if xAI updates
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": "grok", "messages": [{"role": "user", "content": query}]}
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        elif self.mode == "gemini":
            response = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                headers={"Content-Type": "application/json", "x-goog-api-key": self.api_key},
                json={"contents": [{"parts": [{"text": query}]}]}
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def init_chatbot():
    return Chatbot()