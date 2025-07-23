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
