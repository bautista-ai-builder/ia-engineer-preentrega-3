"""Recuperación y respuesta fundada en documentos locales."""

import os

from config import require_key, vector_store
from langchain_core.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Responde en español únicamente con el contexto proporcionado. "
     "Si el contexto no permite responder, di 'No encuentro esa información en los documentos'. "
     "No inventes hechos. Cita las fuentes por su nombre."),
    ("human", "Pregunta: {question}\n\nContexto:\n{context}"),
])


def default_model():
    from langchain_openai import ChatOpenAI

    require_key()
    return ChatOpenAI(model=os.getenv("CHAT_MODEL", "gpt-4o-mini"), temperature=0)


def answer_question(question: str, *, store=None, model=None, k: int = 4,
                    min_relevance: float = 0.35) -> dict:
    if not question.strip():
        raise ValueError("La pregunta no puede estar vacía")
    if k < 1:
        raise ValueError("k debe ser >= 1")
    target = store if store is not None else vector_store()
    matches = target.similarity_search_with_relevance_scores(question, k=k)
    selected = [(doc, score) for doc, score in matches if score >= min_relevance]
    if not selected:
        return {"answer": "No encuentro esa información en los documentos.", "sources": []}
    context = "\n\n".join(
        f"[{i}] Fuente: {doc.metadata.get('source', 'desconocida')}\n{doc.page_content}"
        for i, (doc, _) in enumerate(selected, start=1)
    )
    selected_model = model if model is not None else default_model()
    reply = selected_model.invoke(PROMPT.invoke({"question": question, "context": context}))
    answer = reply.content if hasattr(reply, "content") else str(reply)
    sources = sorted({doc.metadata.get("source", "desconocida") for doc, _ in selected})
    return {"answer": answer, "sources": sources}
