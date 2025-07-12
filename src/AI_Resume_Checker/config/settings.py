from pydantic_settings import BaseSettings
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    #tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    #SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY")
    x_rapidapi_key: str = os.getenv("x_rapidapi_key")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT")
    LANGSMITH_TRACING: str = os.getenv("LANGSMITH_TRACING")
    # Application settings
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    supported_file_types: List[str] = ["pdf", "docx", "txt"]
    max_file_size_mb: int = 10
    
    # Model settings
    
    
    # Streamlit settings
    page_title: str = "AI Resume Checker"
    page_icon: str = "📝"
    layout: str = "wide"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a global settings instance
settings = Settings()