import os
from app.ingestion.loader import load_document
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import dynamic_chunk
from app.embeddings.embedder import embed_chunks
from app.storage.vector_store import vector_store
from app.storage.document_registry import document_registry
from app.observability.logger import log_ingestion


def preload_resume():
    path = "app/bootstrap/resume.pdf"

    if not os.path.exists(path):
        return

    text = load_document(path)
    clean = clean_text(text)
    chunks = dynamic_chunk(clean)

    if not chunks:
        return

    embeddings = embed_chunks(chunks)

    vector_store.add(
        chunks=chunks,
        embeddings=embeddings,
        source="resume.pdf"
    )

    document_registry.add("resume.pdf")
    log_ingestion("resume.pdf (preloaded)", len(chunks))
