import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # MongoDB settings
    mongo_details: str = Field(
        default="mongodb://localhost:27017",
        env="MONGO_DETAILS",
        description="MongoDB connection string"
    )
    database_name: str = Field(
        default="ecommerce",
        env="DATABASE_NAME",
        description="MongoDB database name"
    )
    
    # Application settings
    app_name: str = Field(
        default="E-Commerce Backend API",
        env="APP_NAME",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        env="APP_VERSION",
        description="Application version"
    )
    debug: bool = Field(
        default=False,
        env="DEBUG",
        description="Debug mode"
    )
    
    # API settings
    api_prefix: str = Field(
        default="/api/v1",
        env="API_PREFIX",
        description="API prefix"
    )
    
    # CORS settings
    cors_origins: list = Field(
        default=["*"],
        env="CORS_ORIGINS",
        description="CORS allowed origins"
    )
    
    # Pagination settings
    default_limit: int = Field(
        default=10,
        env="DEFAULT_LIMIT",
        description="Default pagination limit"
    )
    max_limit: int = Field(
        default=100,
        env="MAX_LIMIT",
        description="Maximum pagination limit"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings() 