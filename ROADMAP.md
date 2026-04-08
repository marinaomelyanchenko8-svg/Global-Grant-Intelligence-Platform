# Global Grant Intelligence Platform — MVP Roadmap

**Development Plan | Parallel Execution Strategy**

---

## Overview

This roadmap enables the team of 3 to work in parallel with minimal dependencies. Tasks are sequenced to maximize efficiency while ensuring smooth integration.

**Principles:**
- No work directly in `main` branch
- Marina creates project structure first
- Arvin and Nazar can begin scaffolding immediately after structure is ready
- Intelligence and coordination tasks assigned to Marina
- Final integration and merging coordinated by Marina

---

## Phase 1: Foundation (Day 1)

| Task | Owner | Branch | Output |
|------|-------|--------|--------|
| Create project structure | Marina | `marina/project-structure` | Root directories, MASTER-PROMPT.md, README.md, .gitignore |
| Initialize repository | Marina | `marina/project-structure` | Working Git setup with `main` protected |
| Create backend scaffolding | Arvin | `arvin/backend-mvp` | `backend/` directory with FastAPI skeleton, requirements.txt |
| Create frontend scaffolding | Nazar | `nazar/frontend-mvp` | `frontend/` directory with HTML/CSS/JS structure |

**Dependencies:**
- Marina's structure task must complete first
- Arvin and Nazar can work in parallel after structure is pushed

**Acceptance Criteria:**
- [ ] Project root has `backend/`, `frontend/`, `intelligence/`, `docs/` directories
- [ ] Each team member has created their working branch
- [ ] Basic scaffold files exist and run without errors

---

## Phase 2: Core Development (Days 2-4)

### Backend Track (Arvin)

| Task | Owner | Branch | Output |
|------|-------|--------|--------|
| Define data models | Arvin | `arvin/backend-mvp` | Pydantic models matching shared data structure |
| Create mock data (10 grants) | Arvin | `arvin/backend-mvp` | `backend/data/grants.json` with complete sample data |
| Implement GET /grants endpoint | Arvin | `arvin/backend-mvp` | Working API returning structured JSON |
| Add CORS middleware | Arvin | `arvin/backend-mvp` | Frontend can call API from different port |
| API documentation | Arvin | `arvin/backend-mvp` | Auto-generated docs at `/docs` |

### Frontend Track (Nazar)

| Task | Owner | Branch | Output |
|------|-------|--------|--------|
| Create grant card component | Nazar | `nazar/frontend-mvp` | HTML/CSS card showing title, funding, score, explanation |
| Implement grant list view | Nazar | `nazar/frontend-mvp` | Container for multiple grant cards |
| Add API client | Nazar | `nazar/frontend-mvp` | JavaScript fetch to `localhost:8000/grants` |
| Add score color coding | Nazar | `nazar/frontend-mvp` | Green (70+), yellow (40-69), red (<40) |
| Loading and error states | Nazar | `nazar/frontend-mvp` | User feedback for async operations |

### Intelligence Track (Marina)

| Task | Owner | Branch | Output |
|------|-------|--------|--------|
| Create topic detection module | Marina | `marina/intelligence-and-coordination` | Keyword-based topic extraction |
| Implement trend classifier | Marina | `marina/intelligence-and-coordination` | Logic for Emerging/Growing/Stable/Declining |
| Build scoring engine | Marina | `marina/intelligence-and-coordination` | Rule-based 0-100 scoring |
| Add explanation generator | Marina | `marina/intelligence-and-coordination` | Template-based rationale generation |
| Integration hook | Marina | `marina/intelligence-and-coordination` | Function to enrich raw grant data |

**Dependencies:**
- Arvin and Nazar work independently after scaffolding
- Marina's intelligence module can begin with mock data if needed
- No cross-dependencies between Arvin and Nazar tasks

**Acceptance Criteria:**
- [ ] Backend returns 10 grants at `GET /grants`
- [ ] Frontend displays grant cards with all required fields
- [ ] Intelligence module can process a grant and return enriched fields

---

## Phase 3: Integration (Day 5)

