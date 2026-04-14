# Marina — Phase 2 Coordination & Quality Assurance

**Role:** Team Leader + QA Coordinator  
**Branch:** `marina/phase2-coordination`  
**Goal:** Validate data integrity, verify system integration, ensure backend-frontend synchronization

---

## Overview

Phase 2 coordination focuses on ensuring the transition from mock data to real data sources is seamless. Validate data structure compliance, verify `/grants` endpoint returns real data, ensure UI behaves correctly with real datasets, and coordinate the implementation of 2-3 real sources.

---

## Task 1: Define Initial 3 Sources for Implementation

**Estimated Effort:** Small  
**Execution Order:** First (Day 1)  
**Dependencies:** None

### Description
Research and document the 3 real data sources Arvin will implement. Verify API availability and stability.

### Files to Create/Modify
- `docs/data-sources.md` — create new documentation
- `TASKS-arvin-phase2.md` — update with source specifics

### Acceptance Criteria
- [ ] Research and select 3 sources meeting criteria:
  - **Source 1 (US Government):** Grants.gov (already implemented, verify still works)
  - **Source 2 (International):** EU Funding & Tenders Portal (CORDIS API or RSS)
  - **Source 3 (Private Foundation):** Open Philanthropy (web scraping or API if available)
- [ ] Document for each source:
  - API endpoint or feed URL
  - Authentication requirements (none preferred for MVP)
  - Rate limits
  - Data format (XML, JSON, HTML)
  - Update frequency
  - Typical grant count per fetch
- [ ] Verify each source is accessible (test URLs in browser/curl)
- [ ] Document any source-specific field mapping requirements
- [ ] Create fallback priority order: grants.gov → eu.funding → open.philanthropy → mock

### Test Verification
```bash
# Test source 1
curl -I https://www.grants.gov/rss/GG_NewOppByAgency.xml

# Test source 2 (EU)
curl "https://cordis.europa.eu/api/v1/search?query=..."

# Test source 3 (Open Phil)
curl https://www.openphilanthropy.org/grants/
```

### Commit Message
```
git commit -m "docs: define initial 3 data sources with API specs"
```

---

## Task 2: Validate Grant Data Structure Compliance

**Estimated Effort:** Small  
**Execution Order:** After Arvin Task 1  
**Dependencies:** Arvin Task 1 complete (modular architecture)

### Description
Verify all grants (from any source) conform to the shared data structure defined in `app/models.py`.

### Files to Create
- `backend/tests/test_data_validation.py` — create validation tests

### Acceptance Criteria
- [ ] Create validation function that checks every grant has required fields:
  - **Raw fields:** `id`, `title`, `description`, `funding_amount`, `currency`, `deadline`, `eligibility`, `region`, `source_name`, `source_url`, `status`
  - **Intelligence fields:** `topics`, `confidence`, `trend_label`, `score`, `explanation`
  - **Metadata:** `data_source`
- [ ] Validate field types:
  - `id`: string, non-empty
  - `title`: string, non-empty
  - `description`: string, non-empty
  - `funding_amount`: number >= 0
  - `currency`: string (ISO format preferred: USD, EUR)
  - `deadline`: string (ISO date format: YYYY-MM-DD)
  - `status`: one of "open", "closed", "draft"
  - `topics`: array of strings
  - `score`: integer 0-100
  - `confidence`: float 0.0-1.0
  - `trend_label`: one of "Emerging", "Growing", "Stable", "Declining"
- [ ] Create test that validates grants from each source
- [ ] Log validation errors with grant ID and missing/invalid field

### Test Verification
```bash
cd backend
python -m pytest tests/test_data_validation.py -v
# All tests should pass for both mock and real data
```

### Commit Message
```
git commit -m "test: add data structure validation tests"
```

---

## Task 3: Verify /grants Returns Real Non-Empty Data

**Estimated Effort:** Small  
**Execution Order:** After Arvin Tasks 2-3  
**Dependencies:** Arvin has 2-3 real sources implemented

### Description
Systematically verify that `/grants` endpoint returns real data from actual sources, not just mock data.

