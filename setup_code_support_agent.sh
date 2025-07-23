#!/bin/bash

# Create project structure
mkdir -p {app,vectorstore,data}

# Create files with starter code
cat > requirements.txt <<EOL
fastapi
uvicorn
openai
langchain
chromadb
tqdm
python-dotenv
EOL

cat > app/config.py <<EOL
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DB_DIR = "vectorstore"
EOL

cat > app/ingest.py <<EOL
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
EOL

cat > app/agent.py <<EOL
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from app.config import OPENAI_API_KEY, CHROMA_DB_DIR

def get_code_agent():
    db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=OpenAIEmbeddings())
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=retriever,
        return_source_documents=True
    )
    return qa
EOL

cat > app/main.py <<EOL
from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.agent import get_code_agent

app = FastAPI()
qa = get_code_agent()

class QueryInput(BaseModel):
    question: str

@app.post("/ask")
def ask_codebase(query: QueryInput):
    response = qa(query.question)
    answer = response["result"]
    sources = [
        {
            "file": doc.metadata.get("source"),
            "lines": doc.metadata.get("lines")
        } for doc in response["source_documents"]
    ]
    return {"answer": answer, "sources": sources}
EOL

cat > .env <<EOL
OPENAI_API_KEY=your-openai-api-key
EOL

echo "✅ Project scaffold created successfully in ./"
