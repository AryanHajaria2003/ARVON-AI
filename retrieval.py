
import pickle
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever


# Use paths relative to this Python file
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"
CHUNKS_FILE = BASE_DIR / "chunks.pkl"


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

vector_db = Chroma(
    collection_name="freshworks",
    embedding_function=embeddings,
    persist_directory=str(DB_DIR)
)

with open(CHUNKS_FILE, "rb") as f:
    chunks = pickle.load(f)

bm25 = BM25Retriever.from_documents(chunks)
bm25.k = 20


def hybrid_search(query, k=10):

    chroma_results = vector_db.similarity_search(query, k=10)
    bm25_results = bm25.invoke(query)

    scores = {}
    documents = {}

    for rank, doc in enumerate(chroma_results, 1):
        key = (
            doc.metadata.get("source", "")
            + str(doc.metadata.get("page", ""))
            + doc.page_content
        )

        scores[key] = scores.get(key, 0) + 1 / (60 + rank)
        documents[key] = doc

    for rank, doc in enumerate(bm25_results, 1):
        key = (
            doc.metadata.get("source", "")
            + str(doc.metadata.get("page", ""))
            + doc.page_content
        )

        scores[key] = scores.get(key, 0) + 1 / (60 + rank)
        documents[key] = doc

    ranked = sorted(scores, key=scores.get, reverse=True)

    return [documents[key] for key in ranked[:k]]


if __name__ == "__main__":

    print("Database:", DB_DIR)
    print("Chunks file:", CHUNKS_FILE)
    print("Chroma collection count:", vector_db._collection.count())

    results = hybrid_search(
        "What was Freshworks' Q2 2026 revenue?",
        k=5
    )

    for i, doc in enumerate(results, 1):
        print(f"\n--- RESULT {i} ---")
        print("Source:", doc.metadata.get("source"))
        print("Page:", doc.metadata.get("page"))
        print(doc.page_content[:500])
