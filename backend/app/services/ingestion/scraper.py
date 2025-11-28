import aiohttp
from bs4 import BeautifulSoup
from newspaper import Article as NewspaperArticle
from typing import Optional, Dict
import re
from datetime import datetime


class ArticleScraper:
    """Scraper for extracting article content from URLs"""
    
    @staticmethod
    async def scrape_article(url: str) -> Optional[Dict]:
        """Scrape article content from a URL"""
        try:
            # Use newspaper3k for article extraction
            article = NewspaperArticle(url)
            article.download()
            article.parse()
            
            if not article.text or len(article.text) < 100:
                # Fallback to BeautifulSoup
                return await ArticleScraper._scrape_with_bs4(url)
            
            return {
                "title": article.title,
                "text": article.text,
                "author": ", ".join(article.authors) if article.authors else None,
                "published_at": article.publish_date or datetime.utcnow(),
                "raw_html": article.html,
                "images": article.images,
                "keywords": article.keywords
            }
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            # Fallback to BeautifulSoup
            return await ArticleScraper._scrape_with_bs4(url)
    
    @staticmethod
    async def _scrape_with_bs4(url: str) -> Optional[Dict]:
        """Fallback scraper using BeautifulSoup"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Try to find title
                    title = None
                    if soup.title:
                        title = soup.title.get_text()
                    elif soup.find("h1"):
                        title = soup.find("h1").get_text()
                    
                    # Extract main content
                    # Try common article selectors
                    content_selectors = [
                        'article',
                        '[role="article"]',
                        '.article-content',
                        '.post-content',
                        '.entry-content',
                        'main',
                        '.content'
                    ]
                    
                    text = ""
                    for selector in content_selectors:
                        content = soup.select_one(selector)
                        if content:
                            text = content.get_text(separator=' ', strip=True)
                            break
                    
                    if not text:
                        # Fallback to body text
                        text = soup.get_text(separator=' ', strip=True)
                    
                    # Clean up text
                    text = re.sub(r'\s+', ' ', text)
                    
                    # Try to find author
                    author = None
                    author_selectors = [
                        '[rel="author"]',
                        '.author',
                        '[itemprop="author"]',
                        'meta[name="author"]'
                    ]
                    for selector in author_selectors:
                        author_elem = soup.select_one(selector)
                        if author_elem:
                            author = author_elem.get_text() if hasattr(author_elem, 'get_text') else author_elem.get('content')
                            break
                    
                    # Try to find publish date
                    published_at = datetime.utcnow()
                    date_selectors = [
                        'time[datetime]',
                        '[itemprop="datePublished"]',
                        'meta[property="article:published_time"]'
                    ]
                    for selector in date_selectors:
                        date_elem = soup.select_one(selector)
                        if date_elem:
                            date_str = date_elem.get('datetime') or date_elem.get('content')
                            if date_str:
                                try:
                                    published_at = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                                except:
                                    pass
                            break
                    
                    return {
                        "title": title or "Untitled",
                        "text": text,
                        "author": author,
                        "published_at": published_at,
                        "raw_html": html
                    }
        except Exception as e:
            print(f"Error in BS4 scrape for {url}: {str(e)}")
            return None

