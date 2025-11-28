from typing import List, Dict, Optional
import pinecone
from app.core.config import settings
import uuid


class VectorStore:
    def __init__(self):
        pinecone.init(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENVIRONMENT
        )
        self.index_name = settings.PINECONE_INDEX_NAME
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure the Pinecone index exists"""
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=settings.EMBEDDING_DIMENSION,
                metric="cosine"
            )
        
        self.index = pinecone.Index(self.index_name)
    
    def upsert_vectors(
        self,
        vectors: List[Dict],
        namespace: Optional[str] = None
    ):
        """Upsert vectors to Pinecone
        
        Args:
            vectors: List of dicts with 'id', 'values', and 'metadata'
            namespace: Optional namespace for the vectors
        """
        if not vectors:
            return
        
        # Format for Pinecone
        pinecone_vectors = []
        for vec in vectors:
            pinecone_vectors.append({
                "id": vec.get("id", str(uuid.uuid4())),
                "values": vec["values"],
                "metadata": vec.get("metadata", {})
            })
        
        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(pinecone_vectors), batch_size):
            batch = pinecone_vectors[i:i + batch_size]
            self.index.upsert(vectors=batch, namespace=namespace)
    
    def query_vectors(
        self,
        query_vector: List[float],
        top_k: int = 10,
        filter: Optional[Dict] = None,
        namespace: Optional[str] = None
    ) -> List[Dict]:
        """Query similar vectors from Pinecone"""
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter,
            namespace=namespace
        )
        
        return [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in results.matches
        ]
    
    def delete_vectors(
        self,
        ids: List[str],
        namespace: Optional[str] = None
    ):
        """Delete vectors by IDs"""
        if ids:
            self.index.delete(ids=ids, namespace=namespace)
    
    def delete_by_filter(
        self,
        filter: Dict,
        namespace: Optional[str] = None
    ):
        """Delete vectors by metadata filter"""
        self.index.delete(filter=filter, namespace=namespace)

