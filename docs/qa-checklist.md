# QA Checklist - FlowFacilitator MVP

## Acceptance Tests (Manual)

### Test A: Flow Entry
**Objective**: Verify that flow state is detected and protections are activated

**Prerequisites**:
- Agent running with Accessibility permission granted
- Chrome extension installed and connected
- Default settings (Balanced mode)

**Steps**:
1. Open a text editor or IDE
2. Type continuously at ~45 keystrokes per minute
3. Stay in the same application (no switching)
4. Continue for 5 minutes without idle gaps >4 seconds

**Expected Results**:
- ✅ After 5 minutes, menu bar icon turns green
- ✅ macOS Do Not Disturb is enabled
- ✅ Chrome extension blocks configured domains
- ✅ New session appears in dashboard
- ✅ Dashboard shows "In Flow" status

**Pass Criteria**: All expected results occur within 10 seconds of 5-minute mark

---

### Test B: Flow Exit by App Switching
**Objective**: Verify that flow state exits when user switches apps frequently

**Prerequisites**:
- Currently in flow state (green icon)

**Steps**:
1. Switch between 4 different applications within 30 seconds
2. Wait 30 seconds

**Expected Results**:
- ✅ Menu bar icon changes from green to yellow/gray
- ✅ Do Not Disturb is disabled
- ✅ Chrome extension stops blocking
- ✅ Session is closed in database
- ✅ Dashboard shows session ended with reason "app_switches"

**Pass Criteria**: Flow exits within 30-40 seconds of excessive switching

---

### Test C: Flow Exit by Idle
**Objective**: Verify that flow state exits when user goes idle

**Prerequisites**:
- Currently in flow state (green icon)

**Steps**:
1. Stop all keyboard and mouse activity
2. Wait 10 seconds without any input
3. Observe system response

**Expected Results**:
- ✅ Menu bar icon changes from green to yellow/gray within 30 seconds
- ✅ Do Not Disturb is disabled
- ✅ Chrome extension stops blocking
- ✅ Session is closed with reason "idle"
- ✅ Dashboard shows session ended

**Pass Criteria**: Flow exits within 30-40 seconds of idle period

---

### Test D: Whitelist Functionality
**Objective**: Verify that whitelisted sites are not blocked during flow

**Prerequisites**:
- Agent running
- Chrome extension installed

**Steps**:
1. Open dashboard → Settings
2. Add "example.com" to whitelist
3. Click Save
4. Enter flow state (follow Test A steps)
5. In Chrome, navigate to example.com

**Expected Results**:
- ✅ example.com loads normally (not blocked)
- ✅ Other blocklist domains still blocked
- ✅ Flow state remains active

**Pass Criteria**: Whitelisted site accessible, others blocked

---

### Test E: Permission Denied Handling
**Objective**: Verify graceful handling when Accessibility permission is denied

**Prerequisites**:
- Fresh install or permission revoked

**Steps**:
1. Launch FlowFacilitator
2. When prompted for Accessibility permission, click "Deny" or "Don't Allow"

**Expected Results**:
- ✅ App does not crash
- ✅ Onboarding overlay appears with instructions
- ✅ "Retry" button is visible
- ✅ Menu bar shows warning icon or disabled state
- ✅ Clicking "Retry" re-checks permission

**Pass Criteria**: App remains functional and guides user to grant permission

---

### Test F: Database Offline Recovery
**Objective**: Verify event buffering when database is unavailable

**Prerequisites**:
- Agent running normally
- Supabase local running

**Steps**:
1. Stop Supabase: `docker stop $(docker ps -q --filter ancestor=supabase/postgres)`
2. Generate some activity (typing, app switches)
3. Check menu bar - should show "DB offline" warning
4. Restart Supabase: `cd ~/Library/Application\ Support/FlowFacilitator && ./scripts/start-local.sh`
5. Wait 60 seconds

