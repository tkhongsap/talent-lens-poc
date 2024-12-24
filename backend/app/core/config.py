from pydantic import BaseModel, Field
from functools import lru_cache
import os
from dotenv import load_dotenv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Get the absolute path to the .env file
env_path = Path(__file__).parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseModel):
    LLAMA_CLOUD_API_KEY: str = Field(default="")
    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Add function to clear settings cache
def refresh_settings():
    get_settings.cache_clear()