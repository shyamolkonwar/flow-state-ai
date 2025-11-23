import Foundation
import Security

class KeychainService {
    private let service = "com.flowfacilitator.app"
    private let accessTokenKey = "access_token"
    private let refreshTokenKey = "refresh_token"
    private let expiresAtKey = "expires_at"
    
    func saveSession(_ session: Session) {
        save(key: accessTokenKey, value: session.accessToken)
        save(key: refreshTokenKey, value: session.refreshToken)
        save(key: expiresAtKey, value: ISO8601DateFormatter().string(from: session.expiresAt))
    }
    
    func getSession() -> Session? {
        guard let accessToken = get(key: accessTokenKey),
              let refreshToken = get(key: refreshTokenKey),
              let expiresAtString = get(key: expiresAtKey),
              let expiresAt = ISO8601DateFormatter().date(from: expiresAtString) else {
            return nil
        }
        
        return Session(accessToken: accessToken, refreshToken: refreshToken, expiresAt: expiresAt)
    }
    
    func clearSession() {
        delete(key: accessTokenKey)
        delete(key: refreshTokenKey)
        delete(key: expiresAtKey)
    }
    
    // MARK: - Private Methods
    
    private func save(key: String, value: String) {
        let data = value.data(using: .utf8)!
        
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]
        
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }
    
    private func get(key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        guard status == errSecSuccess,
              let data = result as? Data,
              let value = String(data: data, encoding: .utf8) else {
            return nil
        }
        
        return value
    }
    
    private func delete(key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key
        ]
        
        SecItemDelete(query as CFDictionary)
    }
}
