# DocMind — Conversational RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with LangChain that supports conversational memory for follow-up questions. Features a FastAPI backend and Streamlit frontend with document upload capabilities.

---

## 🚀 Features

- **Document Upload**: Supports PDF, DOCX, HTML files
- **Conversational Memory**: Maintains context for follow-up questions
- **Free LLM Models**: Powered by OpenRouter — no paid API key needed
- **Local Embeddings**: HuggingFace `all-MiniLM-L6-v2` runs fully offline
- **Vector Storage**: Efficient document retrieval with ChromaDB
- **Interactive API**: FastAPI backend with Swagger documentation
- **LangSmith Integration**: Built-in tracing and monitoring (optional)

---

## ⚙️ Configuration

Create a `.env` file in the root with the following variables:

```env
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="rag-chatbot"
```

Get a free OpenRouter API key at [openrouter.ai/keys](https://openrouter.ai/keys).

---

## 📦 Project Structure

```
DocMind/
├── api/                         # FastAPI backend server
│   ├── chroma_db/               # ChromaDB vector storage
│   ├── app.log                  # Logging file
│   ├── chroma_utils.py          # ChromaDB & embedding utilities
│   ├── db_utils.py              # Chat history & metadata DB logic
│   ├── langchain_utils.py       # LangChain RAG pipeline (LCEL)
│   ├── main.py                  # FastAPI entry point
│   ├── pydantic_models.py       # Request/response validation
│   └── rag_app.db               # SQLite DB
├── app/                         # Streamlit frontend
│   ├── api_utils.py             # FastAPI client utils
│   ├── chat_interface.py        # Chat UI
│   ├── sidebar.py               # File upload & model switch
│   └── streamlit_app.py         # Streamlit entry point
├── docs/                        # Sample documents
├── documentation/               # Guides & screenshots
├── .env.example                 # Environment variable template
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ⚡ Quick Start

### 🔧 Prerequisites

* Python 3.9+
* OpenRouter API Key (free — [openrouter.ai/keys](https://openrouter.ai/keys))

### 🛠 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR-USERNAME/docmind.git
   cd docmind
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

4. **Run the FastAPI backend**

   ```bash
   cd api
   uvicorn main:app --reload --port 8000
   ```

5. **Run the Streamlit frontend**

   In a new terminal:

   ```bash
   cd app
   streamlit run streamlit_app.py --server.port 8500
   ```

6. **Access the application**

   * Streamlit UI: [http://localhost:8500](http://localhost:8500)
   * Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🤖 Supported Models

All models are **free** via OpenRouter:

| Model | Provider |
|---|---|
| `nvidia/nemotron-3-ultra-550b-a55b:free` | NVIDIA (default) |
| `google/gemini-2.0-flash-exp:free` | Google |
| `meta-llama/llama-3.2-3b-instruct:free` | Meta |
| `mistralai/mistral-7b-instruct:free` | Mistral AI |

Switch models anytime from the sidebar dropdown.

---

## 📚 Usage Guide

### 📤 Upload Documents

1. Open the Streamlit UI
2. Use the sidebar to upload PDF, DOCX, or HTML files
3. Uploaded docs are chunked and indexed into ChromaDB

### 💬 Chat with Documents

1. Ask a question related to the uploaded content
2. Ask follow-up questions — context is remembered per session
3. Switch models via the sidebar dropdown

---

## 🧪 API Usage Example (Python)

```python
import requests

# Upload a document
files = {'file': open('document.pdf', 'rb')}
upload_res = requests.post('http://localhost:8000/upload-doc', files=files)

# Chat with the document
chat_payload = {
    "question": "What is this document about?",
    "session_id": "user123"
}
chat_res = requests.post('http://localhost:8000/chat', json=chat_payload)
print(chat_res.json())
```

---

## 🔌 API Endpoints

| Endpoint      | Method | Description                  |
| ------------- | ------ | ---------------------------- |
| `/chat`       | POST   | Chat with uploaded documents |
| `/upload-doc` | POST   | Upload and index a document  |
| `/list-docs`  | GET    | List all uploaded documents  |
| `/delete-doc` | POST   | Delete a specific document   |

---

## 🧠 Architecture Overview

1. **Document Ingestion**: Files are split into 1000-character chunks (200 overlap)
2. **Embedding**: Text is embedded locally using HuggingFace `all-MiniLM-L6-v2`
3. **Storage**: Embeddings are persisted in ChromaDB
4. **Retrieval**: Top-2 relevant chunks are fetched per query
5. **Generation**: LangChain LCEL pipeline passes context + history to the LLM via OpenRouter
6. **Memory**: Session IDs stored in SQLite preserve conversation history across requests

---

## 🔑 Required API Keys

* **OPENROUTER\_API\_KEY**: Required for LLM completions (free tier available)
* **LANGCHAIN\_API\_KEY**: Optional — for LangSmith tracing and monitoring

---

## 🖼 Screenshots

Screenshots are located in:

```
documentation/screenshots/
```

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create a feature branch
3. Make your changes and commit
4. Open a pull request

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

* Built with [LangChain](https://www.langchain.com/)
* LLM routing by [OpenRouter](https://openrouter.ai/)
* Embeddings by [HuggingFace](https://huggingface.co/)
* Vector storage by [ChromaDB](https://www.trychroma.com/)
* UI by [Streamlit](https://streamlit.io/)
* Backend by [FastAPI](https://fastapi.tiangolo.com/)
* Observability via [LangSmith](https://smith.langchain.com/)
