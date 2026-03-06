from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment: str
    azure_openai_api_version: str
    azure_openai_embedding_deployment: str
    azure_openai_embedding_endpoint : str

    class Config:
        env_file = ".env"


settings = Settings()