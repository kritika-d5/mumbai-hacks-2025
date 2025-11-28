from typing import List, Optional, Dict
from datetime import datetime
from app.services.ingestion.newsapi_client import NewsAPIClient
from app.services.ingestion.scraper import ArticleScraper
from app.models.article import Article
from app.core.database import get_database
from bson import ObjectId


class IngestionService:
    def __init__(self):
        self.newsapi = NewsAPIClient()
        self.scraper = ArticleScraper()
    
    async def ingest_from_query(
        self,
        query: str,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        sources: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict]:
        """Ingest articles from NewsAPI based on a query"""
        db = get_database()
        articles = []
        
        try:
            # Fetch from NewsAPI
            newsapi_articles = await self.newsapi.search_articles(
                query=query,
                date_from=date_from,
                date_to=date_to,
                sources=sources,
                page_size=limit
            )
            
            for article_data in newsapi_articles:
                try:
                    url = article_data.get("url")
                    if not url:
                        continue
                    
                    # Check if article already exists
                    existing = await db.articles.find_one({"url": url})
                    if existing:
                        articles.append(existing)
                        continue
                    
                    # Scrape full content if URL is available
                    scraped_content = None
                    if url:
                        scraped_content = await self.scraper.scrape_article(url)
                    
                    # Create article record
                    article_dict = {
                        "source": article_data.get("source", {}).get("name", "Unknown"),
                        "url": url,
                        "title": article_data.get("title", "Untitled"),
                        "author": article_data.get("author"),
                        "published_at": self._parse_date(article_data.get("publishedAt")),
                        "text": scraped_content.get("text") if scraped_content else article_data.get("description", ""),
                        "raw_html": scraped_content.get("raw_html") if scraped_content else None,
                        "language": "en",  # Default, can be detected later
                        "country": None,
                        "scraped_at": datetime.utcnow(),
                        "chunks": None,
                        "ner_entities": None,
                        "tone_score": None,
                        "lexical_bias_score": None,
                        "omission_score": None,
                        "consistency_score": None,
                        "bias_index": None,
                        "cluster_id": None
                    }
                    
                    # Insert into MongoDB
                    result = await db.articles.insert_one(article_dict)
                    article_dict["_id"] = result.inserted_id
                    article_dict["id"] = str(result.inserted_id)
                    articles.append(article_dict)
                    
                except Exception as e:
                    print(f"Error processing article {url}: {str(e)}")
                    continue
            
            return articles
            
        except Exception as e:
            print(f"Error in ingestion: {str(e)}")
            return articles
    
    def _parse_date(self, date_str: Optional[str]) -> datetime:
        """Parse date string from NewsAPI format"""
        if not date_str:
            return datetime.utcnow()
        
        try:
            # NewsAPI format: "2024-01-15T12:00:00Z"
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.utcnow()
