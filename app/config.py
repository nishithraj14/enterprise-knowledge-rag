import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    VECTOR_DB_DIR = "vector_store"
    MAX_CONTEXT_CHUNKS = 5
    LOG_LEVEL = "INFO"

settings = Settings()
