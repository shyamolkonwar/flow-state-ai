import SwiftUI

// Minimal test view to isolate the crash
struct MinimalOnboardingView: View {
    @ObservedObject var appState: AppState
    let onComplete: () -> Void
    
    var body: some View {
        VStack {
            Text("Minimal Onboarding Test")
                .foregroundColor(.white)
            
            Button("Complete") {
                onComplete()
            }
        }
        .frame(width: 550, height: 650)
        .background(Color.black)
    }
}
