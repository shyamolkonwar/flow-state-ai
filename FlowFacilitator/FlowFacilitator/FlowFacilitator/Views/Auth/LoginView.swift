import SwiftUI

struct LoginView: View {
    @ObservedObject var appState: AppState
    let onSuccess: () -> Void
    
    @State private var isSignUp = false
    @State private var email = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var fullName = ""
    @State private var errorMessage = ""
    @State private var isLoading = false
    @State private var successMessage = ""
    
    var body: some View {
        ZStack {
            Colors.deepNight.ignoresSafeArea()
            
            VStack(spacing: 24) {
                // Logo
                Circle()
                    .fill(Colors.tealToCyan)
                    .frame(width: 80, height: 80)
                    .overlay(
                        Image(systemName: "waveform.path.ecg")
                            .font(.system(size: 40))
                            .foregroundColor(.white)
                    )
                
                // Tab Switcher
                HStack(spacing: 0) {
                    Button(action: { isSignUp = false }) {
                        Text("Login")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(isSignUp ? Colors.surfaceElev : Colors.teal)
                            .foregroundColor(isSignUp ? Colors.textSecondary : Colors.deepNight)
                    }
                    .buttonStyle(.plain)
                    
                    Button(action: { isSignUp = true }) {
                        Text("Sign Up")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(isSignUp ? Colors.teal : Colors.surfaceElev)
                            .foregroundColor(isSignUp ? Colors.deepNight : Colors.textSecondary)
                    }
                    .buttonStyle(.plain)
                }
                .cornerRadius(8)
                
                // Form
                if isSignUp {
                    signUpForm
                } else {
                    loginForm
                }
                
                // Error Message
                if !errorMessage.isEmpty {
                    Text(errorMessage)
                        .foregroundColor(Colors.magenta)
                        .padding()
                        .background(Colors.surfaceElev)
                        .cornerRadius(6)
                }
                
                // Success Message
                if !successMessage.isEmpty {
                    Text(successMessage)
                        .foregroundColor(Colors.teal)
                        .padding()
                        .background(Colors.surfaceElev)
                        .cornerRadius(6)
                }
                
                Spacer()
            }
            .padding(40)
        }
        .frame(width: 500, height: 650)
    }
    
    var loginForm: some View {
        VStack(spacing: 16) {
            VStack(alignment: .leading, spacing: 8) {
                Text("Email")
                    .foregroundColor(Colors.textOnDark)
                TextField("your@email.com", text: $email)
                    .textFieldStyle(PremiumTextFieldStyle())
            }
            
            VStack(alignment: .leading, spacing: 8) {
                Text("Password")
                    .foregroundColor(Colors.textOnDark)
                SecureField("••••••••", text: $password)
                    .textFieldStyle(PremiumTextFieldStyle())
            }
            
            Button(action: handleLogin) {
                Text(isLoading ? "Logging in..." : "Login")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Colors.teal)
                    .foregroundColor(Colors.deepNight)
                    .cornerRadius(8)
            }
            .buttonStyle(.plain)
            .disabled(isLoading)
        }
    }
    
    var signUpForm: some View {
        VStack(spacing: 16) {
            VStack(alignment: .leading, spacing: 8) {
                Text("Full Name")
                    .foregroundColor(Colors.textOnDark)
                TextField("John Doe", text: $fullName)
                    .textFieldStyle(PremiumTextFieldStyle())
            }
            
            VStack(alignment: .leading, spacing: 8) {
                Text("Email")
                    .foregroundColor(Colors.textOnDark)
                TextField("your@email.com", text: $email)
                    .textFieldStyle(PremiumTextFieldStyle())
            }
            
            VStack(alignment: .leading, spacing: 8) {
                Text("Password")
                    .foregroundColor(Colors.textOnDark)
                SecureField("••••••••", text: $password)
                    .textFieldStyle(PremiumTextFieldStyle())
            }
            
            VStack(alignment: .leading, spacing: 8) {
                Text("Confirm Password")
                    .foregroundColor(Colors.textOnDark)
                SecureField("••••••••", text: $confirmPassword)
                    .textFieldStyle(PremiumTextFieldStyle())
            }
            
            Button(action: handleSignUp) {
                Text(isLoading ? "Creating account..." : "Create Account")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Colors.teal)
                    .foregroundColor(Colors.deepNight)
                    .cornerRadius(8)
            }
            .buttonStyle(.plain)
            .disabled(isLoading)
        }
    }
    
    func handleLogin() {
        guard !email.isEmpty, !password.isEmpty else {
            errorMessage = "Please enter email and password"
            return
        }

        isLoading = true
        errorMessage = ""
        successMessage = ""

        Task {
            do {
                print("🔐 [DEBUG] LoginView: Starting sign in")
                try await appState.signIn(email: email, password: password)
                print("🔐 [DEBUG] LoginView: Sign in successful, calling onSuccess")
                await MainActor.run {
                    if appState.onboardingComplete {
                        // User is already onboarded - show success message
                        successMessage = "✓ Successfully logged in! Onboarding already completed."
                        isLoading = false
                    } else {
                        // User needs onboarding
                        onSuccess()
                    }
                }
            } catch {
                print("🔐 [DEBUG] LoginView: Sign in failed with error: \(error)")
                await MainActor.run {
                    errorMessage = "Login failed: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }
    }
    
    func handleSignUp() {
        guard !email.isEmpty, !password.isEmpty, !fullName.isEmpty else {
            errorMessage = "Please fill in all fields"
            return
        }
        
        guard password == confirmPassword else {
            errorMessage = "Passwords do not match"
            return
        }
        
        isLoading = true
        errorMessage = ""
        
        Task {
            do {
                try await appState.signUp(email: email, password: password, fullName: fullName)
                await MainActor.run {
                    onSuccess()
                }
            } catch {
                await MainActor.run {
                    errorMessage = "Sign up failed: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }
    }
}

struct PremiumTextFieldStyle: TextFieldStyle {
    func _body(configuration: TextField<Self._Label>) -> some View {
        configuration
            .padding()
            .background(Colors.surfaceElev)
            .cornerRadius(8)
            .foregroundColor(Colors.textOnDark)
    }
}
