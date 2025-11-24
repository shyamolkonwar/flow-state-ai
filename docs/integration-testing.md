# Integration Testing Guide

## Overview

This guide covers end-to-end integration testing for the FlowFacilitator MVP.

## Prerequisites

1. **Supabase Running**: `./scripts/start-local.sh`
2. **Agent Running**: `cd agent && python main.py --dev --debug`
3. **Dashboard Running**: `cd dashboard/ui && npm run dev`
4. **Extension Loaded**: Load unpacked from `chrome-extension/` directory
5. **Native Messaging Installed**: Run `./scripts/install-native-messaging.sh`

## Test Scenarios

### 1. Flow Detection End-to-End

**Objective**: Verify flow state is detected and all components respond correctly.

**Steps**:
1. Start typing continuously in any app (>40 kpm)
2. Keep app switches to minimum (≤2 per 5 min)
3. Avoid idle gaps (≤4 seconds)
4. Continue for 5 minutes

**Expected Results**:
- ✅ Agent logs show "State transition: working -> in_flow"
- ✅ Dashboard shows "🎯 In Flow" status
- ✅ macOS Do Not Disturb is enabled
- ✅ Extension icon changes to "blocking" state
- ✅ New session created in database

**Verification**:
```bash
# Check agent logs
tail -f ~/Library/Application\ Support/FlowFacilitator/logs/agent.log

# Check database
docker exec -it supabase-db psql -U postgres -d postgres -c "SELECT * FROM sessions ORDER BY start_ts DESC LIMIT 1;"
```

### 2. Overlay Blocking

**Objective**: Test overlay appears when blocked app is opened during flow.

**Steps**:
1. Enter flow state (see Test 1)
2. Try to open Instagram/Steam/Twitter

**Expected Results**:
- ✅ Full-screen overlay appears immediately
- ✅ Countdown starts at 10 seconds
- ✅ "Unlock" button is disabled
- ✅ After 10 seconds, unlock button becomes active
- ✅ Clicking "Stay in Flow" closes overlay and adds Resilience +1
- ✅ Clicking "Unlock" breaks flow and ends session

### 3. Micro-Interventions

**Objective**: Test cognitive fatigue detection and soft reset.

**Steps**:
1. Enter flow state
2. Simulate fatigue by:
   - Typing erratically (fast then slow)
   - Taking longer idle breaks
   - Gradually slowing typing rate

**Expected Results**:
- ✅ Agent detects fatigue after 5+ samples
- ✅ Blur overlay appears
- ✅ Audio fades out smoothly (2 seconds)
- ✅ Message shows "Micro-Break - Take a deep breath"
- ✅ After 30 seconds, overlay disappears
- ✅ Audio fades back in

### 4. Gamification Stats

**Objective**: Verify stats are tracked and displayed correctly.

**Steps**:
1. Complete a flow session (5+ minutes)
2. Resist a distraction (click "Stay in Flow")
3. Open dashboard gamification page

**Expected Results**:
- ✅ Stamina increased by session duration
- ✅ Resilience increased by 1
- ✅ Experience points awarded (10 XP/min + 50 XP/resistance)
- ✅ Level up if XP threshold reached
- ✅ Progressive goal updated (5% above average)
- ✅ Stats displayed correctly on dashboard

**Verification**:
```bash
# Check gamification stats file
cat ~/Library/Application\ Support/FlowFacilitator/user_stats.json
```

### 5. Native Messaging

**Objective**: Test agent ↔ extension communication.

**Steps**:
1. Open Chrome extension popup
2. Check console for connection status
3. Enter flow state
4. Verify extension receives blocking command

**Expected Results**:
- ✅ Extension console shows "Connected to native messaging host"
- ✅ When flow starts, extension receives "enable_blocking" message
- ✅ Extension creates blocking rules
- ✅ Badge shows "ON"
- ✅ When flow ends, extension receives "disable_blocking"

**Debugging**:
```bash
# Check native messaging manifest
cat ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.flowfacilitator.helper.json

# Check extension console
# Open chrome://extensions/ -> FlowFacilitator -> "Inspect views: service worker"
```

### 6. Dashboard API

**Objective**: Test dashboard ↔ agent API communication.

