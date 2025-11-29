# Grok to Groq Migration

All references to Grok (xAI) have been replaced with Groq throughout the codebase.

## Changes Made

### 1. Configuration (`backend/app/core/config.py`)
- Changed `GROK_API_KEY` → `GROQ_API_KEY`
- Changed `GROK_API_URL` from `https://api.x.ai/v1` → `https://api.groq.com/openai/v1`

### 2. Agent Orchestrator (`backend/app/services/agents/orchestrator.py`)
- Updated all `grok_api_key` → `groq_api_key`
- Updated all `grok_api_url` → `groq_api_url`
- Changed model from `grok-2` → `mixtral-8x7b-32768` (Groq model)
- Updated comments and error messages

### 3. Fact Extractor (`backend/app/services/facts/fact_extractor.py`)
- Updated all `grok_api_key` → `groq_api_key`
- Updated all `grok_api_url` → `groq_api_url`
- Changed model from `grok-2` → `mixtral-8x7b-32768` (Groq model)
- Updated comments and error messages

### 4. Requirements (`backend/requirements.txt`)
- Updated comment from "Grok API" → "Groq API"

### 5. Documentation (`RUN_INSTRUCTIONS.md`)
- Updated all references from Grok → Groq
- Updated API key URL from `https://x.ai/api` → `https://console.groq.com/keys`
- Updated environment variable names in examples

## Environment Variables

Update your `.env` file:

```env
# Old (Grok)
GROK_API_KEY=your-key-here
GROK_API_URL=https://api.x.ai/v1

# New (Groq)
GROQ_API_KEY=your-key-here
GROQ_API_URL=https://api.groq.com/openai/v1
```

## Groq API Setup

1. **Get API Key**: Visit https://console.groq.com/keys
2. **Create an account** (if you don't have one)
3. **Generate an API key**
4. **Update your `.env` file** with:
   ```
   GROQ_API_KEY=your-actual-groq-api-key-here
   ```

## Available Groq Models

The code uses `mixtral-8x7b-32768` by default. Other available models include:
- `mixtral-8x7b-32768` (current default - fast and capable)
- `llama2-70b-4096`
- `gemma-7b-it`
- `llama-3-70b-8192`

To change the model, update the `model` field in:
- `backend/app/services/agents/orchestrator.py` (line ~285)
- `backend/app/services/facts/fact_extractor.py` (line ~107)

## API Compatibility

Groq uses OpenAI-compatible API endpoints, so the code structure remains the same. Only the URL and model names changed.

## Next Steps

1. Update your `backend/.env` file with the new variable names
2. Get your Groq API key from https://console.groq.com/keys
3. Restart your backend server
4. Test the API calls to ensure everything works

