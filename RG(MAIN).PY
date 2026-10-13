import os
import re

from langchain_community.document_loaders import (
    PyPDFLoader,
    BSHTMLLoader,
    UnstructuredWordDocumentLoader
)

from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever


folder ="DATA2"
docs = []

for file in os.listdir(folder):

    path = os.path.join(folder, file)

    try:

        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)

        elif file.endswith(".html"):
            try:
                loader = BSHTMLLoader(path, open_encoding="utf-8")
                docs.extend(loader.load())
                continue
            except UnicodeDecodeError:
                loader = BSHTMLLoader(path, open_encoding="cp1252")

        elif file.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(path)

        else:
            continue

        docs.extend(loader.load())

    except Exception as e:
        print("Skipped:", file)
        print("Error:", e)


print("Files found:", len(os.listdir(folder)))
print("Documents loaded:", len(docs))


for doc in docs:

    doc.page_content = re.sub(
        r"\s+",
        " ",
        doc.page_content
    ).strip()

    doc.metadata["company"] = "Freshworks"

    doc.metadata["file_type"] = os.path.splitext(
        doc.metadata["source"]
    )[1].replace(".", "")


print("Cleaning and metadata completed.")


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)


def semantic_chunk_documents(docs):

    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile"
    )

    return splitter.split_documents(docs)


chunks = semantic_chunk_documents(docs)

print("Documents:", len(docs))
print("Chunks:", len(chunks))


vector_db = Chroma(
    collection_name="freshworks",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

vector_db.add_documents(chunks)

print("Chunks stored in ChromaDB:", len(chunks))

query = "What was Freshworks' Q2 2026 revenue?"

results = vector_db.similarity_search(query, k=3)

for i, doc in enumerate(results, 1):
    print(f"\n--- RESULT {i} ---")
    print("Source:", doc.metadata.get("source"))
    print("Page:", doc.metadata.get("page"))
    print(doc.page_content[:1000])
    
print("Chunks stored in ChromaDB:", len(chunks))
import pickle

with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Chunks saved to chunks.pkl")
