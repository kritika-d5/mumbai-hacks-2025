from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_database
from app.schemas.article import SearchRequest, ArticleResponse, ClusterResponse, AnalyzeRequest
from app.services.agents.orchestrator import AgentOrchestrator
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=List[ArticleResponse])
async def search_articles(request: SearchRequest):
    """Search for articles by query"""
    db = get_database()
    
    # Simple text search in MongoDB
    query_pattern = {"$regex": request.query, "$options": "i"}
    
    cursor = db.articles.find({
        "$or": [
            {"title": query_pattern},
            {"text": query_pattern}
        ]
    }).limit(request.limit)
    
    articles = await cursor.to_list(length=request.limit)
    
    # Convert ObjectId to string for response
    for article in articles:
        article["id"] = str(article["_id"])
    
    return articles


@router.post("/analyze")
async def analyze_query(request: AnalyzeRequest):
    """Analyze articles for a query (full pipeline)"""
    orchestrator = AgentOrchestrator()
    
    try:
        result = await orchestrator.analyze_query(
            query=request.query,
            date_from=request.date_from,
            date_to=request.date_to,
            sources=request.sources
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clusters/{cluster_id}", response_model=ClusterResponse)
async def get_cluster(cluster_id: str):
    """Get cluster details"""
    db = get_database()
    
    try:
        cluster = await db.clusters.find_one({"_id": ObjectId(cluster_id)})
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid cluster ID")
    
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    # Get articles for this cluster
    articles = await db.articles.find({"cluster_id": cluster_id}).to_list(length=100)
    for article in articles:
        article["id"] = str(article["_id"])
    
    cluster["id"] = str(cluster["_id"])
    cluster["articles"] = articles
    
    return cluster


@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: str):
    """Get article details"""
    db = get_database()
    
    try:
        article = await db.articles.find_one({"_id": ObjectId(article_id)})
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid article ID")
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article["id"] = str(article["_id"])
    
    return article