| Task | Owner | Branch | Output |
|------|-------|--------|--------|
| Integrate intelligence into backend | Arvin | `arvin/backend-mvp` | Backend calls intelligence module before returning grants |
| Test end-to-end flow | Marina | `marina/intelligence-and-coordination` | Verify frontend → backend → intelligence → frontend works |
| Fix integration issues | All | Individual branches | Resolve any cross-component bugs |
| Verify data contracts | Marina | `marina/intelligence-and-coordination` | Confirm all fields match shared structure |

**Dependencies:**
- Requires completion of Phase 2 core tasks
- All three tracks must have working code

**Acceptance Criteria:**
- [ ] Frontend displays grants with intelligence fields populated
- [ ] Score, trend_label, topics, and explanation are visible
- [ ] No console errors or API failures

---

## Phase 4: UI Polish & Documentation (Day 6)

| Task | Owner | Branch | Output |
|------|-------|--------|--------|
| Final UI refinements | Nazar | `nazar/frontend-mvp` | Consistent styling, spacing, mobile-friendly |
| Backend documentation | Arvin | `arvin/backend-mvp` | Setup instructions, API usage in `backend/README.md` |
| Frontend documentation | Nazar | `nazar/frontend-mvp` | Setup and run instructions in `frontend/README.md` |
| Architecture documentation | Marina | `marina/intelligence-and-coordination` | System overview in `docs/architecture.md` |
| Create TASKS files | Marina | `marina/intelligence-and-coordination` | `TASKS-arvin.md`, `TASKS-nazar.md`, `TASKS-marina.md` |
| Create WORKFLOW.md | Marina | `marina/intelligence-and-coordination` | Branch and commit protocols |

**Dependencies:**
- Integration testing complete
- All components functional

**Acceptance Criteria:**
- [ ] UI is clean and professional
- [ ] Documentation covers setup and usage
- [ ] New team member could onboard from docs

---

## Phase 5: Final Merge & Delivery (Day 7)

| Task | Owner | Branch | Output |
|------|-------|--------|--------|
| Review all branches | Marina | Local review | Code quality check, verify acceptance criteria |
| Merge backend to main | Marina | `main` | Arvin's work integrated |
| Merge frontend to main | Marina | `main` | Nazar's work integrated |
| Merge intelligence to main | Marina | `main` | Marina's work integrated |
| Final integration test | Marina | `main` | Complete system test on main branch |
| Tag release | Marina | `main` | Git tag `v0.1-mvp` |
| Update main README | Marina | `main` | Project overview, quick start, team credits |

**Dependencies:**
- All previous phases complete
- All branches reviewed and approved

**Acceptance Criteria:**
- [ ] `main` branch contains working MVP
- [ ] All team member contributions merged
- [ ] Tagged release exists
- [ ] README provides clear setup instructions

---

## Dependency Graph

```
Day 1:  Marina creates structure
        │
        ├──▶ Arvin creates backend scaffold
        │
        └──▶ Nazar creates frontend scaffold

Day 2-4: Parallel development
        │
        ├──▶ Arvin: models → mock data → API endpoints
        │
        ├──▶ Nazar: components → list view → API client → polish
        │
        └──▶ Marina: topic detection → trend → scoring → explanation

Day 5:  Integration
        │
        └──▶ All: connect backend + intelligence + frontend

Day 6:  Polish & docs
        │
        └──▶ All: final touches and documentation

Day 7:  Marina merges everything to main
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Intelligence module delays | Marina can use mock intelligence fields in backend temporarily |
| API contract changes | Freeze data structure after Phase 1; changes require team agreement |
| Integration conflicts | Daily check-ins; shared understanding of data contracts |
| Frontend blocked by backend | Nazar uses mock JSON file locally until API is ready |

---

## Daily Check-in Format

Each team member posts daily:

1. **What I completed today**
2. **What I'm working on next**
3. **Blockers or dependencies**
4. **Branch I'm working in**

---

## Success Criteria (End of Day 7)

- [ ] Backend serves 10+ grants via `GET /grants`
- [ ] Each grant has all required fields including intelligence fields
- [ ] Frontend displays grants in clean card format
- [ ] Score is color-coded (green/yellow/red)
- [ ] Explanation text is visible per grant
- [ ] `main` branch is functional and tagged
- [ ] Documentation exists for setup and architecture
- [ ] All team contributions merged successfully

---

*Roadmap Version: 1.0*  
*Created: Project Initiation*  
*Maintainer: Marina*
