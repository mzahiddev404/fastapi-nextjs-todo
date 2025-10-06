"""Configuration settings for the FastAPI TODO application."""

import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database - Option 1: Full URI (recommended)
    mongodb_uri: str = ""
    
    # Database - Option 2: Individual components (fallback)
    mongodb_username: str = ""
    mongodb_password: str = ""
    mongodb_cluster: str = ""
    database_name: str = "todo_app"
    
    @property
    def get_mongodb_uri(self) -> str:
        """Get MongoDB URI from environment variables."""
        if self.mongodb_uri:
            return self.mongodb_uri
        elif self.mongodb_password:
            return f"mongodb+srv://{self.mongodb_username}:{self.mongodb_password}@{self.mongodb_cluster}/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&tlsAllowInvalidCertificates=true"
        else:
            raise ValueError("Either MONGODB_URI or MONGODB_PASSWORD must be set")


    # JWT
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App
    app_name: str = "FastAPI TODO App"
    debug: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()
