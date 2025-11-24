# Flow Detection Configuration

## Overview
This document defines the exact thresholds and parameters for detecting when a user enters and exits a flow state.

## Detection Parameters

### Rolling Window
- **Window Size**: 5 minutes (300 seconds)
- **Evaluation Frequency**: Every 1 second

### Flow Entry Criteria
All conditions must be met continuously for the `flow_entry_window` duration:

| Parameter | Threshold | Description |
|-----------|-----------|-------------|
| `typing_rate` | ≥ 10 kpm | Keystrokes per minute averaged over last 60s (lowered for testing) |
| `app_switches` | ≤ 2 | Number of app switches in last 5 minutes |
| `max_idle_gap` | ≤ 4s | Longest idle gap in last 5 minutes |
| `flow_entry_window` | 30s | Duration all criteria must hold (lowered for testing) |

### Flow Exit Criteria
If ANY condition persists for `off_delay_seconds`:

| Parameter | Threshold | Description |
|-----------|-----------|-------------|
| `typing_rate` | < 5 kpm | Typing rate drops below threshold (lowered for testing) |
| `app_switches` | > 2 | More than 2 app switches |
| `max_idle_gap` | > 6s | Idle gap exceeds threshold |
| `off_delay_seconds` | 10s | Duration before exiting flow (lowered for testing) |

## Configuration Schema

All thresholds are user-configurable and stored in the `settings` table:

```json
{
  "flow_detection": {
    "entry": {
      "typing_rate_min": 40,
      "app_switches_max": 2,
      "max_idle_gap_seconds": 4,
      "window_seconds": 300
    },
    "exit": {
      "typing_rate_min": 30,
      "app_switches_max": 2,
      "max_idle_gap_seconds": 6,
      "delay_seconds": 30
    },
    "metrics": {
      "typing_rate_window_seconds": 60,
      "rolling_window_seconds": 300
    }
  }
}
```

## Default Blocklist

Default domains to block during flow state:

```json
{
  "blocklist": [
    "youtube.com",
    "reddit.com",
    "twitter.com",
    "x.com",
    "facebook.com",
    "instagram.com",
    "tiktok.com",
    "netflix.com",
    "twitch.tv",
    "discord.com"
  ]
}
```

## Metrics Collection

### Event Types
- `keystroke` - Individual keystroke timestamp (no content)
- `mouse_move` - Mouse movement timestamp
- `app_switch` - Foreground application change
- `idle_start` - User becomes idle
- `idle_end` - User resumes activity
- `flow_on` - Flow state entered
- `flow_off` - Flow state exited

### Rolling Metrics Computation
The agent maintains sliding windows to compute:

1. **Typing Rate (kpm)**
   - Count keystrokes in last 60 seconds
   - Divide by 60 to get per-minute rate

2. **App Switch Count**
   - Count `app_switch` events in last 300 seconds

3. **Max Idle Gap**
   - Track time between consecutive input events
   - Record maximum gap in last 300 seconds

## User Customization

Users can adjust thresholds via the dashboard settings page:

- **Sensitivity**: Preset profiles (Relaxed, Balanced, Strict)
- **Custom**: Individual threshold adjustment
- **Blocklist**: Add/remove domains
- **Whitelist**: Exempt specific apps/domains from protection

## Privacy Guarantees

- **No Content Capture**: Only timestamps and counts are recorded
- **Local Storage**: All data stored in local Supabase instance
- **User Control**: Complete data deletion available
- **Transparency**: All thresholds visible and adjustable
