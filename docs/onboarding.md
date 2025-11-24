# Onboarding Guide - FlowFacilitator

## Welcome to FlowFacilitator! 🎯

FlowFacilitator helps you achieve and maintain deep focus by automatically detecting when you enter a flow state and protecting it from distractions.

## First-Time Setup

### Step 1: Install the Application

1. Download `FlowFacilitator.dmg`
2. Open the DMG file
3. Drag FlowFacilitator to your Applications folder
4. Eject the DMG

### Step 2: Launch FlowFacilitator

1. Open Applications folder
2. Double-click FlowFacilitator
3. If you see a security warning:
   - Click "Cancel"
   - Go to System Settings → Privacy & Security
   - Scroll down and click "Open Anyway"
   - Click "Open" in the confirmation dialog

### Step 3: Grant Accessibility Permission

**Why we need this**: To measure your typing rhythm and detect which app you're using - this helps us know when you're in flow.

**What we DON'T do**: We never record what you type, only when you type.

#### How to Grant Permission:

1. When prompted, click "Open System Settings"
2. You'll see System Settings → Privacy & Security → Accessibility
3. Click the lock icon 🔒 to make changes
4. Enter your Mac password
5. Find "FlowFacilitator" in the list
6. Toggle it ON ✅
7. Click the lock icon again to prevent further changes
8. Return to FlowFacilitator and click "Retry"

**Visual Guide**:

```
System Settings
  └─ Privacy & Security
      └─ Accessibility
          └─ [✅] FlowFacilitator
```

### Step 4: Start Local Database

FlowFacilitator stores all data locally on your Mac (nothing goes to the cloud).

1. Click "Start Local Database" in the setup window
2. If prompted, allow Docker to run (or install Docker Desktop if needed)
3. Wait for the green checkmark ✅

**Alternative**: If you prefer to start manually:
```bash
cd ~/Library/Application\ Support/FlowFacilitator
./scripts/start-local.sh
```

### Step 5: Install Chrome Extension (Optional but Recommended)

The Chrome extension blocks distracting websites during flow.

1. Click "Install Chrome Helper" in the setup window
2. Chrome Web Store will open
3. Click "Add to Chrome"
4. Click "Add Extension"
5. The extension icon will appear in your toolbar

**For Development/Testing**:
1. Open Chrome
2. Go to `chrome://extensions/`
3. Enable "Developer mode" (top right)
4. Click "Load unpacked"
5. Navigate to FlowFacilitator extension folder
6. Click "Select"

### Step 6: Configure Your Preferences

1. Click "Open Dashboard" from the menu bar icon
2. Go to Settings
3. Customize:
   - **Flow Detection**: Adjust sensitivity (Relaxed/Balanced/Strict)
   - **Blocklist**: Add websites to block during flow
   - **Whitelist**: Add sites that should never be blocked

**Recommended Starting Settings**: Use "Balanced" preset

## Understanding the Menu Bar

The FlowFacilitator icon in your menu bar shows your current state:

- 🔴 **Gray**: Idle - no significant activity
- 🟡 **Yellow**: Working - activity detected, not yet in flow
- 🟢 **Green**: In Flow - deep focus mode active
- ⏸️ **Blue**: Paused - protection temporarily disabled

### Menu Options

```
┌─────────────────────────────┐
│ ● FlowFacilitator          │
│ Status: In Flow             │
├─────────────────────────────┤
│ Open Dashboard              │ ← View your analytics
│ Pause Protection (10 min)   │ ← Temporarily disable blocking
│ Quick Whitelist...          │ ← Add a site to whitelist
├─────────────────────────────┤
│ Preferences                 │ ← Open settings
│ Quit                        │ ← Exit app
└─────────────────────────────┘
```

## How It Works

### Automatic Flow Detection

FlowFacilitator watches for these signals:

1. **Steady Typing**: You're typing consistently (40+ keystrokes/min)
2. **Focus**: You stay in one app (≤2 app switches per 5 minutes)
3. **Engagement**: No long idle periods (≤4 seconds max gap)

When all three conditions are met for **5 minutes**, you enter Flow Mode.

### What Happens in Flow Mode

✅ **Do Not Disturb** is automatically enabled
✅ **Distracting websites** are blocked in Chrome
✅ **Session tracking** begins
✅ **Menu icon** turns green

### Exiting Flow Mode

You'll exit flow when:
- Typing slows down significantly
- You switch apps frequently
- You go idle for more than 6 seconds

When you exit:
- Do Not Disturb is disabled
- Website blocking is removed
- Session is saved with analytics

## Using the Dashboard

### Viewing Your Progress