### Files to Create
- `backend/tests/test_integration.py` — create integration tests
- `scripts/verify_real_data.sh` — create verification script (optional)

### Acceptance Criteria
- [ ] Create integration test that:
  1. Calls `GET /grants` with network enabled
  2. Verifies response is non-empty array
  3. Verifies at least one grant has `data_source != "mock"`
  4. Verifies grants have intelligence fields populated
- [ ] Verify each source appears in results when available:
  ```bash
  curl http://localhost:8000/grants | jq 'group_by(.data_source) | map({source: .[0].data_source, count: length})'
  # Expected: [{"source":"grants.gov","count":25},{"source":"eu.funding","count":15}]
  ```
- [ ] Verify mock data is NOT primary source when real sources available
- [ ] Document in `docs/verification.md` how to check for real data

### Test Verification
```bash
# Manual verification
curl http://localhost:8000/grants | jq '.[0] | {source: .data_source, title: .title, has_score: (.score != null)}'

# Should return:
# {
#   "source": "grants.gov",
#   "title": "Actual grant title from source",
#   "has_score": true
# }
# NOT: "source": "mock"
```

### Commit Message
```
git commit -m "test: add integration tests for real data verification"
```

---

## Task 4: Verify UI Behavior with Real Data

**Estimated Effort:** Medium  
**Execution Order:** After Nazar Task 3  
**Dependencies:** Nazar has search and filters implemented

### Description
Test frontend behavior with real data from multiple sources. Ensure UI handles edge cases in real data.

### Files to Create
- `docs/ui-verification-checklist.md` — create verification checklist

### Acceptance Criteria
- [ ] **Load Test:**
  - [ ] Frontend loads with 20-50 grants without performance issues
  - [ ] Grant cards render correctly with real data fields
  - [ ] No console errors when rendering
- [ ] **Search Test:**
  - [ ] Search works with real grant titles
  - [ ] Search finds matches in descriptions
  - [ ] Search handles special characters gracefully
  - [ ] Empty search results show appropriate message
- [ ] **Filter Test:**
  - [ ] Source filter shows options matching actual sources in data
  - [ ] Region filter populates from real data regions
  - [ ] Topics filter shows topics from real data
  - [ ] Filters combine correctly (AND logic)
- [ ] **Edge Cases:**
  - [ ] Grants with very long titles display correctly (truncated with ellipsis)
  - [ ] Grants with missing optional fields don't break UI
  - [ ] Grants with special characters render correctly
  - [ ] Score 0 and score 100 display with correct colors

### Test Verification
```bash
# Start full stack
cd backend && uvicorn main:app --reload &
cd frontend && npx serve . &

# Open browser to http://localhost:3000
# Navigate to Grants page
# Verify: grants load, search works, filters work, no console errors
```

### Commit Message
```
git commit -m "docs: add UI verification checklist for real data"
```

---

## Task 5: Backend-Frontend Synchronization

**Estimated Effort:** Small  
**Execution Order:** After Task 4  
**Dependencies:** Both backend and frontend have filter/search features

### Description
Ensure backend query parameters and frontend filter state stay synchronized.

### Files to Modify
- `docs/api-contract.md` — document query parameter contract
- Coordinate with Arvin and Nazar on any mismatches

### Acceptance Criteria
- [ ] Document exact query parameter names and formats:
  | Parameter | Type | Example | Backend Support | Frontend Support |
  |-----------|------|---------|-----------------|------------------|
  | `search` | string | `search=climate` | ✅ | ✅ |
  | `source` | string | `source=grants.gov` | ✅ | ✅ |
  | `region` | string | `region=US` | ✅ | ✅ |
  | `topics` | string | `topics=AI,Climate` | ✅ | ✅ |
  | `min_score` | int | `min_score=70` | ✅ | ✅ |
  | `limit` | int | `limit=12` | ✅ | ✅ |
  | `offset` | int | `offset=24` | ✅ | ✅ |
- [ ] Verify URL params from frontend match backend expectations
- [ ] Test round-trip: frontend sets filter → URL updates → backend receives correct params → results match
- [ ] Verify pagination params work correctly between frontend and backend
- [ ] Document any limitations (e.g., topics filter uses OR vs AND logic)

