from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


# =========================================================
# Embed document chunks
# =========================================================
def embed_chunks(chunks: list[str]) -> list[list[float]]:
    if not chunks:
        return []

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )

    return [item.embedding for item in response.data]


# =========================================================
# Embed user query
# =========================================================
def embed_query(query: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    return response.data[0].embedding
