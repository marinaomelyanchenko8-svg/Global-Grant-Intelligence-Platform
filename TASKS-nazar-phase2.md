# Nazar — Frontend Phase 2 Tasks

**Role:** Frontend Developer  
**Branch:** `nazar/phase2-ui-enhancements`  
**Goal:** Stable frontend with search, filters, and correct real data rendering

---

## Overview

Phase 2 focuses on making the frontend production-ready with real data. Implement search across title and description. Add filters for source, region, and topics. Ensure UI handles 20-50+ grants without performance issues. Fix any false "No grants available" states.

---

## Task 1: Fix "No Grants Available" False State

**Estimated Effort:** Small  
**Execution Order:** First  
**Dependencies:** None

### Description
Debug and fix any cases where "No grants available" shows incorrectly.

### Files to Modify
- `frontend/js/app.js` — `renderGrants()` and `showEmpty()` functions

### Acceptance Criteria
- [ ] Analyze current `renderGrants()` logic for edge cases
- [ ] Handle these data states correctly:
  - Empty array `[]` → show "No grants available" (correct)
  - `null` or `undefined` → show error state (not empty)
  - Network error → show error with retry button
  - Valid array with grants → render cards
- [ ] Add explicit check: if `grants === null` → error state
- [ ] Add explicit check: if `!Array.isArray(grants)` → error state
- [ ] Add debug logging: `console.log('Rendering N grants:', grants?.length)`
- [ ] Ensure loading state shows while fetching, not "No grants"

### Test Verification
1. Start backend with mock data
2. Open frontend
3. Verify grants load without showing "No grants available" briefly
4. Block network (DevTools → Offline) → should show error, not empty
5. Return online → click retry → grants load

### Commit Message
```
git commit -m "fix: eliminate false 'no grants available' state"
```

---

## Task 2: Search Bar Component

**Estimated Effort:** Medium  
**Execution Order:** After Task 1  
**Dependencies:** Task 1 complete

### Description
Add search input that filters grants by title and description content.

### Files to Modify
- `frontend/index.html` — add search bar to grants page
- `frontend/js/app.js` — add search logic
- `frontend/css/styles.css` — style search bar

### Acceptance Criteria
- [ ] Add search input to grants page header:
  ```html
  <div class="search-bar">
    <input type="text" id="search-input" placeholder="Search grants..." />
    <button id="search-btn">Search</button>
  </div>
  ```
- [ ] Search matches both `title` and `description` fields (case-insensitive)
- [ ] Search updates results as user types (debounced, 300ms delay)
- [ ] Empty search shows all grants
- [ ] No matches shows "No grants match your search" (different from empty state)
- [ ] Search works with current filters (combines with AND logic)
- [ ] URL updates with `?search=query` for shareable links
- [ ] Browser back/forward works with search history

### Test Verification
```javascript
// In browser console
searchGrants('climate'); // Should filter to climate-related grants
searchGrants('xyz123'); // Should show "No grants match your search"
```

### Commit Message
```
git commit -m "feat: add search bar with title and description matching"
```

---

## Task 3: Filter Panel (Source, Region, Topics)

**Estimated Effort:** Medium  
**Execution Order:** After Task 2  
**Dependencies:** Task 2 complete

### Description
Add filter panel with dropdowns for source, region, and topics.

### Files to Modify
- `frontend/index.html` — add filter panel
- `frontend/js/app.js` — add filter logic
- `frontend/css/styles.css` — style filter panel

### Acceptance Criteria
- [ ] Add filter panel layout to grants page (sidebar or top bar)
- [ ] **Source filter:** dropdown with options:
  - "All Sources"
  - "Grants.gov"
  - "EU Funding"
  - "Open Philanthropy"
  - "Mock Data" (for debugging)
- [ ] **Region filter:** dropdown populated dynamically from available regions in current grants
- [ ] **Topics filter:** multi-select or tag-based filter showing all unique topics
- [ ] Filters combine with AND logic (source=grants.gov AND region=US)
- [ ] Filters work with search (search within filtered results)
- [ ] Show active filter count (e.g., "2 filters active")
- [ ] Add "Clear All" button to reset filters
- [ ] URL updates with filter params: `?source=grants.gov&region=US`