**Steps**:
1. Open dashboard at http://localhost:3000
2. Verify agent status is displayed
3. Enter flow state
4. Watch status update in real-time

**Expected Results**:
- ✅ Dashboard loads without errors
- ✅ Agent status shows current flow state
- ✅ Status updates every 5 seconds
- ✅ Metrics are displayed correctly
- ✅ Quick actions work (pause, whitelist)

**API Test**:
```bash
# Test status endpoint
curl http://localhost:8765/status

# Test gamification stats
curl http://localhost:8765/stats/gamification
```

### 7. Settings Sync

**Objective**: Verify settings changes propagate to all components.

**Steps**:
1. Open dashboard settings page
2. Change typing rate threshold from 40 to 50
3. Add new domain to blocklist
4. Click "Save Settings"

**Expected Results**:
- ✅ Settings saved to database
- ✅ Agent reloads settings
- ✅ Flow detection uses new threshold
- ✅ Extension receives updated blocklist
- ✅ Dashboard shows confirmation

### 8. Error Handling

**Objective**: Test graceful degradation when components fail.

**Steps**:
1. Stop Supabase: `cd infra/supabase && docker-compose down`
2. Continue using agent
3. Restart Supabase
4. Verify data is synced

**Expected Results**:
- ✅ Agent continues running
- ✅ Events are buffered locally
- ✅ When database reconnects, buffer is flushed
- ✅ No data loss
- ✅ Error logged but agent doesn't crash

## Performance Testing

### CPU Usage

```bash
# Monitor agent CPU usage
top -pid $(pgrep -f "python.*main.py")
```

**Target**: <3% average CPU usage

### Memory Usage

```bash
# Monitor agent memory
ps aux | grep "python.*main.py"
```

**Target**: <150MB RAM

### Event Processing Latency

Check agent logs for event processing times.

**Target**: <100ms per event

## Automated Test Suite

Run all unit tests:

```bash
cd agent
pytest tests/unit/ -v
```

Expected output:
```
test_overlay_manager.py::TestOverlayManager::test_set_blocked_apps PASSED
test_overlay_manager.py::TestOverlayManager::test_should_block_app_exact_match PASSED
test_gamification.py::TestGamificationSystem::test_add_flow_session PASSED
test_gamification.py::TestGamificationSystem::test_level_up PASSED
test_micro_interventions.py::TestMicroIntervention::test_detect_fatigue_high_variance PASSED
...
```

## Checklist

Before marking Phase 6 complete, verify:

- [ ] All 8 integration test scenarios pass
- [ ] CPU usage <3%
- [ ] Memory usage <150MB
- [ ] No errors in agent logs during normal operation
- [ ] Dashboard loads and updates in real-time
- [ ] Extension connects to native messaging
- [ ] All unit tests pass
- [ ] Database migrations apply cleanly
- [ ] Settings sync across all components
- [ ] Error recovery works (database disconnect/reconnect)

## Common Issues

### Extension Not Connecting

**Symptom**: "Disconnected from agent" in extension console

**Solutions**:
1. Check native messaging manifest path is correct
2. Verify extension ID in manifest matches actual ID
3. Ensure agent is running
4. Check agent logs for native messaging errors

### Dashboard Can't Reach Agent

**Symptom**: Dashboard shows "Error loading agent status"

**Solutions**:
1. Verify agent API server is running on port 8765
2. Check CORS is enabled
3. Verify `.env` file has correct `VITE_AGENT_API_URL`
4. Check browser console for network errors

### Overlay Not Appearing

**Symptom**: Blocked apps open normally during flow

**Solutions**:
1. Check app name matches blocklist
2. Verify Tkinter is installed
3. Check agent logs for overlay errors
4. Ensure macOS allows Python to control computer

### Stats Not Updating

**Symptom**: Gamification stats don't change after sessions

**Solutions**:
1. Check stats file exists and is writable
2. Verify session duration is >0
3. Check agent logs for gamification errors
4. Manually inspect stats file

## Next Steps

After completing Phase 6:
1. Document any issues found
2. Fix critical bugs
3. Optimize performance if needed
4. Proceed to Phase 7: Packaging and Documentation

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
