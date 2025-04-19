import time
import json
import requests
import streamlit as st


README_FILE = "README.md"
JSON_FILE = "jsonl"
CHAT_ENDPOINT = "http://localhost:8000/chat"


# -------- Initialization --------
def init_state():
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "reply" not in st.session_state:
        st.session_state.reply = ""
    if "message_sent" not in st.session_state:
        st.session_state.message_sent = False


# -------- Chat Handling --------
def on_send():
    query = st.session_state.chat_input.strip()
    if not query:
        return

    with st.spinner("Dravin is thinking..."):
        try:
            response = requests.post("http://localhost:8000/chat", json={"message": query})
            reply = response.json().get("reply", "Error: No reply received.")
        except Exception as e:
            reply = f"❌ Error: {e}"

    # Save to history and clear input
    st.session_state.history.append({"user": query, "dravin": reply})
    st.session_state.reply = reply
    st.session_state.chat_input = ""
    st.session_state.message_sent = True


# -------- UI Sections --------
def render_home_tab():
    left_col, right_col = st.columns([2, 2])

    with left_col:
        with st.container(border=True):
            st.header("💬 Chat with Dravin")
            st.text_area("Your message", key="chat_input", placeholder="Ask me anything...")
            st.button("Send", on_click=on_send)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.session_state.message_sent and st.session_state.reply:
                st.markdown("**🤖 Dravin says:**")
                st.write(st.session_state.reply)
                st.session_state.message_sent = False  # Reset so reply doesn’t show again
        
            st.markdown("<br>", unsafe_allow_html=True)

    with right_col:
        st.header("📜 Chat History")
        if st.session_state.history:
            for chat in reversed(st.session_state.history):
                st.markdown(f"**You:** {chat['user']}")
                st.markdown(f"**🤖 Dravin:** {chat['dravin']}")
                st.markdown("---")
        else:
            st.info("Start chatting to see the conversation here.")


def render_logs_tab():
    st.header("📊 JSONL Log Viewer")
    try:
        with open(JSON_FILE, "r") as f:
            data = [json.loads(line) for line in f if line.strip()]
        data.reverse()
        st.dataframe(data, use_container_width=True)
    except FileNotFoundError:
        st.error("data.jsonl file not found.")
    except json.JSONDecodeError:
        st.error("Invalid line found in data.jsonl.")


def render_readme_tab():
    st.header("📄 Project README")
    try:
        with open(README_FILE, "r") as f:
            readme = f.read()
        st.markdown(readme)
    except FileNotFoundError:
        st.warning("README.md not found.")


# -------- Main --------
def main():
    st.set_page_config(page_title="Dravin - An AI-driven dialogue engine", layout="wide", page_icon=":robot:")
    st.title("🤖 Dravin - Chatbot UI")
    st.write("AI-powered customer support chatbot")

    init_state()

    tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Logs", "📄 README"])

    with tab1:
        render_home_tab()
    with tab2:
        render_logs_tab()
    with tab3:
        render_readme_tab()



# -------- Run --------
if __name__ == "__main__":
    main()

