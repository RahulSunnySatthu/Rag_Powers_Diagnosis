from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os

from pdf_parser import extract_pdf_text
from ocr import extract_image_text
from rag_pipeline import ingest_document, process_query, reset_documents


# =====================================================
# Initialize FastAPI App
# =====================================================

app = FastAPI(title="Medical RAG Chatbot")


# =====================================================
# CORS Configuration (Frontend Support)
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Upload Directory
# =====================================================

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =====================================================
# Upload PDF Endpoint
# =====================================================

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_pdf_text(file_path)

        # Ingest into vector store
        ingest_document(text)

        return JSONResponse(content={
            "message": "PDF processed successfully",
            "characters_extracted": len(text)
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# =====================================================
# Upload Image Endpoint (OCR)
# =====================================================

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_image_text(file_path)

        # Ingest into vector store
        ingest_document(text)

        return JSONResponse(content={
            "message": "Image processed successfully",
            "characters_extracted": len(text)
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# =====================================================
# Ask Question Endpoint
# =====================================================

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    try:
        result = process_query(query)

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# =====================================================
# Reset Document Memory Endpoint
# =====================================================

@app.post("/reset")
def reset():
    reset_documents()
    return {"message": "Document memory cleared successfully."}


# =====================================================
# Health Check Endpoint
# =====================================================

@app.get("/")
def root():
    return {"message": "Medical RAG Chatbot is running"}
