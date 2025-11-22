# System Architecture - Sequence Diagrams

## Overview
This document contains sequence diagrams illustrating the key interactions between components of the FlowFacilitator system.

## 1. Flow Entry Sequence

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Metrics as Metrics Engine
    participant Rules as Rule Engine
    participant DND as macOS DND
    participant Extension as Chrome Extension
    participant DB as Supabase Local

    User->>Agent: Types steadily in app
    Agent->>Metrics: Record keystroke timestamp
    Agent->>Metrics: Record app focus
    
    loop Every 1 second
        Metrics->>Metrics: Update rolling windows
        Metrics->>Rules: Provide current metrics
        Rules->>Rules: Evaluate flow criteria
    end
    
    Note over Rules: All criteria met for 5 min
    
    Rules->>Agent: Flow ON event
    Agent->>DB: start_session(timestamp, app)
    DB-->>Agent: session_id
    
    par Parallel Actions
        Agent->>DND: Enable Do Not Disturb
        DND-->>Agent: Success
    and
        Agent->>Extension: {"cmd":"enable_blocking","domains":[...]}
        Extension->>Extension: Apply blocking rules
        Extension-->>Agent: {"status":"success"}
    and
        Agent->>Agent: Update tray icon (green)
    end
    
    Agent->>DB: insert_event("flow_on", session_id)
    
    Note over User,DB: User is now in protected flow state
```

## 2. Flow Exit Sequence

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Metrics as Metrics Engine
    participant Rules as Rule Engine
    participant DND as macOS DND
    participant Extension as Chrome Extension
    participant DB as Supabase Local

    Note over User,DB: User is in flow state
    
    User->>Agent: Switches apps multiple times
    Agent->>Metrics: Record app switches
    
    loop Every 1 second
        Metrics->>Rules: Provide current metrics
        Rules->>Rules: Check exit criteria
    end
    
    Note over Rules: Exit criteria met for 30s
    
    Rules->>Agent: Flow OFF event
    
    par Parallel Actions
        Agent->>DND: Disable Do Not Disturb
        DND-->>Agent: Success
    and
        Agent->>Extension: {"cmd":"disable_blocking"}
        Extension->>Extension: Remove blocking rules
        Extension-->>Agent: {"status":"success"}
    and
        Agent->>Agent: Update tray icon (yellow/gray)
    end
    
    Agent->>Metrics: Calculate session metrics
    Metrics-->>Agent: avg_typing_rate, max_idle_gap
    
    Agent->>DB: end_session(session_id, metrics, reason)
    Agent->>DB: insert_event("flow_off", session_id)
    
    Note over User,DB: Flow session ended and saved
```

## 3. Dashboard Real-time Update

```mermaid
sequenceDiagram
    participant Dashboard
    participant Supabase as Supabase Local
    participant Agent
    participant User

    Dashboard->>Supabase: Subscribe to sessions table
    Dashboard->>Supabase: Subscribe to events (flow_on/off)
    
    Note over Dashboard,Supabase: Dashboard is listening
    
    User->>Agent: Enters flow state
    Agent->>Supabase: INSERT into sessions
    Agent->>Supabase: INSERT event (flow_on)
    
    Supabase->>Dashboard: Realtime: New session
    Supabase->>Dashboard: Realtime: flow_on event
    
    Dashboard->>Dashboard: Update UI (live status)
    Dashboard->>Dashboard: Add session to list
    Dashboard->>Dashboard: Update metrics
    
    Note over Dashboard: Shows "In Flow" status
    
    User->>Agent: Exits flow state
    Agent->>Supabase: UPDATE session (end_ts, metrics)
    Agent->>Supabase: INSERT event (flow_off)
    
    Supabase->>Dashboard: Realtime: Session updated
    Supabase->>Dashboard: Realtime: flow_off event
    
    Dashboard->>Dashboard: Update UI
    Dashboard->>Dashboard: Show completed session
```

## 4. User Whitelist Addition

```mermaid
sequenceDiagram
    participant User
    participant Dashboard
    participant API as Dashboard API
    participant DB as Supabase Local
    participant Agent
    participant Extension as Chrome Extension

    User->>Dashboard: Clicks "Add to Whitelist"
    User->>Dashboard: Enters "example.com"
    Dashboard->>API: POST /api/whitelist/add {"domain":"example.com"}
    
    API->>DB: upsert_setting("whitelist", updated_list)
    DB-->>API: Success
    
    API->>Agent: Notify settings changed
    Agent->>Agent: Reload whitelist
    
    Agent->>Extension: {"cmd":"update_blocklist","domains":[...]}
    Note over Agent,Extension: Blocklist excludes whitelisted domains
    
    Extension->>Extension: Update blocking rules
    Extension-->>Agent: {"status":"success"}
    
    API-->>Dashboard: {"status":"success"}
    Dashboard->>Dashboard: Update UI
    Dashboard-->>User: "example.com added to whitelist"
```

## 5. Extension Block Attempt

