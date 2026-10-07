# Pre-entrega 3: RAG local con Chroma

Sistema de recuperación semántica local sobre documentos técnicos. Indexa `.txt` y `.md`, divide el texto en fragmentos solapados, guarda embeddings en Chroma y responde con fuentes. Hay tres documentos de ejemplo en `data/`.

## Preparación

Python 3.12+. Crear un entorno virtual, ejecutar `pip install -r requirements.txt`, copiar `.env.example` a `.env` y definir `OPENAI_API_KEY`. La generación de embeddings y respuestas consume la API de OpenAI. `chroma_db/` se crea localmente y está ignorado por Git; el evaluador lo reconstruye con la ingesta.

## Ejecución

```bash
python ingest.py
python chat.py "¿Cuándo se hacen los respaldos de PostgreSQL?"
python chat.py
pytest -q
```

`ingest.py` conserva fuente, documento e identificador estable de fragmento. `rag.py` recupera los fragmentos más relevantes (`k=4`, umbral configurable), compone un prompt que limita la respuesta al contexto y devuelve `answer` y `sources`. Si no supera el umbral, responde que la información no está en los documentos sin llamar al modelo. El umbral reduce respuestas infundadas, pero no garantiza factualidad; se debe revisar la cita contra el documento. Los tests no necesitan clave de API.
