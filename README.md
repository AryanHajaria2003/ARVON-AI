
# ARVON AI — Freshworks RAG Chatbot

img="<img width="618" height="143" alt="image" src="https://github.com/user-attachments/assets/613e245c-1ad3-4320-935e-c8477743189d" />"

ARVON AI is a Retrieval-Augmented Generation (RAG) chatbot designed to answer questions using Freshworks documents.

## Features

- Multi-format document ingestion
- Text cleaning and semantic chunking
- BGE embeddings: `BAAI/bge-base-en-v1.5`
- ChromaDB vector search
- BM25 keyword retrieval
- Reciprocal Rank Fusion (RRF)
- Groq API with GPT-OSS 120B for answer generation
- Streamlit chatbot interface
- Retrieval and generation evaluation scripts

## Architecture

Documents → Cleaning → Semantic Chunking → Embeddings → ChromaDB + BM25 → RRF → Top 5 Chunks → Groq LLM → Answer

## Tech Stack

Python, Streamlit, LangChain, ChromaDB, Sentence Transformers, BM25, Groq API.

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Configure the Groq API key using Streamlit secrets.
5. Prepare the Freshworks document corpus and vector database.
6. Run the application using `streamlit run app.py`.

## API Key Configuration

Create `.streamlit/secrets.toml` locally:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

Never commit API keys or secret configuration files.

## Evaluation

Run the retrieval evaluation:

```bash
python retrieval_evaluation.py
```

Run the generation evaluation:

```bash
python evaluation.py
```

## Limitations

- Answers depend on the relevance and coverage of retrieved documents.
- Keyword-based generation tests do not establish factual accuracy.
- The vector database and source documents must be made available separately for deployment.
