import streamlit as st
import requests

# Constants
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

# Streamlit Page Config
st.set_page_config(page_title="Ollama Chatbot", layout="wide")

# Sidebar for settings
st.sidebar.title("⚙️ Model Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 50, 1000, 300, 50)

# Title
st.title("💬 Chat with Ollama (LLaMA 3.1 - 8B)")
st.write("This chatbot runs locally using **Ollama**. Type below to chat!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role = "🧑 You" if message["role"] == "user" else "🤖 AI"
    with st.chat_message(message["role"]):
        st.markdown(f"**{role}:** {message['content']}")

# Input field
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"**🧑 You:** {user_input}")

    # Call Ollama API
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": user_input,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            stream=True
        )

        # Collect response
        result = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                if '"response":"' in data:
                    text_piece = data.split('"response":"')[-1].split('"')[0]
                    result += text_piece

        # Append AI response to history
        st.session_state.messages.append({"role": "assistant", "content": result})

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(f"**🤖 AI:** {result}")

    except Exception as e:
        st.error(f"Error: {e}")
