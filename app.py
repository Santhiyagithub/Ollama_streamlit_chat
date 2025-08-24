import streamlit as st
import requests
import json

# --------------------------
# Streamlit Page Settings
# --------------------------
st.set_page_config(page_title="💬 Ollama Chat", layout="wide")
st.title("💬 Chat with Ollama LLM")

# --------------------------
# Sidebar Settings
# --------------------------
st.sidebar.header("⚙️ Settings")
model = st.sidebar.text_input("Model Name:", value="llama3.1:8b")
temperature = st.sidebar.slider("Temperature:", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens:", 50, 500, 200)

# --------------------------
# Session State (History)
# --------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --------------------------
# Chat Input
# --------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Send request to Ollama API
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": user_input,
            "options": {"temperature": temperature},
            "max_tokens": max_tokens
        },
        stream=True
    )

    # Collect response
    result = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                result += data["response"]

    # Save bot response
    st.session_state["messages"].append({"role": "assistant", "content": result})

# --------------------------
# Chat Display (UI Layout)
# --------------------------
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Ollama:** {msg['content']}")
