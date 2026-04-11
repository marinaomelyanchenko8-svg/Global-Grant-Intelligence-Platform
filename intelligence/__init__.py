"""Global Grant Intelligence Platform - Intelligence Module.

This module provides rule-based analysis for grant opportunities including:
- Topic detection via keyword matching
- Trend classification (Emerging, Growing, Stable, Declining)
- Opportunity scoring (0-100)
- Explanation generation

Example:
    >>> from intelligence import analyze_grant
    >>> result = analyze_grant({
    ...     "title": "AI Research Grant",
    ...     "description": "Funding for machine learning projects",
    ...     "funding_amount": 100000,
    ...     "deadline": "2025-06-01"
    ... })
    >>> print(result["score"], result["topics"])
    90 ['AI']
"""

from intelligence.analyzer import analyze_grant
from intelligence.topics import detect_topics
from intelligence.trends import classify_trend
from intelligence.scoring import calculate_score, get_score_factors
from intelligence.explanation import generate_explanation

__all__ = [
    "analyze_grant",
    "detect_topics",
    "classify_trend",
    "calculate_score",
    "get_score_factors",
    "generate_explanation",
]
