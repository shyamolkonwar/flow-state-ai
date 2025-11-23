import SwiftUI

struct Colors {
    // Premium Color Palette
    static let deepNight = Color(hex: "0B0710")
    static let surfaceLight = Color(hex: "0F1220")
    static let surfaceElev = Color(hex: "141722")
    static let textOnDark = Color(hex: "EDEFF6")
    static let textSecondary = Color(hex: "9CA3AF")
    static let teal = Color(hex: "2FE6C1")
    static let cyan = Color(hex: "00D9FF")
    static let magenta = Color(hex: "FF6EC7")
    static let gold = Color(hex: "FFD700")
    
    // Gradients
    static let tealToCyan = LinearGradient(
        colors: [teal, cyan],
        startPoint: .leading,
        endPoint: .trailing
    )
    
    static let magentaToCyan = LinearGradient(
        colors: [magenta, cyan],
        startPoint: .leading,
        endPoint: .trailing
    )
}

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}
