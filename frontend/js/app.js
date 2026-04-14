/**
 * Global Grant Intelligence Platform - Frontend Application
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000';
const GRANTS_ENDPOINT = `${API_BASE_URL}/grants`;

// Mock Data (for development when backend is not ready)
const USE_MOCK = false;
const MOCK_GRANTS = [
    {
        id: "1",
        title: "AI for Climate Research",
        funding_amount: 500000,
        score: 85,
        explanation: "High funding with broad eligibility for AI applications in climate science",
        topics: ["AI", "Climate", "Research"],
        trend_label: "rising",
        confidence: 92
    },
    {
        id: "2",
        title: "Renewable Energy Innovation",
        funding_amount: 250000,
        score: 72,
        explanation: "Strong focus on sustainable energy solutions with clear evaluation criteria",
        topics: ["Energy", "Sustainability", "Innovation"],
        trend_label: "stable",
        confidence: 78
    },
    {
        id: "3",
        title: "Community Health Outreach",
        funding_amount: 75000,
        score: 45,
        explanation: "Moderate funding amount, limited to specific geographic regions",
        topics: ["Health", "Community"],
        trend_label: "declining",
        confidence: 65
    },
    {
        id: "4",
        title: "Educational Technology Grant",
        funding_amount: 30000,
        score: 25,
        explanation: "Low funding amount with highly competitive application process",
        topics: ["Education", "Technology"],
        trend_label: "stable",
        confidence: 45
    }
];

// DOM Elements
const grantsContainer = document.getElementById('grants-container');
const dashboardGrantsContainer = document.getElementById('dashboard-grants');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const retryBtn = document.getElementById('retry-btn');

// Navigation & Modal Elements
const navLinks = document.querySelectorAll('.nav-link');
const authBtn = document.getElementById('auth-btn');
const authModal = document.getElementById('auth-modal');
const modalClose = document.querySelector('.modal-close');
const modalOverlay = document.querySelector('.modal-overlay');
const authTabs = document.querySelectorAll('.auth-tab');
const authForms = document.querySelectorAll('.auth-form');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const pages = document.querySelectorAll('.page');

// Utility Functions
/**
 * Show loading state
 */
function showLoading() {
    loadingElement.classList.remove('hidden');
    errorElement.classList.add('hidden');
    grantsContainer.innerHTML = '';
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingElement.classList.add('hidden');
}

/**
 * Show error state
 */
function showError() {
    loadingElement.classList.add('hidden');
    errorElement.classList.remove('hidden');
    grantsContainer.innerHTML = '';
}

/**
 * Show empty state
 */
function showEmpty() {
    hideLoading();
    grantsContainer.innerHTML = '<div class="loading">No grants available</div>';
}

/**
 * Get score color class based on score value
 * @param {number} score - Score value (0-100)
 * @returns {string} CSS class name
 */
function getScoreClass(score) {
    if (score >= 70) return 'high';
    if (score >= 40) return 'medium';
    return 'low';
}

/**
 * Format funding amount with currency
 * @param {number} amount - Funding amount
 * @returns {string} Formatted string
 */
function formatFunding(amount) {
    return `$${amount.toLocaleString()} USD`;
}

/**
 * Create a grant card HTML element
 * @param {Object} grant - Grant object
 * @returns {HTMLElement} Card element
 */
