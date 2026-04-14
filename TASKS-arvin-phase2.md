# Arvin — Backend Phase 2 Tasks

**Role:** Backend Developer  
**Branch:** `arvin/phase2-ingestion`  
**Goal:** Build stable grant aggregation system scalable to 10 sources, 2-3 real working sources

---

## Overview

Phase 2 focuses on replacing mock-first architecture with real data ingestion. Implement a modular adapter system that can scale to 10 sources. Start with 2-3 reliable real sources. Keep mock data only as fallback when all real sources fail.

---

## Task 1: Modular Source Adapter Architecture

**Estimated Effort:** Medium  
**Execution Order:** First  
**Dependencies:** None

### Description
Refactor current source code into a clean adapter pattern that supports multiple data sources with consistent interface.

### Files to Modify
- `backend/app/sources/base.py` — create new base adapter class
- `backend/app/sources/__init__.py` — update exports
- `backend/app/sources/grantsgov.py` — refactor to extend base adapter (NOTE: existing code is ~240 lines with caching/RSS logic — plan time for careful refactor)
- `backend/app/models.py` — expand data_source Literal for new sources

### Acceptance Criteria
- [ ] Create `BaseSourceAdapter` abstract class in `base.py` with methods:
  - `fetch()` → returns list of raw grant dicts
  - `normalize(raw_grant)` → returns standardized grant dict
  - `is_available()` → returns bool (health check)
  - `get_source_name()` → returns string identifier
- [ ] **FIX**: Update `app/models.py` - expand `data_source` Literal to include new sources:
  ```python
  data_source: Literal["grants.gov", "eu.funding", "open.philanthropy", "mock"] = Field(
      default="mock", description="Source of grant data"
  )
  ```
- [ ] Refactor `grantsgov.py` to extend `BaseSourceAdapter`
- [ ] Create adapter registry pattern in `__init__.py`:
  ```python
  ADAPTERS = {
      "grants.gov": GrantsGovAdapter(),
      # future sources added here
  }
  ```
- [ ] Update `main.py` to iterate through all adapters and aggregate results
- [ ] Ensure each adapter tags grants with `data_source` field

### Test Verification
```bash
curl http://localhost:8000/grants | jq '.[].data_source' | sort | uniq -c
# Should show: grants.gov (when available) or mock (fallback)
```

### Commit Message
```
git commit -m "refactor: modular source adapter architecture with base class"
```

---

## Task 2: Add Second Real Source (EU Funding)

**Estimated Effort:** Medium  
**Execution Order:** After Task 1  
**Dependencies:** Task 1 complete

### Description
Implement second real data source from EU Funding & Tenders Portal (or similar stable API).

### Files to Modify
- `backend/app/sources/eu_funding.py` — create new adapter
- `backend/app/sources/__init__.py` — register adapter
- `backend/requirements.txt` — add any new dependencies

### Acceptance Criteria
- [ ] Create `EUFundingAdapter` class extending `BaseSourceAdapter`
- [ ] Implement `fetch()` method calling EU Funding API or RSS
- [ ] Implement `normalize()` converting EU format to our schema
- [ ] Handle EU-specific fields: programme (Horizon Europe, etc.), funding rates, topics
- [ ] Map EU fields to our schema:
  - `title` → project title
  - `funding_amount` → total budget or typical grant size
  - `deadline` → call deadline
  - `region` → "European Union"
  - `eligibility` → extracted from call text
  - `source_name` → "EU Funding & Tenders"
  - `source_url` → direct link to call page
- [ ] Handle API errors gracefully (return empty list, log failure)
- [ ] Register in `ADAPTERS` dict with key `"eu.funding"`

### Test Verification
```bash
curl http://localhost:8000/grants | jq '.[].data_source' | sort | uniq -c
# Should show both: grants.gov and eu.funding entries
```

### Commit Message
```
git commit -m "feat: add EU Funding & Tenders as second data source"
```

---

## Task 3: Add Third Real Source (Open Philanthropy or Similar)

**Estimated Effort:** Medium  
**Execution Order:** After Task 2  
**Dependencies:** Task 2 complete

### Description
Implement third real data source from Open Philanthropy or another stable grant source.

### Files to Modify
- `backend/app/sources/open_phil.py` — create new adapter
- `backend/app/sources/__init__.py` — register adapter
- `backend/app/sources/` — add any helper modules

