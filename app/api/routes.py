from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.loader import load_document
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import dynamic_chunk
from app.embeddings.embedder import embed_chunks
from app.storage.vector_store import vector_store
from app.storage.document_registry import document_registry
from app.retrieval.retriever import retrieve_context
from app.generation.generator import generate_answer
from app.api.schemas import QueryRequest, QueryResponse
from app.security.privacy import ephemeral_file
from app.observability.logger import (
    log_query,
    log_ingestion,
    log_error,
)

router = APIRouter()

# =========================================================
# Document Ingestion (Multi-file, Privacy-safe)
# =========================================================
@router.post("/ingest")
async def ingest_documents(files: List[UploadFile] = File(...)):
    processed_files = 0
    total_chunks = 0

    try:
        for file in files:
            if not file.filename:
                continue

            with ephemeral_file(file) as path:
                raw_text = load_document(path)
                cleaned_text = clean_text(raw_text)

                if not cleaned_text:
                    continue

                chunks = dynamic_chunk(cleaned_text)
                if not chunks:
                    continue

                embeddings = embed_chunks(chunks)

                vector_store.add(
                    chunks=chunks,
                    embeddings=embeddings,
                    source=file.filename
                )

                # Register document for UI sidebar
                document_registry.add(file.filename)

                processed_files += 1
                total_chunks += len(chunks)

                log_ingestion(file.filename, len(chunks))

        if processed_files == 0:
            return {
                "status": "no_valid_documents",
                "message": "No readable documents found"
            }

        return {
            "status": "success",
            "files_processed": processed_files,
            "chunks_created": total_chunks
        }

    except Exception as e:
        log_error(e)
        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed"
        )


# =========================================================
# Knowledge Query (ALL docs or SELECTED doc)
# =========================================================
@router.post("/query", response_model=QueryResponse)
async def query_knowledge(req: QueryRequest):
    try:
        question = req.question.strip()
        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        log_query(question)

        # source=None  -> search ALL documents
        # source=doc   -> search ONLY that document
        context = retrieve_context(
            question=question,
            source=req.source
        )

        if not context or not context.get("documents"):
            return {
                "answer": "The provided documents do not contain enough information to answer this question.",
                "sources": []
            }

        answer, sources = generate_answer(
            question=question,
            context=context
        )

        return {
            "answer": answer,
            "sources": sources
        }

    except HTTPException:
        raise

    except Exception as e:
        log_error(e)
        raise HTTPException(
            status_code=500,
            detail="Query processing failed"
        )


# =========================================================
# Document List (Sidebar)
# =========================================================
@router.get("/documents")
async def list_documents():
    return {
        "documents": document_registry.list()
    }
