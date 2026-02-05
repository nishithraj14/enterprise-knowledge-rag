import os
from pathlib import Path

from app.ingestion.loader import load_document
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import dynamic_chunk
from app.embeddings.embedder import embed_chunks
from app.storage.vector_store import vector_store
from app.storage.document_registry import document_registry
from app.observability.logger import log_ingestion


def preload_resume():

    BASE_DIR = Path(__file__).resolve().parent
    path = BASE_DIR / "resume.pdf"

    if not path.exists():
        print("⚠️ Resume not found:", path)
        return

    text = load_document(str(path))
    clean = clean_text(text)
    chunks = dynamic_chunk(clean)

    if not chunks:
        print("⚠️ Resume had no readable text")
        return

    embeddings = embed_chunks(chunks)

    vector_store.add(
        chunks=chunks,
        embeddings=embeddings,
        source="resume.pdf"
    )

    document_registry.add("resume.pdf")

    log_ingestion("resume.pdf (preloaded)", len(chunks))
