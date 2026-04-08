# Global Grant Intelligence Platform

**MVP | Grant Aggregation & Intelligence System**

---

## Overview

The Global Grant Intelligence Platform is a lightweight MVP that transforms raw grant opportunities into actionable intelligence. It aggregates funding data, applies rule-based analysis for relevance scoring, and presents opportunities through a clean web interface.

**What makes this different:** Unlike simple grant directories, this system actively analyzes each opportunity—detecting topics, classifying trends, calculating opportunity scores, and generating explanations for why each grant matters.

---

## MVP Features

| Feature | Description |
|---------|-------------|
| **Grant Aggregation** | Structured storage of funding opportunities with complete metadata |
| **Topic Detection** | Keyword-based classification into themes (AI, Climate, Healthcare, etc.) |
| **Trend Analysis** | Classification as Emerging, Growing, Stable, or Declining |
| **Opportunity Scoring** | 0-100 relevance score based on funding size, deadline, eligibility |
| **Explanation Generation** | Human-readable rationale for each score |
| **Web Interface** | Clean card-based display of grants with visual score indicators |

---

## Architecture

**Three-Layer System:**

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│  Frontend   │────▶│   Backend   │────▶│  Intelligence   │
│  (Nazar)    │     │   (Arvin)   │     │   (Marina)      │
│  HTML/CSS   │     │   FastAPI   │     │   Rule-based    │
└─────────────┘     └─────────────┘     └─────────────────┘
       │                     │                     │
       │                     │◀────────────────────│
       │                     │    Enriched Data    │
       │◀────────────────────│                     │
       │    JSON Response    │                     │
       │                     │                     │
┌──────▼─────────────────────▼─────────────────────▼──────┐
│                    User Display                        │
│  • Grant cards with title, funding, score, explanation │
└─────────────────────────────────────────────────────────┘
```

**Tech Stack:**
- **Backend:** Python + FastAPI (Port 8000)
- **Frontend:** HTML/CSS/JavaScript (Port 3000 or file-based)
- **Intelligence:** Python rule-based processing
- **Data:** JSON mock data (SQLite/PostgreSQL for future)

---

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, for local frontend server)
- Git

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at: http://localhost:8000  
API docs at: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend

# Option 1: Open directly
open index.html

# Option 2: Use local server
npx serve .
# Opens at http://localhost:3000
```

### Verify Installation

```bash
# Test backend API
curl http://localhost:8000/grants

# You should see JSON array with grant objects
```

---

## Data Structure

**Grant Object (16 fields):**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `title` | string | Grant title |
| `description` | string | Full description |
| `funding_amount` | number | Amount (e.g., 50000) |
| `currency` | string | USD, EUR, etc. |
| `deadline` | string | ISO date |
| `eligibility` | string | Who can apply |
| `region` | string | Geographic scope |
| `source_name` | string | Origin source |
| `source_url` | string | Original link |
| `status` | string | open, closed, draft |
| `topics` | array | Detected themes |
| `confidence` | number | 0-1 detection confidence |
| `trend_label` | string | Emerging/Growing/Stable/Declining |
| `score` | number | 0-100 opportunity score |
| `explanation` | string | Score rationale |

**Example Grant:**
```json
{
  "id": "nsf-2024-001",
  "title": "AI for Climate Adaptation",
  "funding_amount": 500000,
  "currency": "USD",
  "status": "open",
  "topics": ["AI", "Climate"],
  "trend_label": "Growing",
  "score": 82,
  "explanation": "High funding amount with strong alignment to priority research areas"
}
```

---

## Intelligence Logic

**Topic Detection:** Keyword matching on title and description  
**Trend Labels:** Based on funding cycle, deadline proximity, description keywords  
**Scoring Algorithm:**
- Base: 50 points
- +20 for funding >$100K, +10 for >$50K, -10 for <$10K
- +15 for deadline >6 months, -15 for <1 month
- +10 for broad eligibility (global/international)
- +5 for innovation keywords

**Max Score:** 100 | **Min Score:** 0

---

## Project Documentation

| Document | Purpose |
|----------|---------|
| [MASTER-PROMPT.md](./MASTER-PROMPT.md) | Complete project specification |
| [ROADMAP.md](./ROADMAP.md) | 7-day development plan |
| [WORKFLOW.md](./WORKFLOW.md) | Git workflow and team protocols |
| [TASKS-arvin.md](./TASKS-arvin.md) | Backend developer tasks |
| [TASKS-nazar.md](./TASKS-nazar.md) | Frontend developer tasks |
| [TASKS-marina.md](./TASKS-marina.md) | Team lead & intelligence tasks |

---

## Team

| Role | Member | Responsibility |
|------|--------|----------------|
| **Team Lead + Intelligence** | Marina | Project structure, coordination, analysis engine |
| **Backend Developer** | Arvin | FastAPI backend, API endpoints, data models |
| **Frontend Developer** | Nazar | Web interface, UI components, API integration |

---

## MVP Success Criteria

- [ ] Backend returns 10+ grants via `GET /grants`
- [ ] Each grant has all 16 required fields
- [ ] Intelligence fields populated (topics, score, trend, explanation)
- [ ] Frontend displays grants in clean card format
- [ ] Score is color-coded (green/yellow/red)
- [ ] Explanation text visible per grant
- [ ] Complete documentation created
- [ ] All team contributions merged to `main`
- [ ] Release tagged `v0.1-mvp`

---

## Future Roadmap (Post-MVP)

- [ ] Database persistence (PostgreSQL)
- [ ] Real grant source integrations (NSF, EU Horizon, etc.)
- [ ] User authentication and saved searches
- [ ] Email alerts for new opportunities
- [ ] Advanced scoring with ML
- [ ] Commercial SaaS offering

---

## License

MIT License — See [LICENSE](./LICENSE) (if applicable)

---

*Project: Global Grant Intelligence Platform*  
*Version: 0.1-MVP*  
*Status: Development In Progress*

