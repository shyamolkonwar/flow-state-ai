import SwiftUI
import Combine

@main
struct FlowFacilitatorApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        // Menu bar app - no window scene needed initially
        Settings {
            EmptyView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem?
    var popover: NSPopover?
    var appState: AppState?
    private var statusCancellable: AnyCancellable?
    var loginWindow: NSWindow?
    var onboardingWindow: NSWindow?

    func getStatusIcon(for flowState: String) -> NSImage? {
        let imageName: String
        switch flowState.lowercased() {
        case "idle":
            imageName = "Idle"
        case "flow":
            imageName = "Flow"
        case "tracking":
            imageName = "Tracking"
        case "error":
            imageName = "Error"
        default:
            imageName = "Idle"
        }
        return NSImage(named: imageName)
    }

    func updateStatusIcon(for flowState: String) {
        statusItem?.button?.image = getStatusIcon(for: flowState)
    }
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Initialize app state
        appState = AppState()

        // Observe status changes to update icon
        statusCancellable = appState?.$agentStatus
            .map { $0.flowState }
            .receive(on: DispatchQueue.main)
            .sink { [weak self] flowState in
                self?.updateStatusIcon(for: flowState)
            }

        // Create menu bar item
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)

        if let button = statusItem?.button {
            button.image = getStatusIcon(for: appState?.agentStatus.flowState ?? "idle")
            button.action = #selector(togglePopover)
            button.target = self
        }

        // Check authentication status
        Task {
            await checkAuthenticationStatus()
        }
    }
    
    @objc func togglePopover() {
        if statusItem?.button != nil {
            if let popover = popover, popover.isShown {
                popover.performClose(nil)
            } else {
                showMenu()
            }
        }
    }
    
    func showMenu() {
        guard let button = statusItem?.button else { return }
        
        let menu = NSMenu()
        
        // Open Dashboard
        menu.addItem(NSMenuItem(title: "Open Dashboard", action: #selector(openDashboard), keyEquivalent: ""))
        menu.addItem(NSMenuItem.separator())
        
        // Agent Status
        let statusMenuItem = NSMenuItem(title: "Agent Status: \(appState?.agentStatus.flowState ?? "Idle")", action: nil, keyEquivalent: "")
        statusMenuItem.isEnabled = false
        menu.addItem(statusMenuItem)
        menu.addItem(NSMenuItem.separator())

        // Permissions submenu
        let permissionsMenu = NSMenu()
        permissionsMenu.addItem(NSMenuItem(title: "Accessibility: \(appState?.permissions.accessibility == true ? "✓" : "✖")", action: nil, keyEquivalent: ""))
        permissionsMenu.addItem(NSMenuItem(title: "Input Monitoring: \(appState?.permissions.inputMonitoring == true ? "✓" : "✖")", action: nil, keyEquivalent: ""))
        permissionsMenu.addItem(NSMenuItem(title: "Screen Recording: \(appState?.permissions.screenRecording == true ? "✓" : "✖")", action: nil, keyEquivalent: ""))

        let permissionsItem = NSMenuItem(title: "Permissions", action: nil, keyEquivalent: "")
        permissionsItem.submenu = permissionsMenu
        menu.addItem(permissionsItem)
        menu.addItem(NSMenuItem.separator())

        // Agent Control
        let agentAction = appState?.agentStatus.agentRunning == true ? "Stop Agent" : "Start Agent"
        menu.addItem(NSMenuItem(title: agentAction, action: #selector(toggleAgent), keyEquivalent: ""))
        menu.addItem(NSMenuItem(title: "Restart Agent", action: #selector(restartAgent), keyEquivalent: ""))
        menu.addItem(NSMenuItem.separator())

        // Preferences
        menu.addItem(NSMenuItem(title: "Preferences...", action: #selector(showPreferences), keyEquivalent: ","))
        menu.addItem(NSMenuItem.separator())

        // Quit
        menu.addItem(NSMenuItem(title: "Quit FlowFacilitator", action: #selector(quitApp), keyEquivalent: "q"))

        statusItem?.menu = menu
        statusItem?.button?.performClick(nil)
        statusItem?.menu = nil
    }
    
    @objc func openDashboard() {
        if let url = URL(string: "http://localhost:3001") {
            NSWorkspace.shared.open(url)
        }
    }
    
    @objc func toggleAgent() {
        Task {
            await appState?.toggleAgent()
        }
    }
    
    @objc func restartAgent() {
        Task {
            await appState?.restartAgent()
        }
    }
    
    @objc func showPreferences() {
        let preferencesWindow = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 450, height: 600),
            styleMask: [.titled, .closable, .miniaturizable],
            backing: .buffered,
            defer: false
        )
        preferencesWindow.title = "Preferences"
        preferencesWindow.contentView = NSHostingView(rootView: PreferencesView(appState: appState!))
        preferencesWindow.center()
        preferencesWindow.makeKeyAndOrderFront(nil)
    }
    
    @objc func quitApp() {
        NSApplication.shared.terminate(nil)
    }
    
    func checkAuthenticationStatus() async {
        guard let appState = appState else { return }

        print("🔐 [DEBUG] checkAuthenticationStatus - authenticated: \(appState.isAuthenticated), onboardingComplete: \(appState.onboardingComplete)")

        if !appState.isAuthenticated {
            // Show login window
            print("🔐 [DEBUG] Showing login window")
            await MainActor.run {
                showLoginWindow()
            }
        } else {
            // Check onboarding status
            if !appState.onboardingComplete {
                print("🔐 [DEBUG] Showing onboarding window")
                await MainActor.run {
                    showOnboardingWindow()
                }
            } else {
                print("🔐 [DEBUG] User is fully authenticated and onboarded")
                // Don't close windows - they will show success state
            }
        }
    }
    
    func showLoginWindow() {
        loginWindow = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 500, height: 650),
            styleMask: [.titled, .closable],
            backing: .buffered,
            defer: false
        )
        loginWindow?.title = "Welcome to FlowFacilitator"
        
        guard let appState = appState else {
            print("❌ [ERROR] AppState is nil in showLoginWindow")
            return
        }
        
        loginWindow?.contentView = NSHostingView(rootView: LoginView(appState: appState, onSuccess: {
            print("🔐 [DEBUG] Login onSuccess callback called")
            Task { @MainActor in
                print("🔐 [DEBUG] Login onSuccess - calling checkAuthenticationStatus")
                await self.checkAuthenticationStatus()
                print("🔐 [DEBUG] Login onSuccess - done (not closing login window)")
                // Don't close the login window - just let it stay in background
                // The onboarding window will come to front
            }
        }))
        loginWindow?.center()
        loginWindow?.makeKeyAndOrderFront(nil)
    }
    
    func showOnboardingWindow() {
        onboardingWindow = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 550, height: 650),
            styleMask: [.titled, .closable],
            backing: .buffered,
            defer: false
        )
        onboardingWindow?.title = "Welcome to FlowFacilitator"
        
        guard let appState = appState else {
            print("❌ [ERROR] AppState is nil in showOnboardingWindow")
            return
        }
        
        print("🔐 [DEBUG] Creating OnboardingContainerView...")
        onboardingWindow?.contentView = NSHostingView(rootView: OnboardingContainerView(appState: appState, onComplete: {
            print("🔐 [DEBUG] Onboarding complete - not touching windows")
            // Don't touch the windows at all - this prevents crashes
            // They will be cleaned up when the app quits or user closes them manually
        }))
        print("🔐 [DEBUG] OnboardingContainerView created, showing window...")
        onboardingWindow?.center()
        onboardingWindow?.makeKeyAndOrderFront(nil)
        print("🔐 [DEBUG] Onboarding window shown")
    }
}
