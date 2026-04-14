"""Grants.gov RSS feed fetcher and data normalizer."""

import hashlib
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from xml.etree import ElementTree as ET

import requests

# Add backend to path for audit_logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.audit_logger import (
    log_fetch_attempt,
    log_fetch_success,
    log_fetch_failure,
    log_cache_hit,
    log_cache_miss
)

# Constants
GRANTSGOV_RSS_URL = "https://www.grants.gov/rss/GG_NewOppByAgency.xml"
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache", "grantsgov.json")
CACHE_TTL_HOURS = 1
NAMESPACE = {"content": "http://purl.org/rss/1.0/modules/content/"}


def _generate_id(title: str) -> str:
    """Generate unique ID from title hash."""
    return f"grantsgov-{hashlib.md5(title.lower().encode()).hexdigest()[:8]}"


def _parse_deadline(description: str, pub_date: str) -> str:
    """Extract or estimate deadline from description or pub date."""
    # Try to find deadline patterns in description (e.g., "Closing Date: Jan 15, 2025")
    # For MVP, use pub_date + 90 days as estimated deadline
    try:
        pub_dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
        deadline = pub_dt + timedelta(days=90)
        return deadline.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        # Fallback: 90 days from now
        return (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")


def _extract_funding_amount(description: str) -> float:
    """Attempt to extract funding amount from description."""
    # Look for patterns like "$50,000" or "$500,000"
    import re
    amounts = re.findall(r'\$([\d,]+(?:\.\d{2})?)', description)
    if amounts:
        try:
            # Take the first amount found, convert to float
            return float(amounts[0].replace(',', ''))
        except ValueError:
            pass
    return 0.0  # Unknown amount


def _normalize_grant(raw_grant: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Grants.gov RSS item to our Grant model format."""
    title = raw_grant.get("title", "").strip()
    description = raw_grant.get("description", "").strip()
    link = raw_grant.get("link", "").strip()
    pub_date = raw_grant.get("pubDate", "").strip()
    agency = raw_grant.get("agency", "US Government").strip()

    # Generate ID from title
    grant_id = _generate_id(title)

    # Extract or estimate fields
    deadline = _parse_deadline(description, pub_date)
    funding_amount = _extract_funding_amount(description)

    return {
        "id": grant_id,
        "title": title,
        "description": description or "No description available.",
        "funding_amount": funding_amount,
        "currency": "USD",
        "deadline": deadline,
        "eligibility": f"US organizations eligible for {agency} funding",
        "region": "United States",
        "source_name": "Grants.gov",
        "source_url": link,
        "status": "open",
        # Intelligence fields will be populated by analyzer
        "topics": [],
        "confidence": 0.0,
        "trend_label": "Stable",
        "score": 50,
        "explanation": "",
        # Metadata
        "data_source": "grants.gov"
    }


def _load_cache() -> Optional[Dict[str, Any]]:
    """Load cached data if it exists and is fresh."""
    try:
        if not os.path.exists(CACHE_FILE):
            return None

        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)

        # Check if cache is fresh and has actual data
        timestamp = datetime.fromisoformat(cache.get("timestamp", "2000-01-01"))
        if datetime.now() - timestamp < timedelta(hours=CACHE_TTL_HOURS):
            grants = cache.get("grants", [])
            # Return None if grants list is empty to force fresh fetch
            if grants and len(grants) > 0:
                return grants

        return None
    except (json.JSONDecodeError, ValueError, IOError):
        return None


def _save_cache(grants: List[Dict[str, Any]]) -> None:
    """Save grants to cache file."""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        cache = {
            "timestamp": datetime.now().isoformat(),
            "grants": grants
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except IOError:
        pass  # Cache failure is non-critical


def _parse_rss(xml_content: str) -> List[Dict[str, Any]]:
    """Parse RSS XML and extract grant items."""
    grants = []
    try:
        root = ET.fromstring(xml_content)

        # RSS feed structure: rss -> channel -> item[]
        channel = root.find("channel")
        if channel is None:
            return grants

        for item in channel.findall("item"):
            grant = {
                "title": item.findtext("title", ""),
                "description": item.findtext("description", ""),
                "link": item.findtext("link", ""),
                "pubDate": item.findtext("pubDate", ""),
                "agency": item.findtext("{http://www.grants.gov/}Agency", "US Government")
            }
            if grant["title"]:
                grants.append(grant)

    except ET.ParseError:
        pass  # Return empty list on parse error

    return grants


def fetch_grantsgov_data(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch grant data from Grants.gov RSS feed.

    Returns normalized grant dictionaries ready for intelligence analysis.
    Uses local cache to avoid hammering the RSS feed.

    Args:
        limit: Maximum number of grants to return (default 50)

    Returns:
        List of grant dictionaries, or empty list on failure
    """
    # Clear stale cache file if exists - ensures fresh fetch on startup
    try:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
    except IOError:
        pass
    source = "grants.gov"
    
    # Try cache first
    cached = _load_cache()
    if cached is not None:
        log_cache_hit()
        return cached[:limit]
    
    log_cache_miss()
    log_fetch_attempt(source)

    # Fetch from RSS
    try:
        response = requests.get(
            GRANTSGOV_RSS_URL,
            timeout=10,
            headers={
                "User-Agent": "Global-Grant-Intelligence-Platform/1.0"
            }
        )
        response.raise_for_status()

        # Check if response is HTML instead of XML (RSS feed discontinued)
        content_type = response.headers.get('Content-Type', '').lower()
        if 'text/html' in content_type:
            log_fetch_failure(source, f"RSS feed returned HTML (Content-Type: {content_type}) - Grants.gov RSS feed appears to be discontinued")
            return []

        # Also check content starts with XML declaration or rss tag
        content_start = response.text.strip()[:100].lower()
        if not (content_start.startswith('<?xml') or content_start.startswith('<rss') or content_start.startswith('<feed')):
            log_fetch_failure(source, f"RSS feed returned non-XML content (starts with: {response.text.strip()[:50]}) - Grants.gov RSS feed appears to be discontinued")
            return []

        # Parse RSS
        raw_grants = _parse_rss(response.text)

        # Normalize to our format
        normalized = [_normalize_grant(g) for g in raw_grants[:limit]]

        # Save to cache
        _save_cache(normalized)
        
        log_fetch_success(source, len(normalized))

        return normalized

    except requests.RequestException as e:
        # Network error - return empty list, let caller handle fallback
        log_fetch_failure(source, f"Network error: {str(e)}")
        return []
    except ET.ParseError as e:
        # XML parsing error - RSS feed likely returned HTML (discontinued)
        log_fetch_failure(source, f"XML parse error - RSS feed may be discontinued or returning HTML: {str(e)}")
        return []
    except Exception as e:
        # Any other error
        log_fetch_failure(source, f"Unexpected error: {str(e)}")
        return []
