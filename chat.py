"""CLI interactiva de preguntas sobre los documentos indexados."""

import argparse
import json

from rag import answer_question


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="*", help="Pregunta única; sin argumento abre chat")
    args = parser.parse_args()
    if args.question:
        print(json.dumps(answer_question(" ".join(args.question)), ensure_ascii=False, indent=2))
        return
    print("Chat RAG local. Escribe salir para terminar.")
    while True:
        try:
            question = input("Pregunta> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if question.lower() in {"salir", "exit", "quit"}:
            break
        if question:
            print(json.dumps(answer_question(question), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
