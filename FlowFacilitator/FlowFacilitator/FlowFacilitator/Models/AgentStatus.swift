import Foundation

struct AgentStatus: Codable {
    var agentRunning: Bool = false
    var flowState: String = "idle"
    var permissions: Permissions = Permissions()
    
    enum CodingKeys: String, CodingKey {
        case agentRunning = "agent_running"
        case flowState = "flow_state"
        case permissions
    }
}
