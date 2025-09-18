import streamlit as st
import requests
import fitz  # PyMuPDF
import json

# -------------------- CONFIG --------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"  # ✅ light model that fits low-RAM systems

# -------------------- FUNCTIONS --------------------
def query_ollama(prompt, temperature=0.7, max_tokens=300):
    """Send a prompt to Ollama API and return the response."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            stream=True,
            timeout=120,
        )

        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        result += data["response"]
                except Exception:
                    continue
        return result.strip() if result else "⚠️ No response received from model."
    except Exception as e:
        return f"❌ Error connecting to Ollama: {e}"

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file safely."""
    try:
        file_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            text += pdf_document[page_num].get_text()
        return text.strip()
    except Exception as e:
        return f"❌ Could not read PDF: {e}"

# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="Ollama Chatbot", layout="wide")
st.title("💬 Local AI Chatbot (Ollama + Streamlit)")
st.caption("⚡ Powered by LLaMA running locally via Ollama")

# Sidebar: Settings & Upload
st.sidebar.header("⚙️ Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 50, 1000, 300, 50)

st.sidebar.header("📂 Knowledge Source")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
pdf_context = ""
if uploaded_file:
    pdf_context = extract_text_from_pdf(uploaded_file)
    if pdf_context.startswith("❌"):
        st.sidebar.error(pdf_context)
    else:
        st.sidebar.success("✅ PDF Loaded")

# Sidebar: Chat Controls
if st.sidebar.button("🆕 New Chat"):
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- CHAT UI --------------------
for message in st.session_state.messages:
    role = "🧑 You" if message["role"] == "user" else "🤖 AI"
    with st.chat_message(message["role"]):
        st.markdown(f"**{role}:** {message['content']}")

# User Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"**🧑 You:** {user_input}")

    # Combine with PDF context if available
    final_prompt = user_input
    if pdf_context and not pdf_context.startswith("❌"):
        final_prompt = f"Use the following document to answer:\n\n{pdf_context}\n\nQuestion: {user_input}"

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            ai_response = query_ollama(final_prompt, temperature, max_tokens)
            st.markdown(f"**🤖 AI:** {ai_response}")

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
