from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str
    source: Optional[str] = None  # None = search all documents


class Source(BaseModel):
    document: str
    chunk_id: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
