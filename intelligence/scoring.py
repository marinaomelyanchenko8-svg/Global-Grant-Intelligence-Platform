"""Opportunity scoring engine with rule-based algorithm."""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Tuple


def _load_scoring_config() -> Dict[str, Any]:
    """Load scoring configuration from JSON file."""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "backend", "data", "scoring_config.json"
    )
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, FileNotFoundError):
        # Fallback to default config if file missing
        return {
            "base_score": 50,
            "funding_rules": [{"condition": "funding > 100000", "points": 20}],
            "deadline_rules": [{"condition": "months > 6", "points": 15}],
            "eligibility_rules": [{"keywords": ["global"], "points": 10}],
            "description_rules": [{"keywords": ["innovation"], "points": 5}],
            "min_score": 0,
            "max_score": 100
        }


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
    config = _load_scoring_config()
    score = config.get("base_score", 50)
    funding = grant.get("funding_amount", 0)
    
    # Funding size factors
    for rule in config.get("funding_rules", []):
        condition = rule.get("condition", "")
        points = rule.get("points", 0)
        if condition == "funding > 100000" and funding > 100000:
            score += points
        elif condition == "funding > 50000" and funding > 50000:
            score += points
        elif condition == "funding < 10000" and funding < 10000:
            score += points

    # Deadline proximity factors
    deadline_str = grant.get("deadline", "")
    months_until = _months_until_deadline(deadline_str)
    if months_until is not None:
        for rule in config.get("deadline_rules", []):
            condition = rule.get("condition", "")
            points = rule.get("points", 0)
            if condition == "months > 6" and months_until > 6:
                score += points
            elif condition == "months >= 3" and months_until >= 3:
                score += points
            elif condition == "months < 1" and months_until < 1:
                score += points

    # Eligibility breadth
    eligibility = grant.get("eligibility", "").lower()
    for rule in config.get("eligibility_rules", []):
        keywords = rule.get("keywords", [])
        points = rule.get("points", 0)
        if any(term in eligibility for term in keywords):
            score += points

    # Description quality
    description = grant.get("description", "").lower()
    for rule in config.get("description_rules", []):
        keywords = rule.get("keywords", [])
        points = rule.get("points", 0)
        if any(kw in description for kw in keywords):
            score += points

    # Clamp to configured range
    min_score = config.get("min_score", 0)
    max_score = config.get("max_score", 100)
    return max(min_score, min(max_score, score))


def get_score_factors(grant: Dict[str, Any]) -> List[Tuple[str, int]]:
    """
    Get list of factors that contributed to the score.

    Returns list of (factor_name, points) tuples sorted by points.
    """
    config = _load_scoring_config()
    factors = []
    funding = grant.get("funding_amount", 0)

    # Funding size factors
    for rule in config.get("funding_rules", []):
        condition = rule.get("condition", "")
        points = rule.get("points", 0)
        desc = rule.get("description", "funding")
        if condition == "funding > 100000" and funding > 100000:
            factors.append((desc, points))
        elif condition == "funding > 50000" and funding > 50000:
            factors.append((desc, points))
        elif condition == "funding < 10000" and funding < 10000:
            factors.append((desc, points))

    # Deadline proximity factors
    deadline_str = grant.get("deadline", "")
    months_until = _months_until_deadline(deadline_str)
    if months_until is not None:
        for rule in config.get("deadline_rules", []):
            condition = rule.get("condition", "")
            points = rule.get("points", 0)
            desc = rule.get("description", "deadline")
            if condition == "months > 6" and months_until > 6:
                factors.append((desc, points))
            elif condition == "months >= 3" and months_until >= 3:
                factors.append((desc, points))
            elif condition == "months < 1" and months_until < 1:
                factors.append((desc, points))

    # Eligibility breadth
    eligibility = grant.get("eligibility", "").lower()
    for rule in config.get("eligibility_rules", []):
        keywords = rule.get("keywords", [])
        points = rule.get("points", 0)
        desc = rule.get("description", "eligibility")
        if any(term in eligibility for term in keywords):
            factors.append((desc, points))

    # Description quality
    description = grant.get("description", "").lower()
    for rule in config.get("description_rules", []):
        keywords = rule.get("keywords", [])
        points = rule.get("points", 0)
        desc = rule.get("description", "description")
        if any(kw in description for kw in keywords):
            factors.append((desc, points))

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
