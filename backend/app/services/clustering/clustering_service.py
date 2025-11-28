from typing import List, Dict, Optional
import numpy as np
from sklearn.cluster import DBSCAN
from app.services.embeddings.vector_store import VectorStore
from app.services.embeddings.embedding_service import EmbeddingService
from app.core.config import settings


class ClusteringService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding_service = EmbeddingService()
    
    def cluster_articles(
        self,
        query: str,
        article_ids: List[str],
        min_samples: Optional[int] = None,
        eps: Optional[float] = None
    ) -> Dict[str, List[str]]:
        """Cluster articles by semantic similarity
        
        Returns:
            Dict mapping cluster_id to list of article_ids
        """
        if not article_ids:
            return {}
        
        # Get embeddings for all articles
        embeddings = []
        article_metadata = []
        
        for article_id in article_ids:
            # Query vector store for article chunks
            # In a real implementation, you'd fetch the stored embeddings
            # For now, we'll need to re-embed or fetch from vector store
            
            # This is a simplified version - in production, you'd store
            # article embeddings when ingesting
            pass
        
        # For MVP, we'll embed article texts and cluster them
        # In production, you'd fetch stored embeddings from vector DB
        article_texts = []
        article_map = {}
        
        # Fetch article texts (in production, get from DB)
        # For now, we'll need to re-embed - this is simplified
        # In real implementation, store article-level embeddings when ingesting
        
        # Query vector store with the query embedding to get similar articles
        query_embedding = self.embedding_service.embed_text(query)
        similar_articles = self.vector_store.query_vectors(
            query_vector=query_embedding,
            top_k=len(article_ids) * 2  # Get more to cluster
        )
        
        if not similar_articles:
            # Fallback: create single cluster
            return {"cluster_0": article_ids}
        
        # Group by article_id and get representative chunks
        article_chunks = {}
        for result in similar_articles:
            article_id = result["metadata"].get("article_id")
            if article_id and article_id in article_ids:
                if article_id not in article_chunks:
                    article_chunks[article_id] = []
                article_chunks[article_id].append({
                    "text": result["metadata"].get("text", ""),
                    "score": result["score"]
                })
        
        # Get best chunk per article (highest similarity)
        article_embeddings = []
        article_map = {}
        
        for article_id, chunks in article_chunks.items():
            if chunks:
                # Use the chunk with highest score
                best_chunk = max(chunks, key=lambda x: x["score"])
                # Re-embed the chunk text (or use stored embedding)
                embedding = self.embedding_service.embed_text(best_chunk["text"][:512])
                article_embeddings.append(embedding)
                article_map[len(article_embeddings) - 1] = article_id
        
        if len(article_embeddings) < 2:
            # Not enough articles to cluster
            return {"cluster_0": article_ids}
        
        # Convert to numpy array
        X = np.array(article_embeddings)
        
        # Perform DBSCAN clustering
        min_samples = min_samples or settings.CLUSTERING_MIN_SAMPLES
        eps = eps or settings.CLUSTERING_EPS
        
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        cluster_labels = clustering.fit_predict(X)
        
        # Group articles by cluster
        clusters = {}
        for idx, label in enumerate(cluster_labels):
            if label == -1:  # Noise point, assign to its own cluster
                cluster_id = f"cluster_noise_{idx}"
            else:
                cluster_id = f"cluster_{label}"
            
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            
            article_id = article_map.get(idx)
            if article_id:
                clusters[cluster_id].append(article_id)
        
        return clusters
    
    def find_canonical_article(
        self,
        article_ids: List[str],
        articles_data: List[Dict]
    ) -> Optional[str]:
        """Find the canonical (best representative) article for a cluster"""
        if not article_ids or not articles_data:
            return None
        
        # Score articles by:
        # 1. Completeness (length)
        # 2. Metadata quality (has author, date, etc.)
        # 3. Early publication (first to report)
        
        best_score = -1
        best_article_id = None
        
        for article in articles_data:
            if article.get("id") not in article_ids:
                continue
            
            score = 0
            
            # Completeness
            text_length = len(article.get("text", ""))
            score += min(text_length / 1000, 1.0) * 0.3
            
            # Metadata quality
            if article.get("author"):
                score += 0.2
            if article.get("published_at"):
                score += 0.2
            
            # Early publication (inverse - earlier is better)
            # This would need actual date comparison in production
            
            if score > best_score:
                best_score = score
                best_article_id = article.get("id")
        
        return best_article_id or article_ids[0]

