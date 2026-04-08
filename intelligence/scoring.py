"""Opportunity scoring engine with rule-based algorithm."""

from datetime import datetime
from typing import Dict, Any, List, Tuple


def calculate_score(grant: Dict[str, Any]) -> int:
    """
    Calculate 0-100 opportunity score based on configurable rules.

    Args:
        grant: Dictionary with grant data

    Returns:
        Integer score between 0 and 100

    Scoring Rules:
        Base score: 50 points
        - +20 if funding_amount > 100000
        - +10 if funding_amount > 50000
        - -10 if funding_amount < 10000
        - +15 if deadline > 6 months away
        - +5 if deadline 3-6 months away
        - -15 if deadline < 1 month
        - +10 if eligibility contains "global", "any", "all", "international"
        - +5 if description contains "innovation", "growth", "impact"

    Example:
        >>> calculate_score({
        ...     "funding_amount": 150000,
        ...     "eligibility": "Global applicants",
        ...     "description": "Innovation in healthcare",
        ...     "deadline": "2025-12-01"
        ... })
        90
    """
    score = 50  # Base score

    # Funding size factors
    funding = grant.get("funding_amount", 0)
    if funding > 100000:
        score += 20
    elif funding > 50000:
        score += 10
    elif funding < 10000:
        score -= 10

    # Deadline proximity factors
    deadline_str = grant.get("deadline", "")
    months_until = _months_until_deadline(deadline_str)
    if months_until is not None:
        if months_until > 6:
            score += 15
        elif months_until >= 3:
            score += 5
        elif months_until < 1:
            score -= 15

    # Eligibility breadth
    eligibility = grant.get("eligibility", "").lower()
    broad_terms = ["global", "any", "all", "international"]
    if any(term in eligibility for term in broad_terms):
        score += 10

    # Description quality
    description = grant.get("description", "").lower()
    quality_keywords = ["innovation", "growth", "impact"]
    if any(kw in description for kw in quality_keywords):
        score += 5

    # Clamp to 0-100 range
    return max(0, min(100, score))


def get_score_factors(grant: Dict[str, Any]) -> List[Tuple[str, int]]:
    """
    Get list of factors that contributed to the score.

    Returns list of (factor_name, points) tuples sorted by points.
    """
    factors = []

    funding = grant.get("funding_amount", 0)
    if funding > 100000:
        factors.append(("high_funding", 20))
    elif funding > 50000:
        factors.append(("medium_funding", 10))
    elif funding < 10000:
        factors.append(("low_funding", -10))

    deadline_str = grant.get("deadline", "")
    months_until = _months_until_deadline(deadline_str)
    if months_until is not None:
        if months_until > 6:
            factors.append(("distant_deadline", 15))
        elif months_until >= 3:
            factors.append(("moderate_deadline", 5))
        elif months_until < 1:
            factors.append(("urgent_deadline", -15))

    eligibility = grant.get("eligibility", "").lower()
    if any(term in eligibility for term in ["global", "any", "all", "international"]):
        factors.append(("broad_eligibility", 10))

    description = grant.get("description", "").lower()
    if any(kw in description for kw in ["innovation", "growth", "impact"]):
        factors.append(("quality_keywords", 5))

    return sorted(factors, key=lambda x: abs(x[1]), reverse=True)


def _months_until_deadline(deadline_str: str) -> float:
    """Calculate months until deadline from ISO date string."""
    if not deadline_str:
        return None

    try:
        deadline = datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
        now = datetime.now()
        delta = deadline - now
        return delta.days / 30.0
    except (ValueError, TypeError):
        return None
