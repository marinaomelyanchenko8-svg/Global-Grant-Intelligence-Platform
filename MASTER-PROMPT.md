# Global Grant Intelligence Platform

**Project Master Documentation | MVP Specification**

---

## 1. Project Overview

### What is the platform?
The Global Grant Intelligence Platform is an MVP system that aggregates grant opportunities, analyzes them for relevance and trends, and presents them through a simple web interface. It transforms raw grant data into actionable intelligence for users seeking funding.

### What problem does it solve?
Finding relevant grants is time-consuming and fragmented. Organizations waste hours searching multiple sources, manually assessing fit, and tracking deadlines. This platform centralizes grant discovery and applies automated analysis to highlight the best opportunities.

### Why is this not just a simple website?
This is an integrated system with three distinct layers:
- **Data Engine**: Structured storage and API delivery
- **Intelligence Layer**: Rule-based analysis for topics, trends, and scoring
- **Presentation Layer**: Dynamic web interface consuming processed data

The intelligence layer differentiates this from a static directory—it actively analyzes and prioritizes opportunities.

---

## 2. Project Scope and Objectives

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Grant Aggregation** | Collect and structure grant data from multiple sources |
| **Thematic Analysis** | Automatically detect relevant topics per grant |
| **Trend Labeling** | Classify grant trajectories (emerging, growing, stable, declining) |
| **Opportunity Scoring** | Calculate 0-100 relevance score based on configurable rules |
| **Explanation Generation** | Produce concise rationale for each score |
| **Web Visibility** | Display results through a clean, simple interface |

---

## 3. Product Vision

### Internal Use
- Central grant database for strategy team
- Quick opportunity assessment and comparison
- Foundation for future automation and expansion

### Commercial Use
- Potential SaaS offering for grant seekers
- Consultative intelligence for grant writers
- API access for partner integrations

---

## 4. Target Users

| User Type | Primary Need |
|-----------|--------------|
| **Startups and Founders** | Find relevant funding opportunities quickly |
| **Researchers and Academia** | Identify grants matching research areas |
| **NGOs and Social Impact Teams** | Discover aligned funding for mission-driven work |
| **Grant Writers and Consultants** | Efficient opportunity screening for clients |
| **Internal Strategy Team** | Aggregate intelligence for decision-making |

---

## 5. MVP Scope

### What IS Included

- Structured grant data with defined schema
- Backend API with GET /grants endpoint
- Simple frontend interface for browsing grants
- Intelligence layer with rule-based analysis
- Keyword-based topic detection
- Four-tier trend labels (Emerging, Growing, Stable, Declining)
- 0-100 opportunity scoring
- Short explanation generation
- Mock data for initial development
- Real source integration if time permits

### What is NOT Required (MVP)

| Excluded | Reason |
|----------|--------|
| Advanced production infrastructure | MVP focus on functionality |
| Perfect UI/UX | Functional clarity over polish |
| Complex authentication | Not required for initial users |
| Large-scale source integrations | Mock data sufficient for MVP validation |
| Overengineered systems | Simple solutions prioritized |
| User management | Single-user focus for MVP |
| Payment processing | No monetization in MVP phase |

---

## 6. Core System Components

### Backend / Data Engine
- API layer serving structured grant data
- Mock data repository (JSON/database TBD)
- Integration point for intelligence layer

### Intelligence Layer
- Rule-based analysis engine
- Topic detection via keyword matching
- Trend classification logic
- Scoring algorithm
- Explanation generation

### Frontend / Web Interface
- Single-page application or simple HTML/JS
- Grant listing with filtering/sorting
- Visual score representation
- Clean card-based layout

---

## 7. System Architecture

### High-Level Data Flow

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────────────┐
│  User   │────▶│ Frontend │────▶│ Backend  │────▶│ Intelligence    │
│         │     │          │     │          │     │ Layer           │
└─────────┘     └──────────┘     └──────────┘     └─────────────────┘
                                      │                      │
                                      │◀─────────────────────│
                                      │    Enriched Data     │
                                      │                      │
                                      ▼                      │
                              ┌─────────────┐              │
                              │  Response   │──────────────┘
                              │  to Frontend│
                              └─────────────┘
                                      │
                                      ▼
                              ┌─────────────┐
                              │   User      │
                              │   Display   │
                              └─────────────┘
