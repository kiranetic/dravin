from transformers import pipeline
import torch

def init_chatbot():
    print("PyTorch version:", torch.__version__)  # Debug
    return pipeline("sentiment-analysis", model="distilbert-base-uncased", framework="pt", device=-1)  # Force PyTorch, CPU-only

def get_response(chatbot, query):
    return chatbot(query)[0]["label"]  # e.g., "POSITIVE" or "NEGATIVE"