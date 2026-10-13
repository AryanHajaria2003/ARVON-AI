
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

db = Chroma(
    collection_name="freshworks",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

print("Collection count:", db._collection.count())

results = db.similarity_search(
    "Freshworks Q2 2026 revenue",
    k=3
)

for i, doc in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(doc.page_content[:250])
