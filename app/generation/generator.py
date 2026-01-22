from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an enterprise knowledge assistant.

Rules:
- Answer ONLY using the provided context.
- Do NOT use prior knowledge.
- Do NOT infer or assume facts not explicitly stated.
- If the answer is not fully present in the context, say:
  "The provided documents do not contain enough information to answer this question."
- Be concise and factual.
"""

def generate_answer(question: str, context: dict):
    documents = context.get("documents", [[]])[0]
    metadatas = context.get("metadatas", [[]])[0]

    if not documents:
        return (
            "The provided documents do not contain enough information to answer this question.",
            []
        )

    context_block = "\n\n".join(
        f"[Chunk {i+1} | Source: {metadatas[i].get('source', 'unknown')}]\n{doc}"
        for i, doc in enumerate(documents)
    )

    prompt = f"""
Context:
{context_block}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0
    )

    answer = response.choices[0].message.content.strip()

    # ✅ FIX: chunk_id must be STRING
    sources = [
        {
            "document": meta.get("source", "unknown"),
            "chunk_id": f"chunk_{meta.get('chunk_index')}"
        }
        for meta in metadatas
    ]

    return answer, sources
