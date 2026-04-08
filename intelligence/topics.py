"""Keyword-based topic detection for grant analysis."""

from typing import List, Tuple

# Topic keyword mappings
TOPIC_KEYWORDS = {
    "AI": ["artificial intelligence", "machine learning", "ml", "ai", "neural", "deep learning"],
    "Climate": ["climate", "environment", "carbon", "renewable", "sustainability"],
    "Healthcare": ["health", "medical", "healthcare", "disease", "treatment"],
    "Education": ["education", "learning", "student", "school", "university"],
    "Fintech": ["fintech", "financial", "banking", "payment", "blockchain"],
    "Agriculture": ["agriculture", "farming", "crop", "food security", "rural"],
    "Energy": ["energy", "power", "solar", "wind", "grid", "electricity"],
    "Social Impact": ["social impact", "community", "nonprofit", "ngo", "equity"],
}


def detect_topics(text: str) -> Tuple[List[str], float]:
    """
    Detect topics from text using keyword matching.

    Args:
        text: The text to analyze (title + description)

    Returns:
        Tuple of (list of detected topics, confidence score)

    Example:
        >>> detect_topics("AI for climate change research")
        (["AI", "Climate"], 0.67)
    """
    if not text:
        return ([], 0.0)

    text_lower = text.lower()
    matched_keywords = 0
    detected_topics = []

    for topic, keywords in TOPIC_KEYWORDS.items():
        topic_matched = False
        for keyword in keywords:
            if keyword in text_lower:
                matched_keywords += 1
                topic_matched = True
        if topic_matched:
            detected_topics.append(topic)

    total_keywords = sum(len(kw) for kw in TOPIC_KEYWORDS.values())
    confidence = matched_keywords / total_keywords if total_keywords > 0 else 0.0

    return (detected_topics, round(confidence, 2))