function createGrantCard(grant) {
    const card = document.createElement('div');
    card.className = 'grant-card';

    const topics = grant.topics && grant.topics.length > 0 ? escapeHtml(grant.topics.join(', ')) : 'N/A';
    const trend = grant.trend_label ? escapeHtml(grant.trend_label) : 'N/A';
    const confidence = grant.confidence !== undefined && grant.confidence !== null ? `${grant.confidence}%` : 'N/A';
    const sourceName = grant.source_name ? escapeHtml(grant.source_name) : 'Unknown';
    const sourceUrl = grant.source_url ? escapeHtml(grant.source_url) : null;

    const sourceLink = sourceUrl
        ? `<a href="${sourceUrl}" target="_blank" rel="noopener" class="grant-source-link">View on ${sourceName} →</a>`
        : `<span class="grant-source">Source: ${sourceName}</span>`;

    card.innerHTML = `
        <h3 class="grant-title">${escapeHtml(grant.title)}</h3>
        <div class="grant-funding">${formatFunding(grant.funding_amount)}</div>
        <div class="grant-score ${getScoreClass(grant.score)}">Score: ${grant.score}</div>
        <p class="grant-explanation">${escapeHtml(grant.explanation)}</p>
        <div class="grant-topics">Topics: ${topics}</div>
        <div class="grant-trend">Trend: ${trend}</div>
        <div class="grant-confidence">Confidence: ${confidence}</div>
        <div class="grant-source-line">${sourceLink}</div>
    `;
    return card;
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Raw text
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Render grants to the container
 * @param {Array} grants - Array of grant objects
 */
function renderGrants(grants) {
    hideLoading();
    grantsContainer.innerHTML = '';

    // Only show empty state if array is exactly empty (length === 0)
    // null/undefined should be handled by caller
    if (!Array.isArray(grants)) {
        console.error('renderGrants expected array, got:', grants);
        showError();
        return;
    }

    if (grants.length === 0) {
        console.log('renderGrants: empty array received, showing empty state');
        showEmpty();
        return;
    }

    console.log('renderGrants: rendering', grants.length, 'grants');

    grants.forEach(grant => {
        const card = createGrantCard(grant);
        grantsContainer.appendChild(card);
    });
}

/**
 * Fetch grants from the API (or use mock data if USE_MOCK is true)
 * @returns {Promise<Array>} Array of grant objects
 */
async function fetchGrants() {
    showLoading();

    // Use mock data for development when backend is not ready
    if (USE_MOCK) {
        console.log('Using mock data');
        return Promise.resolve(MOCK_GRANTS);
    }

    try {
        const response = await fetch(GRANTS_ENDPOINT);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Fetched grants data:', data);
        console.log('Grants count:', data ? data.length : 0);
        return data;
    } catch (error) {
        console.error('Error fetching grants:', error);
        showError();
        return null;
    }
}

/**
 * Initialize the grants page
 */
async function init() {
    // Only load if on grants page or initial load
    const grants = await fetchGrants();
    console.log('init() received grants:', grants);
    if (grants && Array.isArray(grants)) {
        renderGrants(grants);
    } else if (grants === null) {
        // Error already shown by fetchGrants, just log
        console.log('init() received null, error state shown');
    } else {
        console.error('init() received unexpected data:', grants);
        showError();
    }
}

// Page Navigation
function navigateTo(pageId) {
    // Hide all pages
    pages.forEach(page => page.classList.remove('active'));

    // Show target page
    const targetPage = document.getElementById(`page-${pageId}`);
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // Update nav links
    navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.page === pageId);
    });

    // Load grants on dashboard if navigating there
    if (pageId === 'dashboard' && dashboardGrantsContainer) {
        loadDashboardGrants();
    }

    // Scroll to top
    window.scrollTo(0, 0);
}

function handleNavigation(e) {
    e.preventDefault();
    const pageId = e.target.dataset.page;
    if (pageId) {
        navigateTo(pageId);
        window.history.pushState({ page: pageId }, '', `#${pageId}`);
    }
}

// Auth Modal
function openAuthModal() {
    authModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeAuthModal() {
    authModal.classList.add('hidden');
    document.body.style.overflow = '';
}

function switchAuthTab(tabId) {
    authTabs.forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabId);
    });
    authForms.forEach(form => {
        form.classList.toggle('active', form.id === `${tabId}-form`);
    });
}

// Dashboard grants (limited set)
async function loadDashboardGrants() {
    if (!dashboardGrantsContainer) return;

    dashboardGrantsContainer.innerHTML = '<div class="loading">Loading...</div>';

    const grants = USE_MOCK
        ? MOCK_GRANTS.slice(0, 3)
        : await fetchGrants().then(data => data?.slice(0, 3));

    if (grants && grants.length > 0) {
        dashboardGrantsContainer.innerHTML = '';
        grants.forEach(grant => {
            const card = createGrantCard(grant);
            dashboardGrantsContainer.appendChild(card);
        });
    } else {
        dashboardGrantsContainer.innerHTML = '<div class="loading">No grants available</div>';
    }
}

// Event Listeners
if (retryBtn) {
    retryBtn.addEventListener('click', init);
}

// Navigation
navLinks.forEach(link => {
    link.addEventListener('click', handleNavigation);
});

// Auth Modal
if (authBtn) {
    authBtn.addEventListener('click', openAuthModal);
}

if (modalClose) {
    modalClose.addEventListener('click', closeAuthModal);
}

if (modalOverlay) {
    modalOverlay.addEventListener('click', closeAuthModal);
}

// Auth Tabs
authTabs.forEach(tab => {
    tab.addEventListener('click', () => switchAuthTab(tab.dataset.tab));
});

// Auth Forms
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Demo: Sign in functionality coming soon!');
        closeAuthModal();
    });
}

if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Demo: Registration coming soon!');
        closeAuthModal();
    });
}

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !authModal.classList.contains('hidden')) {
        closeAuthModal();
    }
});

// Handle browser back/forward
window.addEventListener('popstate', (e) => {
    const pageId = window.location.hash.slice(1) || 'dashboard';
    navigateTo(pageId);
});

// Start the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Check URL hash for initial page
    const initialPage = window.location.hash.slice(1) || 'dashboard';
    navigateTo(initialPage);

    // Initialize grants on main grants page
    init();
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { fetchGrants, renderGrants, formatFunding, getScoreClass, escapeHtml };
}
