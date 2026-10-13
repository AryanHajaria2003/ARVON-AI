import pickle

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

vector_db = Chroma(
    collection_name="freshworks",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


bm25 = BM25Retriever.from_documents(chunks)
bm25.k = 5


def hybrid_search(query, k=5):

    chroma_results = vector_db.similarity_search(query, k=5)
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

    ranked = sorted(
        scores,
        key=scores.get,
        reverse=True
    )

    return [
        (documents[key], scores[key])
        for key in ranked[:k]
    ]


query = "What was Freshworks' Q2 2026 revenue?"

results = hybrid_search(query)

print("\n===== HYBRID RRF RESULTS =====")

for i, (doc, score) in enumerate(results, 1):

    print(f"\n--- RESULT {i} ---")
    print("Source:", doc.metadata.get("source"))
    print("Page:", doc.metadata.get("page"))
    print("RRF Score:", round(score, 6))
    print(doc.page_content[:1000])