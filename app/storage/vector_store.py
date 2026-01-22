import chromadb
from chromadb.config import Settings
from typing import List
import uuid


class VectorStore:
    """
    ChromaDB wrapper with:
    - Telemetry disabled
    - Globally unique chunk IDs
    - Source-aware metadata
    """

    def __init__(self):
        self.client = chromadb.Client(
            Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="enterprise_docs"
        )

    def add(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        source: str
    ):
        """
        Store document chunks with unique IDs and source metadata.
        """

        ids = [str(uuid.uuid4()) for _ in chunks]

        metadatas = [
            {
                "source": source,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

    def search(self, query_embedding: List[float], k: int = 5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )


# Singleton instance
vector_store = VectorStore()
