# FlowFacilitator - Swift/SwiftUI Mac App

A native macOS menu bar application for FlowFacilitator with Supabase authentication, onboarding, and agent integration.

---

## ✨ Features

- **Native macOS Experience** - Built with Swift and SwiftUI
- **Supabase Authentication** - Secure login/signup with cloud sync
- **Onboarding Flow** - 4-page guided setup
- **Menu Bar Integration** - Status indicators and quick access
- **Preferences Window** - Account management and settings
- **Keychain Storage** - Secure credential storage
- **Agent Communication** - HTTP API integration with Python agent

---

## 📁 Project Structure

```
FlowFacilitator/
├── FlowFacilitatorApp.swift          # Main app + menu bar
├── Models/
│   ├── AppState.swift                # App state management
│   ├── User.swift                    # User models
│   └── AgentStatus.swift             # Agent status
├── Services/
│   ├── SupabaseService.swift         # Supabase auth + API
│   ├── KeychainService.swift         # Secure storage
│   └── AgentAPIService.swift         # Python agent API
├── Views/
│   ├── Auth/
│   │   └── LoginView.swift           # Login/signup
│   ├── Onboarding/
│   │   └── OnboardingContainerView.swift  # 4-page flow
│   └── Main/
│       └── PreferencesView.swift     # Preferences
└── Utilities/
    ├── Colors.swift                  # Color palette
    └── PermissionChecker.swift       # macOS permissions
```

---

## 🚀 Getting Started

### Prerequisites

- **Xcode 15+** (macOS Sonoma or later)
- **Swift 5.9+**
- **Python agent** running on `localhost:8765`
- **Supabase** project with migrations applied

### Step 1: Create Xcode Project

```bash
cd /Users/shyamolkonwar/Documents/flow-state-ai/FlowFacilitator/FlowFacilitator

# Open Xcode
open -a Xcode
```

In Xcode:
1. **File → New → Project**
2. Select **macOS → App**
3. Product Name: `FlowFacilitator`
4. Interface: **SwiftUI**
5. Language: **Swift**
6. Save to: `/Users/shyamolkonwar/Documents/flow-state-ai/FlowFacilitator/FlowFacilitator`

### Step 2: Add Files to Project

1. In Xcode, right-click on `FlowFacilitator` folder
2. Select **Add Files to "FlowFacilitator"...**
3. Navigate to the `FlowFacilitator/` directory
4. Select all `.swift` files
5. Ensure **"Copy items if needed"** is checked
6. Click **Add**

### Step 3: Configure Project Settings

#### Info.plist

Add these keys:

```xml
<key>LSUIElement</key>
<true/>
<key>NSAppleEventsUsageDescription</key>
<string>FlowFacilitator needs to control System Preferences.</string>
```

#### Signing & Capabilities

1. Select project in navigator
2. Select **FlowFacilitator** target
3. Go to **Signing & Capabilities**
4. Enable **App Sandbox**
5. Under **App Sandbox**, enable:
   - ✅ Outgoing Connections (Network Client)
   - ✅ Incoming Connections (Network Server)

### Step 4: Build and Run

```bash
# Command line build
xcodebuild -project FlowFacilitator.xcodeproj \
  -scheme FlowFacilitator \
  -configuration Debug \
  build

# Or in Xcode: Product → Run (⌘R)
```

---

## 🔧 Configuration

### Supabase Credentials

Update in `SupabaseService.swift`:

```swift
private let supabaseURL = "https://your-project.supabase.co"
private let supabaseAnonKey = "your-anon-key"
```

### Agent API Endpoint

Update in `AgentAPIService.swift`:

```swift
private let baseURL = "http://localhost:8765"
```

---

## 📱 User Flow

### First Launch

```
1. App launches → Menu bar icon appears
2. Login window opens automatically
3. User signs up or logs in
4. Credentials saved to Keychain
5. Onboarding window appears (4 pages)
6. User completes onboarding
7. Onboarding synced to Supabase
8. Main app ready (menu bar only)
```

### Returning User

```
1. App launches → Menu bar icon appears
2. Session restored from Keychain
3. Auto-login successful
4. Check onboarding status
5. If complete → Main app ready
6. If not complete → Show onboarding
```

---

## 🎨 UI Components

### Colors (Premium Palette)

