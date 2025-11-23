import Foundation

struct User: Codable {
    let id: String
    let email: String
    let fullName: String?
    let onboardingComplete: Bool
    let preferences: UserPreferences?
    let permissions: Permissions?
    
    enum CodingKeys: String, CodingKey {
        case id, email
        case fullName = "full_name"
        case onboardingComplete = "onboarding_complete"
        case preferences, permissions
    }
}

struct UserPreferences: Codable {
    var autoStart: Bool
    var dashboardPort: Int
    var agentPort: Int
    var theme: String
    var notificationsEnabled: Bool
    
    enum CodingKeys: String, CodingKey {
        case autoStart = "auto_start"
        case dashboardPort = "dashboard_port"
        case agentPort = "agent_port"
        case theme
        case notificationsEnabled = "notifications_enabled"
    }
}

struct Permissions: Codable {
    var accessibility: Bool = false
    var inputMonitoring: Bool = false
    var screenRecording: Bool = false
    
    enum CodingKeys: String, CodingKey {
        case accessibility
        case inputMonitoring = "input_monitoring"
        case screenRecording = "screen_recording"
    }
}

struct Session: Codable {
    let accessToken: String
    let refreshToken: String
    let expiresAt: Date
    
    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case expiresAt = "expires_at"
    }
}
