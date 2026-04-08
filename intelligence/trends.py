"""Trend classification for grant analysis."""

from datetime import datetime
from typing import Dict, Any


def classify_trend(grant: Dict[str, Any]) -> str:
    """
    Classify grant trend based on available data.

    Args:
        grant: Dictionary with grant data including deadline and description

    Returns:
        One of: "Emerging", "Growing", "Stable", "Declining"

    Rules (MVP simplification):
        - Emerging: deadline > 6 months AND description contains "new", "first", "pilot"
        - Growing: funding_amount > 100000 OR description contains "expanded", "increased"
        - Declining: deadline < 1 month OR description contains "final", "closing", "last"
        - Stable: default if none of above

    Example:
        >>> classify_trend({
        ...     "description": "New pilot program for AI research",
        ...     "deadline": "2025-12-01",
        ...     "funding_amount": 50000
        ... })
        "Emerging"
    """
    description = grant.get("description", "").lower()
    funding_amount = grant.get("funding_amount", 0)
    deadline_str = grant.get("deadline", "")

    # Calculate months until deadline
    months_until = _months_until_deadline(deadline_str)

    # Emerging: new program with distant deadline
    emerging_keywords = ["new", "first", "pilot"]
    if months_until and months_until > 6:
        if any(kw in description for kw in emerging_keywords):
            return "Emerging"

    # Growing: increased funding
    growing_keywords = ["expanded", "increased", "growing"]
    if funding_amount and funding_amount > 100000:
        return "Growing"
    if any(kw in description for kw in growing_keywords):
        return "Growing"

    # Declining: ending soon
    declining_keywords = ["final", "closing", "last", "ending"]
    if months_until and months_until < 1:
        return "Declining"
    if any(kw in description for kw in declining_keywords):
        return "Declining"

    # Default: Stable
    return "Stable"


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
