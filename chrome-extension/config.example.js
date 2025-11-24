// FlowFacilitator Chrome Extension Configuration

// Supabase configuration - update these values for your project
const SUPABASE_CONFIG = {
    URL: 'https://your-project.supabase.co',
    ANON_KEY: 'your-anon-key-here'
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SUPABASE_CONFIG;
}
