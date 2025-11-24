# Integration Testing Guide

## Overview

The integration test (`test_integration.py`) simulates real user activity to test the entire FlowFacilitator system end-to-end.

## What It Tests

✅ **Flow State Detection**
- Simulates typing to trigger flow state
- Verifies state transitions: idle → working → in_flow
- Tests exit from flow after idle period

✅ **Agent API**
- Checks agent is running
- Monitors metrics in real-time
- Verifies status endpoint

⚠️ **Session Creation** (requires authentication)
- Checks if session is created
- Reports session ID

⚠️ **Database Operations** (manual verification needed)
- Sessions table
- Events table
- User ID linkage

⚠️ **DND Mode** (manual verification needed)
- System Settings > Focus

⚠️ **Extension Communication** (manual verification needed)
- Browser extension blocking status

## Prerequisites

1. **Agent must be running**:
   ```bash
   cd /Users/shyamolkonwar/Documents/flow-state-ai/agent
   python main.py
   ```

2. **Install test dependencies** (if not already installed):
   ```bash
   pip install requests pynput
   ```

3. **Grant accessibility permissions** to Terminal/Python (already done)

## Running the Test

```bash
cd /Users/shyamolkonwar/Documents/flow-state-ai/agent
python test_integration.py
```

## What Happens

1. **Checks agent status** - Verifies agent is running
2. **Simulates typing** - Types continuously for 35 seconds at 20 chars/sec
3. **Monitors flow state** - Shows real-time progress every 5 seconds
4. **Verifies flow entry** - Checks if flow state was reached
5. **Checks session** - Verifies session creation
6. **Simulates idle** - Waits 15 seconds with no activity
7. **Verifies flow exit** - Checks if flow state exited
8. **Shows summary** - Reports test results

## Expected Output

```
============================================================
FlowFacilitator Integration Test
============================================================

[19:35:00] Step 1: Checking agent status
[19:35:00] ✓ Agent is running
[19:35:00] Initial state: idle

[19:35:02] Step 2: Simulating user activity to trigger flow
[19:35:02] Simulating typing for 35 seconds...
[19:35:07]   Progress: 5s | State: working | Typing rate: 120.0/min
[19:35:12]   Progress: 10s | State: working | Typing rate: 240.0/min
[19:35:17]   Progress: 15s | State: working | Typing rate: 360.0/min
[19:35:22]   Progress: 20s | State: working | Typing rate: 480.0/min
[19:35:27]   Progress: 25s | State: working | Typing rate: 600.0/min
[19:35:32]   Progress: 30s | State: in_flow | Typing rate: 720.0/min

[19:35:37] Step 3: Verifying flow state
[19:35:39] Current state: in_flow
[19:35:39] ✓ Successfully entered flow state!

[19:35:39] Step 4: Verifying session creation
[19:35:39] ✓ Session created: abc123...

[19:35:39] Step 5: Verifying DND mode
[19:35:39] ⚠ DND verification not implemented

[19:35:39] Step 6: Simulating idle to exit flow
[19:35:54] State after idle: working
[19:35:54] ✓ Successfully exited flow state!

============================================================
Test Summary
============================================================

✓ Flow detection working
✓ Agent API responding
✓ Session was created
⚠ DND verification requires manual check
⚠ Extension communication requires browser extension
⚠ Database verification requires Supabase access
```

## Manual Verification Steps

After running the test, manually verify:

### 1. Supabase Database

Open Supabase dashboard and check:
- **sessions** table - Should have a new session
- **events** table - Should have `flow_on` and `flow_off` events
- **user_id** - Should be populated (if authenticated)

### 2. DND Mode

Check: **System Settings** > **Focus** > **Do Not Disturb**
- Should be enabled when in flow
- Should be disabled after exiting flow

### 3. Browser Extension

If extension is installed:
- Should show blocking status
- Should block configured domains

## Troubleshooting

### "Agent is not running"
Start the agent first:
```bash
python main.py
```

### "No session was created"
You need to authenticate first:
1. Open FlowFacilitator.app
2. Log in with your credentials
3. Run the test again

### Flow state not reached
- Check the thresholds in `agent.py`
- Ensure typing simulation is fast enough
- Verify no app switches during test

### Permission errors
Grant accessibility permissions:
- System Settings > Privacy & Security > Accessibility
- Add Terminal.app or Python

## Customizing the Test

Edit `test_integration.py` to adjust:

```python
# Typing duration and speed
simulate_typing(duration_seconds=35, chars_per_second=20)

# Idle duration
time.sleep(15)  # Wait 15 seconds
```

## CI/CD Integration

To run in CI/CD:
```bash
# Start agent in background
python main.py &
AGENT_PID=$!

# Wait for agent to start
sleep 5

# Run test
python test_integration.py

# Stop agent
kill $AGENT_PID
```
