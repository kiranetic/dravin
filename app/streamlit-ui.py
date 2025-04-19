import requests
import streamlit as st

DRAVIN_API = "http://localhost:8000/chat"

st.set_page_config(page_title="Dravin - An AI-driven dialogue engine", layout="centered")

st.title("🤖 Dravin - Chatbot UI")

st.write("AI-powered customer support chatbot")

query = st.text_area("Your message", placeholder="Ask me anything...")

if st.button("Send") and query.strip():
    with st.spinner("Thinking..."):
        try:
            response = requests.post(DRAVIN_API, json={"message": query})
            reply = response.json().get("reply", "Error: No reply received.")
        except Exception as e:
            reply = f"❌ Error: {e}"

    st.markdown("**Dravin says:**")
    st.write(reply)
