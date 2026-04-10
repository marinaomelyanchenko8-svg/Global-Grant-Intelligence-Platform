# Nazar — Frontend Development Tasks

**Role:** Frontend Developer  
**Responsibility:** Web interface, grant display, UI components, API integration

---

## Branch Naming

All work in branch: `nazar/frontend-mvp`

```bash
git checkout -b nazar/frontend-mvp
```

---

## Task 1: Project Scaffold

**Estimated Effort:** Small  
**Dependencies:** Marina completes project structure

### Description
Set up the frontend directory structure and basic HTML/CSS/JS files.

### Acceptance Criteria
- [x] Create `frontend/` directory structure:
  - [x] `index.html` — main entry point
  - [x] `css/styles.css` — styling
  - [x] `js/app.js` — JavaScript logic
- [x] Basic HTML5 boilerplate in `index.html`
- [x] CSS file linked and loads correctly
- [x] JavaScript file linked and executes on page load
- [x] Page opens without errors in browser

### Commit Message
```
git commit -m "Add frontend scaffold with HTML/CSS/JS structure"
```

---

## Task 2: Grant Card Component

**Estimated Effort:** Small  
**Dependencies:** Task 1 complete

### Description
Create the individual grant card that displays a single grant's information.

### Acceptance Criteria
- [x] Card shows `title` in bold, prominent text
- [x] Card shows `funding_amount` with currency indicator (e.g., "$50,000")
- [x] Card shows `score` as a number with color coding:
  - Green (#22c55e) for 70-100
  - Yellow (#eab308) for 40-69
  - Red (#ef4444) for 0-39
- [x] Card shows `explanation` as smaller, readable text below score
- [x] Card has clean visual design with borders/shadows
- [x] Card layout is responsive (works on mobile and desktop)

### Visual Example
```
┌─────────────────────────────────────┐
│ AI for Climate Research             │  ← Title (bold)
│                                     │
│ 💰 $500,000 USD                     │  ← Funding amount
│                                     │
│ ⭐ Score: 82                        │  ← Score (green color)
│                                     │
│ High funding with broad eligibility │  ← Explanation
└─────────────────────────────────────┘
```

### Commit Message
```
git commit -m "Add grant card component with styling"
```

---

## Task 3: Grant List Container

**Estimated Effort:** Small  
**Dependencies:** Task 2 complete

### Description
Create a container that holds multiple grant cards in a grid or list layout.

### Acceptance Criteria
- [x] Create container div for multiple cards in `index.html`
- [x] Layout uses CSS Grid or Flexbox for card arrangement
- [x] Grid shows 3 cards per row on desktop, 2 on tablet, 1 on mobile
- [x] Cards have consistent spacing (gap of 16-24px)
- [x] Container has max-width and is centered on page
- [x] Page title "Global Grant Intelligence Platform" at top

### Commit Message
```
git commit -m "Add grant list container with responsive grid"
```

---

## Task 4: API Client

**Estimated Effort:** Medium  
**Dependencies:** Task 3 complete (can use mock data temporarily)

### Description
Implement JavaScript to fetch grants from the backend API.

### Acceptance Criteria
- [x] Create `fetchGrants()` function in `js/app.js`
- [x] Function calls `http://localhost:8000/grants`
- [x] Function handles successful response (status 200)
- [x] Function parses JSON response
- [x] Function returns array of grant objects
- [x] Function handles errors gracefully (console.error + user message)
- [x] CORS is handled correctly (backend must enable CORS first)

### Test Code
```javascript
fetchGrants().then(grants => console.log(grants));
```

### Fallback for Development
If backend is not ready, create temporary `js/mock-data.js`:
```javascript
const MOCK_GRANTS = [
  { id: "1", title: "Test Grant", funding_amount: 50000, ... }
];
```

### Commit Message
```
git commit -m "Add API client for fetching grants"
```

---

## Task 5: Dynamic Rendering

**Estimated Effort:** Medium  
**Dependencies:** Task 4 complete

### Description
Connect the API client to render grants dynamically in the list container.

### Acceptance Criteria
- [x] On page load, call `fetchGrants()`
- [x] Create DOM elements for each grant returned
- [x] Apply Task 2 card styling to rendered cards
- [x] Cards display in the Task 3 container
- [x] Page shows "Loading..." while fetching
- [x] Page shows "No grants available" if empty array returned
- [x] Page shows "Error loading grants" if request fails

### Commit Message
```
git commit -m "Add dynamic grant rendering from API"
```

---

## Task 6: Loading and Error States

**Estimated Effort:** Small  
**Dependencies:** Task 5 complete

### Description
Add visual feedback for loading and error states.

### Acceptance Criteria
- [x] Show spinner or "Loading grants..." text while fetching
- [x] Hide loading indicator when data loaded
- [x] Show error message if API call fails
- [x] Error message includes retry button (calls fetchGrants again)
- [x] Loading/error states have consistent styling

### Commit Message
```
git commit -m "Add loading and error state handling"
```

---

## Task 7: UI Polish

**Estimated Effort:** Medium  
**Dependencies:** Task 6 complete

### Description
Refine the visual design for a professional appearance.

### Acceptance Criteria
- [x] Consistent color scheme (suggest: blue primary, gray secondary)
- [x] Proper spacing and padding throughout
- [x] Readable font sizes (16px base, scale up for titles)
- [x] Hover effects on cards (slight shadow increase)
- [x] Header with project title and brief description
- [x] Footer with simple copyright/credits
- [x] Works in Chrome, Firefox, Safari

### Commit Message
```
git commit -m "Polish UI styling and responsive design"
```

---

## Task 8: Frontend Documentation

**Estimated Effort:** Small  
**Dependencies:** All above tasks complete

### Description
Document the frontend setup for other team members.

### Acceptance Criteria
- [x] Create `frontend/README.md` with sections:
  - [x] Setup instructions (none needed for static files, or `npx serve`)
  - [x] How to run (open `index.html` or use local server)
  - [x] API endpoint it connects to
  - [x] File structure overview
- [x] Document that backend must be running on port 8000
- [x] Include troubleshooting for CORS issues

### Commit Message
```
git commit -m "Add frontend README with setup documentation"
```

---

## Task Summary

| Task | Effort | Status | Notes |
|------|--------|--------|-------|
| 1. Project Scaffold | Small | ✅ | Done |
| 2. Grant Card | Small | ✅ | Core component |
| 3. List Container | Small | ✅ | Done |
| 4. API Client | Medium | ✅ | Done |
| 5. Dynamic Rendering | Medium | ✅ | Done |
| 6. Loading/Error | Small | ✅ | Done |
| 7. UI Polish | Medium | ✅ | Done |
| 8. Documentation | Small | ✅ | Done |

---

## Daily Workflow

1. **Start of day:** Pull latest from `main` and rebase your branch
   ```bash
   git checkout main
   git pull origin main
   git checkout nazar/frontend-mvp
   git rebase main
   ```

2. **During work (after completing each task):**
   ```bash
   # 1. Commit the task code
   git add .
   git commit -m "descriptive message"
   
   # 2. Update this tasks file (mark task as complete ✅)
   # Edit TASKS-nazar.md and change ⬜ to ✅ for completed task
   
   # 3. Commit the tasks file update
   git add TASKS-nazar.md
   git commit -m "docs: update TASKS-nazar.md - mark completed tasks"
   
   # 4. Push everything
   git push origin nazar/frontend-mvp
   ```

3. **End of day:** Push all commits and update team on progress

---

## Development Tips

### Running Frontend Locally

**Option 1: Open directly**
```bash
cd frontend
# Double-click index.html or right-click → Open in browser
```

**Option 2: Use local server (recommended)**
```bash
cd frontend
npx serve .
# Opens at http://localhost:3000
```

### Testing with Mock Data

If backend is not ready, temporarily add to `js/app.js`:
```javascript
// TEMPORARY: Use mock data until backend is ready
const USE_MOCK = true;

async function fetchGrants() {
  if (USE_MOCK) {
    return Promise.resolve(MOCK_GRANTS);
  }
  // ... real API call
}
```

### CORS Issues

If you see CORS errors in browser console:
1. Confirm Arvin has added CORS middleware to backend
2. Check that backend is running on `localhost:8000`
3. Verify frontend is calling correct URL

---

## Key Rules

- **Never commit to `main` directly**
- **Work only in `nazar/frontend-mvp` branch**
- **Do not modify backend or intelligence code**
- **Use the shared data structure—do not rename fields**
- `funding_amount` is a **number** (not string with $)
- Display it with `$` prefix for users: `$${grant.funding_amount.toLocaleString()}`
- `score` is 0-100, color code it accordingly

---

*Task File Version: 1.0*  
*Created: Project Initiation*
