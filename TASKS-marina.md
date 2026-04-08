# Marina — Team Leader & Intelligence Tasks

**Role:** Team Leader + Intelligence Developer  
**Responsibility:** Project structure, intelligence layer, coordination, final integration

---

## Branch Naming

Main work branch: `marina/intelligence-and-coordination`
Structure setup: `marina/project-structure` (for initial setup)

```bash
# Initial structure setup
git checkout -b marina/project-structure

# Intelligence and coordination work
git checkout -b marina/intelligence-and-coordination
```

---

## PHASE 1: Project Foundation (Day 1)

These tasks must complete before other team members begin work.

### Task 1.1: Create Directory Structure

**Estimated Effort:** Small  
**Dependencies:** None (first task)

### Description
Create the root project structure that all team members will work within.

### Acceptance Criteria
- [ ] Create top-level directories:
  - `backend/` — Arvin's work
  - `frontend/` — Nazar's work
  - `intelligence/` — Marina's intelligence modules
  - `docs/` — Documentation
  - `admin/` — Project management files
- [ ] Add `.gitkeep` files to empty directories so Git tracks them
- [ ] Create `.gitignore` for Python, Node.js, and OS files
- [ ] Create root `README.md` with project overview

### Commit Message
```
git commit -m "Add project directory structure for team collaboration"
```

---

### Task 1.2: Create Master Documentation

**Estimated Effort:** Medium  
**Dependencies:** Task 1.1 complete

### Description
Create the main project specification document that defines the entire MVP.