### Test Verification
```javascript
// Test each filter
applyFilter('source', 'grants.gov');
applyFilter('region', 'United States');
applyFilter('topics', ['AI', 'Climate']);

// Verify combined
currentFilters = {source: 'grants.gov', search: 'health'};
// Should show only grants.gov grants matching "health"
```

### Commit Message
```
git commit -m "feat: add filter panel for source, region, and topics"
```

---

## Task 4: Grant Counter and Result Stats

**Estimated Effort:** Small  
**Execution Order:** After Task 3  
**Dependencies:** Task 3 complete

### Description
Show grant count and result statistics to give users context.

### Files to Modify
- `frontend/index.html` — add stats display
- `frontend/js/app.js` — update stats on render
- `frontend/css/styles.css` — style stats

### Acceptance Criteria
- [ ] Show total grant count: "Showing 47 grants"
- [ ] When filtered: "Showing 12 of 47 grants"
- [ ] Show breakdown by source:
  ```
  Grants.gov: 25 | EU Funding: 15 | Open Philanthropy: 7
  ```
- [ ] Show last updated timestamp: "Last updated: 2 hours ago"
- [ ] Stats update immediately when filters/search applied

### Test Verification
1. Load page → see "Showing X grants"
2. Apply filter → count updates
3. Clear filters → returns to total count

### Commit Message
```
git commit -m "feat: add grant counter and source breakdown stats"
```

---

## Task 5: Pagination for Large Datasets

**Estimated Effort:** Medium  
**Execution Order:** After Task 4  
**Dependencies:** Task 4 complete

### Description
Add pagination to handle 20-50+ grants efficiently.

### Files to Modify
- `frontend/index.html` — add pagination controls
- `frontend/js/app.js` — add pagination logic
- `frontend/css/styles.css` — style pagination

### Acceptance Criteria
- [ ] Show 12 grants per page by default (configurable)
- [ ] Add pagination controls at bottom:
  - Previous / Next buttons
  - Page numbers (1 2 3 ... 10)
  - "Page X of Y" text
- [ ] Pagination works with filters and search
- [ ] URL updates with `?page=2`
- [ ] Browser back/forward works across pages
- [ ] First page loads without page param in URL
- [ ] Changing filters resets to page 1

### Test Verification
```javascript
// Load 50 grants
goToPage(2); // Should show grants 13-24
goToPage(5); // Should show grants 49-50 (last page)
```

### Commit Message
```
git commit -m "feat: add pagination for large grant datasets"
```

---

## Task 6: Backend Query Integration

**Estimated Effort:** Medium  
**Execution Order:** After Task 5  
**Dependencies:** Task 5 complete, Arvin Task 5 complete

### Description
Connect filters and search to backend query parameters for server-side filtering.

### Files to Modify
- `frontend/js/app.js` — update `fetchGrants()` function

### Acceptance Criteria
- [ ] Update `fetchGrants()` to accept params object:
  ```javascript
  fetchGrants({
    search: 'climate',
    source: 'grants.gov',
    region: 'United States',
    topics: ['AI'],
    limit: 12,
    offset: 0
  })
  ```
- [ ] Build query string from params: `?search=climate&source=grants.gov`
- [ ] Use backend filtering when possible (reduces data transfer)
- [ ] Fall back to client-side filtering if backend params not supported
- [ ] Maintain current filter state between requests

### Test Verification
```bash
# Check network tab in DevTools
# Should see requests like:
GET /grants?search=climate&source=grants.gov&limit=12&offset=0
```

### Commit Message
```
git commit -m "feat: integrate filters with backend query parameters"
```

---

## Task 7: Responsive Filter Panel

**Estimated Effort:** Small  
**Execution Order:** After Task 6  
**Dependencies:** Task 6 complete

### Description
Make filter panel responsive for mobile devices.

### Files to Modify
- `frontend/css/styles.css` — responsive styles
- `frontend/index.html` — mobile filter toggle

