from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL


prompt = "You are an AI customer support assistant. Answer user questions in a helpful, polite, and concise way. If you don't know the answer, say so honestly."

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def gpt_fallback_response(user_input: str) -> str:
    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=prompt,
            input=user_input,
        )

        return response.output_text.strip()

    except Exception as e:
        print("❌ GPT fallback failed:", str(e))
        return "Sorry, I'm having trouble understanding that right now."
