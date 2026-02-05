# =========================================================
# PAGE CONFIG — MUST BE FIRST
# =========================================================
import streamlit as st

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# IMPORTS — YOUR EXISTING RAG ENGINE
# =========================================================
import os
from dotenv import load_dotenv

from app.ingestion.loader import load_document
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import dynamic_chunk

from app.embeddings.embedder import embed_chunks
from app.retrieval.retriever import retrieve_context
from app.generation.generator import generate_answer

from app.storage.vector_store import vector_store
from app.storage.document_registry import document_registry

from app.bootstrap.preload import preload_resume

# =========================================================
# ENV LOADING (Local + Cloud Safe)
# =========================================================
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not configured")
    st.stop()

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# =========================================================
# PRELOAD DEMO DOC
# =========================================================
@st.cache_resource
def bootstrap():
    preload_resume()

bootstrap()

# =========================================================
# UI HEADER
# =========================================================
st.title("🧠 Enterprise Knowledge Assistant")
st.caption("Privacy-First Retrieval Augmented Knowledge System")

st.divider()

# =========================================================
# SIDEBAR — DOCUMENTS
# =========================================================
st.sidebar.header("📂 Knowledge Base")

docs = document_registry.list()

selected_doc = st.sidebar.selectbox(
    "Select document scope",
    ["All Documents"] + docs
)

# =========================================================
# FILE INGESTION
# =========================================================
st.sidebar.subheader("Upload Documents")

files = st.sidebar.file_uploader(
    "PDF / DOCX / HTML",
    accept_multiple_files=True
)

if st.sidebar.button("Ingest Documents"):

    if not files:
        st.sidebar.warning("Upload files first")

    else:
        with st.spinner("Processing documents..."):

            for file in files:

                # Save temp
                path = f"temp_{file.name}"
                with open(path, "wb") as f:
                    f.write(file.read())

                # Pipeline
                raw = load_document(path)
                clean = clean_text(raw)
                chunks = dynamic_chunk(clean)

                if not chunks:
                    continue

                embeddings = embed_chunks(chunks)

                vector_store.add(
                    chunks=chunks,
                    embeddings=embeddings,
                    source=file.name
                )

                document_registry.add(file.name)

                os.remove(path)

        st.sidebar.success("Ingestion complete")

# =========================================================
# QUERY UI
# =========================================================
st.subheader("Ask a Knowledge Question")

question = st.text_area(
    "Enter your question",
    height=120,
    placeholder="Ask anything about your documents..."
)

ask = st.button("Ask")

# =========================================================
# QUERY EXECUTION
# =========================================================
if ask and question:

    with st.spinner("Retrieving knowledge..."):

        context = retrieve_context(
            question=question,
            source=None if selected_doc == "All Documents" else selected_doc
        )

        if not context or not context.get("documents"):
            st.warning(
                "The provided documents do not contain enough information."
            )

        else:
            answer, sources = generate_answer(
                question=question,
                context=context
            )

            # -----------------------------
            # Answer
            # -----------------------------
            st.subheader("Answer")
            st.write(answer)

            # -----------------------------
            # Sources
            # -----------------------------
            st.subheader("Sources")

            for s in sources:
                st.caption(
                    f"📄 {s['document']} — {s['chunk_id']}"
                )
