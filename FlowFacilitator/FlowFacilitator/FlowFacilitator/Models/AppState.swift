import Foundation
import Combine

@MainActor
class AppState: ObservableObject {
    // Authentication
    @Published var isAuthenticated: Bool = false
    @Published var currentUser: User?
    @Published var onboardingComplete: Bool = false
    
    // Agent Status
    @Published var agentStatus: AgentStatus = AgentStatus()
    
    // Permissions
    @Published var permissions: Permissions = Permissions()
    
    // Services
    private let supabaseService: SupabaseService
    private let agentAPIService: AgentAPIService
    private let keychainService: KeychainService
    
    // Timer for status updates
    private var statusTimer: Timer?
    
    init() {
        self.supabaseService = SupabaseService()
        self.agentAPIService = AgentAPIService()
        self.keychainService = KeychainService()
        
        // Try to restore session
        Task {
            await restoreSession()
            startStatusUpdates()
        }
    }
    
    // MARK: - Authentication
    
    func restoreSession() async {
        if let session = keychainService.getSession() {
            // Restore session with Supabase
            do {
                let user = try await supabaseService.restoreSession(session)
                self.currentUser = user
                self.isAuthenticated = true
                self.onboardingComplete = user.onboardingComplete
            } catch {
                print("Failed to restore session: \(error)")
                keychainService.clearSession()
            }
        }
    }
    
    func signIn(email: String, password: String) async throws {
        let (user, session) = try await supabaseService.signIn(email: email, password: password)

        // Save session to keychain
        keychainService.saveSession(session)

        self.currentUser = user
        self.isAuthenticated = true
        self.onboardingComplete = user.onboardingComplete

        print("🔐 [DEBUG] AppState signIn complete - authenticated: \(self.isAuthenticated), onboardingComplete: \(self.onboardingComplete)")
    }
    
    func signUp(email: String, password: String, fullName: String) async throws {
        let (user, session) = try await supabaseService.signUp(email: email, password: password, fullName: fullName)
        
        // Save session to keychain
        keychainService.saveSession(session)
        
        self.currentUser = user
        self.isAuthenticated = true
        self.onboardingComplete = false
    }
    
    func signOut() async {
        do {
            try await supabaseService.signOut()
            keychainService.clearSession()
            
            self.currentUser = nil
            self.isAuthenticated = false
            self.onboardingComplete = false
        } catch {
            print("Sign out error: \(error)")
        }
    }
    
    // MARK: - Onboarding
    
    func completeOnboarding() async {
        do {
            try await supabaseService.markOnboardingComplete()
            self.onboardingComplete = true
            
            // Sync permissions
            await syncPermissions()
        } catch {
            print("Failed to complete onboarding: \(error)")
        }
    }
    
    // MARK: - Permissions
    
    func checkPermissions() {
        permissions = PermissionChecker.checkAll()
    }
    
    func syncPermissions() async {
        checkPermissions()
        
        do {
            try await supabaseService.updatePermissions(permissions)
        } catch {
            print("Failed to sync permissions: \(error)")
        }
    }
    
    // MARK: - Agent Control
    
    func startStatusUpdates() {
        statusTimer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { [weak self] _ in
            Task { @MainActor in
                await self?.updateAgentStatus()
            }
        }
        
        // Initial update
        Task {
            await updateAgentStatus()
        }
    }
    
    func updateAgentStatus() async {
        do {
            let status = try await agentAPIService.getStatus()
            self.agentStatus = status
            self.permissions = status.permissions
        } catch {
            print("Failed to get agent status: \(error)")
        }
    }
    
    func toggleAgent() async {
        if agentStatus.agentRunning {
            await stopAgent()
        } else {
            await startAgent()
        }
    }
    
    func startAgent() async {
        do {
            try await agentAPIService.startAgent()
            await updateAgentStatus()
        } catch {
            print("Failed to start agent: \(error)")
        }
    }
    
    func stopAgent() async {
        do {
            try await agentAPIService.stopAgent()
            await updateAgentStatus()
        } catch {
            print("Failed to stop agent: \(error)")
        }
    }
    
    func restartAgent() async {
        await stopAgent()
        try? await Task.sleep(nanoseconds: 1_000_000_000) // 1 second
        await startAgent()
    }
}
