from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os
from app.models import Grant

# Import intelligence module with fallback
try:
    from intelligence.analyzer import analyze_grant
    INTELLIGENCE_AVAILABLE = True
except ImportError:
    INTELLIGENCE_AVAILABLE = False
    analyze_grant = None

app = FastAPI(
    title="Global Grant Intelligence Platform API",
    description="Backend API for grant aggregation and intelligence",
    version="0.1.0"
)

# CORS middleware - configured for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/")
async def root():
    return {"message": "Global Grant Intelligence Platform API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def load_grants() -> List[Grant]:
    """Load grants from JSON file and enrich with intelligence if available."""
    data_path = os.path.join(os.path.dirname(__file__), "data", "grants.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    grants = []
    for grant_data in data:
        if INTELLIGENCE_AVAILABLE and analyze_grant:
            try:
                # Enrich grant with intelligence fields
                enriched = analyze_grant(dict(grant_data))
                grants.append(Grant(**enriched))
            except Exception:
                # Fallback to mock data if analysis fails
                grants.append(Grant(**grant_data))
        else:
            # Use mock data as-is when intelligence module unavailable
            grants.append(Grant(**grant_data))
    
    return grants


@app.get("/grants", response_model=List[Grant])
async def get_grants():
    """
    Return all grants with intelligence fields.
    Data loaded from data/grants.json.
    """
    return load_grants()
