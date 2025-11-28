# NewsPrism Architecture

## System Overview

NewsPrism is a full-stack news analysis platform that detects bias, extracts facts, and shows how different outlets frame the same events.

## Architecture Diagram

```
┌─────────────────┐
│   React Frontend │
│   (Vite + React) │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   FastAPI Backend│
│   (Python)       │
└────────┬────────┘
         │
    ┌────┴────┬──────────────┬─────────────┐
    │         │              │             │
┌───▼───┐ ┌──▼────┐   ┌──────▼─────┐ ┌────▼────┐
│PostgreSQL│ │Pinecone│   │  OpenAI API │ │NewsAPI │
│(Metadata)│ │(Vectors)│   │   (LLM)     │ │(News)  │
└─────────┘ └────────┘   └────────────┘ └────────┘
```

## Component Details

### Frontend (React)

**Location**: `frontend/src/`

**Key Components**:
- `SearchPage.jsx` - Main search interface
- `ClusterDetailPage.jsx` - Detailed cluster analysis view
- `SearchForm.jsx` - Query input form
- `FactSummary.jsx` - Displays verified facts
- `FrameAnalysis.jsx` - Shows per-source framing
- `BiasChart.jsx` - Visual bias comparison
- `FactHeatmap.jsx` - Fact coverage matrix

**Tech Stack**:
- React 18
- React Router for navigation
- Chart.js for visualizations
- Tailwind CSS for styling
- Axios for API calls

### Backend (FastAPI)

**Location**: `backend/app/`

#### API Layer (`app/api/`)
- RESTful endpoints for search, analysis, and data retrieval
- Request/response validation with Pydantic schemas

#### Core Services (`app/services/`)

1. **Ingestion Service** (`ingestion/`)
   - `newsapi_client.py` - NewsAPI integration
   - `scraper.py` - Web scraping with newspaper3k/BeautifulSoup
   - `ingestion_service.py` - Orchestrates article collection

2. **Embedding Service** (`embeddings/`)
   - `embedding_service.py` - Sentence transformers for embeddings
   - `vector_store.py` - Pinecone integration for vector storage

3. **Clustering Service** (`clustering/`)
   - `clustering_service.py` - DBSCAN clustering for event grouping

4. **Bias Analysis** (`bias/`)
   - `bias_analyzer.py` - Sentiment, lexical, and subjectivity analysis
   - `omission_detector.py` - Detects missing facts

5. **Fact Extraction** (`facts/`)
   - `fact_extractor.py` - NER + LLM verification

6. **Agent Orchestration** (`agents/`)
   - `orchestrator.py` - LangChain-based workflow coordination

#### Data Models (`app/models/`)
- `Article` - News article metadata and content
- `Cluster` - Grouped articles covering same event
- `ArticleAnalysis` - Analysis results storage

#### Database (`app/core/`)
- PostgreSQL for structured data
- Alembic for migrations
- SQLAlchemy ORM

## Data Flow

### 1. Query Processing

```
User Query → SearchForm → API /search/analyze → AgentOrchestrator
```

### 2. Article Ingestion

```
AgentOrchestrator → IngestionService → NewsAPIClient/Scraper → Article (DB)
```

### 3. Embedding & Vector Storage

```
Article → EmbeddingService → Chunks → VectorStore (Pinecone)
```

### 4. Clustering

```
Articles → ClusteringService → DBSCAN → Clusters
```

### 5. Analysis Pipeline

```
Cluster → [
  FactExtractor → Facts (LLM verified),
  BiasAnalyzer → Bias scores,
  OmissionDetector → Missing facts
] → Cluster (updated with results)
```

### 6. Response

```
Cluster → API → Frontend → Dashboard visualization
```

## Key Algorithms

### Bias Index Calculation

```
BiasMag = w1 * |Tone - ClusterMeanTone| + 
          w2 * LexicalBias + 
          w3 * OmissionScore + 
          w4 * ConsistencyScore

BiasIndex = 100 * (BiasMag / MaxBiasMag)
```

Where:
- `w1=0.4, w2=0.25, w3=0.2, w4=0.15` (configurable weights)
- Tone: -1 (negative) to +1 (positive) sentiment
- LexicalBias: 0 to 1 (proportion of loaded language)
- OmissionScore: 0 to 1 (fraction of facts missing)
- ConsistencyScore: 0 to 1 (conflicts with majority)

### Transparency Score

```
Transparency = 100 * (1 - (0.4*Omission + 0.4*Consistency + 0.2*LexicalBias))
```

### Clustering

- Algorithm: DBSCAN with cosine similarity
- Parameters: `eps=0.5, min_samples=2` (configurable)
- Input: Article embeddings (384-dimensional vectors)
- Output: Clusters of semantically similar articles

## Technology Choices

### Why FastAPI?
- Async/await support for I/O-bound operations
- Automatic OpenAPI documentation
- Type validation with Pydantic
- High performance

### Why Pinecone?
- Managed vector database (no infrastructure)
- Fast similarity search
- Scales automatically
- Easy integration

### Why LangChain?
- Agent orchestration patterns
- Tool integration
- LLM abstraction
- Observability (LangSmith)

### Why React?
- Component reusability
- Rich ecosystem
- Fast development
- Good for dashboards

## Scalability Considerations

### Current (MVP)
- Single backend instance
- Direct database connections
- Synchronous processing

### Production Recommendations
1. **Backend**: 
   - Multiple workers (Gunicorn + Uvicorn)
   - Redis for caching
   - Celery for async tasks
   - Load balancer

2. **Database**:
   - Read replicas
   - Connection pooling
   - Indexing strategy

3. **Vector DB**:
   - Pinecone handles scaling automatically
   - Consider sharding for very large datasets

4. **Frontend**:
   - CDN for static assets
   - API response caching
   - Lazy loading

## Security

- Environment variables for secrets
- CORS configuration
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- Rate limiting (recommended for production)

## Monitoring & Observability

- FastAPI automatic OpenAPI docs
- LangSmith for agent tracing (optional)
- Logging throughout services
- Health check endpoint (`/health`)

## Future Enhancements

1. User authentication & personalization
2. Scheduled ingestion jobs (Celery)
3. Real-time updates (WebSockets)
4. Advanced visualizations (D3.js)
5. Export functionality (PDF, CSV)
6. Multi-language support
7. Fine-tuned bias detection models
8. User feedback loop for model improvement

