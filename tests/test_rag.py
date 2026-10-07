from ingest import ingest, load_documents, make_chunks
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from rag import answer_question


def test_ingestion_has_sources_and_stable_ids(tmp_path):
    (tmp_path / "one.md").write_text("PostgreSQL guarda pedidos. " * 30, encoding="utf-8")
    docs = load_documents(tmp_path)
    chunks, ids = make_chunks(docs)
    assert chunks and len(chunks) == len(ids)
    assert all(chunk.metadata["source"] == "one.md" for chunk in chunks)
    assert make_chunks(docs)[1] == ids

    class Store:
        def add_documents(self, documents, ids):
            self.documents, self.ids = documents, ids

    store = Store()
    assert ingest(tmp_path, store=store) == len(ids)
    assert store.ids == ids


def test_answer_uses_retrieved_context_and_cites_sources():
    class Store:
        def similarity_search_with_relevance_scores(self, query, k):
            assert query == "¿Qué base de datos?" and k == 4
            return [(Document(page_content="Se usa PostgreSQL.", metadata={"source": "a.md"}), .9)]

    class Model:
        def invoke(self, prompt):
            assert "PostgreSQL" in str(prompt)
            return type("Reply", (), {"content": "Se usa PostgreSQL [a.md]."})()

    result = answer_question("¿Qué base de datos?", store=Store(), model=Model())
    assert result == {"answer": "Se usa PostgreSQL [a.md].", "sources": ["a.md"]}


def test_low_relevance_does_not_call_model():
    class Store:
        def similarity_search_with_relevance_scores(self, query, k):
            return [(Document(page_content="irrelevante"), .1)]

    assert answer_question("¿Cuál es el salario?", store=Store())["sources"] == []


def test_chroma_persists_index_between_instances(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "database.md").write_text(
        "PostgreSQL conserva los pedidos y sus identificadores.", encoding="utf-8"
    )
    persist_dir = tmp_path / "chroma"
    embedding = DeterministicFakeEmbedding(size=32)
    first = Chroma(collection_name="test_rag", embedding_function=embedding,
                   persist_directory=str(persist_dir))
    assert ingest(data_dir, store=first) == 1
    second = Chroma(collection_name="test_rag", embedding_function=embedding,
                    persist_directory=str(persist_dir))
    results = second.similarity_search("pedidos", k=1)
    assert results[0].metadata["source"] == "database.md"