- **Deep Night**: `#0B0710` - Background
- **Surface Light**: `#0F1220` - Cards
- **Surface Elevated**: `#141722` - Inputs
- **Text on Dark**: `#EDEFF6` - Primary text
- **Text Secondary**: `#9CA3AF` - Secondary text
- **Teal**: `#2FE6C1` - Primary actions
- **Cyan**: `#00D9FF` - Accents
- **Magenta**: `#FF6EC7` - Errors/warnings
- **Gold**: `#FFD700` - Highlights

### Gradients

- **Teal to Cyan** - Primary gradient
- **Magenta to Cyan** - Accent gradient

---

## 🔌 API Integration

### Python Agent Endpoints

**Get Status:**
```swift
GET http://localhost:8765/status

Response:
{
  "agent_running": true,
  "flow_state": "idle|tracking|flow",
  "permissions": {
    "accessibility": true,
    "input_monitoring": false,
    "screen_recording": false
  }
}
```

**Start Agent:**
```swift
POST http://localhost:8765/start
```

**Stop Agent:**
```swift
POST http://localhost:8765/stop
```

### Supabase RPC Functions

- `get_user_profile()` - Get user profile
- `complete_onboarding()` - Mark onboarding complete
- `update_user_permissions(p_permissions)` - Update permissions

---

## 🔒 Security

### Keychain Storage

Credentials are stored securely in macOS Keychain:
- Access Token
- Refresh Token
- Expiration Date

### Permissions Required

- **Accessibility** - Monitor user activity
- **Input Monitoring** - Track keyboard/mouse
- **Screen Recording** - Capture app usage (optional)

---

## 🏗️ Building for Distribution

### Create App Bundle

```bash
xcodebuild -project FlowFacilitator.xcodeproj \
  -scheme FlowFacilitator \
  -configuration Release \
  -archivePath FlowFacilitator.xcarchive \
  archive

xcodebuild -exportArchive \
  -archivePath FlowFacilitator.xcarchive \
  -exportPath ./build \
  -exportOptionsPlist ExportOptions.plist
```

### Code Signing

1. Get Apple Developer account
2. Create App ID
3. Create provisioning profile
4. Sign app in Xcode

### Create DMG Installer

```bash
create-dmg \
  --volname "FlowFacilitator" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "FlowFacilitator.app" 200 190 \
  --hide-extension "FlowFacilitator.app" \
  --app-drop-link 600 185 \
  "FlowFacilitator.dmg" \
  "build/FlowFacilitator.app"
```

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Launch app → Menu bar icon appears
- [ ] Login window appears for new user
- [ ] Sign up with new account
- [ ] Credentials saved to Keychain
- [ ] Onboarding appears after signup
- [ ] Complete all 4 onboarding pages
- [ ] Onboarding synced to Supabase
- [ ] Menu bar menu displays correctly
- [ ] Agent status updates every 3 seconds
- [ ] Permissions status accurate
- [ ] Start/stop agent works
- [ ] Preferences window opens
- [ ] Logout works
- [ ] Session restored on relaunch

---

## 📝 Next Steps

### Immediate
1. Create Xcode project
2. Add all Swift files
3. Configure project settings
4. Build and test

### Future Enhancements
1. OAuth providers (Google, GitHub, Apple)
2. Notifications for flow state changes
3. Widgets for Today view
4. Shortcuts integration
5. Auto-updater (Sparkle)
6. Analytics dashboard
7. Multi-device sync status

---

## 🐛 Troubleshooting

### App doesn't appear in menu bar

Check `Info.plist` has `LSUIElement` set to `true`.

### Login fails

1. Check Supabase URL and anon key
2. Verify migrations are applied
3. Check network connectivity

### Permissions not detected

1. Grant permissions in System Preferences
2. Restart app after granting permissions
3. Check `PermissionChecker` implementation

### Agent API fails

1. Ensure Python agent is running on port 8765
2. Check firewall settings
3. Verify API endpoints

---

## 📄 License

Copyright (c) 2025 Shyamol Konwar. All rights reserved.

This software and associated documentation files (the "Software") are proprietary and confidential. No part of the Software may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of Shyamol Konwar.

The Software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall Shyamol Konwar be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

For licensing inquiries, please contact Shyamol Konwar.