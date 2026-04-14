import json
import os
import sys
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add project root to path for intelligence module
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from app.audit_logger import log_deduplication, log_fallback
from app.deduplicator import deduplicate_grants
from app.models import Grant
from app.sources import fetch_grantsgov_data
from intelligence.analyzer import analyze_grant

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

# Serve frontend static files
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")

@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def load_mock_grants() -> List[Grant]:
    """Load mock grants from JSON file as fallback."""
    data_path = os.path.join(os.path.dirname(__file__), "data", "grants.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Add data_source = "mock" to each grant
    for grant in data:
        grant["data_source"] = "mock"
    return [Grant(**grant) for grant in data]


def load_grants() -> List[Grant]:
    """
    Load grants from Grants.gov with fallback to mock data.

    Attempts to fetch from Grants.gov RSS feed first.
    Falls back to mock data if fetch fails or returns empty.
    All grants are processed through intelligence analyzer.
    Includes data_source field to indicate source (grants.gov or mock).
    """
    # Try to fetch from Grants.gov
    raw_grants = fetch_grantsgov_data(limit=50)

    if raw_grants:
        # Deduplicate before processing
        original_count = len(raw_grants)
        unique_grants = deduplicate_grants(raw_grants)
        deduped_count = len(unique_grants)
        
        if original_count != deduped_count:
            log_deduplication(original_count, deduped_count)

        # Process through intelligence analyzer (preserves data_source field)
        enriched_grants = [analyze_grant(grant) for grant in unique_grants]

        # Convert to Grant models
        return [Grant(**grant) for grant in enriched_grants]

    # Fallback to mock data
    log_fallback("grants.gov")
    return load_mock_grants()


@app.get("/grants", response_model=List[Grant])
async def get_grants():
    """
    Return all grants with intelligence fields.

    Sources data from Grants.gov RSS feed when available,
    with automatic fallback to mock data if source is unavailable.
    All grants are enriched with AI-powered analysis (topics, score, trend).
    """
    return load_grants()
