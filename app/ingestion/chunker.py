import tiktoken
from typing import List

def dynamic_chunk(
    text: str,
    max_tokens: int = 400,
    overlap_tokens: int = 50
) -> List[str]:
    """
    Dynamic, token-aware chunking.
    Guarantees non-empty chunks for non-empty input.
    """

    if not text.strip():
        return []

    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    if len(tokens) <= max_tokens:
        # Small document → single chunk
        return [text]

    chunks = []
    start = 0
    text_len = len(tokens)

    while start < text_len:
        end = start + max_tokens
        chunk_tokens = tokens[start:end]

        chunk_text = encoding.decode(chunk_tokens).strip()
        if chunk_text:
            chunks.append(chunk_text)

        # Move window with overlap
        start = end - overlap_tokens
        if start < 0:
            start = 0

    return chunks
