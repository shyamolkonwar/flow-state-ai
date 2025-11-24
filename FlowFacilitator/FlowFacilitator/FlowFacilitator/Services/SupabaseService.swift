init() {
        // Try to load from SupabaseConfig.plist first (production config)
        if let configURL = Bundle.main.url(forResource: "SupabaseConfig", withExtension: "plist"),
           let config = NSDictionary(contentsOf: configURL),
           let url = config["SUPABASE_URL"] as? String, !url.contains("your-project"),
           let key = config["SUPABASE_ANON_KEY"] as? String, !key.contains("your-anon-key") {
            self.supabaseURL = url
            self.supabaseAnonKey = key
        }
        // Fallback to SupabaseConfig.example.plist (development template)
        else if let exampleConfigURL = Bundle.main.url(forResource: "SupabaseConfig.example", withExtension: "plist"),
                let exampleConfig = NSDictionary(contentsOf: exampleConfigURL),
                let url = exampleConfig["SUPABASE_URL"] as? String,
                let key = exampleConfig["SUPABASE_ANON_KEY"] as? String {
            self.supabaseURL = url
            self.supabaseAnonKey = key
        }
        // Final fallback to environment variables
        else {
            self.supabaseURL = ProcessInfo.processInfo.environment["SUPABASE_URL"] ?? ""
            self.supabaseAnonKey = ProcessInfo.processInfo.environment["SUPABASE_ANON_KEY"] ?? ""
        }
    }