**Expected Results**:
- ✅ Agent continues running when DB stops
- ✅ Menu shows offline warning
- ✅ Events are buffered locally
- ✅ When DB reconnects, buffered events are written
- ✅ No data loss

**Pass Criteria**: All buffered events appear in database after recovery

---

### Test G: Chrome Extension Communication
**Objective**: Verify native messaging between agent and extension

**Prerequisites**:
- Agent running
- Extension installed

**Steps**:
1. Open Chrome DevTools → Extensions → FlowFacilitator Helper → Background page
2. Check console for connection status
3. Enter flow state
4. Observe console messages

**Expected Results**:
- ✅ Console shows "Connected to native host"
- ✅ When flow starts, receives `enable_blocking` message
- ✅ Blocking rules are applied
- ✅ When flow ends, receives `disable_blocking` message

**Pass Criteria**: All messages sent and received correctly

---

### Test H: Dashboard Real-time Updates
**Objective**: Verify dashboard updates in real-time as sessions occur

**Prerequisites**:
- Dashboard open in browser
- Agent running

**Steps**:
1. Open dashboard at http://localhost:3000
2. Keep dashboard visible
3. In another window, enter flow state (Test A)
4. Observe dashboard without refreshing

**Expected Results**:
- ✅ Dashboard shows "In Flow" status automatically
- ✅ New session appears in session list
- ✅ Today's metrics update (total time, session count)
- ✅ When flow ends, session updates with final duration

**Pass Criteria**: All updates occur without manual refresh

---

### Test I: Settings Persistence
**Objective**: Verify settings are saved and applied across restarts

**Steps**:
1. Open dashboard → Settings
2. Change typing rate threshold to 50 kpm
3. Add "github.com" to blocklist
4. Click Save
5. Quit FlowFacilitator completely
6. Restart FlowFacilitator
7. Open dashboard → Settings

**Expected Results**:
- ✅ Typing rate shows 50 kpm
- ✅ Blocklist includes "github.com"
- ✅ Settings are applied (flow detection uses new threshold)

**Pass Criteria**: All settings persist across restart

---

### Test J: Data Export
**Objective**: Verify CSV export functionality

**Steps**:
1. Ensure you have at least 2 completed sessions
2. Open dashboard → Settings
3. Click "Export Data"
4. Select date range (last 7 days)
5. Click "Download CSV"

**Expected Results**:
- ✅ CSV file downloads
- ✅ File contains session data with headers
- ✅ Data matches what's shown in dashboard
- ✅ Timestamps are readable

**Pass Criteria**: Valid CSV with correct data

---

## Performance Tests

### Test P1: CPU Usage
**Objective**: Verify agent has minimal CPU impact

**Steps**:
1. Start agent
2. Open Activity Monitor
3. Find FlowFacilitator process
4. Monitor CPU usage for 5 minutes during normal work

**Expected Results**:
- ✅ Average CPU usage < 3%
- ✅ Peak CPU usage < 10%
- ✅ No sustained high CPU periods

**Pass Criteria**: Meets CPU targets

---

### Test P2: Memory Usage
**Objective**: Verify reasonable memory footprint

**Steps**:
1. Start agent
2. Open Activity Monitor
3. Monitor memory usage over 30 minutes

**Expected Results**:
- ✅ Memory usage < 150MB
- ✅ No significant memory leaks (steady or slowly growing)

**Pass Criteria**: Memory stays under 150MB

---

### Test P3: Event Processing Latency
**Objective**: Verify quick event processing

**Steps**:
1. Enable debug logging
2. Generate rapid keyboard input
3. Check logs for event timestamps

**Expected Results**:
- ✅ Events processed within 100ms of occurrence
- ✅ No event queue backlog

**Pass Criteria**: <100ms latency

---

## Security Tests

### Test S1: Local-Only Database
**Objective**: Verify database is not exposed externally

**Steps**:
1. Start Supabase local
2. Run: `lsof -i -P | grep postgres`
3. Check listening addresses

