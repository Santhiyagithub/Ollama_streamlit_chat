# Ollama_streamlit_chat
A streamlit web app that lets us chat with ollama LLM (like llama3.1:8b) running locally

---

## ⚡ Requirements
- Python 3.9+
- [Ollama](https://ollama.ai) installed on your system
- Streamlit installed

---

## 🚀 Setup

1. **Clone this repo**
   ```bash
   git clone https://github.com/Santhiyagithub/Ollama_streamlit_chat.git
   cd Ollama_streamlit_chat
   ```

2. **Creating a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```
3.**Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```
4.**pull an ollama model**
  ```bash
  ollama pull llama3.1:8b
  ```

5.**Run the ollama server**
  ```bash
  ollama run llama3.1:8b
  ```

6.**Run the streamlit app**
  ```bash
  streamlit run app.py
  ```
---

## Usage

- Type your message in the text box.
- Get a response from the local Ollama model.
- Example models you can use:
   llama3.1:8b
   llama2:7b
   mistral
