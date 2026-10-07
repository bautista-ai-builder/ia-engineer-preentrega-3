"""Ingesta repetible de archivos .txt/.md en Chroma persistente."""

import argparse
import hashlib
from pathlib import Path

from config import ROOT, vector_store
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(data_dir: Path) -> list[Document]:
    files = sorted(
        p for p in data_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".txt"}
    )
    if not files:
        raise ValueError(f"No hay documentos .md/.txt en {data_dir}")
    documents = []
    for path in files:
        text = path.read_text(encoding="utf-8").strip()
        if text:
            documents.append(Document(
                page_content=text,
                metadata={"source": str(path.relative_to(data_dir)), "doc_id": path.stem},
            ))
    if not documents:
        raise ValueError("Todos los documentos están vacíos")
    return documents


def make_chunks(documents: list[Document]) -> tuple[list[Document], list[str]]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(documents)
    ids = []
    for position, chunk in enumerate(chunks):
        content_hash = hashlib.sha256(chunk.page_content.encode("utf-8")).hexdigest()[:16]
        chunk.metadata["chunk_id"] = f"{chunk.metadata['doc_id']}:{position}:{content_hash}"
        ids.append(chunk.metadata["chunk_id"])
    return chunks, ids


def ingest(data_dir: Path, store=None) -> int:
    chunks, ids = make_chunks(load_documents(data_dir))
    target = store if store is not None else vector_store()
    target.add_documents(chunks, ids=ids)
    return len(chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexar documentos técnicos en Chroma")
    parser.add_argument("--data", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    count = ingest(args.data)
    print(f"Indexados {count} fragmentos en Chroma")
