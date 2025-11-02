"""Application configuration utilities for the Togo Real Estate backend."""

from functools import lru_cache
from pydantic import BaseSettings, Field, field_validator


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

    mysql_user: str = Field(default="realestate", description="MySQL user name.")
    mysql_password: str = Field(
        default="realestate", description="MySQL user password."
    )
    mysql_host: str = Field(default="db", description="MySQL host name or IP.")
    mysql_port: int = Field(default=3306, description="MySQL port number.")
    mysql_database: str = Field(
        default="realestate", description="Name of the target MySQL database."
    )

    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:4200",
            "http://127.0.0.1:4200",
            "http://localhost",
        ],
        description="List of allowed origins for CORS.",
    )

    ollama_host: str = Field(
        default="http://llm:11434",
        description="Base URL for the Ollama inference server.",
    )
    ollama_model: str = Field(
        default="llama3",
        description="Name of the model to use for natural language search assistance.",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def split_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of application settings."""

    return Settings()
