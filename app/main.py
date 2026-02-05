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

    print("🚀 PRELOAD STARTED")

    BASE_DIR = Path(__file__).resolve().parent
    path = BASE_DIR / "resume.pdf"

    print("📄 Resume path:", path)

    if not path.exists():
        print("❌ Resume not found")
        return

    text = load_document(str(path))

    if not text:
        print("❌ No text extracted")
        return

    clean = clean_text(text)
    chunks = dynamic_chunk(clean)

    print("✂️ Chunks:", len(chunks))

    if not chunks:
        print("❌ No chunks created")
        return

    embeddings = embed_chunks(chunks)

    vector_store.add(
        chunks=chunks,
        embeddings=embeddings,
        source="resume.pdf"
    )

    document_registry.add("resume.pdf")

    log_ingestion("resume.pdf (preloaded)", len(chunks))

    print("✅ Resume preloaded successfully")
