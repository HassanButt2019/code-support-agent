import os
import time
from app.ingest import ingest_codebase
from app.utils import build_github_link, clone_github_repo
from fastapi import Body, Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.agent import get_code_agent
from dotenv import set_key ,load_dotenv

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth import authenticate_user, create_access_token, Token, get_current_user

app = FastAPI()
qa = get_code_agent()
GITHUB_REPO_URL = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class LoginInput(BaseModel):
    username: str
    password: str

class QueryInput(BaseModel):
    question: str


class IngestInput(BaseModel):
    github_repo_url: str

def normalize_lines(line_str):
    """Converts '4-9' to tuple of ints (4, 9)."""
    parts = line_str.split("-")
    return (int(parts[0]), int(parts[1])) if len(parts) == 2 else (int(parts[0]), int(parts[0]))

def is_overlapping(a, b):
    """Returns True if line range a overlaps with b."""
    return not (a[1] < b[0] or b[1] < a[0])


# In-memory mapping (replace with DB in production)
user_repo_map = {}

@app.post("/ingest")
def ingest_repo(input: IngestInput, user: str = Depends(get_current_user)):
    start = time.time()
    repo_path = clone_github_repo(input.github_repo_url)
    ingest_codebase(repo_path)

    # Save user's repo URL for later lookup
    user_repo_map[user] = input.github_repo_url

    end = time.time()
    return {
        "message": "✅ Ingestion complete.",
        "repo": input.github_repo_url,
        "local_path": repo_path,
        "duration_seconds": round(end - start, 2)
    }



@app.post("/ask")
def ask_codebase(query: QueryInput, user: str = Depends(get_current_user)):
    if user not in user_repo_map:
        raise HTTPException(status_code=400, detail="❌ No ingested repo found for this user.")

    github_repo_url = user_repo_map[user]

    response = qa(query.question)
    answer = response["result"]
    selected_sources = []

    for doc in response["source_documents"]:
        file = doc.metadata.get("source")
        lines = doc.metadata.get("lines")
        line_range = normalize_lines(lines)

        skip = any(
            src["file"] == file and is_overlapping(line_range, src["line_range"])
            for src in selected_sources
        )
        if skip:
            continue

        selected_sources.append({
            "file": file,
            "lines": lines,
            "line_range": line_range,
            "github_url": build_github_link(file, lines, github_repo_url)
        })

    sources_cleaned = [{k: v for k, v in src.items() if k != "line_range"} for src in selected_sources]

    return {"answer": answer.strip(), "sources": sources_cleaned}



@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
