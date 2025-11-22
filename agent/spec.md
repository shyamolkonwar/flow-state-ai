# macOS Agent Specification

## Overview
The macOS Agent is the core component that monitors user behavior, detects flow states, and orchestrates protection mechanisms.

## Architecture

### Modules

#### 1. Input Collector
**Purpose**: Capture user input events without recording content

**Responsibilities**:
- Monitor keyboard events (timestamps only, no key content)
- Track mouse movement timestamps
- Detect foreground application changes
- Measure idle time

**macOS APIs**:
- `CGEventTap` for global event monitoring
- `NSWorkspace.shared.frontmostApplication` for app detection
- Accessibility API for reliable event capture

**Permissions Required**:
- **Accessibility Permission**: Required for event monitoring
  - User-facing text: "FlowFacilitator needs Accessibility permission to measure typing cadence and detect app focus so it can help you enter & protect flow. We DO NOT record typed text."

#### 2. Rolling Metrics Engine
**Purpose**: Compute real-time metrics from collected events

**Metrics Computed**:
- `typing_rate`: Keystrokes per minute (60s window)
- `app_switch_count`: Number of app switches (300s window)
- `max_idle_gap`: Longest idle period (300s window)

**Data Structures**:
```python
class RollingWindow:
    events: deque  # Time-ordered events
    window_size: int  # Seconds
    
    def add_event(timestamp, event_type)
    def get_typing_rate() -> float
    def get_app_switches() -> int
    def get_max_idle_gap() -> float
    def cleanup_old_events()
```

#### 3. Flow Rule Engine
**Purpose**: Evaluate flow state based on configurable thresholds

**State Machine**:
```
IDLE → WORKING → IN_FLOW → WORKING → IDLE
```

**States**:
- `IDLE`: No significant activity
- `WORKING`: Activity detected but not meeting flow criteria
- `IN_FLOW`: All flow criteria met for required duration
- `EXITING_FLOW`: Criteria no longer met, waiting for off_delay

**Evaluation Logic**:
```python
def evaluate_flow_state(metrics, config):
    if current_state == WORKING:
        if all_entry_criteria_met(metrics, config):
            if duration >= config.flow_entry_window:
                transition_to(IN_FLOW)
    
    elif current_state == IN_FLOW:
        if any_exit_criteria_met(metrics, config):
            start_exit_timer()
            if exit_timer >= config.off_delay_seconds:
                transition_to(WORKING)
```

#### 4. Protection Controller
**Purpose**: Execute protection actions when flow state changes

**Actions on Flow Entry**:
1. Enable macOS Do Not Disturb
2. Send `enable_blocking` command to Chrome extension
3. Update tray icon to "In Flow" state
4. Log session start to Supabase

**Actions on Flow Exit**:
1. Disable Do Not Disturb
2. Send `disable_blocking` command to Chrome extension
3. Update tray icon to "Working" or "Idle"
4. Log session end to Supabase

**DND Toggle Implementation**:
```bash
# Enable DND (macOS 12+)
defaults -currentHost write ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean true
killall NotificationCenter

# Disable DND
defaults -currentHost write ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean false
killall NotificationCenter
```

Alternative: Use `NSUserNotificationCenter` or AppleScript

#### 5. Persistence Layer
**Purpose**: Write events and sessions to Supabase

**Database Operations**:
- `start_session()`: Create new session record
- `end_session()`: Update session with final metrics
- `insert_event()`: Log individual events
- `upsert_setting()`: Update user preferences

**Connection Handling**:
- Use Supabase Python/Swift client
- Implement connection pooling
- Buffer writes if database unavailable
- Retry logic with exponential backoff

#### 6. Local API
**Purpose**: Provide HTTP interface for dashboard

**Endpoints**:
```
GET  /status           - Current agent state
GET  /metrics          - Real-time metrics
POST /pause            - Pause protection temporarily
POST /resume           - Resume protection
POST /whitelist/add    - Add domain/app to whitelist
POST /whitelist/remove - Remove from whitelist
GET  /health           - Health check
```