1. Click the menu bar icon
2. Select "Open Dashboard"
3. Dashboard opens at `http://localhost:3000`

### Dashboard Sections

#### Home
- Today's total flow time
- Number of sessions
- Longest session
- Current streak

#### Sessions
- Complete history of all flow sessions
- Filter by date, app, or duration
- Click any session for detailed analysis

#### Timeline
- Visual representation of your day
- See when you were most productive
- Identify patterns

#### Analytics
- Long-term trends
- Best times for flow
- Most productive apps
- Improvement over time

#### Settings
- Adjust detection thresholds
- Manage blocklist/whitelist
- Export or delete data
- Configure retention policy

## Tips for Success

### 1. Start with Default Settings
Don't customize too much initially. Use the app for a few days to understand your natural flow patterns.

### 2. Review Your Analytics
Check the dashboard weekly to identify:
- Your most productive hours
- Which apps help you focus
- When you get distracted most

### 3. Customize Gradually
After a week, adjust thresholds based on your patterns:
- **Too many false positives?** → Switch to "Strict" mode
- **Not detecting flow?** → Switch to "Relaxed" mode

### 4. Use Quick Whitelist
If you need to access a blocked site during flow:
1. Click menu bar icon
2. Select "Quick Whitelist"
3. Enter the domain
4. It's immediately accessible

### 5. Pause When Needed
Need a break or to check something?
- Click "Pause Protection (10 min)"
- Blocking is temporarily disabled
- Resumes automatically after 10 minutes

## Troubleshooting

### "Permission Denied" Error

**Solution**:
1. Go to System Settings → Privacy & Security → Accessibility
2. Remove FlowFacilitator from the list (click -, enter password)
3. Re-add it (click +, select FlowFacilitator, enter password)
4. Restart FlowFacilitator

### Chrome Extension Not Working

**Solution**:
1. Open Chrome
2. Go to `chrome://extensions/`
3. Find "FlowFacilitator Helper"
4. Ensure it's enabled (toggle should be blue)
5. Click "Details" → "Extension options"
6. Verify connection status

### Database Won't Start

**Solution**:
1. Ensure Docker is installed and running
2. Open Terminal
3. Run: `docker ps` to check if containers are running
4. If not, run: `cd ~/Library/Application\ Support/FlowFacilitator && ./scripts/start-local.sh`

### Flow Not Detected

**Possible causes**:
- Thresholds too strict → Try "Relaxed" mode
- Not enough continuous activity → Work for at least 5 minutes without switching apps
- Accessibility permission not granted → Check System Settings

### Dashboard Won't Open

**Solution**:
1. Check if agent is running (menu bar icon should be visible)
2. Try manually opening: `http://localhost:3000`
3. Check logs: `~/Library/Application Support/FlowFacilitator/logs/agent.log`

## Privacy Reminder

🔒 **All your data stays on your Mac**
- No cloud sync
- No external servers
- No tracking
- Complete control

See [Privacy Policy](privacy.md) for details.

## Getting Help

### Check Documentation
- [Flow Detection Config](flow-detection-config.md)
- [Agent Specification](../agent/spec.md)
- [Privacy Policy](privacy.md)

### Common Questions

**Q: Can I use this without the Chrome extension?**
A: Yes! Flow detection works independently. You just won't have website blocking.

**Q: Does this work with other browsers?**
A: Currently Chrome only. Firefox and Safari support planned.

**Q: Can I use this on multiple Macs?**
A: Yes, but data doesn't sync between them (local-only storage).

**Q: Will this slow down my Mac?**
A: No. FlowFacilitator uses <3% CPU and <150MB RAM on average.

**Q: Can I export my data?**
A: Yes! Dashboard → Settings → Export Data (CSV or JSON).

## Next Steps

1. ✅ Complete setup (you're done!)
2. 📊 Use FlowFacilitator for a week
3. 📈 Review your analytics
4. ⚙️ Customize settings based on your patterns
5. 🎯 Achieve deeper, longer flow states!

---

**Need Help?** Check the logs or create an issue on GitHub.

**Enjoying FlowFacilitator?** Share it with fellow deep workers!

## License

This software is proprietary and all rights are reserved by Shyamol Konwar. No part of the software may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of Shyamol Konwar.

The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall Shyamol Konwar be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

For licensing inquiries, please contact Shyamol Konwar.

## Contact

Email: shyamol@fusionfocus.in
Website: https://fusionfocus.in

## Acknowledgments

Built for students and knowledge workers who want to achieve deeper, more sustained focus in an increasingly distracting digital world.

---

**No contributions needed. This software is fully licensed and proprietary.**
