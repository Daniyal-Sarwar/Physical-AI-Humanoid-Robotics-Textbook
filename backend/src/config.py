"""
Configuration Management for Physical AI Textbook Backend

Loads environment variables and provides typed configuration settings.
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All values have sensible defaults for development.
    For production, set these in .env file or environment.
    """
    
    # === JWT Configuration ===
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    jwt_expiration_seconds: int = 604800  # 7 days default
    
    # === Session Configuration ===
    session_secret: str = "dev-session-secret-change-in-production"
    
    # === Database Configuration ===
    sqlite_db_path: str = "sqlite:///./data/users.db"
    
    @property
    def sqlite_connection_string(self) -> str:
        """Get SQLite connection string in proper SQLAlchemy format."""
        if self.sqlite_db_path.startswith("sqlite:///"):
            return self.sqlite_db_path
        # Add sqlite:/// prefix if missing
        return f"sqlite:///{self.sqlite_db_path}"
    
    # === Rate Limiting ===
    anonymous_rate_limit: int = 5
    rate_limit_window_hours: int = 24
    
    # === CORS Configuration ===
    frontend_url: str = "http://localhost:3000"
    
    # === Application Settings ===
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # === Gemini API ===
    gemini_api_key: Optional[str] = None
    
    # === ChromaDB Configuration ===
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "physical_ai_textbook"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"  # Ignore extra fields from .env
    }
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    @property
    def cors_origins(self) -> list[str]:
        """
        Get list of allowed CORS origins.
        
        In production: Only allow the configured frontend URL
        In development: Allow localhost variants for testing
        """
        origins = [self.frontend_url]
        if not self.is_production:
            # Allow additional dev origins in development only
            origins.extend([
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:8000",
                "http://127.0.0.1:8000",
            ])
        return list(set(origins))  # Remove duplicates


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are only loaded once.
    """
    return Settings()


# Convenience export
settings = get_settings()
