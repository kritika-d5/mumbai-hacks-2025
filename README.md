# NewsPrism

A comprehensive news analysis platform that detects bias, extracts facts, and shows how different outlets frame the same events.

## Features

- **Multi-source news aggregation** from NewsAPI and custom scrapers
- **Semantic clustering** of articles covering the same events
- **Bias detection** using sentiment analysis, lexical analysis, and omission detection
- **Fact extraction** with cross-source verification
- **Interactive dashboard** showing fact summaries vs. framing analysis
- **Bias Index & Transparency Scores** for each source

## Architecture

- **Backend**: FastAPI (Python) with LangChain agent orchestration
- **Frontend**: React with Chart.js for visualizations
- **Database**: MongoDB for metadata, Pinecone for vectors
- **NLP**: spaCy for NER, Hugging Face transformers for sentiment, sentence-transformers for embeddings
- **LLM**: Groq (llama-3.3-70b-versatile) for fact verification and summarization

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB (local or Atlas)
- Pinecone account (for vector storage)
- NewsAPI account
- Groq API key

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
# Create .env file (see RUN_INSTRUCTIONS.md for template)
# Edit .env with your API keys (MongoDB, Pinecone, Groq, NewsAPI)
python run.py  # or: python -m uvicorn app.main:app --reload
```

**Note**: MongoDB doesn't require migrations. Make sure MongoDB is running before starting the backend.

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your backend URL (default: http://localhost:8000/api/v1)
npm run dev
```

### Environment Variables

Create a `.env` file in `backend/` with:
- `MONGODB_URL` - MongoDB connection string (default: `mongodb://localhost:27017`)
- `PINECONE_API_KEY` - Your Pinecone API key
- `GROQ_API_KEY` - Your Groq API key (get from https://console.groq.com/keys)
- `NEWSAPI_KEY` - Your NewsAPI key

For detailed setup instructions, see [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md) or [SETUP.md](SETUP.md).

## Project Structure

```
newsprism/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── core/         # Config, database, security
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   │   ├── ingestion/    # News scraping
│   │   │   ├── embeddings/   # Vector embeddings
│   │   │   ├── clustering/   # Event clustering
│   │   │   ├── bias/         # Bias analysis
│   │   │   ├── facts/        # Fact extraction
│   │   │   └── agents/       # LangChain agents
│   │   └── schemas/      # Pydantic schemas
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API clients
│   │   └── utils/        # Utilities
│   └── package.json
└── README.md
```

## API Endpoints

- `GET /` - API root
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `POST /api/v1/search` - Search for articles by query
- `POST /api/v1/search/analyze` - Trigger full analysis pipeline for a query
- `GET /api/v1/search/clusters/{cluster_id}` - Get cluster details
- `GET /api/v1/search/articles/{article_id}` - Get article details

## Tech Stack

- **Backend**: FastAPI, Pydantic v2, MongoDB (Motor), Pinecone, Groq
- **Frontend**: React, Vite, Tailwind CSS, Chart.js
- **ML/NLP**: spaCy, Hugging Face Transformers, Sentence Transformers

## Getting API Keys

1. **Groq**: https://console.groq.com/keys (for LLM features)
2. **Pinecone**: https://www.pinecone.io (for vector storage)
3. **NewsAPI**: https://newsapi.org (for news articles)

## Quick Troubleshooting

- **Backend won't start**: Check `.env` file exists and MongoDB is running
- **Import errors**: Make sure you've installed dependencies: `pip install -r requirements.txt`
- **Missing modules**: Install spaCy model: `python -m spacy download en_core_web_sm`
- **CORS errors**: Backend defaults allow `localhost:3000` and `localhost:5173`
- **Pinecone errors**: Make sure your Pinecone index exists and API key is correct

For more detailed troubleshooting, see [RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md).

## Documentation

- [SETUP.md](SETUP.md) - Complete setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture details

## License

MIT

