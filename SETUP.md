# NewsPrism Setup Guide

Complete setup instructions for NewsPrism.

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Pinecone account (or Weaviate)
- NewsAPI account
- OpenAI API key

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with:
- `DATABASE_URL`: PostgreSQL connection string
- `PINECONE_API_KEY`: Your Pinecone API key
- `OPENAI_API_KEY`: Your OpenAI API key
- `NEWSAPI_KEY`: Your NewsAPI key

### 4. Set Up Database

Create PostgreSQL database:

```sql
CREATE DATABASE newsprism;
```

Run migrations:

```bash
alembic upgrade head
```

### 5. Run Backend

```bash
python -m uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set `VITE_API_URL` to your backend URL (default: `http://localhost:8000/api/v1`)

### 3. Run Frontend

```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## Pinecone Setup

1. Create account at https://www.pinecone.io
2. Create a new index:
   - Name: `newsprism-vectors`
   - Dimension: `384` (for all-MiniLM-L6-v2)
   - Metric: `cosine`
3. Copy your API key to `.env`

## Testing the System

1. Start backend: `cd backend && python -m uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser to `http://localhost:3000`
4. Enter a search query (e.g., "climate change")
5. Click "Analyze News"
6. Wait for analysis to complete
7. View clusters and bias analysis

## API Documentation

Once backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Verify database exists: `psql -l | grep newsprism`

### Pinecone Issues

- Verify API key is correct
- Check index name matches in `.env`
- Ensure index dimension is 384

### spaCy Model Not Found

```bash
python -m spacy download en_core_web_sm
```

### Import Errors

Ensure you're in the correct directory and virtual environment is activated.

## Production Deployment

### Backend

- Use a production ASGI server (e.g., Gunicorn with Uvicorn workers)
- Set up proper environment variables
- Use a managed PostgreSQL database
- Set up monitoring and logging

### Frontend

- Build for production: `npm run build`
- Deploy to Vercel, Netlify, or similar
- Configure environment variables in deployment platform

## Next Steps

- Fine-tune bias detection models
- Add more news sources
- Implement user feedback system
- Add authentication
- Set up scheduled ingestion jobs

