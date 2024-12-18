from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = Field(default="mongodb://localhost:27017")
    MONGODB_MAX_CONNECTIONS: int = Field(default=10)
    MONGODB_MIN_CONNECTIONS: int = Field(default=1)
    
    # JWT settings
    JWT_SECRET_KEY: str = Field(default="your-secret-key-here")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # API Keys
    LLAMA_CLOUD_API_KEY: str = Field(default=...)
    OPENAI_API_KEY: str = Field(default=...)
    
    # Model settings
    OPENAI_MODEL: str = Field(default="gpt-4o-mini")
    
    # File upload settings
    UPLOAD_FOLDER: str = Field(default="uploads")
    ALLOWED_EXTENSIONS: set = Field(default={"pdf", "doc", "docx", "txt"})

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()