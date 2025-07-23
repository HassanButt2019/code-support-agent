import os
import ast
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from app.config import OPENAI_API_KEY, CHROMA_DB_DIR

def chunk_code_file(filepath):
    with open(filepath, 'r') as f:
        source = f.read()

    tree = ast.parse(source)
    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            start_line = node.lineno
            end_line = getattr(node, 'end_lineno', start_line + 10)
            chunk = {
                "file": filepath,
                "start_line": start_line,
                "end_line": end_line,
                "code": ast.get_source_segment(source, node)
            }
            chunks.append(chunk)

    return chunks

def ingest_codebase(directory="data"):
    docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                for chunk in chunk_code_file(filepath):
                    metadata = {
                        "source": chunk["file"],
                        "lines": f'{chunk["start_line"]}-{chunk["end_line"]}'
                    }
                    docs.append(Document(page_content=chunk["code"], metadata=metadata))

    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(docs, embedding=embeddings, persist_directory=CHROMA_DB_DIR)
    db.persist()
    print(f"Ingested {len(docs)} chunks into Chroma.")

if __name__ == "__main__":
    ingest_codebase()
