import Foundation

class AgentAPIService {
    private let baseURL = "http://127.0.0.1:8765"
    
    func getStatus() async throws -> AgentStatus {
        let url = URL(string: "\(baseURL)/status")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(AgentStatus.self, from: data)
    }
    
    func startAgent() async throws {
        let url = URL(string: "\(baseURL)/start")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        _ = try await URLSession.shared.data(for: request)
    }
    
    func stopAgent() async throws {
        let url = URL(string: "\(baseURL)/stop")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        _ = try await URLSession.shared.data(for: request)
    }
}
