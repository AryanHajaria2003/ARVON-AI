
import os

import streamlit as st
from groq import Groq

from retrieval import hybrid_search


def generate_answer(question):

    # Retrieve relevant documents
    results = hybrid_search(question, k=5)

    # Build context
    context = "\n\n".join(
        doc.page_content for doc in results
    )

    # Read API key from Streamlit secrets
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Configure it in "
            ".streamlit/secrets.toml."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
       model="openai/gpt-oss-120b", 
        messages=[
            {
                "role": "system",
                "content": """
You are a Freshworks RAG assistant.

Answer only using the supplied context.
Do not invent facts or use outside knowledge.
For actual financial results, prefer reported figures
over forecasts or future guidance.
If the answer is missing, say:
"I don't know based on the provided documents."
Keep answers concise.
"""
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}

Answer in 1-3 sentences.
"""
            }
        ],
        temperature=0.1,
        max_tokens=300
    )

    answer = response.choices[0].message.content

    return answer, results
