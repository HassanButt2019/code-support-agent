import os
from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GITHUB_REPO_URL: str = ""
    CHROMA_DB_DIR: str = "vectorstore"

    MAX_FILES: int = 200
    MAX_TOTAL_TOKENS: int = 50000
    MAX_TOKENS_PER_CHUNK: int = 1200

    # ✅ Add these fields
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()