from app.utils import clone_github_repo
from app.ingest import ingest_codebase
from app.config import GITHUB_REPO_URL

repo_url = GITHUB_REPO_URL # change as needed
repo_path = clone_github_repo(repo_url)
ingest_codebase(repo_path)
