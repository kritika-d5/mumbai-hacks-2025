# LLM Prompt Templates

This document contains the prompt templates used in NewsPrism for fact verification, framing extraction, and summarization.

## Fact Verification Prompt

Used by `FactExtractor` to verify facts across multiple sources.

```
You are a fact verification assistant. Given a candidate fact and excerpts from multiple sources, determine:

1. Is the fact (A) Supported - appears verbatim or clearly implied by at least one reliable source
2. (B) Contradicted - some sources claim the opposite
3. (C) Unverified - no sufficient evidence

Candidate fact: {fact_text}

Sources:
{source_excerpts}

Return your analysis in this format:
STATUS: [A/B/C]
JUSTIFICATION: [1-line explanation]
QUOTES: [up to 2 supporting quotes with source URLs]
```

## Framing Extraction Prompt

Used to extract biased phrases and framing from articles.

```
Given the article excerpt, list phrases that express opinion, emotion, or interpretation (max 8). 

For each phrase, classify as [emotive|interpretive|prescriptive|loaded] and give a 4-word reason.

Article excerpt:
{article_text}

Return in format:
PHRASE: [phrase text]
TYPE: [emotive|interpretive|prescriptive|loaded]
REASON: [4-word explanation]
```

## Fact Summary Generation

Used to generate concise fact summaries from verified facts.

```
Summarize the following verified facts into a concise fact summary (3-5 sentences):

{facts_list}

Return only the summary, no additional commentary.
```

## Frame Summary Generation

Used to generate per-source framing summaries.

```
For each source in this cluster, provide:
1. Overall tone (positive/negative/neutral)
2. Key framing techniques used
3. Notable omissions or emphasis

Sources and their articles:
{sources_data}

Return a structured summary for each source.
```

## Usage in Code

These prompts are used in:
- `app/services/facts/fact_extractor.py` - Fact verification
- `app/services/agents/orchestrator.py` - Summary generation
- Future: Framing extraction service

## Customization

You can customize these prompts by:
1. Modifying the prompt strings in the respective service files
2. Adding system messages for better control
3. Using structured outputs (JSON mode) for more reliable parsing
4. Fine-tuning temperature and max_tokens for different use cases

