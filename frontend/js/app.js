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
        explanation: "High funding with broad eligibility for AI applications in climate science"
    },
    {
        id: "2",
        title: "Renewable Energy Innovation",
        funding_amount: 250000,
        score: 72,
        explanation: "Strong focus on sustainable energy solutions with clear evaluation criteria"
    },
    {
        id: "3",
        title: "Community Health Outreach",
        funding_amount: 75000,
        score: 45,
        explanation: "Moderate funding amount, limited to specific geographic regions"
    },
    {
        id: "4",
        title: "Educational Technology Grant",
        funding_amount: 30000,
        score: 25,
        explanation: "Low funding amount with highly competitive application process"
    }
];

// DOM Elements
const grantsContainer = document.getElementById('grants-container');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const retryBtn = document.getElementById('retry-btn');

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
    card.innerHTML = `
        <h3 class="grant-title">${escapeHtml(grant.title)}</h3>
        <div class="grant-funding">${formatFunding(grant.funding_amount)}</div>
        <div class="grant-score ${getScoreClass(grant.score)}">Score: ${grant.score}</div>
        <p class="grant-explanation">${escapeHtml(grant.explanation)}</p>
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

    if (!grants || grants.length === 0) {
        showEmpty();
        return;
    }

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
        return data;
    } catch (error) {
        console.error('Error fetching grants:', error);
        showError();
        return null;
    }
}

/**
 * Initialize the application
 */
async function init() {
    const grants = await fetchGrants();
    if (grants) {
        renderGrants(grants);
    }
}

// Event Listeners
if (retryBtn) {
    retryBtn.addEventListener('click', init);
}

// Start the app when DOM is ready
document.addEventListener('DOMContentLoaded', init);

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { fetchGrants, renderGrants, formatFunding, getScoreClass, escapeHtml };
}
