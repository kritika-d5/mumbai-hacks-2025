from typing import List, Dict, Optional
from datetime import datetime
import httpx
from app.services.ingestion.ingestion_service import IngestionService
from app.services.clustering.clustering_service import ClusteringService
from app.services.bias.bias_analyzer import BiasAnalyzer
from app.services.bias.omission_detector import OmissionDetector
from app.services.facts.fact_extractor import FactExtractor
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.embeddings.vector_store import VectorStore
from app.core.config import settings
from app.models.article import Article, Cluster
from app.core.database import get_database
from bson import ObjectId


class AgentOrchestrator:
    def __init__(self):
        self.grok_api_key = settings.GROK_API_KEY
        self.grok_api_url = settings.GROK_API_URL
        
        self.ingestion_service = IngestionService()
        self.clustering_service = ClusteringService()
        self.bias_analyzer = BiasAnalyzer()
        self.omission_detector = OmissionDetector()
        self.fact_extractor = FactExtractor()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
    
    async def analyze_query(
        self,
        query: str,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        sources: Optional[List[str]] = None
    ) -> Dict:
        """Main orchestration method for analyzing a query"""
        db = get_database()
        
        try:
            # Step 1: Ingest articles
            print(f"Ingesting articles for query: {query}")
            articles = await self.ingestion_service.ingest_from_query(
                query=query,
                date_from=date_from,
                date_to=date_to,
                sources=sources,
                limit=50
            )
            
            if not articles:
                return {"error": "No articles found"}
            
            # Step 2: Embed and store in vector DB
            print("Embedding articles...")
            article_ids = [str(a.get("id") or a.get("_id")) for a in articles]
            await self._embed_and_store_articles(articles)
            
            # Step 3: Cluster articles
            print("Clustering articles...")
            clusters = self.clustering_service.cluster_articles(
                query=query,
                article_ids=article_ids
            )
            
            # Step 4: Process each cluster
            cluster_results = []
            
            for cluster_id, cluster_article_ids in clusters.items():
                cluster_articles = [
                    a for a in articles if str(a.get("id") or a.get("_id")) in cluster_article_ids
                ]
                
                if len(cluster_articles) < 2:
                    continue
                
                # Create cluster record
                cluster_data = {
                    "query": query,
                    "created_at": datetime.utcnow(),
                    "fact_summary": None,
                    "frame_summary": None,
                    "facts": None
                }
                cluster_result = await db.clusters.insert_one(cluster_data)
                cluster_id = str(cluster_result.inserted_id)
                
                # Step 5: Extract facts
                print(f"Extracting facts for cluster {cluster_id}...")
                articles_data = [
                    {
                        "id": str(a.get("id") or a.get("_id")),
                        "text": a.get("text", ""),
                        "url": a.get("url", ""),
                        "source": a.get("source", "Unknown")
                    }
                    for a in cluster_articles
                ]
                
                facts = await self.fact_extractor.extract_facts_from_articles(articles_data)
                
                # Step 6: Analyze bias for each article
                print(f"Analyzing bias for cluster {cluster_id}...")
                bias_results = []
                tone_scores = []
                
                for article in cluster_articles:
                    article_id = str(article.get("id") or article.get("_id"))
                    article_text = article.get("text", "")
                    
                    bias_analysis = self.bias_analyzer.analyze_article(article_text)
                    
                    # Detect omissions
                    omission_result = self.omission_detector.detect_omissions(
                        cluster_facts=facts,
                        article_text=article_text,
                        article_id=article_id
                    )
                    
                    tone_score = bias_analysis["tone_score"]
                    tone_scores.append(tone_score)
                    
                    # Compute consistency (simplified - would compare with other articles)
                    consistency_score = 0.1  # Placeholder
                    
                    # Compute cluster mean tone
                    cluster_mean_tone = sum(tone_scores) / len(tone_scores) if tone_scores else 0
                    
                    # Compute bias index
                    bias_index = self.bias_analyzer.compute_bias_index(
                        tone_score=tone_score,
                        lexical_bias=bias_analysis["lexical_bias_score"],
                        omission_score=omission_result["omission_score"],
                        consistency_score=consistency_score,
                        cluster_mean_tone=cluster_mean_tone
                    )
                    
                    # Compute transparency
                    transparency = self.bias_analyzer.compute_transparency_score(
                        omission_score=omission_result["omission_score"],
                        consistency_score=consistency_score,
                        lexical_bias=bias_analysis["lexical_bias_score"]
                    )
                    
                    # Update article with bias scores
                    await db.articles.update_one(
                        {"_id": ObjectId(article_id)},
                        {
                            "$set": {
                                "tone_score": tone_score,
                                "lexical_bias_score": bias_analysis["lexical_bias_score"],
                                "omission_score": omission_result["omission_score"],
                                "consistency_score": consistency_score,
                                "bias_index": bias_index,
                                "cluster_id": cluster_id
                            }
                        }
                    )
                    
                    bias_results.append({
                        "article_id": article_id,
                        "source": article.get("source", "Unknown"),
                        "tone": tone_score,
                        "lexical_bias": bias_analysis["lexical_bias_score"],
                        "omission_score": omission_result["omission_score"],
                        "bias_index": bias_index,
                        "transparency_score": transparency,
                        "loaded_phrases": bias_analysis["loaded_phrases"]
                    })
                
                # Step 7: Generate summaries
                print(f"Generating summaries for cluster {cluster_id}...")
                fact_summary = await self._generate_fact_summary(facts)
                frame_summary = self._generate_frame_summary(bias_results, articles_data)
                
                # Update cluster
                canonical_id = self.clustering_service.find_canonical_article(
                    article_ids=cluster_article_ids,
                    articles_data=articles_data
                )
                
                await db.clusters.update_one(
                    {"_id": ObjectId(cluster_id)},
                    {
                        "$set": {
                            "fact_summary": fact_summary,
                            "frame_summary": frame_summary,
                            "facts": facts,
                            "canonical_article_id": canonical_id
                        }
                    }
                )
                
                cluster_results.append({
                    "cluster_id": cluster_id,
                    "articles_count": len(cluster_articles),
                    "facts_count": len(facts),
                    "bias_results": bias_results
                })
            
            return {
                "query": query,
                "total_articles": len(articles),
                "clusters": cluster_results
            }
            
        except Exception as e:
            raise e
    
    async def _embed_and_store_articles(self, articles: List[Dict]):
        """Embed articles and store in vector DB"""
        vectors = []
        db = get_database()
        
        for article in articles:
            article_id = str(article.get("id") or article.get("_id"))
            article_text = article.get("text", "")
            article_source = article.get("source", "")
            published_at = article.get("published_at")
            
            # Chunk and embed article
            chunks = self.embedding_service.embed_article(article_text)
            
            # Store chunks in article metadata
            chunks_data = [
                {
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                    "start": chunk["start"],
                    "end": chunk["end"]
                }
                for chunk in chunks
            ]
            
            # Update article in MongoDB
            await db.articles.update_one(
                {"_id": ObjectId(article_id)},
                {"$set": {"chunks": chunks_data}}
            )
            
            # Prepare vectors for Pinecone
            for chunk in chunks:
                vectors.append({
                    "id": f"{article_id}_{chunk['chunk_id']}",
                    "values": chunk["embedding"],
                    "metadata": {
                        "article_id": article_id,
                        "chunk_id": chunk["chunk_id"],
                        "text": chunk["text"][:500],  # Truncate for metadata
                        "source": article_source,
                        "published_at": published_at.isoformat() if published_at else None
                    }
                })
        
        # Upsert to vector store
        if vectors:
            self.vector_store.upsert_vectors(vectors)
    
    async def _generate_fact_summary(self, facts: List[Dict]) -> str:
        """Generate fact summary using Grok LLM"""
        facts_text = "\n".join([
            f"- {f.get('fact', '')[:200]}"
            for f in facts[:10]
        ])
        
        prompt = f"""Summarize the following verified facts into a concise fact summary (3-5 sentences):

{facts_text}

Return only the summary, no additional commentary."""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.grok_api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.grok_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "grok-beta",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.1,
                        "max_tokens": 300
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except:
            return "Fact summary generation failed."
    
    def _generate_frame_summary(self, bias_results: List[Dict], articles: List[Dict]) -> List[Dict]:
        """Generate frame summary for each source"""
        frame_summaries = []
        
        for result in bias_results:
            frame_summaries.append({
                "source": result["source"],
                "tone": result["tone"],
                "bias_index": result["bias_index"],
                "transparency_score": result["transparency_score"],
                "top_phrases": result.get("loaded_phrases", [])[:5]
            })
        
        return frame_summaries