### Test Verification
```bash
# Test URL round-trip
# 1. Frontend: select source=grants.gov, search=health
# 2. URL should be: /grants?source=grants.gov&search=health
# 3. Backend receives: source=grants.gov, search=health
# 4. Results: only grants.gov grants matching "health"

curl "http://localhost:8000/grants?source=grants.gov&search=health" | jq length
# Count should match what frontend displays
```

### Commit Message
```
git commit -m "docs: document API contract for query parameters"
```

---

## Task 6: Fallback Behavior Verification

**Estimated Effort:** Small  
**Execution Order:** After Arvin Task 7  
**Dependencies:** Arvin has stable startup with fallback implemented

### Description
Verify system behaves correctly when sources fail and fallback to mock data.

### Files to Create
- `backend/tests/test_fallback.py` — create fallback tests

### Acceptance Criteria
- [ ] Test scenario: All real sources unavailable
  - [ ] Backend starts successfully
  - [ ] `/grants` returns mock data
  - [ ] Response includes header or field indicating fallback
  - [ ] Frontend displays grants without error
- [ ] Test scenario: One source available, others fail
  - [ ] Backend returns data from available source only
  - [ ] No mock data included
  - [ ] UI shows correct source breakdown
- [ ] Test scenario: Source recovers after being down
  - [ ] Subsequent requests fetch from recovered source
  - [ ] Cache is refreshed appropriately
- [ ] Document fallback behavior in `docs/resilience.md`

### Test Verification
```bash
# Simulate source failure (block grants.gov DNS or use test flag)
# Verify fallback to mock
curl http://localhost:8000/grants | jq '.[0].data_source'
# Should return "mock" when all real sources fail

# Check health endpoint
curl http://localhost:8000/health/sources | jq
# Should show available: false for failed sources
```

### Commit Message
```
git commit -m "test: add fallback behavior verification tests"
```

---

## Task 7: Final Integration Test and Sign-off

**Estimated Effort:** Medium  
**Execution Order:** Last (end of Phase 2)  
**Dependencies:** All other tasks complete

### Description
Run complete end-to-end test and sign off on Phase 2 completion.

### Files to Create
- `docs/phase2-completion-report.md` — create completion report

### Acceptance Criteria
- [ ] **Pre-flight Checklist:**
  - [ ] Backend starts with `uvicorn main:app --reload`
  - [ ] Frontend opens without errors
  - [ ] `/grants` returns real data (non-mock) when sources available
  - [ ] `/health/sources` shows correct source status
  - [ ] Search works across title and description
  - [ ] Filters (source, region, topics) work correctly
  - [ ] Pagination works for large datasets
  - [ ] Mobile responsive layout works
  - [ ] Fallback to mock works when sources fail
- [ ] **Performance Check:**
  - [ ] Page loads in < 3 seconds with 50 grants
  - [ ] Search/filter responds in < 500ms
  - [ ] No memory leaks after extended use
- [ ] **Sign-off:**
  - [ ] All acceptance criteria met
  - [ ] Arvin confirms backend tasks complete
  - [ ] Nazar confirms frontend tasks complete
  - [ ] Marina confirms integration tests pass
  - [ ] Create Phase 2 completion report

### Test Verification
```bash
# Run full integration suite
cd backend
python -m pytest tests/ -v

# Manual end-to-end test
# 1. Start backend
# 2. Open frontend
# 3. Verify grants load from real sources
# 4. Test search: "climate" → results filter
# 5. Test filters: source=grants.gov → only gov grants
# 6. Test pagination: navigate pages
# 7. Simulate offline → verify fallback
# 8. All tests pass → sign off
```

### Commit Message
```
git commit -m "docs: add Phase 2 completion report"
```

---

## Task Summary

