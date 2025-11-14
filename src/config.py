"""
Configuration management for Moemou application.
Loads settings from environment variables and provides typed configuration objects.
"""

from typing import Literal, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Provider Configuration
    llm_provider: Literal["openai", "anthropic"] = Field(default="openai", alias="LLM_PROVIDER")
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")

    # LLM Model Configuration
    openai_model: str = Field(default="gpt-4-turbo-preview", alias="OPENAI_MODEL")
    anthropic_model: str = Field(default="claude-3-opus-20240229", alias="ANTHROPIC_MODEL")
    llm_temperature: float = Field(default=0.7, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=2000, alias="LLM_MAX_TOKENS")

    # Application Settings
    app_name: str = Field(default="Moemou", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # API Configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_prefix: str = Field(default="/api/v1", alias="API_PREFIX")

    # CORS Settings
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        alias="CORS_ORIGINS"
    )

    # Database (optional)
    database_url: str = Field(default="sqlite:///./moemou.db", alias="DATABASE_URL")

    # Agent Configuration
    agent_type: str = Field(default="skincare_specialist", alias="AGENT_TYPE")
    enable_biomarker_analysis: bool = Field(default=True, alias="ENABLE_BIOMARKER_ANALYSIS")
    enable_product_recommendations: bool = Field(default=True, alias="ENABLE_PRODUCT_RECOMMENDATIONS")
    enable_routine_builder: bool = Field(default=True, alias="ENABLE_ROUTINE_BUILDER")

    # Knowledge Base
    knowledge_base_path: str = Field(default="./src/knowledge", alias="KNOWLEDGE_BASE_PATH")

    # Security
    secret_key: str = Field(default="dev-secret-key-change-in-production", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    def get_active_model(self) -> str:
        """Get the active LLM model based on provider."""
        if self.llm_provider == "openai":
            return self.openai_model
        return self.anthropic_model

    def get_active_api_key(self) -> Optional[str]:
        """Get the active API key based on provider."""
        if self.llm_provider == "openai":
            return self.openai_api_key
        return self.anthropic_api_key


# Global settings instance
settings = Settings()
