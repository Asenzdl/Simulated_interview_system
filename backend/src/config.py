from pydantic_settings import BaseSettings
from pathlib import Path

# Project root: mianshi-system/ (parent of backend/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    # LLM
    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"
    llm_model_id: str = "deepseek-chat"

    # Embedding
    embedding_api_key: str = ""
    embedding_base_url: str = "https://api.deepseek.com"
    embedding_model_id: str = "text-embedding-v3"

    # Backend
    backend_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000"]
    database_url: str = f"sqlite+aiosqlite:///{(DATA_DIR / 'mianshi.db').as_posix()}"
    chroma_path: str = str(DATA_DIR / "chroma")

    model_config = {"env_file": str(PROJECT_ROOT / ".env"), "env_file_encoding": "utf-8"}


settings = Settings()
