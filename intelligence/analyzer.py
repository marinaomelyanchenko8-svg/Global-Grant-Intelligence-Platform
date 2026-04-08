"""Main grant analyzer that combines all intelligence components."""

from typing import Dict, Any

from intelligence.topics import detect_topics
from intelligence.trends import classify_trend
from intelligence.scoring import calculate_score, get_score_factors
from intelligence.explanation import generate_explanation


def analyze_grant(grant: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a grant and return enriched data with intelligence fields.

    This is the main entry point for the intelligence layer. It accepts a raw
    grant dictionary, applies all analysis functions, and returns a new
    dictionary with intelligence fields added.

    Args:
        grant: Dictionary with raw grant fields (title, description, etc.)

    Returns:
        Dictionary with all original fields plus:
            - topics (list): Detected thematic categories
            - confidence (float): 0-1 confidence in topic detection
            - trend_label (str): Emerging, Growing, Stable, or Declining
            - score (int): 0-100 opportunity score
            - explanation (str): Human-readable score rationale

    Example:
        >>> raw_grant = {
        ...     "id": "nsf-2024-001",
        ...     "title": "AI for Climate Adaptation",
        ...     "description": "Funding for innovative AI applications...",
        ...     "funding_amount": 500000,
        ...     "currency": "USD",
        ...     "deadline": "2024-08-15",
        ...     "eligibility": "US universities and research institutions",
        ...     "region": "United States",
        ...     "source_name": "NSF",
        ...     "source_url": "https://nsf.gov/grants/...",
        ...     "status": "open",
        ... }
        >>> enriched = analyze_grant(raw_grant)
        >>> enriched["topics"]
        ["AI", "Climate"]
        >>> enriched["score"]
        90
    """
    # Create a copy to avoid modifying the original
    result = dict(grant)

    # Combine title and description for text analysis
    text = f"{result.get('title', '')} {result.get('description', '')}"

    # Topic detection
    topics, confidence = detect_topics(text)
    result["topics"] = topics
    result["confidence"] = confidence

    # Trend classification
    result["trend_label"] = classify_trend(result)

    # Score calculation
    score = calculate_score(result)
    result["score"] = score

    # Get score factors for explanation
    score_factors = get_score_factors(result)
    result["explanation"] = generate_explanation(result, score_factors)

    return result