**Security**:
- Bind to `localhost` only
- Require bearer token (stored in local config)
- CORS restricted to local dashboard origin

#### 7. Tray/Menu UI
**Purpose**: Provide user controls and status visibility

**Menu Items**:
```
┌─────────────────────────────┐
│ ● FlowFacilitator          │
│ Status: In Flow             │
├─────────────────────────────┤
│ Open Dashboard              │
│ Pause Protection (10 min)   │
│ Quick Whitelist...          │
├─────────────────────────────┤
│ Preferences                 │
│ Quit                        │
└─────────────────────────────┘
```

**Status Indicators**:
- 🔴 Idle (gray)
- 🟡 Working (yellow)
- 🟢 In Flow (green)
- ⏸️ Paused (blue)

## Native Messaging Protocol

### Agent → Extension Messages

**Enable Blocking**:
```json
{
  "cmd": "enable_blocking",
  "domains": ["youtube.com", "reddit.com"],
  "ttl_seconds": 3600
}
```

**Disable Blocking**:
```json
{
  "cmd": "disable_blocking"
}
```

**Update Blocklist**:
```json
{
  "cmd": "update_blocklist",
  "domains": ["youtube.com", "reddit.com", "twitter.com"]
}
```

### Extension → Agent Messages

**Block Attempt**:
```json
{
  "event": "block_attempt",
  "domain": "twitter.com",
  "ts": "2024-01-15T10:30:00Z",
  "url": "https://twitter.com/home"
}
```

**Extension Ready**:
```json
{
  "event": "extension_installed",
  "version": "1.0.0"
}
```

## Configuration

### Config File Location
`~/Library/Application Support/FlowFacilitator/config.json`

### Config Schema
```json
{
  "supabase": {
    "url": "http://localhost:54321",
    "service_key": "eyJhbGc...",
    "max_retries": 3
  },
  "agent": {
    "api_port": 8765,
    "api_token": "local_secret_token",
    "log_level": "info"
  },
  "native_messaging": {
    "host_name": "com.flowfacilitator.helper",
    "manifest_path": "~/Library/Application Support/Google/Chrome/NativeMessagingHosts/"
  }
}
```

## Error Handling

### Permission Denied
```python
if not has_accessibility_permission():
    show_onboarding_overlay()
    # Display step-by-step instructions
    # Provide "Retry" button
    # Do not crash
```

### Database Unavailable
```python
if not supabase_connected():
    enter_offline_mode()
    buffer_events_locally()
    show_tray_warning("Local DB offline - buffering")
    retry_connection_periodically()
```

### Extension Not Responding
```python
if extension_message_failed():
    log_error("Extension communication failed")
    show_tray_warning("Chrome helper not responding")
    continue_flow_detection()  # Don't crash
```

## Logging

### Log Locations
- **Application Logs**: `~/Library/Application Support/FlowFacilitator/logs/agent.log`
- **Database Logs**: `agent_logs` table in Supabase

### Log Levels
- `DEBUG`: Detailed event information
- `INFO`: State transitions, session start/end
- `WARNING`: Failed DND toggle, extension timeout
- `ERROR`: Database connection failure, permission denied
- `CRITICAL`: Unrecoverable errors requiring restart

### Log Rotation
- Max file size: 10MB
- Keep last 5 log files
- Compress old logs

## Performance Requirements

- **CPU Usage**: < 3% average, < 10% peak
- **Memory**: < 150MB
- **Event Processing Latency**: < 100ms
- **State Transition Delay**: < 1s

## Testing

### Unit Tests
- Metrics computation accuracy
- Flow rule evaluation logic
- Event buffering and retry

### Integration Tests
- Database write/read operations
- Extension messaging
- DND toggle functionality

### Manual QA
- Permission request flow
- Tray menu interactions
- Dashboard API responses
