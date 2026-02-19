from embeddings import TfidfEmbedding
from vector_store import VectorStore
from llm_service import generate_medical_response
import re


# ===============================
# Initialize Global Models
# ===============================

embedding_model = TfidfEmbedding()
vector_store = VectorStore()
vector_store.set_embedding_model(embedding_model)


# ===============================
# Reset Function
# ===============================

def reset_documents():
    global embedding_model, vector_store
    embedding_model = TfidfEmbedding()
    vector_store = VectorStore()
    vector_store.set_embedding_model(embedding_model)


# ===============================
# Text Cleaning
# ===============================

def clean_text(text: str) -> str:
    text = text.lower()

    # Remove common report noise
    text = re.sub(r"registration no:.*", "", text)
    text = re.sub(r"page \d+ of \d+", "", text)
    text = re.sub(r"end of report.*", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ===============================
# Chunking
# ===============================

def chunk_text(text: str, chunk_size=600):
    text = clean_text(text)

    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if len(chunk) > 100:
            chunks.append(chunk)

    return chunks


# ===============================
# Ingest Document
# ===============================

def ingest_document(text: str):
    chunks = chunk_text(text)
    if chunks:
        vector_store.add_documents(chunks)


# ===============================
# Main Query Processing
# ===============================

def process_query(query: str):

    retrieved_chunks, confidence = vector_store.search(query, top_k=3)

    if not retrieved_chunks:
        return {
            "response": "The uploaded document does not contain enough information to answer this question.",
            "confidence_score": round(confidence, 3)
        }

    # Combine only top relevant chunks
    context = " ".join(retrieved_chunks)

    # ===============================
    # STRICT SUMMARY MODE
    # Only if EXACT phrase used
    # ===============================

    if query.strip().lower() == "summarize my report":

        llm_response = generate_medical_response(
            query="Provide a structured summary of the uploaded medical report.",
            context=context,
            mode="summary"
        )

        return {
            "response": llm_response,
            "confidence_score": round(confidence, 3)
        }

    # ===============================
    # STRICT QUESTION ANSWERING MODE
    # ===============================

    llm_response = generate_medical_response(
        query=query,
        context=context,
        mode="qa"
    )

    return {
        "response": llm_response,
        "confidence_score": round(confidence, 3)
    }