| Task | Effort | Execution Order | Files |
|------|--------|-----------------|-------|
| 1. Define 3 Sources | Small | 1st | `docs/data-sources.md` |
| 2. Validate Data Structure | Small | 2nd | `tests/test_data_validation.py` |
| 3. Verify /grants Real Data | Small | 3rd | `tests/test_integration.py` |
| 4. Verify UI Behavior | Medium | 4th | `docs/ui-verification-checklist.md` |
| 5. Backend-Frontend Sync | Small | 5th | `docs/api-contract.md` |
| 6. Fallback Verification | Small | 6th | `tests/test_fallback.py` |
| 7. Final Integration Test | Medium | 7th | `docs/phase2-completion-report.md` |

---

## Expected Final Result

### System State
```
Backend (Port 8000)
├── /grants          → Returns real data from 2-3 sources
├── /health          → Returns "healthy"
├── /health/sources  → Shows source availability
└── Query Params     → Supports search, filters, pagination

Frontend (Port 3000)
├── Search Bar       → Filters by title + description
├── Filter Panel     → Source, Region, Topics
├── Grant Counter    → Shows "X of Y grants"
├── Pagination       → Handles 20-50+ grants
└── Mobile Layout    → Responsive filters

Data Sources (3 total)
├── grants.gov       → US government grants
├── eu.funding       → EU Funding & Tenders
└── open.philanthropy → Open Philanthropy grants
```

### Verification Matrix

| Feature | Backend | Frontend | Integration |
|---------|---------|----------|-------------|
| Real data ingestion | ✅ | N/A | ✅ |
| Search (title + description) | ✅ | ✅ | ✅ |
| Filter by source | ✅ | ✅ | ✅ |
| Filter by region | ✅ | ✅ | ✅ |
| Filter by topics | ✅ | ✅ | ✅ |
| Pagination | ✅ | ✅ | ✅ |
| Fallback to mock | ✅ | ✅ | ✅ |
| Mobile responsive | N/A | ✅ | ✅ |

### Sign-off Criteria

Phase 2 is complete when:
1. `/grants` returns real data from at least 2 sources
2. Search works across title and description
3. All 3 filters (source, region, topics) work correctly
4. UI handles 20-50 grants with pagination
5. Fallback to mock works when sources fail
6. All tests pass
7. Documentation is complete

---

## Daily Workflow

```bash
# Start of day
git checkout main && git pull origin main
git checkout marina/phase2-coordination && git rebase main

# After each task
git add .
git commit -m "descriptive message"
git add TASKS-marina-phase2.md  # update status
git commit -m "docs: update phase2 tasks"
git push origin marina/phase2-coordination

# Coordination
check_in_with_arvin()  # verify backend progress
check_in_with_nazar()   # verify frontend progress
```

---

## Key Rules

- **Never commit to `main` directly**
- **Coordinate daily** — check in with Arvin and Nazar
- **Document everything** — API contracts, verification steps
- **Verify with real data** — not just mock data
- **Test edge cases** — long titles, special characters, empty fields
- **Phase 2 complete only when all 7 tasks pass sign-off**

---

## Coordination Checklist

### Week 1
- [ ] Day 1: Task 1 complete (sources defined), Arvin starts Task 1
- [ ] Day 2: Check Arvin progress on modular architecture
- [ ] Day 3: Task 2 complete (data validation), Nazar starts Task 1
- [ ] Day 4: Check Nazar progress on false empty state fix
- [ ] Day 5: Mid-week review — all Task 1s should be complete

### Week 2
- [ ] Day 1: Task 3 complete (real data verification), Arvin Task 2-3 in progress
- [ ] Day 2: Check Arvin progress on 2nd/3rd sources
- [ ] Day 3: Task 4 started (UI verification), Nazar Task 2-3 in progress
- [ ] Day 4: Check Nazar progress on search and filters
- [ ] Day 5: Task 4 complete, Task 5 (sync) in progress

### Week 3
- [ ] Day 1: Task 5 complete, Task 6 (fallback) in progress
- [ ] Day 2: Task 6 complete
- [ ] Day 3: Task 7 (final integration) started
- [ ] Day 4: Final testing and bug fixes
- [ ] Day 5: Phase 2 completion report, sign-off

---

*Task File Version: Phase 2*  
*Created: Phase 2 Planning*
