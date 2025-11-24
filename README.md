# FlowFacilitator 🎯

**AI-Powered Flow State Detection & Amplification for macOS**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/shyamolkonwar/flow-state-ai/releases)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![macOS](https://img.shields.io/badge/macOS-12.0+-black.svg)](https://www.apple.com/macos/)
[![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)](https://www.python.org/)

> Detect, amplify, and analyze your flow states with privacy-first, local-only tracking.

## 🚀 Quick Start

```bash
git clone https://github.com/shyamolkonwar/flow-state-ai.git
cd flow-state-ai
./scripts/install.sh
```

**Then**: Start the agent, install the Chrome extension, and open the dashboard!

## 📖 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
- [Documentation](#-documentation)
- [Architecture](#-architecture)
- [macOS Swift App Setup](#-macos-swift-app-setup)
- [Supabase Setup](#-supabase-setup)
- [Development](#-development)
- [License](#-license)

## 🎯 What is FlowFacilitator?

FlowFacilitator helps students and knowledge workers achieve and maintain deep focus by:
- **Automatically detecting** when you enter a flow state based on your work patterns
- **Protecting your focus** by enabling Do Not Disturb and blocking distracting websites
- **Tracking your progress** with detailed analytics and insights
- **Building focus stamina** over time through intelligent interventions

## 🔒 Privacy First

- ✅ **100% Local** - All data stays on your Mac
- ✅ **No Content Capture** - We only record timestamps, never what you type
- ✅ **No Cloud Sync** - No external servers, no tracking
- ✅ **Complete Control** - Export or delete your data anytime


## 📚 Documentation

### For Users
- [Onboarding Guide](docs/onboarding.md) - Get started with FlowFacilitator
- [Privacy Policy](docs/privacy.md) - How we handle your data

### For Developers
- [Development Setup](docs/dev-setup.md) - Set up your local environment
- [QA Checklist](docs/qa-checklist.md) - Testing procedures
- [Flow Detection Config](docs/flow-detection-config.md) - How flow detection works

### Technical Specifications
- [Agent Specification](agent/spec.md) - macOS background agent
- [Chrome Extension Specification](chrome-extension/spec.md) - Browser helper
- [Dashboard Specification](dashboard/spec.md) - Web UI
- [Sequence Diagrams](docs/sequence-diagrams.md) - System interactions

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User's Mac (Local)                    │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   macOS      │◄────►│   Chrome     │                │
│  │   Agent      │      │  Extension   │                │
│  └──────┬───────┘      └──────────────┘                │
│         │              ┌──────────────┐                 │
│         ├─────────────►│  Dashboard   │◄─────────────┐ │
│         │              │   (Web UI)   │              │ │
│         │              └──────────────┘              │ │
│         │                                             │ │
│         │              ┌──────────────┐              │ │
│         └─────────────►│  Supabase    │◄─────────────┘ │
│                        │   (Remote)   │                 │
│                        └──────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

### Components

- **macOS Agent**: Monitors user behavior, detects flow states, controls protections
- **Chrome Extension**: Blocks distracting websites during flow
- **Dashboard**: Displays analytics and settings (React + Vite)
- **Supabase**: Remote PostgreSQL database with authentication and real-time features

## 🚀 Quick Start (For Developers)

### Prerequisites
- macOS 12+
- Node.js 18+
- Python 3.10+
- Chrome browser

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/flow-state-ai.git
cd flow-state-ai

# Set up agent
cd agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up dashboard
cd ../dashboard/ui
npm install
npm run dev

# Load Chrome extension
# 1. Open chrome://extensions/
# 2. Enable Developer mode
# 3. Click "Load unpacked"
# 4. Select chrome-extension/ directory
```

See [Development Setup Guide](docs/dev-setup.md) for detailed instructions.

## 🍎 macOS Swift App Setup

FlowFacilitator includes a native macOS menu bar application built with Swift and SwiftUI.

### Prerequisites
- **macOS 12.0+**
- **Xcode 15+** (available from Mac App Store)
- **Swift 5.9+**
- **Python agent** running on `localhost:8765`

### Step 1: Open Xcode Project

```bash
cd FlowFacilitator/FlowFacilitator

# Open the Xcode project
open FlowFacilitator.xcodeproj
```

### Step 2: Configure Project Settings

In Xcode:

1. **Select the project** in the Project Navigator
2. **Select the FlowFacilitator target**
3. **Go to Signing & Capabilities tab**
4. **Enable App Sandbox**
5. **Under App Sandbox**, enable:
   - ✅ **Outgoing Connections (Network Client)**
   - ✅ **Incoming Connections (Network Server)**

### Step 3: Build and Run

```bash
# In Xcode: Product → Run (⌘R)
# Or command line:
xcodebuild -project FlowFacilitator.xcodeproj \
  -scheme FlowFacilitator \
  -configuration Debug \
  build
```

### Step 4: Grant Permissions

After first launch, grant these permissions in **System Preferences → Security & Privacy**:

- **Accessibility** - Required for activity monitoring
- **Input Monitoring** - Required for keyboard/mouse tracking
- **Screen Recording** - Optional, for app usage detection

### Features

- **Menu Bar Icon** - Shows current flow state (Idle/Flow/Tracking/Error)
- **Authentication** - Login/signup with secure Keychain storage
- **Onboarding** - 4-page guided setup process
- **Agent Control** - Start/stop/restart the Python agent
- **Preferences** - Account management and settings
- **Dashboard Access** - Quick link to web dashboard

### Troubleshooting

**App doesn't appear in menu bar:**
- Check that `LSUIElement` is set to `true` in Info.plist

**Permissions not working:**
- Restart the app after granting permissions
- Check System Preferences → Security & Privacy

**Agent communication fails:**
- Ensure Python agent is running on port 8765
- Check firewall settings

## 🗄️ Supabase Setup

FlowFacilitator uses Supabase as the remote database for user authentication, session tracking, and analytics.

### Database Schema

The database includes the following tables:
- **all_users**: User profiles with onboarding status
- **sessions**: Flow session tracking with metrics
- **events**: User activity events
- **settings**: User preferences and configurations
- **agent_logs**: Application logging

### Supabase Configuration

The Supabase URL and keys are configured through environment variables.

### Environment Variables

For the dashboard, copy `dashboard/ui/.env.example` to `dashboard/ui/.env` and update with your Supabase credentials:

```bash
cp dashboard/ui/.env.example dashboard/ui/.env
```

Then update the `.env` file with your actual Supabase URL and anon key:

```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
VITE_AGENT_API_URL=http://localhost:8765
VITE_AGENT_API_TOKEN=local_dev_token_12345
```

### Database Features

- **Row Level Security (RLS)**: Ensures users can only access their own data
- **Real-time subscriptions**: Live updates for dashboard analytics
- **Authentication**: Secure user signup/login with JWT tokens
- **Functions**: Server-side functions for complex operations
- **Indexes**: Optimized queries for performance

### Migration

The database schema is defined in `supabase/migrations/20251123100727_remote_schema.sql` and includes:
- User management functions
- Session tracking functions
- Settings management
- Event logging
- Automatic triggers for user creation

## ✨ Key Features

### Core Flow Detection
- **Real-time Monitoring**: Tracks typing rate, app switches, and idle time
- **Configurable Thresholds**: Customize entry/exit criteria for flow states
- **Privacy-First**: Only timestamps recorded, no keystroke content

### Enhanced Protection Mechanisms
- **Overlay Blocking**: Full-screen overlay instead of killing processes
  - 10-second countdown before unlock
  - Motivational messaging
  - Resilience tracking for resisting distractions
- **Do Not Disturb**: Automatic macOS DND toggle
- **Smart Blocklist**: Configurable domain and app blocking

### Micro-Interventions
- **Cognitive Fatigue Detection**: Identifies erratic typing, increasing idle gaps
- **Soft Resets**: 
  - Blur effect overlay
  - Linear audio fade (no abrupt stops)
  - Gentle 30-second break
- **No Color Temperature Changes**: Respects user preferences

### RPG Gamification System
- **Stamina**: Total flow time tracking
- **Resilience**: Points for resisting distractions
- **Consistency**: Daily streak system
- **Level & XP**: Gain experience from sessions and resistance
- **Progressive Overload**: AI-adjusted goals (5% increase)
- **Achievements**: Unlock badges for milestones
- **Resilience Ranks**: Bronze → Silver → Gold → Platinum → Diamond

### Analytics Dashboard
- **Today's Summary**: Flow time, sessions, averages
- **Session History**: Complete timeline with metrics
- **RPG Stats Page**: Level, XP, achievements, progressive goals
- **Settings**: Configure thresholds and blocklist
- **Real-time Updates**: Live data visualization of your day
- Long-term trends and insights
- Export data as CSV

### User Control
- Pause protection temporarily
- Quick whitelist for urgent access
- Adjust detection sensitivity
- Complete data deletion

## 🎨 Features

### Automatic Flow Detection
- Monitors typing cadence, app focus, and idle time
- Enters flow mode when all criteria met for 5 minutes
- Configurable thresholds (Relaxed/Balanced/Strict)

### Smart Protection
- Enables macOS Do Not Disturb automatically
- Blocks distracting websites in Chrome
- Customizable blocklist and whitelist

### Analytics Dashboard
- View all flow sessions with detailed metrics
- Timeline visualization of your day
- Long-term trends and insights
- Export data as CSV

### User Control
- Pause protection temporarily
- Quick whitelist for urgent access
- Adjust detection sensitivity
- Complete data deletion

## 📊 How It Works

### Flow Entry Criteria (Default)
All conditions must be met for 5 minutes:
- Typing rate ≥ 40 keystrokes/minute
- App switches ≤ 2
- Maximum idle gap ≤ 4 seconds

### Flow Exit Criteria
Any condition persisting for 30 seconds:
- Typing rate < 30 keystrokes/minute
- App switches > 2
- Idle gap > 6 seconds

See [Flow Detection Config](docs/flow-detection-config.md) for details.

## 🛠️ Tech Stack

- **Agent**: Python (macOS Accessibility APIs)
- **Extension**: JavaScript (Chrome Manifest v3)
- **Dashboard**: React + Vite
- **Database**: Supabase (PostgreSQL + Real-time)
- **Packaging**: macOS app bundle (signed & notarized)

## 📝 License

This software is proprietary and all rights are reserved by Shyamol Konwar. No part of this software may be reproduced, distributed, or transmitted in any form or by any means without prior written permission from Shyamol Konwar.

For licensing inquiries, please contact Shyamol Konwar.



## 📧 Contact

Email: shyamol@fusionfocus.in  
Website: https://fusionfocus.in

## 🙏 Acknowledgments

Built for students and knowledge workers who want to achieve deeper, more sustained focus in an increasingly distracting digital world.

---
