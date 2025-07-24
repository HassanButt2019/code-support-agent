import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")

CHROMA_DB_DIR = "vectorstore"

MAX_FILES = 200
MAX_TOTAL_TOKENS = 50000
MAX_TOKENS_PER_CHUNK = 1200