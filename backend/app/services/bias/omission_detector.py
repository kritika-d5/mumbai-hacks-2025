from typing import List, Dict, Set
from app.services.facts.fact_extractor import FactExtractor


class OmissionDetector:
    def __init__(self):
        self.fact_extractor = FactExtractor()
    
    def detect_omissions(
        self,
        cluster_facts: List[Dict],
        article_text: str,
        article_id: str
    ) -> Dict:
        """Detect which facts are omitted from an article
        
        Args:
            cluster_facts: List of canonical facts for the cluster
            article_text: Text of the article to check
            article_id: ID of the article
        
        Returns:
            Dict with omission_score and missing_facts
        """
        if not cluster_facts:
            return {
                "omission_score": 0.0,
                "missing_facts": [],
                "present_facts": []
            }
        
        missing_facts = []
        present_facts = []
        
        article_lower = article_text.lower()
        
        for fact in cluster_facts:
            fact_text = fact.get("fact", "").lower()
            
            # Check if fact is mentioned in article
            # Simple keyword matching (can be improved with semantic similarity)
            fact_keywords = self._extract_keywords(fact_text)
            mentioned = any(
                keyword in article_lower
                for keyword in fact_keywords
                if len(keyword) > 3  # Ignore very short keywords
            )
            
            if mentioned:
                present_facts.append(fact)
            else:
                missing_facts.append(fact)
        
        # Omission score = fraction of facts missing
        omission_score = len(missing_facts) / len(cluster_facts) if cluster_facts else 0.0
        
        return {
            "omission_score": omission_score,
            "missing_facts": missing_facts,
            "present_facts": present_facts
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key terms from fact text"""
        # Simple extraction - in production, use NER or keyword extraction
        words = text.split()
        
        # Filter out common stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "is", "was", "are", "were", "be", "been", "being"
        }
        
        keywords = [w.lower().strip('.,!?;:') for w in words if w.lower() not in stop_words]
        
        return keywords[:10]  # Return top 10 keywords

