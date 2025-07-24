from app.utils import build_github_link
from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.agent import get_code_agent
from app.config import GITHUB_REPO_URL

app = FastAPI()
qa = get_code_agent()

class QueryInput(BaseModel):
    question: str




def normalize_lines(line_str):
    """Converts '4-9' to tuple of ints (4, 9)."""
    parts = line_str.split("-")
    return (int(parts[0]), int(parts[1])) if len(parts) == 2 else (int(parts[0]), int(parts[0]))

def is_overlapping(a, b):
    """Returns True if line range a overlaps with b."""
    return not (a[1] < b[0] or b[1] < a[0])

@app.post("/ask")
def ask_codebase(query: QueryInput):
    response = qa(query.question)
    answer = response["result"]

    selected_sources = []

    for doc in response["source_documents"]:
        file = doc.metadata.get("source")
        lines = doc.metadata.get("lines")
        line_range = normalize_lines(lines)

        # Skip if already overlapping with a selected chunk
        skip = False
        for src in selected_sources:
            if src["file"] == file and is_overlapping(line_range, src["line_range"]):
                skip = True
                break
        if skip:
            continue

        selected_sources.append({
            "file": file,
            "lines": lines,
            "line_range": line_range,  # for internal checking
            "github_url": build_github_link(file, lines, GITHUB_REPO_URL)
        })

    # Strip internal use before returning
    sources_cleaned = [
        {k: v for k, v in src.items() if k != "line_range"} for src in selected_sources
    ]

    return {"answer": answer.strip(), "sources": sources_cleaned}
