# 🤖 LangGraph Chatbot

A conversational AI chatbot built with **LangGraph**, **LangChain**, and **Streamlit**, powered by **Groq's ultra-fast inference** (Llama 3.3 70B). Supports persistent multi-turn chat history with **SQLite**, multiple concurrent chat threads, real-time token streaming, and an animated UI.

![alt text](image.png)

---

## ✨ Features

- 🧠 **Persistent chat memory** — LangGraph `SqliteSaver` stores message history per thread in `chatbot.db`
- ⚡ **Real-time streaming** — tokens stream word-by-word via `chatbot.stream()`
- 💬 **Multiple chat threads** — create new conversations, switch between threads, and reload previous ones from SQLite
- 🎨 **Animated UI** — gradient title, fade-slide-in bubbles, bouncing typing indicator, floating empty-state, shimmer buttons
- 🔒 **Secure API key handling** — key loaded from `.env` via `python-dotenv`, never hard-coded

---

## 🗂️ Project Structure

```
chatbot/
├── langgraph_database_backend.py     # LangGraph + Groq backend with SqliteSaver
├── streamlit_frontend_database.py    # Main Streamlit app (threading + streaming + SQLite)
├── chatbot.db                        # SQLite database file created/updated at runtime
├── image.png                         # UI screenshot used in README
├── main.py                       # CLI entry point (placeholder)
├── requirements.txt              # Pip-installable dependencies
├── pyproject.toml                # Project metadata (uv / PEP 517)
├── .env                          # 🔑 API keys (not committed)
├── scripts/
│   ├── langgraph_backend.py            # In-memory backend variant
│   ├── streamlit_frontend.py           # Basic frontend variant
│   ├── streamlit_frontend_streaming.py # Streaming frontend variant
│   └── streamlit_frontend_threading.py # Threading frontend variant
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.12+**
- A free [Groq API key](https://console.groq.com/)

### 1. Clone the repository

```bash
git clone https://github.com/SahilGG-4545/chatbot.git
cd chatbot
```

### 2. Create and activate a virtual environment

```bash
# Using uv (recommended)
uv venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# Or using plain venv
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
# With uv
uv add -r requirements.txt

# Or with pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the app

```bash
streamlit run streamlit_frontend_database.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🏗️ Architecture

```
User
  |
  v
Streamlit App
  |
  v
LangGraph Flow  <---->  SQLite (chatbot.db)
  |
  v
Groq LLM (Llama 3.3 70B)
```

- Streamlit handles UI state (`thread_id`, visible messages, and conversation switching)
- LangGraph orchestrates prompts/responses and checkpoints thread state with `SqliteSaver`
- SQLite keeps conversations durable across app restarts, and the UI can reload historical threads

---

## 💾 Data Persistence

- Chat history is stored in a local SQLite database file: `chatbot.db` (project root)
- Each conversation is isolated by a unique `thread_id`
- Clicking **New Chat** creates a new thread and keeps previous threads available

### Reset Chat History Safely

1. Stop the Streamlit app if it is running
2. (Optional) Back up the database file: copy `chatbot.db` to another location
3. Delete `chatbot.db`
4. Run the app again: `streamlit run streamlit_frontend_database.py`

This will create a fresh empty database on startup.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | [Groq](https://groq.com/) — Llama 3.3 70B Versatile |
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM Abstraction | [LangChain](https://github.com/langchain-ai/langchain) |
| Persistence | SQLite (`langgraph-checkpoint-sqlite`) |
| Frontend | [Streamlit](https://streamlit.io/) |
| Env Management | [python-dotenv](https://github.com/theskumar/python-dotenv) |
| Packaging | [uv](https://github.com/astral-sh/uv) / pip |

---

## 📦 Dependencies

```
langgraph
langgraph-checkpoint-sqlite
langchain-core
langchain-openai
python-dotenv
streamlit
```

---

## 🔐 Security

- `.env` is listed in `.gitignore` — **never commit your API key**
- The Groq key is read at startup and never exposed to the frontend

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push and open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
