# How to Run NewsPrism

## Code Analysis Summary

### ✅ What's Correct
1. **Backend Structure**: Well-organized FastAPI application with proper separation of concerns
2. **Frontend Structure**: React + Vite setup is correct
3. **API Routes**: Routes are properly configured and match frontend expectations
4. **Database Setup**: MongoDB connection is properly configured
5. **CORS**: CORS middleware is correctly configured for frontend communication

### ⚠️ Issues Fixed
1. **API Keys Configuration**: Fixed to allow app startup even without all API keys (will fail when services are used, but server will start)
2. **Missing .env.example files**: Created documentation below (files may be gitignored)

### 📝 Notes
- The README mentions PostgreSQL, but the code uses **MongoDB** (this is correct - the code uses MongoDB)
- The README mentions OpenAI, but the code uses **Groq** API
- No database migrations needed for MongoDB (it's schema-less)

## Prerequisites

Before running, ensure you have:

- **Python 3.10+** installed
- **Node.js 18+** installed
- **MongoDB** running (local or remote)
- **API Keys**:
  - Pinecone API key (for vector storage)
  - Groq API key - for LLM features
  - NewsAPI key - for fetching news articles

## Step 1: Backend Setup

### 1.1 Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 1.2 Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 1.3 Create Environment File

Create a file named `.env` in the `backend/` directory with the following content:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=newsprism

# Vector Database (Pinecone)
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=newsprism-vectors

# Groq API
GROQ_API_KEY=your-groq-api-key-here
GROQ_API_URL=https://api.groq.com/openai/v1

# NewsAPI
NEWSAPI_KEY=your-newsapi-key-here

# Redis (Optional - for caching)
REDIS_URL=redis://localhost:6379/0

# Security (Optional)
SECRET_KEY=change-this-in-production-for-jwt-tokens
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important**: Replace the placeholder values with your actual API keys:
- Get Pinecone API key: https://www.pinecone.io
- Get Groq API key: https://console.groq.com/keys
- Get NewsAPI key: https://newsapi.org

### 1.4 Set Up MongoDB

Make sure MongoDB is running:

**Windows:**
```bash
# If MongoDB is installed as a service, it should be running automatically
# Check with: services.msc (look for MongoDB service)

# Or start manually:
mongod --dbpath "C:\data\db"
```

**Linux/Mac:**
```bash
# Start MongoDB service
sudo systemctl start mongod
# OR
mongod
```

**Using MongoDB Atlas (Cloud):**
- Update `MONGODB_URL` in `.env` to your Atlas connection string

### 1.5 Run Backend Server

```bash
# From backend directory
python run.py
```

OR

```bash
python -m uvicorn app.main:app --reload
```

The backend should now be running at: **http://localhost:8000**

You can verify by visiting:
- API Root: http://localhost:8000/
- Health Check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

## Step 2: Frontend Setup

### 2.1 Install Node Dependencies

Open a **new terminal** window/tab:

```bash
cd frontend
npm install
```

### 2.2 Create Environment File (Optional)

Create a file named `.env` in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

**Note**: This is optional - the frontend defaults to this URL if not specified.

### 2.3 Run Frontend Development Server

```bash
npm run dev
```

The frontend should now be running at: **http://localhost:3000** (or check the terminal output for the exact port)

## Step 3: Test the Application

1. Open your browser and go to: **http://localhost:3000**
2. Enter a search query (e.g., "climate change", "technology", etc.)
3. Click "Analyze News"
4. Wait for the analysis to complete (30-60 seconds)
5. View the results with bias analysis and clustering

## Troubleshooting

### Backend Issues

**Problem: Backend won't start - missing API keys**
- **Solution**: Create a `.env` file in the `backend/` directory with at least empty strings for API keys. The server will start but services requiring keys will fail when used.

**Problem: MongoDB connection error**
- **Solution**: 
  - Check if MongoDB is running: `mongosh` or `mongo` command
  - Verify `MONGODB_URL` in `.env` is correct
  - For Atlas: Check connection string and IP whitelist

**Problem: Module not found errors**
- **Solution**: 
  ```bash
  cd backend
  pip install -r requirements.txt
  ```

**Problem: spaCy model not found**
- **Solution**: 
  ```bash
  python -m spacy download en_core_web_sm
  ```

### Frontend Issues

**Problem: Frontend won't start**
- **Solution**:
  ```bash
  cd frontend
  rm -rf node_modules package-lock.json
  npm install
  ```

**Problem: Can't connect to backend API**
- **Solution**: 
  - Verify backend is running on port 8000
  - Check `VITE_API_URL` in frontend `.env` matches backend URL
  - Check browser console for CORS errors (backend CORS should allow localhost:3000)

**Problem: No articles found**
- **Solution**:
  - Verify NewsAPI key is correct in backend `.env`
  - Check NewsAPI quota hasn't been exceeded
  - Try a different query

### API Issues

**Problem: Analysis fails with API errors**
- **Solution**:
  - Check Pinecone API key and index name
  - Verify Groq API key is valid
  - Check backend logs for specific error messages

## Running Both Services Together

You need **two terminal windows**:

**Terminal 1 (Backend):**
```bash
cd backend
python run.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## Quick Command Reference

```bash
# Backend
cd backend
python run.py                    # Start backend server
python -m spacy download en_core_web_sm  # Download spaCy model

# Frontend
cd frontend
npm install                      # Install dependencies
npm run dev                      # Start development server
npm run build                    # Build for production

# MongoDB
mongosh                          # Connect to MongoDB shell (check if running)
```

## API Endpoints

Once backend is running, you can access:

- `GET /` - API root
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `POST /api/v1/search` - Search articles
- `POST /api/v1/search/analyze` - Full analysis pipeline
- `GET /api/v1/search/clusters/{cluster_id}` - Get cluster details
- `GET /api/v1/search/articles/{article_id}` - Get article details

## Next Steps

1. Test the API endpoints using the Swagger UI at http://localhost:8000/docs
2. Try different news queries in the frontend
3. Review the bias analysis results
4. Check the cluster visualizations

## Getting API Keys

1. **Pinecone**: https://www.pinecone.io
   - Create an account
   - Create an index named `newsprism-vectors` with dimension `384` and metric `cosine`
   - Copy your API key

2. **Groq**: https://console.groq.com/keys
   - Create an account
   - Generate an API key
   - Copy the key

3. **NewsAPI**: https://newsapi.org
   - Create a free account
   - Copy your API key
   - Note: Free tier has limitations

## Production Deployment

For production:
1. Set proper `SECRET_KEY` for JWT tokens
2. Use production MongoDB instance
3. Configure proper CORS origins
4. Build frontend: `cd frontend && npm run build`
5. Use a production ASGI server (e.g., Gunicorn with Uvicorn workers)