**Expected Results**:
- ✅ Postgres only listening on 127.0.0.1 (localhost)
- ✅ Not listening on 0.0.0.0 or external IP

**Pass Criteria**: Localhost binding only

---

### Test S2: File Permissions
**Objective**: Verify data files are user-only

**Steps**:
1. Run: `ls -la ~/Library/Application\ Support/FlowFacilitator/`
2. Check permissions on config.json and database files

**Expected Results**:
- ✅ Files owned by current user
- ✅ Permissions are 600 (rw-------)
- ✅ No world-readable files

**Pass Criteria**: Secure file permissions

---

### Test S3: No External Network Requests
**Objective**: Verify no data sent externally

**Steps**:
1. Start agent
2. Run: `sudo tcpdump -i any -n 'not host 127.0.0.1'`
3. Use app normally for 5 minutes

**Expected Results**:
- ✅ No HTTP/HTTPS requests to external servers
- ✅ Only localhost traffic visible

**Pass Criteria**: Zero external network activity

---

## Compatibility Tests

### Test C1: macOS Version Compatibility
**Objective**: Verify app works on supported macOS versions

**Test on**:
- macOS 12 (Monterey)
- macOS 13 (Ventura)
- macOS 14 (Sonoma)

**Expected Results**:
- ✅ App launches successfully
- ✅ Accessibility permission flow works
- ✅ DND toggle works
- ✅ All core features functional

**Pass Criteria**: Works on all tested versions

---

### Test C2: Chrome Version Compatibility
**Objective**: Verify extension works on recent Chrome versions

**Test on**:
- Chrome 120+
- Chrome 119
- Chromium-based browsers (Edge, Brave)

**Expected Results**:
- ✅ Extension installs
- ✅ Native messaging works
- ✅ Blocking functions correctly

**Pass Criteria**: Works on Chrome 119+

---

## Regression Tests (Run before each release)

- [ ] All Acceptance Tests (A-J)
- [ ] All Performance Tests (P1-P3)
- [ ] All Security Tests (S1-S3)
- [ ] Compatibility on primary macOS version
- [ ] Fresh install flow
- [ ] Upgrade from previous version (if applicable)

## Test Environment Setup

### Required Tools
- macOS 12+ machine
- Docker Desktop
- Chrome browser
- Activity Monitor
- Terminal
- Network monitoring tools (tcpdump, lsof)

### Test Data
- At least 5 completed flow sessions
- Various session durations (2 min to 2 hours)
- Different apps used during sessions
- Some sessions with block attempts

## Bug Severity Levels

- **Critical**: App crashes, data loss, security vulnerability
- **High**: Core feature doesn't work, major UX issue
- **Medium**: Feature works but has issues, minor UX problem
- **Low**: Cosmetic issue, edge case

## Test Reporting Template

```markdown
**Test**: [Test ID and Name]
**Date**: [YYYY-MM-DD]
**Tester**: [Name]
**Environment**: macOS [version], Chrome [version]

**Result**: PASS / FAIL

**Notes**:
- [Any observations]
- [Deviations from expected]
- [Screenshots if applicable]

**Issues Found**:
- [Bug ID]: [Description]
```

## Pilot User Feedback Collection

### Metrics to Track
- Daily active usage (% of days used)
- Average sessions per day
- Average session duration
- False positive rate (user-reported)
- Feature usage (whitelist, pause, settings changes)

### Feedback Questions
1. Did the app correctly detect when you were in flow?
2. Were there false positives (flow detected when you weren't focused)?
3. Were there false negatives (missed flow states)?
4. Was the blocking helpful or disruptive?
5. Did you use the whitelist feature? Why?
6. Any features you wish it had?
7. Would you continue using this app?

### Success Criteria (Pilot)
- ✅ >50% of users use app daily during 1-week pilot
- ✅ <10% false positive rate
- ✅ >70% users report accurate flow detection
- ✅ >60% users would continue using

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
