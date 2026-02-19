# Medical RAG Chatbot

> **RAG-powered medical document Q&A** — Upload PDFs or images, ask questions grounded in your documents. Built with Retrieval-Augmented Generation for accurate, context-aware medical insights with confidence scoring.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)

---

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [RAG Pipeline Flow](#rag-pipeline-flow)
- [Data Flow Diagram](#data-flow-diagram)
- [API Sequence](#api-sequence)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Environment Variables](#environment-variables)

---

## Features

- **PDF ingestion** — Extract text from medical PDFs via pdfplumber
- **Image OCR** — Process scanned reports/images with Tesseract
- **RAG-based Q&A** — Retrieval-Augmented Generation for grounded answers
- **TF-IDF retrieval** — Fast semantic search with keyword boosting
- **Gemini LLM** — Google Gemini for response generation
- **Confidence scoring** — Similarity-based confidence for every answer
- **Summary mode** — "Summarize my report" for structured summaries

---

## System Architecture

```mermaid
flowchart TB
    subgraph Frontend["Frontend (React + Vite)"]
        UI[React UI]
        API_CLIENT[Axios API Client]
        UI --> API_CLIENT
    end

    subgraph Backend["Backend (FastAPI)"]
        API[FastAPI REST API]
        RAG[RAG Pipeline]
        API --> RAG
    end

    subgraph RAG_Pipeline["RAG Pipeline"]
        PARSER[PDF Parser / OCR]
        CHUNK[Text Chunking]
        EMB[TF-IDF Embeddings]
        VS[Vector Store]
        LLM[Gemini LLM]
        PARSER --> CHUNK --> EMB --> VS
        VS --> EMB
        EMB --> LLM
    end

    subgraph External["External Services"]
        GEMINI[(Google Gemini API)]
        LLM --> GEMINI
    end

    API_CLIENT -->|HTTP| API
    API --> PARSER
    RAG --> API
```

---

## RAG Pipeline Flow

```mermaid
flowchart LR
    subgraph Ingest["Document Ingestion"]
        A1[Upload PDF/Image]
        A2[Extract Text]
        A3[Clean & Chunk]
        A4[TF-IDF Fit]
        A5[Store Vectors]
        A1 --> A2 --> A3 --> A4 --> A5
    end

    subgraph Query["Query Processing"]
        B1[User Question]
        B2[Embed Query]
        B3[Cosine Similarity]
        B4[Top-K Retrieval]
        B5[Build Context]
        B6[LLM Generate]
        B1 --> B2 --> B3 --> B4 --> B5 --> B6
    end

    A5 -.->|Vector Store| B3
    B6 --> B7[Response + Confidence]
```

---

## Data Flow Diagram

```mermaid
flowchart TD
    USER([User])
    UI[Frontend UI]

    subgraph Backend["Backend"]
        UP_PDF[upload_pdf]
        UP_IMG[upload_image]
        ASK[ask]
        RESET[reset]
    end

    subgraph Storage["In-Memory Storage"]
        VS[Vector Store]
        DOCS[Document Chunks]
        TFIDF[TF-IDF Matrix]
        VS --> DOCS
        VS --> TFIDF
    end

    subgraph Processing["Processing"]
        PDF_PARSE[pdfplumber]
        OCR[Tesseract OCR]
        EMB[Embeddings]
        RETRIEVE[Retrieve Top-K]
        GEN[Gemini Generate]
    end

    USER -->|Upload| UI
    UI -->|POST| UP_PDF
    UI -->|POST| UP_IMG
    UI -->|POST| ASK
    UI -->|POST| RESET

    UP_PDF --> PDF_PARSE --> EMB --> VS
    UP_IMG --> OCR --> EMB --> VS
    RESET --> VS

    ASK --> EMB --> RETRIEVE --> VS
    RETRIEVE --> GEN
    GEN -->|JSON| UI --> USER
```

---

## Component Interaction

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        BROWSER[Browser]
    end

    subgraph API_Layer["API Layer"]
        CORS[CORS Middleware]
        ROUTES[FastAPI Routes]
        CORS --> ROUTES
    end

    subgraph Core["Core Services"]
        PDF[pdf_parser]
        OCR_MOD[ocr]
        RAG[rag_pipeline]
        EMB_MOD[embeddings]
        VS_MOD[vector_store]
        LLM_MOD[llm_service]
    end

    subgraph Data["Data Layer"]
        FILES[(data/uploads)]
        VECTOR[(In-Memory Vectors)]
    end

    BROWSER --> CORS
    ROUTES --> PDF
    ROUTES --> OCR_MOD
    ROUTES --> RAG
    PDF --> FILES
    OCR_MOD --> FILES
    RAG --> EMB_MOD
    RAG --> VS_MOD
    RAG --> LLM_MOD
    EMB_MOD --> VS_MOD
    VS_MOD --> VECTOR
```

---

## API Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant API as FastAPI
    participant RAG as RAG Pipeline
    participant VS as Vector Store
    participant LLM as Gemini

    Note over U,LLM: Document Upload Flow
    U->>F: Upload PDF/Image
    F->>API: POST /upload_pdf or /upload_image
    API->>RAG: ingest_document(text)
    RAG->>RAG: clean & chunk
    RAG->>VS: add_documents(chunks)
    VS->>API: OK
    API->>F: {message, characters_extracted}
    F->>U: Show success

    Note over U,LLM: Query Flow
    U->>F: Ask question
    F->>API: POST /ask (query)
    API->>RAG: process_query(query)
    RAG->>VS: search(query, top_k=3)
    VS->>RAG: chunks, confidence
    RAG->>LLM: generate_medical_response(query, context)
    LLM->>RAG: response
    RAG->>API: {response, confidence_score}
    API->>F: JSON
    F->>U: Display answer + confidence
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19, Vite 7, Tailwind CSS, Framer Motion, Lucide React, Axios |
| **Backend** | FastAPI, Uvicorn |
| **Embeddings** | scikit-learn TF-IDF |
| **Vector Store** | In-memory, cosine similarity |
| **LLM** | Google Gemini (`gemini-3-flash-preview`) |
| **PDF** | pdfplumber |
| **OCR** | Tesseract, Pillow |

---

## Project Structure

```
medical-rag-chatbot/
├── backend/
│   ├── main.py           # FastAPI app & REST endpoints
│   ├── rag_pipeline.py   # RAG orchestration (ingest, query)
│   ├── embeddings.py     # TF-IDF embeddings
│   ├── vector_store.py   # In-memory vector store
│   ├── llm_service.py    # Gemini LLM integration
│   ├── pdf_parser.py     # PDF text extraction
│   ├── ocr.py            # Image OCR (Tesseract)
│   ├── requirements.txt
│   ├── .env              # GEMINI_API_KEY (gitignored)
│   └── data/uploads/     # Uploaded files
└── frontend/
    ├── src/
    │   ├── App.jsx       # Main UI
    │   ├── api.js        # Backend API client
    │   └── components/
    ├── package.json
    └── vite.config.js
```

---

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (for image uploads)
- Google Gemini API key

### Backend

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

---

## Usage

### 1. Set environment variables

Create `backend/.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

### 2. Run backend

```bash
cd backend
.\venv\Scripts\activate   # Windows
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Run frontend

```bash
cd frontend
npm run dev
```

### 4. Open the app

- Frontend: http://localhost:5173
- API docs: http://127.0.0.1:8000/docs

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload_pdf` | Upload PDF, extract text, ingest into RAG |
| `POST` | `/upload_image` | Upload image, OCR, ingest |
| `POST` | `/ask` | Ask a question (form: `query`) |
| `POST` | `/reset` | Clear vector store and reset documents |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key for LLM |

---

## License

MIT