### Acceptance Criteria
- [ ] Desktop (>992px): filters in sidebar on left
- [ ] Tablet (768-992px): filters in horizontal bar above results
- [ ] Mobile (<768px): filters in collapsible drawer/panel
- [ ] Mobile toggle button: "Filters" with count badge
- [ ] Selected filters show as chips/tags that can be removed
- [ ] Touch-friendly dropdown sizes (min 44px tap target)

### Test Verification
1. Open in Chrome DevTools mobile view
2. Click "Filters" button → drawer opens
3. Select filters → chips appear
4. Close drawer → grants update
5. Rotate to landscape → layout adapts

### Commit Message
```
git commit -m "feat: responsive filter panel for mobile"
```

---

## Task Summary

| Task | Effort | Execution Order | Files |
|------|--------|-----------------|-------|
| 1. Fix False Empty State | Small | 1st | `js/app.js` |
| 2. Search Bar | Medium | 2nd | `index.html`, `js/app.js`, `css/styles.css` |
| 3. Filter Panel | Medium | 3rd | `index.html`, `js/app.js`, `css/styles.css` |
| 4. Grant Counter | Small | 4th | `index.html`, `js/app.js` |
| 5. Pagination | Medium | 5th | `index.html`, `js/app.js`, `css/styles.css` |
| 6. Backend Query Integration | Medium | 6th | `js/app.js` |
| 7. Responsive Filters | Small | 7th | `css/styles.css`, `index.html` |

---

## Expected Final Result

### UI Layout
```
┌─────────────────────────────────────────────────────────────┐
│  Global Grant Intelligence Platform                         │
├─────────────────────────────────────────────────────────────┤
│  Grants Page                                                │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Search: [_____________________] [Search]              │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ Filters: [Source ▼] [Region ▼] [Topics ▼] [Clear All]  │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ Showing 24 of 47 grants | Last updated: 2 hours ago   │ │
│  │ Grants.gov: 15 | EU Funding: 9 | Open Phil: 0        │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ ┌─────────┐ ┌─────────┐ ┌─────────┐                │ │
│  │ │ Grant 1 │ │ Grant 2 │ │ Grant 3 │ ...              │ │
│  │ └─────────┘ └─────────┘ └─────────┘                │ │
│  │                                                        │ │
│  │ ┌─────────┐ ┌─────────┐ ┌─────────┐                │ │
│  │ │ Grant 4 │ │ Grant 5 │ │ Grant 6 │ ...              │ │
│  │ └─────────┘ └─────────┘ └─────────┘                │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ [Previous] [1] [2] [3] ... [5] [Next]  Page 1 of 5    │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### URL State Examples
```
/grants?search=climate&source=grants.gov&page=1
/grants?region=United+States&topics=AI,Healthcare
/grants?search=education&min_score=60&page=2
```

### Verification Commands

```bash
# Test search
curl "http://localhost:8000/grants?search=climate&limit=100" | jq length

# Test filter by source
curl "http://localhost:8000/grants?source=grants.gov" | jq '.[0].data_source'

# Verify frontend renders correctly
# Open browser, navigate to grants page
# Apply filters, verify count updates
# Search, verify results filter
# Navigate pages, verify pagination works
```

---

## Daily Workflow

```bash
# Start of day
git checkout main && git pull origin main
git checkout nazar/phase2-ui-enhancements && git rebase main

# After each task
git add .
git commit -m "descriptive message"
git add TASKS-nazar-phase2.md  # update status
git commit -m "docs: update phase2 tasks"
git push origin nazar/phase2-ui-enhancements
```

---

## Key Rules

- **Never commit to `main` directly**
- **Search must match both title AND description**
- **Filters must combine with AND logic**
- **URL must reflect current state** — shareable links
- **No false "No grants available"** — distinguish empty from error
- **Mobile-first responsive design**

---

## Coordination with Arvin

- Task 1-5 can be done with client-side filtering (no backend changes needed)
- Task 6 requires Arvin's Task 5 (backend query params) — coordinate timing
- Use mock data for testing filters during development
- Verify with real data once Arvin completes sources

---

*Task File Version: Phase 2*  
*Created: Phase 2 Planning*
