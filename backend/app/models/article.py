from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import IndexModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Article(BaseModel):
    """Article model for MongoDB"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    source: str
    url: str
    title: str
    author: Optional[str] = None
    published_at: datetime
    text: str
    raw_html: Optional[str] = None
    language: str = "en"
    country: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadata
    chunks: Optional[List[Dict[str, Any]]] = None
    ner_entities: Optional[List[Dict[str, Any]]] = None
    
    # Bias metadata
    tone_score: Optional[float] = None
    lexical_bias_score: Optional[float] = None
    omission_score: Optional[float] = None
    consistency_score: Optional[float] = None
    bias_index: Optional[float] = None
    
    # Clustering
    cluster_id: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "source": "BBC News",
                "url": "https://example.com/article",
                "title": "Example Article",
                "published_at": "2024-01-01T00:00:00Z",
                "text": "Article content..."
            }
        }


class Cluster(BaseModel):
    """Cluster model for MongoDB"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    query: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    canonical_article_id: Optional[str] = None
    
    # Analysis results
    fact_summary: Optional[str] = None
    frame_summary: Optional[List[Dict[str, Any]]] = None
    facts: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ArticleAnalysis(BaseModel):
    """ArticleAnalysis model for MongoDB"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    article_id: str
    analysis_type: str  # 'sentiment', 'lexical', 'omission', etc.
    result: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# MongoDB collection indexes
ARTICLE_INDEXES = [
    IndexModel([("source", 1)]),
    IndexModel([("published_at", -1)]),
    IndexModel([("cluster_id", 1)]),
    IndexModel([("url", 1)], unique=True),
]

CLUSTER_INDEXES = [
    IndexModel([("query", 1)]),
    IndexModel([("created_at", -1)]),
]

ANALYSIS_INDEXES = [
    IndexModel([("article_id", 1)]),
    IndexModel([("analysis_type", 1)]),
]
