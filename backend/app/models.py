from pydantic import BaseModel, Field, validator
from typing import List, Literal


class Grant(BaseModel):
    """
    Grant data model with all raw and intelligence fields.
    Matches the shared data structure defined in MASTER-PROMPT.md
    """
    
    # Raw Fields (Input)
    id: str = Field(..., description="Unique identifier for the grant")
    title: str = Field(..., description="Grant title")
    description: str = Field(..., description="Full grant description")
    funding_amount: float = Field(..., description="Amount in numeric value (e.g., 50000)")
    currency: str = Field(..., description="ISO currency code (e.g., 'USD')")
    deadline: str = Field(..., description="Application deadline (ISO date)")
    eligibility: str = Field(..., description="Who can apply")
    region: str = Field(..., description="Geographic scope")
    source_name: str = Field(..., description="Origin source (e.g., 'NSF', 'EU Horizon')")
    source_url: str = Field(..., description="Link to original grant")
    status: Literal["open", "closed", "draft"] = Field(..., description="Grant status")
    
    # Intelligence Fields (Computed)
    topics: List[str] = Field(default=[], description="Detected thematic categories")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="0-1 confidence in topic detection")
    trend_label: Literal["Emerging", "Growing", "Stable", "Declining"] = Field(
        default="Stable", description="Grant trajectory classification"
    )
    score: int = Field(default=50, ge=0, le=100, description="0-100 opportunity score")
    explanation: str = Field(default="", description="Human-readable score rationale")
    
    # Metadata Fields
    data_source: Literal["grants.gov", "mock"] = Field(
        default="mock", description="Source of grant data: grants.gov (live) or mock (fallback)"
    )
    
    @validator("score")
    def validate_score(cls, v):
        if v < 0:
            return 0
        if v > 100:
            return 100
        return v
    
    @validator("confidence")
    def validate_confidence(cls, v):
        if v < 0:
            return 0.0
        if v > 1:
            return 1.0
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "id": "nsf-2024-001",
                "title": "AI for Climate Adaptation Research",
                "description": "Funding for innovative AI applications in climate resilience...",
                "funding_amount": 500000,
                "currency": "USD",
                "deadline": "2024-08-15",
                "eligibility": "US universities and research institutions",
                "region": "United States",
                "source_name": "NSF",
                "source_url": "https://nsf.gov/grants/...",
                "status": "open",
                "topics": ["AI", "Climate"],
                "confidence": 0.85,
                "trend_label": "Growing",
                "score": 82,
                "explanation": "High funding amount with strong alignment to priority research areas"
            }
        }
