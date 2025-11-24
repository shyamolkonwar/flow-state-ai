// Load configuration
async function loadConfig() {
    try {
        // Try to load from chrome.storage first (for user-set values)
        const result = await chrome.storage.sync.get(['supabaseUrl', 'supabaseAnonKey']);
        SUPABASE_URL = result.supabaseUrl;
        SUPABASE_ANON_KEY = result.supabaseAnonKey;

        // If not configured, show error
        if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
            console.error('Supabase not configured. Please set up the extension configuration.');
            showLoginSection();
            return;
        }
    } catch (error) {
        console.error('Error loading configuration:', error);
        showLoginSection();
    }
}
