# Architecture Documentation

## 1. System Overview

The Global Grant Intelligence Platform is a web application that discovers, analyzes, and presents grant opportunities with AI-powered insights.

**Main Components:**
- **Frontend** - Browser-based UI for browsing and viewing grants
- **Backend** - FastAPI service that serves grant data
- **Intelligence** - Analysis layer that enriches grants with AI-generated insights

---

## 2. System Architecture Diagram

### Phase 2: With Grants.gov Integration

```
Frontend (Browser)
    ↓ HTTP Request
Backend API (/grants)
    ↓ Try Fetch
Grants.gov RSS Feed
    ↓ Parse & Normalize
Cache Layer (1-hour TTL)
    ↓ Load (if fresh) or Fetch (if stale)
Deduplicator (title + deadline)
    ↓ Process
Intelligence Layer (analyzer)
    ↓ Enrich
Response (enriched grant data)
    ↓ JSON
Frontend UI (cards with source links)
```

### Fallback Flow (when Grants.gov unavailable)

```
Backend API (/grants)
    ↓ Fetch Fails
Mock Data (grants.json)
    ↓ Load
Intelligence Layer (analyzer)
    ↓ Enrich
Response (enriched grant data)
```

---

## 3. Data Flow

1. **Frontend requests** `/grants` endpoint from backend
2. **Backend loads** raw grant data from data source
3. **Intelligence processes** data (scoring, trends, explanations)
4. **Backend returns** enriched response to frontend
5. **Frontend renders** data as interactive grant cards

---

## 4. API Contract

### Endpoint

**GET** `/grants`

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique grant identifier |
| `title` | string | Grant title |
| `funding_amount` | string | Funding amount range |
| `topics` | array | List of relevant topic tags |
| `trend_label` | string | Trend classification |
| `score` | number | Relevance score (0-100) |
| `confidence` | number | Confidence level (0-1) |
| `explanation` | string | AI-generated summary |

---

## 5. Data Model

### Grant Object

```json
{
  "id": "string",
  "title": "string",
  "funding_amount": "string",
  "topics": ["string"],
  "trend_label": "string",
  "score": 0,
  "confidence": 0.0,
  "explanation": "string"
}
```

**Key Fields:**
- `id` - Unique identifier for the grant
- `title` - Human-readable grant name
- `funding_amount` - Financial range as display string
- `topics` - Categorical tags for filtering
- `trend_label` - Classification (e.g., "rising", "stable")
- `score` - Integer score from 0-100
- `confidence` - Float between 0 and 1
- `explanation` - Natural language description

---

## 6. Setup Instructions

### Run Backend

```bash
uvicorn backend.main:app --reload
```

**Requirement:** Backend must run on port 8000.

### Open Frontend

```bash
open frontend/index.html
```

Or manually open `frontend/index.html` in your browser.
