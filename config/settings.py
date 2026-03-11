from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment: str
    azure_openai_api_version: str
    azure_openai_embedding_deployment: str
    azure_openai_embedding_endpoint : str
    LANGCHAIN_TRACING_V2: Optional[str] = None
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: Optional[str] = None
    class Config:
        env_file = ".env"


settings = Settings()