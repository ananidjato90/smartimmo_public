"""Application configuration utilities for the Togo Real Estate backend."""
from functools import lru_cache
from typing import Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    """Environment-driven settings for the FastAPI application."""
    
    app_name: str = Field(
        default="Togo Real Estate API",
        description="Human-readable name for the FastAPI application.",
    )
    environment: str = Field(
        default="development", description="Deployment environment label."
    )
    debug: bool = Field(default=True, description="Toggle FastAPI debug mode.")
    
    api_v1_prefix: str = Field(
        default="/api/v1",
        description="Base path prefix for versioned API routes.",
    )
    
    mysql_user: str = Field(default="root", description="MySQL user name.")
    mysql_password: str = Field(
        default="", description="MySQL user password."
    )
    mysql_host: str = Field(default="localhost", description="MySQL host name or IP.")
    mysql_port: int = Field(default=3306, description="MySQL port number.")
    mysql_database: str = Field(
        default="smartimmo", description="Name of the target MySQL database."
    )
    
    database_url: str | None = Field(
        default=None,
        description="Full database connection URL (overrides individual MySQL settings).",
    )
    
    # CHANGEMENT ICI : Union[str, list[str]] pour accepter les deux formats
    cors_allowed_origins: Union[str, list[str]] = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="List of allowed origins for CORS.",
    )
    
    ollama_host: str = Field(
        default="http://localhost:11434",
        description="Base URL for the Ollama inference server.",
    )
    ollama_model: str = Field(
        default="llama3.3",
        description="Name of the model to use for natural language search assistance.",
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # IMPORTANT : Empêcher le parsing JSON automatique
        json_schema_extra={"env_parse_none_str": None}
    )
    
    @field_validator("cors_allowed_origins", mode="after")
    @classmethod
    def ensure_list(cls, value):
        """Ensure CORS origins is always a list."""
        if isinstance(value, str):
            # Séparer par virgules
            origins = [item.strip() for item in value.split(",") if item.strip()]
            return origins if origins else ["http://localhost:3000"]
        
        if isinstance(value, list):
            return value
        
        return ["http://localhost:3000"]

    # AJOUTEZ CETTE MÉTHODE ICI
    def get_cors_origins_list(self) -> list[str]:
        """Return CORS origins as a list."""
        if isinstance(self.cors_allowed_origins, list):
            return self.cors_allowed_origins
        if isinstance(self.cors_allowed_origins, str):
            return [item.strip() for item in self.cors_allowed_origins.split(",") if item.strip()]
        return ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of application settings."""
    return Settings()