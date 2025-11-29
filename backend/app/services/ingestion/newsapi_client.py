import httpx
from typing import List, Dict, Optional
from datetime import datetime
from app.core.config import settings


class NewsAPIClient:
    def __init__(self):
        self.api_key = settings.NEWSAPI_KEY
        self.base_url = "https://newsapi.org/v2"
    
    async def search_articles(
        self,
        query: str,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        sources: Optional[List[str]] = None,
        language: str = "en",
        page_size: int = 100
    ) -> List[Dict]:
        """Search for articles using NewsAPI"""
        async with httpx.AsyncClient() as client:
            params = {
                "apiKey": self.api_key,
                "q": query,
                "language": language,
                "pageSize": min(page_size, 100),
                "sortBy": "publishedAt",
                "searchIn": "title,description"  # Restrict search to title/desc for better relevance
            }
            
            if date_from:
                params["from"] = date_from.strftime("%Y-%m-%d")
            if date_to:
                params["to"] = date_to.strftime("%Y-%m-%d")
            if sources:
                params["sources"] = ",".join(sources)
            
            try:
                response = await client.get(
                    f"{self.base_url}/everything",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "ok":
                    return data.get("articles", [])
                else:
                    raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            except httpx.HTTPError as e:
                raise Exception(f"NewsAPI request failed: {str(e)}")
    
    async def get_top_headlines(
        self,
        country: str = "us",
        category: Optional[str] = None,
        sources: Optional[List[str]] = None,
        page_size: int = 100
    ) -> List[Dict]:
        """Get top headlines from NewsAPI"""
        async with httpx.AsyncClient() as client:
            params = {
                "apiKey": self.api_key,
                "pageSize": min(page_size, 100)
            }
            
            if country:
                params["country"] = country
            if category:
                params["category"] = category
            if sources:
                params["sources"] = ",".join(sources)
            
            try:
                response = await client.get(
                    f"{self.base_url}/top-headlines",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "ok":
                    return data.get("articles", [])
                else:
                    raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            except httpx.HTTPError as e:
                raise Exception(f"NewsAPI request failed: {str(e)}")