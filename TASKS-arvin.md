# Arvin — Backend Development Tasks

**Role:** Backend Developer  
**Responsibility:** FastAPI backend, API endpoints, data models, mock data

---

## Branch Naming

All work in branch: `arvin/backend-mvp`

```bash
git checkout -b arvin/backend-mvp
```

---

## Task 1: Project Scaffold

**Estimated Effort:** Small  
**Dependencies:** Marina completes project structure

### Description
Set up the backend directory structure and basic FastAPI application.

### Acceptance Criteria
- [ ] Create `backend/` directory with subdirectories:
  - `app/` — application code
  - `data/` — mock data storage
  - `tests/` — test files
- [ ] Create `main.py` with basic FastAPI app
- [ ] Create `requirements.txt` with dependencies:
  - fastapi
  - uvicorn
  - pydantic
- [ ] App runs with `uvicorn main:app --reload`
- [ ] `/docs` endpoint shows auto-generated documentation

### Commit Message
```
git commit -m "Add backend scaffold with FastAPI structure"
```

---

## Task 2: Data Models

**Estimated Effort:** Small  
**Dependencies:** Task 1 complete

### Description
Create Pydantic models matching the shared data structure exactly.

### Acceptance Criteria
- [ ] Create `app/models.py` with `Grant` model
- [ ] Model includes all raw fields:
  - id (str)
  - title (str)
  - description (str)
  - funding_amount (number)
  - currency (str)
  - deadline (str)
  - eligibility (str)
  - region (str)
  - source_name (str)
  - source_url (str)
  - status (str with values: open, closed, draft)
- [ ] Model includes all intelligence fields:
  - topics (list[str])
  - confidence (float)
  - trend_label (str)
  - score (int)
  - explanation (str)
- [ ] Model validates status is one of: open, closed, draft
- [ ] Model validates score is 0-100

### Commit Message
```
git commit -m "Add Pydantic Grant model with all required fields"
```

---

## Task 3: Mock Data

**Estimated Effort:** Medium  
**Dependencies:** Task 2 complete

### Description
Create 10 sample grants with realistic data for development and testing.

### Acceptance Criteria
- [ ] Create `data/grants.json` with 10 grant objects
- [ ] Each grant has all required fields (raw + intelligence)
- [ ] Variety of topics represented: AI, Climate, Healthcare, Education, etc.
- [ ] Different funding amounts: small (<$10K), medium ($50-100K), large (>$100K)
- [ ] Mix of trend labels: Emerging, Growing, Stable, Declining
- [ ] Scores distributed across ranges: high (70+), medium (40-69), low (<40)
- [ ] Data loads without errors in Python

### Sample Data Format
```json
{
  "id": "nsf-2024-001",
  "title": "AI for Climate Adaptation Research",
  "description": "Funding for innovative AI applications in climate resilience...",
  "funding_amount": 500000,
  "currency": "USD",
  "deadline": "2024-08-15",
  "eligibility": "US universities and research institutions",
  "region": "United States",
  "source_name": "NSF",
  "source_url": "https://nsf.gov/grants/...",
  "status": "open",
  "topics": ["AI", "Climate"],
  "confidence": 0.85,
  "trend_label": "Growing",
  "score": 82,
  "explanation": "High funding amount with strong alignment to priority research areas"
}
```

### Commit Message
```
git commit -m "Add mock data with 10 sample grants"
```

---

## Task 4: GET /grants Endpoint

**Estimated Effort:** Small  
**Dependencies:** Task 2 and Task 3 complete

### Description
Implement the main API endpoint that returns all grants.

### Acceptance Criteria
- [ ] Create `GET /grants` endpoint in `main.py`
- [ ] Endpoint returns list of Grant objects as JSON
- [ ] Response includes all intelligence fields populated
- [ ] Data loads from `data/grants.json`
- [ ] Response status is 200 OK
- [ ] Content-Type is `application/json`

### Test Command
```bash
curl http://localhost:8000/grants
```

### Expected Output
```json
[
  {
    "id": "nsf-2024-001",
    "title": "AI for Climate Adaptation Research",
    ...
  }
]
```

### Commit Message
```
git commit -m "Add GET /grants endpoint returning enriched grant data"
```

---

## Task 5: CORS Configuration

**Estimated Effort:** Small  
**Dependencies:** Task 4 complete

### Description
Enable Cross-Origin Resource Sharing so the frontend can call the API.

### Acceptance Criteria
- [ ] Add CORS middleware to FastAPI app
- [ ] Allow origins: `http://localhost:3000`, `http://localhost:5173`
- [ ] Allow methods: GET, POST, OPTIONS
- [ ] Allow headers: Content-Type, Authorization
- [ ] Frontend running on different port can successfully call `/grants`

### Commit Message
```
git commit -m "Configure CORS for frontend access"
```

---

## Task 6: Backend Documentation

**Estimated Effort:** Small  
**Dependencies:** All above tasks complete

### Description
Document the backend setup and API for other team members.

### Acceptance Criteria
- [ ] Create `backend/README.md` with sections:
  - Setup instructions (install, run)
  - API endpoint description
  - Data model overview
  - Testing commands
- [ ] Include sample `curl` command for testing
- [ ] Document port (8000) and auto-docs URL (`/docs`)

### Commit Message
```
git commit -m "Add backend README with setup and API documentation"
```

---

## Task 7: Integration Hook (Optional)

**Estimated Effort:** Medium  
**Dependencies:** Marina's intelligence module ready

### Description
Integrate Marina's intelligence module to enrich grants dynamically.

### Acceptance Criteria
- [ ] Import intelligence module from `intelligence/` directory
- [ ] Call `analyze_grant()` for each grant before returning
- [ ] Handle case where intelligence module not available (use mock data)
- [ ] Ensure no errors if intelligence module raises exceptions

### Note
This task can be skipped if time is short—mock data already includes intelligence fields.

### Commit Message
```
git commit -m "Integrate intelligence module for dynamic grant enrichment"
```

---

## Task Summary

| Task | Effort | Status | Notes |
|------|--------|--------|-------|
| 1. Project Scaffold | Small | ⬜ | Do first |
| 2. Data Models | Small | ⬜ | After scaffold |
| 3. Mock Data | Medium | ⬜ | Needs variety |
| 4. GET /grants | Small | ⬜ | Core endpoint |
| 5. CORS Config | Small | ⬜ | For frontend |
| 6. Documentation | Small | ⬜ | Final polish |
| 7. Integration | Medium | ⬜ | If time allows |

---

## Daily Workflow

1. **Start of day:** Pull latest from `main` and rebase your branch
   ```bash
   git checkout main
   git pull origin main
   git checkout arvin/backend-mvp
   git rebase main
   ```

2. **During work:** Commit after completing each task
   ```bash
   git add .
   git commit -m "descriptive message"
   git push origin arvin/backend-mvp
   ```

3. **End of day:** Push all commits and update team on progress

---

## Key Rules

- **Never commit to `main` directly**
- **Work only in `arvin/backend-mvp` branch**
- **Do not modify frontend or intelligence code**
- **Follow the shared data structure exactly—no field renaming**
- **Ask Marina if data contracts need clarification**

---

*Task File Version: 1.0*  
*Created: Project Initiation*
