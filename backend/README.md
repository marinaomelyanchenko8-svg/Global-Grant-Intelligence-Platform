# Global Grant Intelligence Platform — Backend

**FastAPI Backend | Port 8000**

---

## Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Server

```bash
# From project root (recommended):
.\start-server.ps1

# Or manually from backend directory:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Server available at:** http://localhost:8000  
**API docs at:** http://localhost:8000/docs

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and version |
| `/health` | GET | Health check |
| `/grants` | GET | List all grants with intelligence fields |

### GET /grants

Returns all grants from `data/grants.json` with full intelligence enrichment.

**Response:** `200 OK`  
**Content-Type:** `application/json`

**Example Response:**
```json
[
  {
    "id": "nsf-2024-001",
    "title": "AI for Climate Adaptation Research",
    "description": "Funding for innovative AI applications...",
    "funding_amount": 500000,
    "currency": "USD",
    "deadline": "2024-08-15",
    "eligibility": "US universities and research institutions",
    "region": "United States",
    "source_name": "NSF",
    "source_url": "https://nsf.gov/grants/climate-ai-2024",
    "status": "open",
    "topics": ["AI", "Climate"],
    "confidence": 0.85,
    "trend_label": "Growing",
    "score": 82,
    "explanation": "High funding amount with strong alignment to priority research areas"
  }
]
```

---

## Data Model

### Grant (16 fields)

**Raw Fields (Input):**
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `title` | string | Grant title |
| `description` | string | Full description |
| `funding_amount` | number | Amount (e.g., 50000) |
| `currency` | string | ISO code (USD, EUR) |
| `deadline` | string | ISO date |
| `eligibility` | string | Who can apply |
| `region` | string | Geographic scope |
| `source_name` | string | Origin source |
| `source_url` | string | Original link |
| `status` | string | open, closed, draft |

**Intelligence Fields (Computed):**
| Field | Type | Description |
|-------|------|-------------|
| `topics` | array[string] | Detected themes |
| `confidence` | number | 0-1 detection confidence |
| `trend_label` | string | Emerging, Growing, Stable, Declining |
| `score` | number | 0-100 opportunity score |
| `explanation` | string | Score rationale |

---

## Testing Commands

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test grants endpoint
curl http://localhost:8000/grants

# Pretty print JSON
curl http://localhost:8000/grants | python -m json.tool
```

---

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Dependencies
├── README.md            # This file
├── app/
│   ├── __init__.py
│   └── models.py        # Pydantic Grant model
├── data/
│   └── grants.json      # Mock grant data (10 samples)
└── tests/
    └── (test files)
```

---

## Troubleshooting

**CORS errors from frontend:**
- CORS is configured for ports 3000 and 5173
- Ensure frontend is running on one of these ports

**Virtual environment issues:**
- Make sure `.venv` is created in `backend/` directory
- Run `start-server.ps1` from project root

**Port 8000 in use:**
```bash
# Find and kill process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

*Part of Global Grant Intelligence Platform MVP*
