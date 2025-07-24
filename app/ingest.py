import os
import ast
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

from app.config import OPENAI_API_KEY, CHROMA_DB_DIR
from app.config import (
    OPENAI_API_KEY, CHROMA_DB_DIR,
    MAX_FILES, MAX_TOTAL_TOKENS, MAX_TOKENS_PER_CHUNK
)
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

def chunk_code_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"⚠️ Failed to parse {filepath}: {e}")
        return []

    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            start = node.lineno
            end = getattr(node, 'end_lineno', start + 10)
            code = ast.get_source_segment(source, node)
            if not code:
                continue

            tokens = len(tokenizer.encode(code))
            if tokens > MAX_TOKENS_PER_CHUNK:
                print(f"⚠️ Skipped large chunk ({tokens} tokens): {filepath} lines {start}-{end}")
                continue

            chunks.append({
                "file": filepath,
                "start_line": start,
                "end_line": end,
                "code": code,
                "tokens": tokens
            })

    return chunks

def ingest_codebase(directory="data"):
    docs = []
    total_tokens = 0
    file_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                if file_count >= MAX_FILES:
                    print("🚫 File limit reached.")
                    break

                filepath = os.path.join(root, file)
                file_chunks = chunk_code_file(filepath)

                for chunk in file_chunks:
                    if total_tokens + chunk["tokens"] > MAX_TOTAL_TOKENS:
                        print("🚫 Token budget exceeded.")
                        break

                    metadata = {
                        "source": chunk["file"],
                        "lines": f'{chunk["start_line"]}-{chunk["end_line"]}'
                    }
                    docs.append(Document(page_content=chunk["code"], metadata=metadata))
                    total_tokens += chunk["tokens"]

                file_count += 1

    print(f"📄 Ingested {len(docs)} chunks from {file_count} files. Total tokens: {total_tokens}")

    if not docs:
        print("⚠️ No valid chunks to embed.")
        return

    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(docs, embedding=embeddings, persist_directory=CHROMA_DB_DIR)
    db.persist()
    print("✅ Chroma DB updated.")