### Acceptance Criteria
- [ ] Create `OpenPhilanthropyAdapter` class extending `BaseSourceAdapter`
- [ ] Implement `fetch()` parsing Open Philanthropy grants page or API
- [ ] Implement `normalize()` converting their format to our schema
- [ ] Map fields to our schema:
  - `title` → grant title
  - `funding_amount` → grant amount in USD
  - `deadline` → use rolling deadline or next funding cycle date
  - `region` → extracted from focus area or "Global"
  - `eligibility` → from grant description
  - `source_name` → "Open Philanthropy"
  - `source_url` → grant page URL
- [ ] Handle parsing errors gracefully
- [ ] Register in `ADAPTERS` dict with key `"open.philanthropy"`

### Test Verification
```bash
curl http://localhost:8000/grants | jq '.[].data_source' | sort | uniq -c
# Should show: grants.gov, eu.funding, open.philanthropy
```

### Commit Message
```
git commit -m "feat: add Open Philanthropy as third data source"
```

---

## Task 4: Enhanced Deduplication System

**Estimated Effort:** Medium  
**Execution Order:** After Task 3  
**Dependencies:** Task 3 complete

### Description
Improve deduplication to handle cross-source duplicates (same grant from different sources).

### Files to Modify
- `backend/app/deduplicator.py` — enhance logic
- `backend/app/deduplicator.py` — add fuzzy matching

### Acceptance Criteria
- [ ] Implement exact match detection on `title` + `deadline` + `funding_amount`
- [ ] Implement fuzzy title matching (80% similarity threshold) for near-duplicates
- [ ] Normalize titles before matching: lowercase, remove punctuation, trim whitespace
- [ ] When duplicates found, keep grant from preferred source order:
  1. grants.gov (official government source)
  2. eu.funding (official EU source)
  3. open.philanthropy
  4. mock (lowest priority)
- [ ] Log deduplication stats: total fetched, unique grants, duplicates removed
- [ ] Add `duplicate_of` field to track which grant this was merged with (optional)

### Test Verification
```bash
# Check logs for deduplication stats
tail -f backend/logs/audit.log | grep dedup
# Should show: "Deduplication: X total, Y unique, Z duplicates removed"
```

### Commit Message
```
git commit -m "feat: enhanced cross-source deduplication with fuzzy matching"
```

---

## Task 5: Query Parameters for /grants Endpoint

**Estimated Effort:** Small  
**Execution Order:** After Task 4  
**Dependencies:** Task 4 complete

### Description
Add query parameters to `/grants` endpoint to support frontend filtering.

### Files to Modify
- `backend/main.py` — update `get_grants()` function

### Acceptance Criteria
- [ ] Add query parameter `source` (string) — filter by data_source
- [ ] Add query parameter `region` (string) — filter by region field
- [ ] Add query parameter `topics` (comma-separated string) — filter by topics
- [ ] Add query parameter `search` (string) — search in title + description
- [ ] Add query parameter `min_score` (int) — filter by minimum score
- [ ] Add query parameter `limit` (int, default=50, max=100) — limit results
- [ ] Add query parameter `offset` (int, default=0) — pagination
- [ ] Filtering logic:
  - `source`: exact match on `data_source`
  - `region`: case-insensitive substring match
  - `topics`: match any of the provided topics (OR logic)
  - `search`: case-insensitive search in both `title` and `description`
  - `min_score`: grants with score >= value
- [ ] Return filtered results maintaining original sort order (by score desc)

### Test Verification
```bash
# Test each filter
curl "http://localhost:8000/grants?source=grants.gov"
curl "http://localhost:8000/grants?region=United%20States"
curl "http://localhost:8000/grants?topics=AI,Climate"
curl "http://localhost:8000/grants?search=healthcare"
curl "http://localhost:8000/grants?min_score=70&limit=10"
```

### Commit Message
```
git commit -m "feat: add query parameters for filtering and search to /grants"
```

---

## Task 6: Source Availability Health Check

**Estimated Effort:** Small  
**Execution Order:** After Task 5  
**Dependencies:** Task 5 complete

### Description
Add health check endpoint showing status of each data source.

### Files to Modify
- `backend/main.py` — add `/health/sources` endpoint
- `backend/app/sources/__init__.py` — add health check function

