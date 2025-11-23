// FlowFacilitator Extension Popup Script

// Supabase configuration
const SUPABASE_URL = 'https://fxombpzgqotfacyrlule.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4b21icHpncW90ZmFjeXJsdWxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4OTE1ODYsImV4cCI6MjA3OTQ2NzU4Nn0.DbsgRs_SJM3oujOEvYiehaVzScnspFyETlRWJmEeTfY';

let supabase;
let currentUser = null;

document.addEventListener('DOMContentLoaded', () => {
    initializeSupabase();
});

function initializeSupabase() {
    // Supabase is now loaded locally via script tag in HTML
    if (window.supabase) {
        supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        initializeApp();
    } else {
        console.error('Supabase library not loaded');
        showLoginSection();
    }
}

function initializeApp() {
    // Show loading state initially
    showLoadingState();

    checkAuthStatus();
    setupEventListeners();

    // Refresh status every 2 seconds
    setInterval(loadStatus, 2000);
}

function showLoadingState() {
    // Hide all sections and show a loading message
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('signup-section').style.display = 'none';
    document.getElementById('authenticated-section').style.display = 'none';

    // Create and show loading message
    if (!document.getElementById('loading-section')) {
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading-section';
        loadingDiv.innerHTML = `
            <div class="glass-card" style="margin-bottom: 20px; padding: 20px; text-align: center;">
                <div style="color: var(--prism-cyan); font-size: 16px; margin-bottom: 8px;">Initializing...</div>
                <div style="color: rgba(255, 255, 255, 0.6); font-size: 12px;">Connecting to crystal core</div>
            </div>
        `;
        document.querySelector('.container').insertBefore(loadingDiv, document.querySelector('.footer'));
    }
    document.getElementById('loading-section').style.display = 'block';
}

function setupEventListeners() {
    // Auth event listeners
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('signup-form').addEventListener('submit', handleSignup);
    document.getElementById('show-signup').addEventListener('click', showSignup);
    document.getElementById('show-login').addEventListener('click', showLogin);
    document.getElementById('logout').addEventListener('click', handleLogout);

    // Other event listeners
    document.getElementById('open-dashboard').addEventListener('click', () => {
        chrome.tabs.create({ url: 'http://localhost:3001' });
    });

    document.getElementById('settings').addEventListener('click', () => {
        chrome.runtime.openOptionsPage();
    });
}

async function checkAuthStatus() {
    try {
        const { data: { session } } = await supabase.auth.getSession();
        currentUser = session?.user || null;
        updateUI();
    } catch (error) {
        console.error('Error checking auth status:', error);
        showLoginSection();
    }
}

function updateUI() {
    // Hide loading section
    const loadingSection = document.getElementById('loading-section');
    if (loadingSection) {
        loadingSection.style.display = 'none';
    }

    const loginSection = document.getElementById('login-section');
    const signupSection = document.getElementById('signup-section');
    const authenticatedSection = document.getElementById('authenticated-section');

    if (currentUser) {
        loginSection.style.display = 'none';
        signupSection.style.display = 'none';
        authenticatedSection.style.display = 'block';
        loadStatus();
    } else {
        showLoginSection();
    }
}

function showLoginSection() {
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('signup-section').style.display = 'none';
    document.getElementById('authenticated-section').style.display = 'none';
}

function showSignupSection() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('signup-section').style.display = 'block';
    document.getElementById('authenticated-section').style.display = 'none';
}

function showSignup() {
    showSignupSection();
}

function showLogin() {
    showLoginSection();
}

async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const submitBtn = document.getElementById('login-submit');
    const errorDiv = document.getElementById('login-error');

    submitBtn.textContent = 'Signing In...';
    submitBtn.disabled = true;
    errorDiv.style.display = 'none';

    try {
        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password
        });

        if (error) throw error;

        currentUser = data.user;
        updateUI();
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    } finally {
        submitBtn.textContent = 'Sign In';
        submitBtn.disabled = false;
    }
}

async function handleSignup(e) {
    e.preventDefault();

    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const submitBtn = document.getElementById('signup-submit');
    const errorDiv = document.getElementById('signup-error');

    submitBtn.textContent = 'Creating Account...';
    submitBtn.disabled = true;
    errorDiv.style.display = 'none';

    try {
        const { data, error } = await supabase.auth.signUp({
            email,
            password,
            options: {
                data: {
                    full_name: name
                }
            }
        });

        if (error) throw error;

        alert('Account created successfully! Please check your email to verify your account, then sign in.');
        showLoginSection();
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    } finally {
        submitBtn.textContent = 'Create Account';
        submitBtn.disabled = false;
    }
}

async function handleLogout() {
    try {
        await supabase.auth.signOut();
        currentUser = null;
        updateUI();
    } catch (error) {
        console.error('Error signing out:', error);
    }
}

async function loadStatus() {
    try {
        const result = await chrome.storage.local.get([
            'isBlocking',
            'blockedDomains',
            'blocksToday'
        ]);

        const isBlocking = result.isBlocking || false;
        const blockedDomains = result.blockedDomains || [];
        const blocksToday = result.blocksToday || 0;

        // Update status
        const statusEl = document.getElementById('status');
        const statusText = document.getElementById('status-text');

        if (isBlocking) {
            statusEl.className = 'status active';
            statusText.textContent = '🎯 Blocking Active';
        } else {
            statusEl.className = 'status inactive';
            statusText.textContent = 'Not Blocking';
        }

        // Update stats
        document.getElementById('blocks-today').textContent = blocksToday;
        document.getElementById('domain-count').textContent = blockedDomains.length;

    } catch (error) {
        console.error('Error loading status:', error);
    }
}