```mermaid
sequenceDiagram
    participant User
    participant Browser as Chrome
    participant Extension as Chrome Extension
    participant Agent
    participant DB as Supabase Local
    participant BlockPage as Blocked Page

    Note over User,DB: User is in flow state
    
    User->>Browser: Navigates to twitter.com
    Browser->>Extension: Request to load twitter.com
    
    Extension->>Extension: Check blocking rules
    Note over Extension: Domain is in blocklist
    
    Extension->>BlockPage: Redirect to blocked.html
    BlockPage-->>User: Display "Stay Focused" page
    
    Extension->>Agent: {"event":"block_attempt","domain":"twitter.com"}
    Agent->>DB: insert_event("block_attempt", {...})
    
    User->>BlockPage: Clicks "Whitelist This Site"
    BlockPage->>Extension: Request whitelist
    Extension->>Agent: {"event":"whitelist_request","domain":"twitter.com"}
    
    Agent->>Agent: Show confirmation dialog
    Agent-->>User: "Add twitter.com to whitelist?"
    User->>Agent: Confirms
    
    Agent->>DB: upsert_setting("whitelist", updated_list)
    Agent->>Extension: {"cmd":"update_blocklist","domains":[...]}
    Extension->>Extension: Remove twitter.com from rules
    
    Browser->>Browser: Reload page
    Browser-->>User: twitter.com loads normally
```

## 6. Permission Request Flow

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant macOS as macOS System
    participant Onboarding as Onboarding UI

    User->>Agent: Launches app (first time)
    Agent->>macOS: Check Accessibility permission
    macOS-->>Agent: Permission not granted
    
    Agent->>Onboarding: Show onboarding overlay
    Onboarding-->>User: Display permission instructions
    
    User->>Onboarding: Clicks "Open System Settings"
    Onboarding->>macOS: Open System Settings (Accessibility)
    macOS-->>User: Shows Accessibility preferences
    
    User->>macOS: Enables FlowFacilitator
    User->>Onboarding: Clicks "Retry"
    
    Onboarding->>Agent: Check permission again
    Agent->>macOS: Check Accessibility permission
    macOS-->>Agent: Permission granted ✅
    
    Agent->>Onboarding: Hide overlay
    Agent->>Agent: Start event collection
    Agent->>Agent: Show tray icon
    
    Note over User,Agent: App is ready to use
```

## 7. Database Offline Recovery

```mermaid
sequenceDiagram
    participant Agent
    participant DB as Supabase Local
    participant Buffer as Local Buffer
    participant Tray as Tray UI

    Agent->>DB: Attempt to write event
    DB-->>Agent: Connection failed ❌
    
    Agent->>Agent: Enter offline mode
    Agent->>Buffer: Initialize event buffer
    Agent->>Tray: Show "DB offline - buffering"
    
    loop While offline
        Agent->>Buffer: Buffer events locally
        Agent->>DB: Retry connection (every 30s)
        DB-->>Agent: Still offline
    end
    
    Agent->>DB: Retry connection
    DB-->>Agent: Connection successful ✅
    
    Agent->>Agent: Exit offline mode
    Agent->>Buffer: Get buffered events
    
    loop For each buffered event
        Agent->>DB: Write event
        DB-->>Agent: Success
    end
    
    Agent->>Buffer: Clear buffer
    Agent->>Tray: Update status (normal)
    
    Note over Agent,Tray: Fully recovered, no data lost
```

## 8. Settings Update Propagation

```mermaid
sequenceDiagram
    participant User
    participant Dashboard
    participant DB as Supabase Local
    participant Agent
    participant Extension as Chrome Extension

    User->>Dashboard: Adjusts flow thresholds
    User->>Dashboard: Clicks "Save Settings"
    
    Dashboard->>DB: upsert_setting("flow_detection", new_config)
    DB-->>Dashboard: Success
    
    Note over DB: Realtime notification
    
    DB->>Agent: Settings changed event
    Agent->>Agent: Reload configuration
    Agent->>Agent: Update rule engine thresholds
    
    Dashboard->>Dashboard: Show "Settings saved ✅"
    
    Note over User,Extension: New thresholds active immediately
    
    User->>Dashboard: Updates blocklist
    Dashboard->>DB: upsert_setting("blocklist", new_list)
    DB-->>Dashboard: Success
    
    DB->>Agent: Settings changed event
    Agent->>Agent: Reload blocklist
    Agent->>Extension: {"cmd":"update_blocklist","domains":[...]}
    Extension->>Extension: Apply new rules
    Extension-->>Agent: Success
```

## Component Interaction Summary

### Key Communication Patterns

1. **Agent ↔ Supabase**: Direct database operations via client SDK
2. **Agent ↔ Extension**: Native Messaging (JSON over stdio)
3. **Dashboard ↔ Supabase**: Direct queries + Realtime subscriptions
4. **Dashboard ↔ Agent**: REST API (local HTTP)
5. **Agent ↔ macOS**: System APIs (DND, Accessibility)

### Data Flow

```
User Input → Agent → Metrics Engine → Rule Engine → Protection Actions
                ↓                                          ↓
            Supabase ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
                ↓
            Dashboard (Realtime)
```

### Error Handling Pattern

All components follow:
1. Attempt operation
2. If fails, log error
3. Show user-friendly message
4. Implement fallback or retry
5. Never crash the app
