# Global Grant Intelligence Platform - Frontend

Static frontend for the Global Grant Intelligence Platform MVP.

## Setup

No build step required. This is a static HTML/CSS/JS frontend.

## Running Locally

**Option 1: Open directly**
Double-click `index.html` or right-click → Open in browser.

**Option 2: Use local server (recommended)**
```bash
cd frontend
npx serve .
# Opens at http://localhost:3000
```

## API Endpoint

The frontend connects to the backend API at:
```
http://localhost:8000/grants
```

Backend must be running on port 8000 with CORS enabled.

## File Structure

```
frontend/
├── index.html      # Main entry point with multi-page structure
├── css/
│   └── styles.css  # All styling including modal & navigation
├── js/
│   └── app.js      # API client, routing & rendering logic
└── assets/         # Static assets
```

## Pages

The frontend is a single-page application with multiple views:

- **Dashboard** (`#dashboard`) - Overview with feature placeholders and recommended grants
- **Grants** (`#grants`) - Full list of available grants
- **Saved** (`#saved`) - Bookmarked opportunities (placeholder)

Navigation updates URL hash and supports browser back/forward.

## Features

### Grant Cards
- Title with bold formatting
- Funding amount with currency indicator
- Score with color coding (green/yellow/red)
- Explanation text
- Hover effects and responsive layout

### Navigation
- Header navigation with Dashboard, Grants, and Saved links
- URL hash-based routing
- Active state highlighting

### Authentication (Placeholder)
- Sign In modal with Login/Register tabs
- Form validation
- Escape key and overlay click to close
- Demo alert on submit (not yet connected to backend)

### Core Feature Placeholders
- Smart Search (AI-powered matching)
- Analytics (Success rate tracking)
- Alerts (New grant notifications)
- Documents (Application materials)

## Data Structure

Grant objects returned by the API:
```javascript
{
  id: string,
  title: string,
  funding_amount: number,  // e.g., 50000 (displayed as $50,000)
  score: number,           // 0-100 (color-coded)
  explanation: string
}
```

Score color coding:
- **Green (#22c55e)**: 70-100
- **Yellow (#eab308)**: 40-69
- **Red (#ef4444)**: 0-39

## Troubleshooting

### CORS Issues

If you see CORS errors in browser console:
1. Confirm backend has CORS middleware enabled
2. Verify backend is running on `localhost:8000`
3. Check that frontend is calling correct URL

### Backend Not Ready

To test with mock data temporarily, edit `js/app.js`:
```javascript
const USE_MOCK = true;
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)

## Responsive Breakpoints

- Desktop: 3 cards per row
- Tablet (≤992px): 2 cards per row
- Mobile (≤576px): 1 card per row

---

*Frontend for Global Grant Intelligence Platform MVP*
