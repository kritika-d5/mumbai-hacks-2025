from typing import List, Dict
import spacy
import httpx
from app.core.config import settings


class FactExtractor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        self.groq_api_key = settings.GROQ_API_KEY
        self.groq_api_url = settings.GROQ_API_URL
    
    async def extract_facts_from_articles(
        self,
        articles: List[Dict]
    ) -> List[Dict]:
        """Extract facts from a list of articles"""
        # Step 1: Extract candidate facts using NER
        candidate_facts = self._extract_candidate_facts(articles)
        
        # Step 2: Verify facts across sources using LLM
        verified_facts = await self._verify_facts_with_llm(candidate_facts, articles)
        
        return verified_facts
    
    def _extract_candidate_facts(self, articles: List[Dict]) -> List[Dict]:
        """Extract candidate facts using NER"""
        if not self.nlp:
            return self._simple_fact_extraction(articles)
        
        facts = []
        
        for article in articles:
            text = article.get("text", "")
            doc = self.nlp(text)
            
            # Extract entities and key sentences
            entities = {}
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG", "GPE", "EVENT", "DATE"]:
                    if ent.label_ not in entities:
                        entities[ent.label_] = []
                    entities[ent.label_].append(ent.text)
            
            # Extract sentences with entities (likely factual)
            for sent in doc.sents:
                has_entity = any(ent in sent.text for ents in entities.values() for ent in ents)
                if has_entity and len(sent.text) > 20:
                    facts.append({
                        "fact": sent.text.strip(),
                        "source_url": article.get("url"),
                        "source_name": article.get("source"),
                        "entities": {k: list(set(v)) for k, v in entities.items()}
                    })
        
        return facts[:50]  # Limit for performance
    
    def _simple_fact_extraction(self, articles: List[Dict]) -> List[Dict]:
        """Simple fact extraction without spaCy"""
        facts = []
        
        for article in articles:
            text = article.get("text", "")
            sentences = text.split('.')
            
            for sent in sentences:
                if len(sent.strip()) > 30:
                    if any(c.isdigit() for c in sent) or any(c.isupper() for c in sent[:10]):
                        facts.append({
                            "fact": sent.strip(),
                            "source_url": article.get("url"),
                            "source_name": article.get("source"),
                            "entities": {}
                        })
        
        return facts[:50]
    
    async def _verify_facts_with_llm(
        self,
        candidate_facts: List[Dict],
        articles: List[Dict]
    ) -> List[Dict]:
        """Verify facts using LLM cross-checking"""
        verified_facts = []
        
        # Group similar facts
        fact_groups = self._group_similar_facts(candidate_facts)
        
        for fact_group in fact_groups[:20]:  # Limit for cost
            prompt = self._create_verification_prompt(fact_group, articles)
            
            try:
                # Use Groq API
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.groq_api_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.groq_api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            # CHANGED: Updated from mixtral-8x7b-32768 to llama-3.3-70b-versatile
                            "model": "llama-3.3-70b-versatile",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "You are a fact verification assistant. Analyze candidate facts and determine their status across sources."
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            "temperature": 0.1,
                            "max_tokens": 1000
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code != 200:
                        print(f"Groq API Error in Verification ({response.status_code}): {response.text}")
                        # Continue to next fact instead of crashing
                        continue

                    data = response.json()
                    
                    # Parse response
                    content = data["choices"][0]["message"]["content"]
                    result = self._parse_verification_response(
                        content,
                        fact_group,
                        articles
                    )
                
                if result:
                    verified_facts.append(result)
            
            except Exception as e:
                print(f"Error in LLM verification: {str(e)}")
                # Fallback: mark as unverified
                if fact_group:
                    verified_facts.append({
                        "fact": fact_group[0].get("fact", ""),
                        "sources": [f.get("source_url", "") for f in fact_group],
                        "quotes": [f.get("fact", "") for f in fact_group[:2]],
                        "status": "unverified"
                    })
        
        return verified_facts
    
    def _group_similar_facts(self, facts: List[Dict]) -> List[List[Dict]]:
        """Group similar facts together"""
        groups = []
        used = set()
        
        for i, fact in enumerate(facts):
            if i in used:
                continue
            
            group = [fact]
            used.add(i)
            
            fact_keywords = set(self._extract_keywords(fact.get("fact", "")))
            
            for j, other_fact in enumerate(facts[i+1:], start=i+1):
                if j in used:
                    continue
                
                other_keywords = set(self._extract_keywords(other_fact.get("fact", "")))
                
                # If significant overlap, group together
                overlap = len(fact_keywords & other_keywords)
                if overlap >= 2:
                    group.append(other_fact)
                    used.add(j)
            
            groups.append(group)
        
        return groups
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        words = text.lower().split()
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        return [w.strip('.,!?;:') for w in words if w.lower() not in stop_words and len(w) > 3]
    
    def _create_verification_prompt(
        self,
        fact_group: List[Dict],
        articles: List[Dict]
    ) -> str:
        """Create prompt for LLM fact verification"""
        fact_text = fact_group[0].get("fact", "")
        
        sources_text = "\n".join([
            f"Source: {f.get('source_name', 'Unknown')} ({f.get('source_url', '')})\n"
            f"Excerpt: {f.get('fact', '')[:200]}\n"
            for f in fact_group[:5]
        ])
        
        prompt = f"""You are a fact verification assistant. Given a candidate fact and excerpts from multiple sources, determine:

1. Is the fact (A) Supported - appears verbatim or clearly implied by at least one reliable source
2. (B) Contradicted - some sources claim the opposite
3. (C) Unverified - no sufficient evidence

Candidate fact: {fact_text}

Sources:
{sources_text}

Return your analysis in this format:
STATUS: [A/B/C]
JUSTIFICATION: [1-line explanation]
QUOTES: [up to 2 supporting quotes with source URLs]
"""
        return prompt
    
    def _parse_verification_response(
        self,
        response: str,
        fact_group: List[Dict],
        articles: List[Dict]
    ) -> Dict:
        """Parse LLM verification response"""
        lines = response.split('\n')
        
        status = "unverified"
        justification = ""
        quotes = []
        
        for line in lines:
            if line.startswith("STATUS:"):
                status_part = line.split(":", 1)[1].strip().upper()
                if "A" in status_part or "supported" in status_part.lower():
                    status = "supported"
                elif "B" in status_part or "contradicted" in status_part.lower():
                    status = "contradicted"
            elif line.startswith("JUSTIFICATION:"):
                justification = line.split(":", 1)[1].strip()
            elif line.startswith("QUOTES:"):
                quotes_text = line.split(":", 1)[1].strip()
                quotes = [q.strip() for q in quotes_text.split('\n') if q.strip()]
        
        if not quotes:
            quotes = [f.get("fact", "")[:100] for f in fact_group[:2]]
        
        sources = [f.get("source_url", "") for f in fact_group]
        
        return {
            "fact": fact_group[0].get("fact", ""),
            "sources": sources,
            "quotes": quotes,
            "status": status,
            "justification": justification
        }