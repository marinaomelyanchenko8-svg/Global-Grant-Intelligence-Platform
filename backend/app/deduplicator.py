"""Simple grant deduplication based on title + deadline similarity."""

from typing import List, Dict, Any


def deduplicate_grants(grants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate grants based on title and deadline similarity.

    Two grants are considered duplicates if they have the same:
    - Normalized title (lowercase, stripped)
    - Deadline date

    Args:
        grants: List of grant dictionaries

    Returns:
        List with duplicates removed (first occurrence kept)
    """
    seen = set()
    unique = []

    for grant in grants:
        # Create unique key from title + deadline
        title = grant.get("title", "").lower().strip()
        deadline = grant.get("deadline", "")

        # Skip grants with missing critical fields
        if not title or not deadline:
            continue

        key = f"{title}|{deadline}"

        if key not in seen:
            seen.add(key)
            unique.append(grant)

    return unique
