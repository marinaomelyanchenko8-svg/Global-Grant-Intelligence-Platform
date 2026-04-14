"""Simple audit logging for data ingestion operations."""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

# Log file path
LOG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "logs",
    "ingestion.log"
)


def _ensure_log_dir():
    """Ensure log directory exists."""
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)


def _write_log(level: str, event: str, details: Optional[Dict[str, Any]] = None):
    """Write a log entry to the ingestion log file."""
    _ensure_log_dir()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "event": event
    }
    
    if details:
        entry["details"] = details
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except IOError:
        # Log failures are non-critical
        pass


def log_fetch_attempt(source: str):
    """Log when a fetch attempt is initiated."""
    _write_log("INFO", "fetch_attempt", {"source": source})


def log_fetch_success(source: str, count: int):
    """Log when a fetch is successful."""
    _write_log("INFO", "fetch_success", {"source": source, "count": count})


def log_fetch_failure(source: str, error: str):
    """Log when a fetch fails."""
    _write_log("ERROR", "fetch_failure", {"source": source, "error": error})


def log_fallback(source: str):
    """Log when fallback data is used."""
    _write_log("WARNING", "fallback_used", {"source": source})


def log_deduplication(original_count: int, deduplicated_count: int):
    """Log deduplication results."""
    removed = original_count - deduplicated_count
    _write_log("INFO", "deduplication", {
        "original_count": original_count,
        "deduplicated_count": deduplicated_count,
        "removed": removed
    })


def log_cache_hit():
    """Log when cache is used."""
    _write_log("INFO", "cache_hit")


def log_cache_miss():
    """Log when cache is missed."""
    _write_log("INFO", "cache_miss")
