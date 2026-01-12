from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "RAG-Project"
    APP_VERSION: str = "1.0.0"

    FILE_DEFAULT_CHUNK_SIZE: int  
    FILE_ALLOWED_TYPES: list[str] = [
        "text/plain",
        "application/pdf"
    ]

    FILE_MAX_SIZE: int = 10  

    class Config:
        env_file = ".env"      
        extra = "forbid"


@lru_cache
def get_settings() -> Settings:
    return Settings()