### Acceptance Criteria
- [ ] Create `GET /health/sources` endpoint
- [ ] Return JSON with status for each adapter:
  ```json
  {
    "grants.gov": {"available": true, "last_fetch": "2026-04-14T10:00:00", "grant_count": 25},
    "eu.funding": {"available": true, "last_fetch": "2026-04-14T10:05:00", "grant_count": 15},
    "open.philanthropy": {"available": false, "error": "Connection timeout", "grant_count": 0},
    "mock": {"available": true, "is_fallback": false}
  }
  ```
- [ ] Each adapter stores last fetch timestamp and result
- [ ] Track if mock data is being used as fallback

### Test Verification
```bash
curl http://localhost:8000/health/sources | jq
```

### Commit Message
```
git commit -m "feat: add source health check endpoint"
```

---

## Task 7: Stable Startup with Fallback Chain

**Estimated Effort:** Small  
**Execution Order:** Last  
**Dependencies:** All above tasks complete

### Description
Ensure backend always starts successfully, using fallback chain when sources fail.

### Files to Modify
- `backend/main.py` — enhance `load_grants()` function

### Acceptance Criteria
- [ ] Backend starts even if all real sources are unavailable
- [ ] Attempt all registered adapters in sequence
- [ ] If all real sources fail, log warning and use mock data
- [ ] If mock data also fails, return empty list with error message
- [ ] Set `USE_MOCK_FALLBACK` flag in response headers or log
- [ ] Ensure `/grants` never returns HTTP 500 — always returns 200 with data or empty array

### Test Verification
```bash
# Start with network disabled (simulate all sources down)
# Should still return mock data with 200 OK
curl -v http://localhost:8000/grants
# Check response header: X-Data-Source: fallback-mock
```

### Commit Message
```
git commit -m "feat: stable startup with fallback chain, never fail on /grants"
```

---

## Task Summary

| Task | Effort | Execution Order | Files |
|------|--------|-----------------|-------|
| 1. Modular Architecture | Medium | 1st | `sources/base.py`, `sources/__init__.py`, `sources/grantsgov.py` |
| 2. EU Funding Source | Medium | 2nd | `sources/eu_funding.py` |
| 3. Open Philanthropy | Medium | 3rd | `sources/open_phil.py` |
| 4. Deduplication | Medium | 4th | `deduplicator.py` |
| 5. Query Parameters | Small | 5th | `main.py` |
| 6. Health Check | Small | 6th | `main.py`, `sources/__init__.py` |
| 7. Stable Startup | Small | 7th | `main.py` |

---

## Expected Final Result

### Data Flow
```
Request /grants
    ↓
Try all adapters (grants.gov, eu.funding, open.philanthropy)
    ↓
Aggregate results from available sources
    ↓
Deduplicate (exact + fuzzy matching)
    ↓
Apply filters (if query params provided)
    ↓
Enrich with intelligence layer
    ↓
Return grants[] (or mock fallback if all real sources fail)
```

### API Contract

**GET** `/grants?source=&region=&topics=&search=&min_score=&limit=&offset=`

Response always includes `data_source` field per grant:
- `"grants.gov"` — from US government source
- `"eu.funding"` — from EU Funding & Tenders
- `"open.philanthropy"` — from Open Philanthropy
- `"mock"` — fallback data when all real sources unavailable

### Verification Commands

```bash
# Verify real data (not mock)
curl http://localhost:8000/grants | jq '.[0].data_source'
# Expected: "grants.gov" or "eu.funding" or "open.philanthropy" (NOT "mock")

# Verify search works
curl "http://localhost:8000/grants?search=climate" | jq length

# Verify filter works
curl "http://localhost:8000/grants?source=grants.gov" | jq '.[].data_source' | uniq

# Verify health endpoint
curl http://localhost:8000/health/sources | jq
```

---

## Daily Workflow

```bash
# Start of day
git checkout main && git pull origin main
git checkout arvin/phase2-ingestion && git rebase main

# After each task
git add .
git commit -m "descriptive message"
git add TASKS-arvin-phase2.md  # update status
git commit -m "docs: update phase2 tasks"
git push origin arvin/phase2-ingestion
```

---

## Key Rules

- **Never commit to `main` directly**
- **Mock data is FALLBACK ONLY** — not primary source
- **All sources must use adapter pattern** — no hardcoded fetch logic
- **Always include `data_source` field** — frontend needs this for filters
- **Deduplication must handle cross-source duplicates**
- **Backend must never crash on source failure**

---

*Task File Version: Phase 2*  
*Created: Phase 2 Planning*
