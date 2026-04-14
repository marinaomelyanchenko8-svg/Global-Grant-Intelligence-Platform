# Global Grant Intelligence Platform

A lightweight system that transforms raw grant opportunities into actionable intelligence. Aggregates funding data from real sources (Grants.gov), applies AI-powered analysis for relevance scoring, and presents opportunities through a clean web interface.

---

## Features

- **Real Data Integration** — Live grant data from Grants.gov RSS feed with 1-hour cache
- **Grant Discovery** — Structured aggregation of funding opportunities with complete metadata
- **AI-Powered Scoring** — 0-100 relevance scores based on funding size, deadline, and eligibility criteria
- **Trend Analysis** — Classification of opportunities as Emerging, Growing, Stable, or Declining
- **Source Attribution** — Direct links to original grant listings on Grants.gov
- **Smart Fallback** — Mock data when live source is unavailable

---

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   Frontend  │────▶│   Backend   │────▶│  Intelligence   │
│  HTML/CSS   │     │   FastAPI   │     │  Rule-based AI  │
└─────────────┘     └─────────────┘     └─────────────────┘
```

| Layer | Technology | Responsibility |
|-------|------------|----------------|
| **Frontend** | HTML/CSS/JS | Web interface, grant display |
| **Backend** | Python + FastAPI | API endpoints, data models |
| **Intelligence** | Python | Scoring, topic detection, trend analysis |

---

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
open index.html
```

---

## API

**GET `/grants`** — Returns array of enriched grant objects with scores, topics, and explanations.

---

*Version: 0.1-MVP*

