from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database (MongoDB)
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "newsprism"
    
    # Vector Database
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "newsprism-vectors"
    
    # Grok API (xAI)
    GROK_API_KEY: str
    GROK_API_URL: str = "https://api.x.ai/v1"
    
    # NewsAPI
    NEWSAPI_KEY: str
    
    # Security (Optional - for future JWT authentication)
    # These are used if you add user authentication later
    SECRET_KEY: str = "change-this-in-production-for-jwt-tokens"
    ALGORITHM: str = "HS256"  # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # JWT token expiration time
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

