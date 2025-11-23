import SwiftUI

struct SimpleOnboardingView: View {
    @ObservedObject var appState: AppState
    let onComplete: () -> Void
    
    var body: some View {
        VStack(spacing: 32) {
            Text("Welcome to FlowFacilitator")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Let's get you set up")
                .font(.title3)
            
            Spacer()
            
            Button("Complete Setup") {
                Task {
                    await appState.completeOnboarding()
                    await MainActor.run {
                        onComplete()
                    }
                }
            }
            .padding(.horizontal, 24)
            .padding(.vertical, 12)
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)
        }
        .padding(40)
        .frame(width: 550, height: 650)
        .background(Color(white: 0.1))
    }
}
