"""Explanation generator for grant scores."""

from typing import Dict, Any, List, Tuple


# Template mapping for factors
FACTOR_TEMPLATES = {
    "high_funding": "High funding amount",
    "medium_funding": "Good funding amount",
    "low_funding": "Limited funding",
    "distant_deadline": "Long application window",
    "moderate_deadline": "Reasonable deadline",
    "urgent_deadline": "Time-sensitive opportunity",
    "broad_eligibility": "broad eligibility",
    "quality_keywords": "innovation focus",
}


def generate_explanation(grant: Dict[str, Any], score_factors: List[Tuple[str, int]]) -> str:
    """
    Generate human-readable explanation for scores.

    Args:
        grant: Dictionary with grant data
        score_factors: List of (factor_name, points) tuples

    Returns:
        Concise explanation string (max 100 characters)

    Examples:
        "High funding amount with broad eligibility"
        "Time-sensitive opportunity with innovation focus"
    """
    if not score_factors:
        return "Standard opportunity based on available data"

    # Get top 2 positive factors
    positive_factors = [f for f in score_factors if f[1] > 0][:2]

    if not positive_factors:
        # If no positive factors, use first factor (likely negative)
        factor_name = score_factors[0][0]
        template = FACTOR_TEMPLATES.get(factor_name, factor_name.replace("_", " "))
        return template

    # Build explanation from top factors
    phrases = []
    for factor_name, _ in positive_factors:
        template = FACTOR_TEMPLATES.get(factor_name, factor_name.replace("_", " "))
        phrases.append(template)

    if len(phrases) == 1:
        return phrases[0]

    # Combine with "with" connector for second phrase
    if "funding" in phrases[0].lower():
        return f"{phrases[0]} with {phrases[1].lower()}"
    elif "deadline" in phrases[0].lower():
        return f"{phrases[0]} with {phrases[1].lower()}"
    else:
        return f"{phrases[0]} and {phrases[1].lower()}"
