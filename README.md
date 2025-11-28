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
- **Database**: PostgreSQL for metadata, Pinecone/Weaviate for vectors
- **NLP**: spaCy for NER, Hugging Face transformers for sentiment, sentence-transformers for embeddings
- **LLM**: OpenAI/Anthropic for fact verification and summarization

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Pinecone account (or Weaviate)
- NewsAPI account
- OpenAI API key

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
# Edit .env with your API keys
alembic upgrade head  # Create database tables
python run.py  # or: python -m uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your backend URL (default: http://localhost:8000/api/v1)
npm run dev
```

### Environment Variables

See `.env.example` files in both `backend/` and `frontend/` directories.

For detailed setup instructions, see [SETUP.md](SETUP.md).

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

- `POST /api/search` - Search for articles by query
- `GET /api/clusters/{cluster_id}` - Get cluster details
- `GET /api/articles/{article_id}` - Get article details
- `POST /api/analyze` - Trigger analysis for a query
- `GET /api/bias/{cluster_id}` - Get bias scores for a cluster

## License

MIT

