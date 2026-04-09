from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.models import Grant

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


@app.get("/grants", response_model=List[Grant])
async def get_grants():
    """
    Return all grants with intelligence fields.
    Data loaded from mock data (Task 3).
    """
    # TODO: Load from data/grants.json in Task 3
    # For now, return empty list to verify endpoint structure
    return []
