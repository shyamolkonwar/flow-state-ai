import Foundation

class SupabaseService {
    private let supabaseURL = "https://fxombpzgqotfacyrlule.supabase.co"
    private let supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4b21icHpncW90ZmFjeXJsdWxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4OTE1ODYsImV4cCI6MjA3OTQ2NzU4Nn0.DbsgRs_SJM3oujOEvYiehaVzScnspFyETlRWJmEeTfY"
    
    private var currentSession: Session?
    
    // MARK: - Authentication
    
    func signIn(email: String, password: String) async throws -> (User, Session) {
        print("🔐 [DEBUG] Starting sign in for email: \(email)")
        let url = URL(string: "\(supabaseURL)/auth/v1/token?grant_type=password")!
        print("🔐 [DEBUG] Sign in URL: \(url)")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")

        let body = ["email": email, "password": password]
        request.httpBody = try JSONEncoder().encode(body)
        print("🔐 [DEBUG] Sign in request body: \(String(data: request.httpBody!, encoding: .utf8) ?? "nil")")

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            print("🔐 [DEBUG] Sign in failed: Invalid response type")
            throw SupabaseError.authenticationFailed
        }

        print("🔐 [DEBUG] Sign in response status: \(httpResponse.statusCode)")
        print("🔐 [DEBUG] Sign in response data: \(String(data: data, encoding: .utf8) ?? "nil")")

        guard httpResponse.statusCode == 200 else {
            print("🔐 [DEBUG] Sign in failed with status: \(httpResponse.statusCode)")
            throw SupabaseError.authenticationFailed
        }

        let authResponse = try JSONDecoder().decode(AuthResponse.self, from: data)
        print("🔐 [DEBUG] Sign in auth response decoded successfully")

        let session = Session(
            accessToken: authResponse.accessToken,
            refreshToken: authResponse.refreshToken,
            expiresAt: Date(timeIntervalSinceNow: TimeInterval(authResponse.expiresIn))
        )

        self.currentSession = session
        print("🔐 [DEBUG] Sign in session created")

        // Fetch user profile
        print("🔐 [DEBUG] Fetching user profile...")
        let user = try await getUserProfile(accessToken: session.accessToken)
        print("🔐 [DEBUG] Sign in completed successfully for user: \(user.email)")

        return (user, session)
    }
    
    func signUp(email: String, password: String, fullName: String) async throws -> (User, Session) {
        print("🔐 [DEBUG] Starting sign up for email: \(email), fullName: \(fullName)")
        let url = URL(string: "\(supabaseURL)/auth/v1/signup")!
        print("🔐 [DEBUG] Sign up URL: \(url)")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")

        let body: [String: Any] = [
            "email": email,
            "password": password,
            "data": ["full_name": fullName]
        ]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        print("🔐 [DEBUG] Sign up request body: \(String(data: request.httpBody!, encoding: .utf8) ?? "nil")")

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            print("🔐 [DEBUG] Sign up failed: Invalid response type")
            throw SupabaseError.signupFailed
        }

        print("🔐 [DEBUG] Sign up response status: \(httpResponse.statusCode)")
        print("🔐 [DEBUG] Sign up response data: \(String(data: data, encoding: .utf8) ?? "nil")")

        guard httpResponse.statusCode == 200 else {
            print("🔐 [DEBUG] Sign up failed with status: \(httpResponse.statusCode)")
            throw SupabaseError.signupFailed
        }

        let authResponse = try JSONDecoder().decode(AuthResponse.self, from: data)
        print("🔐 [DEBUG] Sign up auth response decoded successfully")

        let session = Session(
            accessToken: authResponse.accessToken,
            refreshToken: authResponse.refreshToken,
            expiresAt: Date(timeIntervalSinceNow: TimeInterval(authResponse.expiresIn))
        )

        self.currentSession = session
        print("🔐 [DEBUG] Sign up session created")

        // Fetch user profile
        print("🔐 [DEBUG] Fetching user profile after signup...")
        let user = try await getUserProfile(accessToken: session.accessToken)
        print("🔐 [DEBUG] Sign up completed successfully for user: \(user.email)")

        return (user, session)
    }
    
    func signOut() async throws {
        guard let session = currentSession else { return }
        
        let url = URL(string: "\(supabaseURL)/auth/v1/logout")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        
        _ = try await URLSession.shared.data(for: request)
        
        self.currentSession = nil
    }
    
    func restoreSession(_ session: Session) async throws -> User {
        self.currentSession = session
        return try await getUserProfile(accessToken: session.accessToken)
    }
    
    // MARK: - User Profile
    
    func getUserProfile(accessToken: String) async throws -> User {
        let url = URL(string: "\(supabaseURL)/rest/v1/rpc/get_user_profile")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw SupabaseError.profileFetchFailed
        }
        
        let profiles = try JSONDecoder().decode([User].self, from: data)
        guard let user = profiles.first else {
            throw SupabaseError.profileNotFound
        }
        
        return user
    }
    
    func markOnboardingComplete() async throws {
        guard let session = currentSession else {
            throw SupabaseError.notAuthenticated
        }
        
        let url = URL(string: "\(supabaseURL)/rest/v1/rpc/complete_onboarding")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        
        _ = try await URLSession.shared.data(for: request)
    }
    
    func updatePermissions(_ permissions: Permissions) async throws {
        guard let session = currentSession else {
            throw SupabaseError.notAuthenticated
        }
        
        let url = URL(string: "\(supabaseURL)/rest/v1/rpc/update_user_permissions")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        
        let body = ["p_permissions": permissions]
        request.httpBody = try JSONEncoder().encode(body)
        
        _ = try await URLSession.shared.data(for: request)
    }
}

// MARK: - Helper Types

struct AuthResponse: Codable {
    let accessToken: String
    let refreshToken: String
    let expiresIn: Int
    
    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case expiresIn = "expires_in"
    }
}

enum SupabaseError: Error {
    case authenticationFailed
    case signupFailed
    case profileFetchFailed
    case profileNotFound
    case notAuthenticated
}
