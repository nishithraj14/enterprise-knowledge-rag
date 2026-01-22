from app.embeddings.embedder import embed_query
from app.storage.vector_store import vector_store


def retrieve_context(question: str, source: str | None = None):
    """
    Retrieve relevant chunks.
    If source is provided → restrict to that document.
    If source is None → search across all documents.
    """

    query_embedding = embed_query(question)

    where = None
    if source:
        where = {"source": source}

    results = vector_store.collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where=where
    )

    return results
