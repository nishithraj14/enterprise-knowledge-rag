from typing import Dict, List
from threading import Lock


class DocumentRegistry:
    """
    In-memory registry of ingested documents (metadata only).
    No raw content or text is stored.
    """

    def __init__(self):
        self._docs: Dict[str, str] = {}
        self._lock = Lock()

    def add(self, source: str):
        with self._lock:
            self._docs[source] = source

    def list(self) -> List[str]:
        with self._lock:
            return list(self._docs.values())


document_registry = DocumentRegistry()
