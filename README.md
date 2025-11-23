# FlowFacilitator 🎯

**AI-Powered Flow State Detection & Amplification for macOS**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/shyamolkonwar/flow-state-ai/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
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

👉 **[Full Quick Start Guide](QUICKSTART.md)**

## 📖 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
- [Documentation](#-documentation)
- [Architecture](#-architecture)
- [Development](#-development)
- [Contributing](#-contributing)
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

## 🏗️ Project Status

**Current Phase**: Phase 1 - Requirements Analysis and Design ✅ **COMPLETE**

This project is being built in 8 phases:
1. ✅ Requirements Analysis and Design
2. ⏳ Infrastructure Setup
3. ⏳ Agent Core Development
4. ⏳ Chrome Extension Development
5. ⏳ Dashboard Development
6. ⏳ Integration and Testing
7. ⏳ Packaging and Documentation
8. ⏳ Pilot Testing and Iteration

See [mvp_phases.md](mvp_phases.md) for detailed phase breakdown.

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
- [Database Schema](infra/supabase/migrations/001_initial_schema.sql) - Data model

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User's Mac (Local)                    │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   macOS      │◄────►│   Chrome     │                │
│  │   Agent      │      │  Extension   │                │
│  └──────┬───────┘      └──────────────┘                │
│         │                                                │
│         │              ┌──────────────┐                 │
│         ├─────────────►│  Dashboard   │                 │
│         │              │   (Web UI)   │                 │
│         │              └──────────────┘                 │
│         │                                                │
│         │              ┌──────────────┐                 │
│         └─────────────►│  Supabase    │                 │
│                        │   (Local)    │                 │
│                        └──────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

### Components

- **macOS Agent**: Monitors user behavior, detects flow states, controls protections
- **Chrome Extension**: Blocks distracting websites during flow
- **Dashboard**: Displays analytics and settings (React + Vite)
- **Supabase Local**: PostgreSQL database with realtime capabilities

## 🚀 Quick Start (For Developers)

### Prerequisites
- macOS 12+
- Docker Desktop
- Node.js 18+
- Python 3.10+
- Chrome browser

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/flow-state-ai.git
cd flow-state-ai

# Start local database
cd infra/supabase
docker-compose up -d

# Set up agent
cd ../../agent
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
- **Real-time Updates**: Live data from Supabase visualization of your day
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
- **Database**: Supabase (PostgreSQL + Realtime)
- **Packaging**: macOS app bundle (signed & notarized)

## 📝 License

[To be determined]

## 🤝 Contributing

This project is currently in early development. Contribution guidelines will be added soon.

## 📧 Contact

[To be determined]

## 🙏 Acknowledgments

Built for students and knowledge workers who want to achieve deeper, more sustained focus in an increasingly distracting digital world.

---

**Status**: Phase 1 Complete - Specifications and design finalized
**Next**: Phase 2 - Infrastructure setup and development environment