```

---

## 8. Shared Grant Data Structure

### Field Definitions (DO NOT RENAME)

#### Raw Fields (Input)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `title` | string | Grant title |
| `description` | string | Full grant description |
| `funding_amount` | number | Amount in numeric value (e.g., 50000) |
| `currency` | string | ISO currency code (e.g., "USD") |
| `deadline` | string | Application deadline (ISO date) |
| `eligibility` | string | Who can apply |
| `region` | string | Geographic scope |
| `source_name` | string | Origin source (e.g., "NSF", "EU Horizon") |
| `source_url` | string | Link to original grant |
| `status` | string | open, closed, draft |

#### Intelligence Fields (Computed)

| Field | Type | Description |
|-------|------|-------------|
| `topics` | array[string] | Detected thematic categories |
| `confidence` | number | 0-1 confidence in topic detection |
| `trend_label` | string | Emerging, Growing, Stable, Declining |
| `score` | number | 0-100 opportunity score |
| `explanation` | string | Human-readable score rationale |

---

## 9. Intelligence Logic (MVP Level)

### Topic Detection
- **Method**: Keyword matching on title and description
- **Suggested Topics**: AI, Climate, Healthcare, Education, Fintech, Agriculture, Energy, Social Impact
- **Confidence**: Ratio of matched keywords to total keywords

### Trend Labels
- **Emerging**: New program, first or second funding cycle
- **Growing**: Increased funding year-over-year, expanded eligibility
- **Stable**: Established program with consistent funding
- **Declining**: Reduced funding, narrowed eligibility, ending soon

### Scoring Algorithm (Rule-Based)

Base score: 50 points

| Factor | Rule | Points |
|--------|------|--------|
| Funding Size | >$100K | +20 |
| | $50K-$100K | +10 |
| | <$10K | -10 |
| Deadline Proximity | >6 months | +15 |
| | 3-6 months | +5 |
| | <1 month | -15 |
| Eligibility Breadth | "global", "any", "all", "international" | +10 |
| Description Quality | Contains "innovation", "growth", "impact" | +5 |

Maximum score: 100  
Minimum score: 0

### Explanation Generation
Template-based generation using highest-scoring factors:
- "High funding amount with broad eligibility"
- "Time-sensitive opportunity with significant funding"
- "Strong alignment with innovation-focused programs"

---

## 10. Suggested Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Backend | Python + FastAPI | Lightweight, modern, automatic API docs |
| Frontend | HTML/CSS/JavaScript or simple React | Minimal dependencies, quick iteration |
| Intelligence | Python rule-based processing | Transparent, debuggable, fast |
| Data | Mock JSON initially | Zero setup, easy iteration |
| Database | SQLite or PostgreSQL (later) | If persistence needed post-MVP |

---

## 11. Deployment Strategy

### Phase 1: Local Development
- All components run on localhost
- Backend: port 8000
- Frontend: port 3000 or file-based
- No external dependencies required

### Phase 2: Test Deployment
- Lightweight hosting (Heroku, Render, or similar)
- Single-node deployment
- Environment-based configuration

### Phase 3: Production (Post-MVP)
- Scalable infrastructure
- Separate staging and production
- Monitoring and logging

### Independence
Frontend and backend must be runnable independently for parallel development.

---

## 12. Expected Final MVP

At completion, the system will:

1. **Backend**: Return structured grant data via GET /grants endpoint
2. **Intelligence**: Enrich each grant with topics, trend_label, score, and explanation
3. **Frontend**: Display grants in a clean, card-based interface
4. **Integration**: Support end-to-end flow from data to display
5. **Documentation**: Include setup instructions and API docs

Success criteria:
- API responds with correctly structured JSON
- Intelligence fields are populated with sensible values
- Frontend renders all required fields
- Mock data demonstrates full capability

---

## 13. Deliverables

| Deliverable | Owner | Description |
|-------------|-------|-------------|
| Backend MVP | Arvin | FastAPI service with /grants endpoint |
| Frontend MVP | Nazar | Web interface displaying grant cards |
| Intelligence MVP | Marina | Rule-based analysis module |
| Shared Project Structure | Marina | Root organization, data contracts |
| ROADMAP.md | Marina | Task sequencing with parallel work support |
| Task Files | Marina | Per-member task breakdowns |
| WORKFLOW.md | Marina | Branch and commit protocols |

---

## 14. Team Roles

### Marina — Team Leader + Intelligence
- Creates main project structure
- Develops intelligence layer
- Coordinates integration
- Performs final merge and testing

### Arvin — Backend
- Develops FastAPI backend
- Creates mock data
- Implements API endpoints
- Ensures CORS and data contracts

### Nazar — Frontend
- Develops web interface
- Implements grant display
- Connects to backend API
- Basic styling and layout

### Working Protocol

| Rule | Enforcement |
|------|-------------|
| Each member works in their own branch | `marina/`, `arvin/`, `nazar/` prefixes |
| No direct work in main | Main is protected; only merge via PR |
| Marina creates structure first | Initial commit establishes project skeleton |
| Marina handles final integration | Coordinates merging into main |
| Tasks allow maximum parallel work | Minimal cross-dependencies |

---

## 15. Requirements for ROADMAP.md

The future ROADMAP.md must:

- **Enable parallel work**: Tasks should have minimal dependencies between team members
- **Begin with structure**: Marina creates project skeleton first
- **Assign backend tasks**: All API and data work to Arvin
- **Assign frontend tasks**: All UI and display work to Nazar
- **Assign intelligence/coordination**: Analysis and integration to Marina
- **End with integration**: Marina coordinates final merge, testing, and deployment
- **Remain MVP-focused**: No scope creep; each task directly serves MVP goals

### Suggested Sequence
1. Project structure (Marina)
2. Backend scaffolding (Arvin)
3. Frontend scaffolding (Nazar)
4. Intelligence module (Marina)
5. Mock data population (Arvin)
6. API integration (parallel)
7. UI refinement (Nazar)
8. Integration testing (Marina)
9. Final merge and documentation (Marina)

---

## 16. Requirements for Task Files

Individual task files must:

- **Be created per team member**: `TASKS-arvin.md`, `TASKS-nazar.md`, `TASKS-marina.md`
- **Clearly describe responsibilities**: Specific features and acceptance criteria
- **Enforce branch-based work**: Explicit branch naming in each task
- **Avoid overlap**: No shared files without clear coordination points

### Task File Structure

Each task file should include:
1. Team member name and role
2. Working branch name
3. List of tasks with acceptance criteria
4. Dependencies on other members (if any)
5. Estimated effort (small/medium/large)

---

## 17. Requirements for WORKFLOW.md

The future WORKFLOW.md must document:

### Branch Strategy
- `main`: Production-ready code only
- `marina/*`: Marina's feature branches
- `arvin/*`: Arvin's feature branches
- `nazar/*`: Nazar's feature branches

### Commit Standards
- Commit after completing each discrete task
- Clear, descriptive commit messages
- Regular pushes to remote (minimize local-only work)

### Merge Process
- Marina coordinates all merges to main
- Review required before merge
- Integration testing performed by Marina

### Communication
- Regular progress updates in team channel
- Blockers raised immediately
- Cross-member dependencies communicated in advance

---

## Appendix: Quick Reference

### Data Contract (JSON Example)

```json
{
  "id": "nsf-2024-001",
  "title": "AI for Climate Adaptation",
  "description": "Funding for innovative AI applications...",
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

### API Endpoint

```
GET /grants
Response: 200 OK
Content-Type: application/json
Body: [grant objects]
```

---

*Document Version: 1.0*  
*Last Updated: Project Initiation*  
*Maintainer: Marina*
