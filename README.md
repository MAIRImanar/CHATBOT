# 🤖 E16 Banking Chatbot

<p align="center">
  <b>An intelligent bilingual chatbot (FR/AR) that answers banking questions using your own PDF documents, powered by Google Gemini AI and RAG (Retrieval-Augmented Generation).</b>
</p>

<p align="center">
  🌐 <a href="https://chatbot-fp5h.onrender.com/">Live Demo</a>
</p>


## 🌟 Overview

**E16 Bot** is a smart conversational assistant designed for banking use cases. It reads and understands two banking PDF documents (in French and Arabic), stores their content in a FAISS vector database, and answers user questions with highly accurate, context-aware responses using Google's Gemini Pro model.

If the answer cannot be found in the documents, the bot falls back to Gemini Pro's general knowledge to still provide a useful response.

---

## ✨ Features

| Feature | Description |
|---|---|
|  **RAG Pipeline** | Retrieval-Augmented Generation for accurate, document-grounded answers |
|  **Bilingual Support** | Works with both French (`Banque_FR.pdf`) and Arabic (`Banque_AR.pdf`) documents |
|  **Chat History** | Maintains conversation context across multiple turns |
|  **Smart Fallback** | Falls back to Gemini Pro general knowledge when context is unavailable |
|  **PDF Parsing** | Automatically extracts and indexes PDF content at startup |
|  **Docker Ready** | Fully containerized for easy deployment |
|  **Cloud Deployed** | Live on Render.com |

---

##  Architecture
```
            User Query
               │
               ▼
┌─────────────────────────────────┐
│         Streamlit UI            │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│    FAISS Vector Store Search    │◄── GoogleGenerativeAI Embeddings
│    (Similarity Search, top-k)   │
└──────────────┬──────────────────┘
               │  Relevant Chunks
               ▼
┌─────────────────────────────────┐
│    LangChain QA Chain           │
│    (Gemini Pro + Prompt)        │
└──────────────┬──────────────────┘
               │  Answer found?
        ┌──────┴──────┐
        │ YES         │ NO
        ▼             ▼
   Return Answer   Gemini Pro
   from Context    Fallback
```

---

##  Tech Stack

- **[Streamlit](https://streamlit.io/)** — Web UI framework
- **[Google Gemini Pro](https://deepmind.google/technologies/gemini/)** — LLM for response generation
- **[LangChain](https://www.langchain.com/)** — LLM orchestration framework
- **[FAISS](https://github.com/facebookresearch/faiss)** — Vector similarity search
- **[PyPDF2](https://pypdf2.readthedocs.io/)** — PDF text extraction
- **[Docker](https://www.docker.com/)** — Containerization
- **[Render](https://render.com/)** — Cloud deployment

---

##  Getting Started

### Prerequisites

- Python 3.9+
- A [Google AI Studio](https://aistudio.google.com/) API key

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/MAIRImanar/chatbot.git
cd chatbot

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 5. Run the application
streamlit run app.py
```

The app will be available at `http://localhost:8501`

---

##  Environment Variables

Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_generative_ai_api_key_here
```

>  Never commit your `.env` file. It is already listed in `.gitignore`.

---

##  Docker Deployment

### Using Docker
```bash
# Build the image
docker build -t e16-chatbot .

# Run the container
docker run -p 8501:8501 --env-file .env e16-chatbot
```

### Using Docker Compose
```bash
docker-compose up --build
```

---

## 📁 Project Structure
```
chatbot/
├── app.py                  # Main Streamlit application
├── Banque_FR.pdf           # French banking knowledge base
├── Banque_AR.pdf           # Arabic banking knowledge base
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── compose.yaml            # Docker Compose configuration
├── render.yaml             # Render.com deployment config
├── .env                    # Environment variables (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

1. **Startup** — The app loads `Banque_FR.pdf` and `Banque_AR.pdf`, extracts all text, splits it into overlapping chunks (10,000 chars, 1,000 overlap), and stores them in a FAISS vector index.

2. **Query** — When the user asks a question, it is embedded using `GoogleGenerativeAIEmbeddings` and the most relevant document chunks are retrieved via similarity search.

3. **Answer** — The retrieved chunks + the user question are passed to a `ChatGoogleGenerativeAI` chain (Gemini Pro). If the answer is found in context, it is returned. If not, a direct Gemini Pro call is made as a fallback.

4. **Chat UI** — All messages are stored in `st.session_state` to maintain a persistent conversation history within the session.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👥 Team — Groupe E16

| # | Nom | Prénom | Groupe | GitHub |
|---|-----|--------|--------|--------|
| 1 | MAIRI | Manar | G3 | [@MAIRImanar](https://github.com/MAIRImanar) |
| 2 | MAIRI | Rahma | G4 | [@rahma203](https://github.com/rahma203) |

---

<p align="center">Made with ❤️ by the <strong>E16</strong> team</p>
