from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./cardguard.db"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6-terra"
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "cardguard-production"
    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def settings():
    return Settings()