### Acceptance Criteria
- [ ] Create `MASTER-PROMPT.md` with all required sections:
  - Project overview and scope
  - Product vision and target users
  - MVP scope (what is/isn't included)
  - System components and architecture
  - Shared grant data structure (all 16 fields)
  - Intelligence logic specifications
  - Tech stack and deployment strategy
  - Team roles and responsibilities
  - Requirements for ROADMAP.md, task files, WORKFLOW.md
- [ ] Ensure `funding_amount` is defined as **number** type
- [ ] Ensure `status` values are: open, closed, draft
- [ ] JSON example shows correct data format

### Commit Message
```
git commit -m "Add MASTER-PROMPT.md with complete project specification"
```

---

### Task 1.3: Push Structure and Notify Team

**Estimated Effort:** Small  
**Dependencies:** Task 1.2 complete

### Description
Commit and push the project structure so Arvin and Nazar can begin their work.

### Acceptance Criteria
- [ ] All initial files committed
- [ ] Push `marina/project-structure` branch to remote
- [ ] Merge to `main` after quick review (self-review acceptable for structure)
- [ ] Notify team that structure is ready
- [ ] Provide branch naming guidance to team members

### Commands
```bash
git add .
git commit -m "Initial project structure and documentation"
git push origin marina/project-structure
git checkout main
git merge marina/project-structure
git push origin main
```

---

## PHASE 2: Intelligence Development (Days 2-4)

These tasks run parallel to Arvin's and Nazar's development.

### Task 2.1: Intelligence Module Scaffold

**Estimated Effort:** Small  
**Dependencies:** Phase 1 complete

### Description
Set up the intelligence directory and module structure.

### Acceptance Criteria
- [ ] Create `intelligence/` subdirectory structure:
  - `analyzer.py` — main analysis functions
  - `topics.py` — topic detection logic
  - `trends.py` — trend classification
  - `scoring.py` — score calculation
  - `explanation.py` — explanation generation
- [ ] Create `__init__.py` to make it a Python package
- [ ] Create `requirements.txt` with dependencies (if any beyond standard library)

### Commit Message
```
git commit -m "Add intelligence module scaffold"
```

---

### Task 2.2: Topic Detection Engine

**Estimated Effort:** Medium  
**Dependencies:** Task 2.1 complete

### Description
Implement keyword-based topic detection for grants.

### Acceptance Criteria
- [ ] Define topic keywords mapping:
  - AI: ["artificial intelligence", "machine learning", "ml", "ai", "neural", "deep learning"]
  - Climate: ["climate", "environment", "carbon", "renewable", "sustainability"]
  - Healthcare: ["health", "medical", "healthcare", "disease", "treatment"]
  - Education: ["education", "learning", "student", "school", "university"]
  - Fintech: ["fintech", "financial", "banking", "payment", "blockchain"]
  - Agriculture: ["agriculture", "farming", "crop", "food security", "rural"]
  - Energy: ["energy", "power", "solar", "wind", "grid", "electricity"]
  - Social Impact: ["social impact", "community", "nonprofit", "ngo", "equity"]
- [ ] Create `detect_topics(text)` function
- [ ] Function returns list of detected topics
- [ ] Calculate confidence as (matched keywords / total keywords)
- [ ] Handle case with no matches (empty list, confidence 0)

### Usage Example
```python
from intelligence.topics import detect_topics

result = detect_topics("AI for climate change research")
# Returns: (["AI", "Climate"], 0.67)
```

### Commit Message
```
git commit -m "Add topic detection with keyword matching"
```

---

### Task 2.3: Trend Classification

**Estimated Effort:** Small  
**Dependencies:** Task 2.2 complete

### Description
Implement logic to classify grant trends based on available data.

### Acceptance Criteria
- [ ] Create `classify_trend(grant)` function
- [ ] Returns one of: "Emerging", "Growing", "Stable", "Declining"
- [ ] Rules (MVP simplification):
  - Emerging: deadline > 6 months away AND description contains "new", "first", "pilot"
  - Growing: funding_amount > 100000 OR description contains "expanded", "increased"
  - Declining: deadline < 1 month OR description contains "final", "closing", "last"
  - Stable: default if none of above
- [ ] Document that this is rule-based MVP logic (can be improved later)

### Commit Message
```
git commit -m "Add trend classification logic"
```

---

### Task 2.4: Scoring Engine

**Estimated Effort:** Medium  
**Dependencies:** Task 2.3 complete

### Description
Implement 0-100 opportunity scoring based on configurable rules.

### Acceptance Criteria
- [ ] Create `calculate_score(grant)` function
- [ ] Start with base score of 50
- [ ] Add/subtract points based on rules:
  - +20 if funding_amount > 100000
  - +10 if funding_amount > 50000
  - -10 if funding_amount < 10000
  - +15 if deadline > 6 months away
  - +5 if deadline 3-6 months away
  - -15 if deadline < 1 month
  - +10 if eligibility contains "global", "any", "all", "international"
  - +5 if description contains "innovation", "growth", "impact"
- [ ] Clamp final score to 0-100 range
- [ ] Return integer score

### Commit Message
```
git commit -m "Add opportunity scoring engine with rule-based algorithm"
```

---

### Task 2.5: Explanation Generator

**Estimated Effort:** Small  
**Dependencies:** Task 2.4 complete

### Description
Generate human-readable explanations for scores.

### Acceptance Criteria
- [ ] Create `generate_explanation(grant, score_factors)` function
- [ ] Identify top 2 scoring factors
- [ ] Generate template-based explanation:
  - High funding: "High funding amount"
  - Broad eligibility: "with broad eligibility"
  - Time sensitive: "Time-sensitive opportunity"
  - Innovation focus: "Strong alignment with innovation priorities"
- [ ] Combine factors into one sentence (max 100 characters)
- [ ] Example: "High funding amount with broad eligibility"
- [ ] Example: "Time-sensitive opportunity with innovation focus"

### Commit Message
```
git commit -m "Add explanation generator"
```

---

### Task 2.6: Main Analyzer Function

**Estimated Effort:** Medium  
**Dependencies:** Tasks 2.2-2.5 complete

### Description
Create the main entry point that processes a grant and returns enriched data.

### Acceptance Criteria
- [ ] Create `analyze_grant(grant)` function in `analyzer.py`
- [ ] Accepts dictionary with raw grant fields
- [ ] Calls topic detection, trend classification, scoring, explanation
- [ ] Returns dictionary with all intelligence fields added:
  - topics (list)
  - confidence (float)
  - trend_label (str)
  - score (int)
  - explanation (str)
- [ ] Original grant data is preserved
- [ ] Function has docstring with example usage

### Usage Example
```python
from intelligence.analyzer import analyze_grant

raw_grant = {
    "title": "Climate Research Funding",
    "description": "...",
    "funding_amount": 75000,
    ...
}

enriched = analyze_grant(raw_grant)
# enriched now has topics, score, trend_label, explanation
```

### Commit Message
```
git commit -m "Add main grant analyzer function integrating all components"
```

---

### Task 2.7: Intelligence Testing

**Estimated Effort:** Small  
**Dependencies:** Task 2.6 complete

### Description
Create test cases to verify intelligence logic works correctly.

### Acceptance Criteria
- [ ] Create `test_analyzer.py` with 5-10 test cases
- [ ] Test different grant types (high funding, time-sensitive, broad eligibility)
- [ ] Verify score ranges are 0-100
- [ ] Verify topics are from approved list
- [ ] Verify trend labels are valid values
- [ ] Run tests and fix any issues

### Commit Message
```
git commit -m "Add intelligence module tests"
```

---

## PHASE 3: Coordination & Integration (Day 5)

### Task 3.1: Code Review

**Estimated Effort:** Medium  
**Dependencies:** Arvin and Nazar have pushed their work

### Description
Review team members' code for compliance with project standards.

### Acceptance Criteria
- [ ] Review Arvin's backend code
  - Data models match shared structure
  - API returns correct format
  - Mock data has all required fields
- [ ] Review Nazar's frontend code
  - Uses correct field names
  - Displays score with color coding
  - Handles loading/error states
- [ ] Leave comments/suggestions if needed
- [ ] Approve for merge when ready

### Notes
- Be constructive in feedback
- Focus on data contract compliance
- UI polish is secondary to functionality for MVP

---

### Task 3.2: Integration Testing

**Estimated Effort:** Medium  
**Dependencies:** Task 3.1 complete

### Description
Test the complete end-to-end flow of the application.

### Acceptance Criteria
- [ ] Start backend server (`uvicorn main:app --reload`)
- [ ] Open frontend in browser
- [ ] Verify frontend successfully calls `GET /grants`
- [ ] Verify grants display with all fields
- [ ] Verify intelligence fields are populated:
  - Topics show as tags/badges
  - Trend label is visible
  - Score is color-coded
  - Explanation text is readable
- [ ] Test with different grants to verify variety
- [ ] Document any integration issues

### Integration Issue Resolution
- [ ] If backend issues: coordinate with Arvin
- [ ] If frontend issues: coordinate with Nazar
- [ ] If intelligence issues: fix in `marina/intelligence-and-coordination` branch

---

## PHASE 4: Documentation & Management (Day 6)

### Task 4.1: Create ROADMAP.md

**Estimated Effort:** Medium  
**Dependencies:** None (can be done early)

### Description
Create the detailed development roadmap for the team.

### Acceptance Criteria
- [ ] Create `ROADMAP.md` in project root
- [ ] Include phases: Foundation, Core Development, Integration, Polish, Delivery
- [ ] Assign tasks to each team member
- [ ] Show dependencies between tasks
- [ ] Enable parallel work (minimize cross-dependencies)
- [ ] Include daily check-in format
- [ ] Include risk mitigation strategies

### Commit Message
```
git commit -m "Add ROADMAP.md with development phases and task assignments"
```

---

### Task 4.2: Create Team Task Files

**Estimated Effort:** Medium  
**Dependencies:** None (can be done early)

### Description
Create individual task files for Arvin and Nazar.

### Acceptance Criteria
- [ ] Create `TASKS-arvin.md` with:
  - Role and branch naming
  - 6-8 specific tasks with acceptance criteria
  - Effort estimates
  - Dependencies noted
- [ ] Create `TASKS-nazar.md` with:
  - Role and branch naming
  - 7-8 specific tasks with acceptance criteria
  - Effort estimates
  - Dependencies noted
- [ ] Both files enforce branch-based work
- [ ] Both files reference shared data structure

### Commit Message
```
git commit -m "Add individual task files for Arvin and Nazar"
```

---

### Task 4.3: Create WORKFLOW.md

**Estimated Effort:** Small  
**Dependencies:** None

### Description
Document the Git workflow for the team.

### Acceptance Criteria
- [ ] Create `WORKFLOW.md` with sections:
  - Branch naming convention
  - Commit message guidelines
  - Daily workflow (pull, rebase, push)
  - Merge process (Marina coordinates)
  - Conflict resolution tips
- [ ] Include command examples
- [ ] Reference this document in daily standups

### Commit Message
```
git commit -m "Add WORKFLOW.md with Git protocols"
```

---

### Task 4.4: Architecture Documentation

**Estimated Effort:** Small  
**Dependencies:** Integration testing complete

### Description
Document the system architecture for future reference.

### Acceptance Criteria
- [ ] Create `docs/architecture.md`
- [ ] Include system diagram (ASCII art acceptable)
- [ ] Describe data flow: Frontend → Backend → Intelligence → Response
- [ ] Document API contracts
- [ ] Document data models
- [ ] Include setup instructions for each component

### Commit Message
```
git commit -m "Add architecture documentation"
```

---

## PHASE 5: Final Delivery (Day 7)

### Task 5.1: Final Review

**Estimated Effort:** Medium  
**Dependencies:** All development complete

### Description
Perform final review of all code before merging to main.

### Acceptance Criteria
- [ ] Review all three branches:
  - `arvin/backend-mvp`
  - `nazar/frontend-mvp`
  - `marina/intelligence-and-coordination`
- [ ] Verify all acceptance criteria met
- [ ] Check that no one committed directly to `main`
- [ ] Verify all files are in correct directories
- [ ] Run final integration test

---

### Task 5.2: Merge to Main

**Estimated Effort:** Small  
**Dependencies:** Task 5.1 complete

### Description
Coordinate merging all branches to main.

### Acceptance Criteria
- [ ] Merge `arvin/backend-mvp` → `main`
- [ ] Merge `nazar/frontend-mvp` → `main`
- [ ] Merge `marina/intelligence-and-coordination` → `main`
- [ ] Resolve any merge conflicts
- [ ] Verify `main` branch is functional after all merges

### Commands
```bash
git checkout main
git pull origin main

# Merge each branch
git merge arvin/backend-mvp
git merge nazar/frontend-mvp
git merge marina/intelligence-and-coordination

# Push to remote
git push origin main
```

---

### Task 5.3: Tag Release

**Estimated Effort:** Small  
**Dependencies:** Task 5.2 complete

### Description
Tag the final MVP release.

### Acceptance Criteria
- [ ] Create Git tag: `v0.1-mvp`
- [ ] Push tag to remote
- [ ] Verify tag exists on GitHub/GitLab

### Commands
```bash
git tag -a v0.1-mvp -m "MVP Release 0.1"
git push origin v0.1-mvp
```

---

### Task 5.4: Update Root README

**Estimated Effort:** Small  
**Dependencies:** Task 5.3 complete

### Description
Update the root README with final project information.

### Acceptance Criteria
- [ ] Add project overview
- [ ] Add quick start instructions
- [ ] Add team member credits
- [ ] Link to ROADMAP.md and architecture docs
- [ ] Include screenshot or description of final result
- [ ] Add license (if applicable)

### Commit Message
```
git commit -m "Update README for v0.1-mvp release"
```

---

### Task 5.5: Final Documentation

**Estimated Effort:** Small  
**Dependencies:** Task 5.4 complete

### Description
Create final summary document.

### Acceptance Criteria
- [ ] Create `docs/retrospective.md`
- [ ] Document what was achieved in MVP
- [ ] Note any shortcuts or technical debt
- [ ] Suggest future improvements
- [ ] Include lessons learned

### Commit Message
```
git commit -m "Add MVP retrospective documentation"
```

---

## Task Summary

### Phase 1: Foundation (Day 1)
| Task | Effort | Status |
|------|--------|--------|
| 1.1 Directory Structure | Small | ⬜ |
| 1.2 Master Documentation | Medium | ⬜ |
| 1.3 Push and Notify | Small | ⬜ |

### Phase 2: Intelligence (Days 2-4)
| Task | Effort | Status |
|------|--------|--------|
| 2.1 Intelligence Scaffold | Small | ⬜ |
| 2.2 Topic Detection | Medium | ⬜ |
| 2.3 Trend Classification | Small | ⬜ |
| 2.4 Scoring Engine | Medium | ⬜ |
| 2.5 Explanation Generator | Small | ⬜ |
| 2.6 Main Analyzer | Medium | ⬜ |
| 2.7 Testing | Small | ⬜ |

### Phase 3: Integration (Day 5)
| Task | Effort | Status |
|------|--------|--------|
| 3.1 Code Review | Medium | ⬜ |
| 3.2 Integration Testing | Medium | ⬜ |

### Phase 4: Documentation (Day 6)
| Task | Effort | Status |
|------|--------|--------|
| 4.1 Create ROADMAP.md | Medium | ✅ |
| 4.2 Create Task Files | Medium | ✅ |
| 4.3 Create WORKFLOW.md | Small | ✅ |
| 4.4 Architecture Docs | Small | ⬜ |

### Phase 5: Delivery (Day 7)
| Task | Effort | Status |
|------|--------|--------|
| 5.1 Final Review | Medium | ⬜ |
| 5.2 Merge to Main | Small | ⬜ |
| 5.3 Tag Release | Small | ⬜ |
| 5.4 Update README | Small | ⬜ |
| 5.5 Final Docs | Small | ⬜ |

---

## Daily Workflow

1. **Start of day:**
   ```bash
   git checkout main
   git pull origin main
   git checkout marina/intelligence-and-coordination
   git rebase main
   ```

2. **During work:**
   ```bash
   git add .
   git commit -m "descriptive message"
   git push origin marina/intelligence-and-coordination
   ```

3. **End of day:**
   - Push all commits
   - Update team on progress
   - Review team members' progress

---

## Key Rules

- **Create project structure FIRST** — block other work until this is done
- **Never commit to `main` directly** (except initial structure after review)
- **All merges to `main` go through Marina**
- **Coordinate integration personally** — this is your responsibility
- **Document everything** — team relies on your docs
- **Be available for questions** — you're the project lead

---

## Coordination Checklist

- [ ] Day 1: Structure pushed, team notified
- [ ] Day 2: Check in with Arvin and Nazar
- [ ] Day 3: Mid-week progress review
- [ ] Day 4: Confirm Phase 2 completion
- [ ] Day 5: Integration testing
- [ ] Day 6: Documentation complete
- [ ] Day 7: Final merge and release

---

*Task File Version: 1.0*  
*Created: Project Initiation*
