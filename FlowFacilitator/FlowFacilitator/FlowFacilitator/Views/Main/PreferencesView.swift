import SwiftUI

struct PreferencesView: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        ZStack {
            Colors.deepNight.ignoresSafeArea()
            
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    Text("Preferences")
                        .font(.largeTitle)
                        .foregroundColor(Colors.textOnDark)
                    
                    // Account Section
                    VStack(alignment: .leading, spacing: 12) {
                        Text("ACCOUNT")
                            .font(.caption)
                            .foregroundColor(Colors.textSecondary)
                        
                        VStack(alignment: .leading, spacing: 8) {
                            if let user = appState.currentUser {
                                Text(user.fullName ?? "User")
                                    .foregroundColor(Colors.textOnDark)
                                Text(user.email)
                                    .foregroundColor(Colors.textSecondary)
                            }
                            
                            Button("Logout") {
                                Task {
                                    await appState.signOut()
                                }
                            }
                            .padding(.horizontal, 16)
                            .padding(.vertical, 8)
                            .background(Colors.magenta)
                            .foregroundColor(.white)
                            .cornerRadius(6)
                        }
                        .padding()
                        .background(Colors.surfaceLight)
                        .cornerRadius(12)
                    }
                    
                    // Permissions Section
                    VStack(alignment: .leading, spacing: 12) {
                        Text("SYSTEM PERMISSIONS")
                            .font(.caption)
                            .foregroundColor(Colors.textSecondary)
                        
                        VStack(spacing: 8) {
                            PermissionRow(title: "Accessibility", granted: appState.permissions.accessibility)
                            PermissionRow(title: "Input Monitoring", granted: appState.permissions.inputMonitoring)
                            PermissionRow(title: "Screen Recording", granted: appState.permissions.screenRecording)
                        }
                        .padding()
                        .background(Colors.surfaceLight)
                        .cornerRadius(12)
                    }
                    
                    // Version Info
                    VStack(alignment: .leading, spacing: 12) {
                        Text("VERSION INFO")
                            .font(.caption)
                            .foregroundColor(Colors.textSecondary)
                        
                        VStack(alignment: .leading, spacing: 8) {
                            Text("App Version: 1.0.0")
                                .foregroundColor(Colors.textOnDark)
                            Text("Agent Version: 1.0.0")
                                .foregroundColor(Colors.textOnDark)
                        }
                        .padding()
                        .background(Colors.surfaceLight)
                        .cornerRadius(12)
                    }
                }
                .padding(40)
            }
        }
        .frame(width: 450, height: 600)
    }
}

struct PermissionRow: View {
    let title: String
    let granted: Bool
    
    var body: some View {
        HStack {
            Text(title)
                .foregroundColor(Colors.textOnDark)
            Spacer()
            Image(systemName: granted ? "checkmark.circle.fill" : "xmark.circle.fill")
                .foregroundColor(granted ? Colors.teal : Colors.magenta)
        }
    }
}
