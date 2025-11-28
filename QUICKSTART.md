# NewsPrism Quick Start

Get NewsPrism running in 5 minutes.

## Prerequisites Check

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL running
- [ ] API keys ready (NewsAPI, OpenAI, Pinecone)

## Step 1: Backend Setup (2 minutes)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Configure environment
cp .env.example .env
# Edit .env with your keys

# Create database
createdb newsprism  # or use psql

# Run migrations
alembic upgrade head

# Start server
python run.py
```

Backend should be running at `http://localhost:8000`

## Step 2: Frontend Setup (1 minute)

```bash
cd frontend

# Install dependencies
npm install

# Configure (optional - defaults work)
cp .env.example .env

# Start dev server
npm run dev
```

Frontend should be running at `http://localhost:3000`

## Step 3: Test It (1 minute)

1. Open `http://localhost:3000`
2. Enter a query: "climate change"
3. Click "Analyze News"
4. Wait 30-60 seconds for analysis
5. View results!

## Troubleshooting

### Backend won't start
- Check `.env` file exists and has all keys
- Verify PostgreSQL is running: `psql -l`
- Check Python version: `python --version`

### Frontend won't start
- Check Node version: `node --version`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

### No articles found
- Verify NewsAPI key is correct
- Check NewsAPI quota hasn't been exceeded
- Try a different query

### Analysis fails
- Check OpenAI API key
- Verify Pinecone index exists and dimension is 384
- Check backend logs for errors

## Next Steps

- Read [SETUP.md](SETUP.md) for detailed setup
- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
- Customize bias weights in `backend/app/core/config.py`
- Add more news sources

## API Testing

Test the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Search
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "technology", "limit": 10}'

# View docs
open http://localhost:8000/docs
```

## Common Commands

```bash
# Backend
cd backend
python run.py                    # Start server
alembic upgrade head            # Run migrations
alembic revision --autogenerate # Create migration

# Frontend
cd frontend
npm run dev      # Development
npm run build    # Production build
npm run preview  # Preview build
```

