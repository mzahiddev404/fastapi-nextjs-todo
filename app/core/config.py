"""Configuration settings for the FastAPI TODO application."""

import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "todo_app"
    
    # JWT
    jwt_secret: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App
    app_name: str = "FastAPI TODO App"
    debug: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()
