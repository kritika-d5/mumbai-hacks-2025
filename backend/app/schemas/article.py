from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class ArticleBase(BaseModel):
    source: str
    url: str
    title: str
    author: Optional[str] = None
    published_at: datetime
    text: str
    language: str = "en"
    country: Optional[str] = None


class ArticleCreate(ArticleBase):
    raw_html: Optional[str] = None


class Chunk(BaseModel):
    chunk_id: str
    text: str
    embedding_id: Optional[str] = None
    start: int
    end: int


class NEREntity(BaseModel):
    entity: str
    type: str
    span: str


class ArticleResponse(ArticleBase):
    id: UUID
    scraped_at: datetime
    chunks: Optional[List[Chunk]] = None
    ner_entities: Optional[List[NEREntity]] = None
    tone_score: Optional[float] = None
    lexical_bias_score: Optional[float] = None
    omission_score: Optional[float] = None
    consistency_score: Optional[float] = None
    bias_index: Optional[float] = None
    cluster_id: Optional[UUID] = None
    
    class Config:
        from_attributes = True


class ClusterBase(BaseModel):
    query: str


class Fact(BaseModel):
    fact: str
    sources: List[str]  # URLs
    quotes: List[str]
    status: str  # "supported", "contradicted", "unverified"


class FrameSummary(BaseModel):
    source: str
    tone: float
    top_phrases: List[Dict[str, Any]]
    transparency_score: float
    bias_index: float


class ClusterResponse(BaseModel):
    id: UUID
    query: str
    created_at: datetime
    canonical_article_id: Optional[UUID] = None
    fact_summary: Optional[str] = None
    frame_summary: Optional[List[FrameSummary]] = None
    facts: Optional[List[Fact]] = None
    articles: List[ArticleResponse]
    
    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    query: str
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    sources: Optional[List[str]] = None
    limit: int = 50


class AnalyzeRequest(BaseModel):
    query: str
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    sources: Optional[List[str]] = None

