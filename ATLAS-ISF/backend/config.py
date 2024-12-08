from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database configurations
    TIMESCALE_DB_HOST: str = "localhost"
    TIMESCALE_DB_PORT: int = 5002
    TIMESCALE_DB_USER: str = "postgres"
    TIMESCALE_DB_PASSWORD: str = "postgres"
    TIMESCALE_DB_NAME: str = "postgres"
    
    # Vector DB configurations
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    # LLM configurations
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "mistral"
    
    # AWS configurations (for hourly data sync)
    AWS_DB_HOST: str = ""
    AWS_DB_PORT: str = ""
    AWS_DB_USER: str = ""
    AWS_DB_PASSWORD: str = ""
    AWS_DB_NAME: str = ""
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 