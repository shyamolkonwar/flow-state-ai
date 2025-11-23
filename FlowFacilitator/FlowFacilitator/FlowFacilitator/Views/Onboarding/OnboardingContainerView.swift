import SwiftUI

struct OnboardingContainerView: View {
    @ObservedObject var appState: AppState
    let onComplete: () -> Void
    
    @State private var currentPage = 0
    
    var body: some View {
        ZStack {
            Colors.deepNight.ignoresSafeArea()
            
            VStack(spacing: 24) {
                // Progress bar
                ProgressView(value: Double(currentPage + 1), total: 4)
                    .tint(Colors.teal)
                
                // Pages
                TabView(selection: $currentPage) {
                    WelcomeView().tag(0)
                    PermissionsView(appState: appState).tag(1)
                    ExtensionView().tag(2)
                    CompletionView(onComplete: handleComplete).tag(3)
                }
                
                // Navigation
                HStack {
                    if currentPage > 0 {
                        Button("Back") {
                            currentPage -= 1
                        }
                        .foregroundColor(Colors.textSecondary)
                    }
                    
                    Spacer()
                    
                    if currentPage < 3 {
                        Button(currentPage == 0 ? "Get Started" : "Continue") {
                            currentPage += 1
                        }
                        .padding(.horizontal, 24)
                        .padding(.vertical, 12)
                        .background(Colors.teal)
                        .foregroundColor(Colors.deepNight)
                        .cornerRadius(8)
                    }
                }
            }
            .padding(40)
        }
        .frame(width: 550, height: 650)
    }
    
    func handleComplete() {
        Task {
            await appState.completeOnboarding()
            await MainActor.run {
                onComplete()
            }
        }
    }
}

struct WelcomeView: View {
    var body: some View {
        VStack(spacing: 24) {
            Circle()
                .fill(Colors.tealToCyan)
                .frame(width: 120, height: 120)
                .overlay(
                    Image(systemName: "waveform.path.ecg")
                        .font(.system(size: 60))
                        .foregroundColor(.white)
                )
            
            Text("Welcome to FlowFacilitator")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundStyle(Colors.tealToCyan)
            
            Text("FlowFacilitator helps you detect and protect\nyour flow state on macOS.\n\nLet's get you set up in just a few steps.")
                .multilineTextAlignment(.center)
                .foregroundColor(Colors.textOnDark)
        }
    }
}

struct PermissionsView: View {
    @ObservedObject var appState: AppState
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Grant System Permissions")
                .font(.title)
                .foregroundColor(Colors.textOnDark)
            
            Text("FlowFacilitator needs these permissions to monitor\nyour activity and protect your flow state.")
                .multilineTextAlignment(.center)
                .foregroundColor(Colors.textSecondary)
            
            PermissionCard(
                title: "Accessibility",
                granted: appState.permissions.accessibility,
                optional: false,
                onGrant: {
                    PermissionChecker.openSystemPreferences(for: "accessibility")
                }
            )
            
            PermissionCard(
                title: "Input Monitoring",
                granted: appState.permissions.inputMonitoring,
                optional: false,
                onGrant: {
                    PermissionChecker.openSystemPreferences(for: "input_monitoring")
                }
            )
            
            PermissionCard(
                title: "Screen Recording",
                granted: appState.permissions.screenRecording,
                optional: true,
                onGrant: {
                    PermissionChecker.openSystemPreferences(for: "screen_recording")
                }
            )
        }
    }
}

struct ExtensionView: View {
    var body: some View {
        VStack(spacing: 24) {
            Text("Install Chrome Extension")
                .font(.title)
                .foregroundColor(Colors.textOnDark)
            
            Text("For full functionality, install the\nFlowFacilitator Chrome extension.\n\nThis allows the app to detect when you're\nin a focused work session.")
                .multilineTextAlignment(.center)
                .foregroundColor(Colors.textSecondary)
            
            Text("🧩")
                .font(.system(size: 80))
            
            Button("Open Extension Setup Guide") {
                // Open guide
            }
            .padding(.horizontal, 24)
            .padding(.vertical, 12)
            .background(Colors.teal)
            .foregroundColor(Colors.deepNight)
            .cornerRadius(8)
        }
    }
}

struct CompletionView: View {
    let onComplete: () -> Void
    
    var body: some View {
        VStack(spacing: 24) {
            Text("✓")
                .font(.system(size: 100))
                .foregroundColor(Colors.teal)
            
            Text("You're All Set!")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundStyle(Colors.tealToCyan)
            
            Text("FlowFacilitator is now ready to help you\ndetect and protect your flow state.\n\nOpen the dashboard to start tracking your productivity.")
                .multilineTextAlignment(.center)
                .foregroundColor(Colors.textOnDark)
            
            Button("Open Dashboard") {
                if let url = URL(string: "http://localhost:3001") {
                    NSWorkspace.shared.open(url)
                }
                onComplete()
            }
            .padding(.horizontal, 24)
            .padding(.vertical, 12)
            .background(Colors.teal)
            .foregroundColor(Colors.deepNight)
            .cornerRadius(8)
        }
    }
}

struct PermissionCard: View {
    let title: String
    let granted: Bool
    let optional: Bool
    let onGrant: () -> Void
    
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(title)
                    .foregroundColor(Colors.textOnDark)
                if optional {
                    Text("Optional")
                        .font(.caption)
                        .foregroundColor(Colors.textSecondary)
                }
            }
            
            Spacer()
            
            if granted {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundColor(Colors.teal)
            } else {
                Button("Grant") {
                    onGrant()
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(Colors.gold)
                .foregroundColor(Colors.deepNight)
                .cornerRadius(6)
            }
        }
        .padding()
        .background(Colors.surfaceLight)
        .cornerRadius(12)
    }
}
