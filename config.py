"""Configuración de la colección local."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parent


def chroma_path() -> Path:
    configured = Path(os.getenv("CHROMA_DIR", "chroma_db"))
    return configured if configured.is_absolute() else ROOT / configured


def require_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Falta OPENAI_API_KEY en .env")


def embeddings():
    from langchain_openai import OpenAIEmbeddings

    require_key()
    return OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))


def vector_store():
    from langchain_chroma import Chroma

    return Chroma(collection_name="preentrega3", embedding_function=embeddings(),
                  persist_directory=str(chroma_path()))
