from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    project_db_url: str = "mongodb://localhost:27017"
    project_db_name: str = "todo_app"
    
    # JWT
    jwt_secret: str = "your-secret-key-change-this-in-production"
    jwt_expire_minutes: int = 30
    jwt_refresh_expire_days: int = 7
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # Server
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Rate limiting
    rate_limit_enabled: bool = True
    
    # Monitoring
    enable_metrics: bool = True
    metrics_retention_days: int = 30
    
    # Cache
    cache_ttl_seconds: int = 3600
    cache_enabled: bool = True
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()
