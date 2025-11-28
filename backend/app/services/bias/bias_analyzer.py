from typing import Dict, List
import numpy as np
from transformers import pipeline
import spacy
from app.core.config import settings


class BiasAnalyzer:
    def __init__(self):
        # Load sentiment analysis model
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=-1  # CPU
        )
        
        # Load spaCy for NLP features
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Loaded language patterns
        self.loaded_patterns = {
            "emotive": ["shocking", "devastating", "tragic", "outrageous", "scandalous"],
            "prescriptive": ["must", "should", "ought", "need to"],
            "hedging": ["perhaps", "maybe", "possibly", "might", "could"],
            "intensifiers": ["very", "extremely", "incredibly", "absolutely"]
        }
    
    def analyze_article(self, text: str) -> Dict:
        """Analyze bias in an article"""
        # Tone analysis (sentiment)
        tone_score = self._analyze_tone(text)
        
        # Lexical bias
        lexical_bias = self._analyze_lexical_bias(text)
        
        # Subjectivity
        subjectivity = self._analyze_subjectivity(text)
        
        return {
            "tone_score": tone_score,
            "lexical_bias_score": lexical_bias,
            "subjectivity_score": subjectivity,
            "loaded_phrases": self._extract_loaded_phrases(text)
        }
    
    def _analyze_tone(self, text: str) -> float:
        """Analyze sentiment/tone (-1 to 1)"""
        # Split into sentences for better analysis
        sentences = text.split('.')[:10]  # Limit for performance
        
        if not sentences:
            return 0.0
        
        scores = []
        for sentence in sentences:
            if len(sentence.strip()) < 10:
                continue
            
            try:
                result = self.sentiment_pipeline(sentence[:512])[0]
                label = result['label'].lower()
                score = result['score']
                
                # Map to -1 to 1 scale
                if 'positive' in label:
                    scores.append(score)
                elif 'negative' in label:
                    scores.append(-score)
                else:
                    scores.append(0)
            except:
                continue
        
        if not scores:
            return 0.0
        
        return np.mean(scores)
    
    def _analyze_lexical_bias(self, text: str) -> float:
        """Analyze lexical bias (0 to 1)"""
        if not self.nlp:
            return self._simple_lexical_bias(text)
        
        doc = self.nlp(text.lower())
        total_tokens = len([t for t in doc if t.is_alpha])
        
        if total_tokens == 0:
            return 0.0
        
        loaded_count = 0
        
        # Check for loaded language patterns
        for pattern_type, words in self.loaded_patterns.items():
            for word in words:
                loaded_count += text.lower().count(word)
        
        # Check for adjectives and adverbs (indicators of opinion)
        adj_adv_count = len([t for t in doc if t.pos_ in ['ADJ', 'ADV']])
        
        # Combine metrics
        lexical_score = min(
            (loaded_count * 2 + adj_adv_count * 0.1) / total_tokens,
            1.0
        )
        
        return lexical_score
    
    def _simple_lexical_bias(self, text: str) -> float:
        """Simple lexical bias without spaCy"""
        words = text.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        loaded_count = 0
        for pattern_type, pattern_words in self.loaded_patterns.items():
            for word in pattern_words:
                loaded_count += words.count(word)
        
        return min(loaded_count / total_words, 1.0)
    
    def _analyze_subjectivity(self, text: str) -> float:
        """Analyze subjectivity (0 to 1)"""
        # Simple heuristic: ratio of opinion indicators
        opinion_indicators = [
            "i think", "i believe", "in my opinion", "seems", "appears",
            "likely", "probably", "suggests", "indicates"
        ]
        
        text_lower = text.lower()
        indicator_count = sum(1 for indicator in opinion_indicators if indicator in text_lower)
        
        # Normalize by text length
        sentences = text.split('.')
        return min(indicator_count / max(len(sentences), 1), 1.0)
    
    def _extract_loaded_phrases(self, text: str, max_phrases: int = 8) -> List[Dict]:
        """Extract loaded/biased phrases from text"""
        phrases = []
        
        if not self.nlp:
            return phrases
        
        doc = self.nlp(text)
        
        # Find phrases with loaded words
        for sent in doc.sents:
            sent_text = sent.text.lower()
            
            for pattern_type, words in self.loaded_patterns.items():
                for word in words:
                    if word in sent_text:
                        # Extract the sentence or phrase
                        phrases.append({
                            "phrase": sent.text[:100],  # Truncate
                            "type": pattern_type,
                            "reason": f"Contains {pattern_type} language"
                        })
                        
                        if len(phrases) >= max_phrases:
                            return phrases
        
        return phrases[:max_phrases]
    
    def compute_bias_index(
        self,
        tone_score: float,
        lexical_bias: float,
        omission_score: float,
        consistency_score: float,
        cluster_mean_tone: float
    ) -> float:
        """Compute Bias Index (0 to 100)"""
        # Tone deviation from cluster mean
        tone_deviation = abs(tone_score - cluster_mean_tone)
        
        # Weighted combination
        bias_mag = (
            settings.BIAS_WEIGHT_TONE * tone_deviation +
            settings.BIAS_WEIGHT_LEXICAL * lexical_bias +
            settings.BIAS_WEIGHT_OMISSION * omission_score +
            settings.BIAS_WEIGHT_CONSISTENCY * consistency_score
        )
        
        # Normalize to 0-100 (assuming max possible is around 2.0)
        bias_index = min(100 * (bias_mag / 2.0), 100)
        
        return bias_index
    
    def compute_transparency_score(
        self,
        omission_score: float,
        consistency_score: float,
        lexical_bias: float
    ) -> float:
        """Compute Transparency Score (0 to 100)"""
        # Higher transparency = lower omissions, conflicts, loaded language
        transparency = 100 * (
            1 - (
                0.4 * omission_score +
                0.4 * consistency_score +
                0.2 * lexical_bias
            )
        )
        
        return max(0, min(100, transparency))

