import Foundation
import AppKit

class PermissionChecker {
    static func checkAll() -> Permissions {
        return Permissions(
            accessibility: checkAccessibility(),
            inputMonitoring: checkInputMonitoring(),
            screenRecording: checkScreenRecording()
        )
    }
    
    static func checkAccessibility() -> Bool {
        let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: false]
        return AXIsProcessTrustedWithOptions(options as CFDictionary)
    }
    
    static func checkInputMonitoring() -> Bool {
        // Input monitoring check
        return CGPreflightScreenCaptureAccess()
    }
    
    static func checkScreenRecording() -> Bool {
        return CGPreflightScreenCaptureAccess()
    }
    
    static func requestAccessibility() {
        let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true]
        AXIsProcessTrustedWithOptions(options as CFDictionary)
    }
    
    static func openSystemPreferences(for permission: String) {
        var prefPane = ""
        
        switch permission {
        case "accessibility":
            prefPane = "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
        case "input_monitoring":
            prefPane = "x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent"
        case "screen_recording":
            prefPane = "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
        default:
            prefPane = "x-apple.systempreferences:com.apple.preference.security"
        }
        
        if let url = URL(string: prefPane) {
            NSWorkspace.shared.open(url)
        }
    }
}
