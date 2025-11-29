from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing import List
import json
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_ignore_empty=True,
        extra="ignore",  # Ignore extra fields in .env
    )
    
    # Database (MongoDB)
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "newsprism"
    
    # Vector Database
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "newsprism-vectors"
    
    # Groq API
    GROQ_API_KEY: str = ""
    GROQ_API_URL: str = "https://api.groq.com/openai/v1"
    
    # NewsAPI
    NEWSAPI_KEY: str = ""
    
    # Security (Optional - for future JWT authentication)
    # These are used if you add user authentication later
    SECRET_KEY: str = "change-this-in-production-for-jwt-tokens"
    ALGORITHM: str = "HS256"  # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # JWT token expiration time
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS - will be set by model_validator after init
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    @model_validator(mode='after')
    def parse_cors_origins(self):
        """Parse CORS_ORIGINS from environment after initialization"""
        # Read directly from env to avoid pydantic_settings JSON parsing
        env_value = os.getenv("CORS_ORIGINS", "").strip()
        
        # If empty or not set, keep defaults
        if not env_value:
            return self
        
        # Try parsing as JSON
        try:
            parsed = json.loads(env_value)
            if isinstance(parsed, list) and len(parsed) > 0:
                self.CORS_ORIGINS = parsed
                return self
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
        
        # Split by comma
        origins = [origin.strip() for origin in env_value.split(',') if origin.strip()]
        if origins:
            self.CORS_ORIGINS = origins
        
        return self
    
    # Application
    PROJECT_NAME: str = "NewsPrism"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Embedding Model
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # Clustering
    CLUSTERING_MIN_SAMPLES: int = 2
    CLUSTERING_EPS: float = 0.5
    
    # Bias Analysis Weights
    BIAS_WEIGHT_TONE: float = 0.4
    BIAS_WEIGHT_LEXICAL: float = 0.25
    BIAS_WEIGHT_OMISSION: float = 0.2
    BIAS_WEIGHT_CONSISTENCY: float = 0.15


settings = Settings()

