# Chrome Extension Specification

## Overview
The Chrome Extension (Helper) blocks distraction domains when commanded by the macOS Agent during flow states.

## Manifest (v3)

### Basic Info
```json
{
  "manifest_version": 3,
  "name": "FlowFacilitator Helper",
  "version": "1.0.0",
  "description": "Blocks distracting websites during flow states to help maintain deep focus",
  "permissions": [
    "declarativeNetRequest",
    "declarativeNetRequestFeedback",
    "storage",
    "nativeMessaging"
  ],
  "host_permissions": [
    "<all_urls>"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  }
}
```

## Architecture

### Components

#### 1. Background Service Worker (`background.js`)
**Purpose**: Maintain connection with agent and manage blocking rules

**Responsibilities**:
- Establish native messaging connection with agent
- Receive commands from agent
- Update declarativeNetRequest rules
- Send block attempt events back to agent
- Sync blocklist/whitelist with local storage

#### 2. Popup UI (`popup.html`)
**Purpose**: Quick status view and manual controls

**UI Elements**:
- Current status indicator (Blocking / Allowing)
- Number of sites blocked today
- Quick whitelist input
- Link to dashboard
- Extension settings

#### 3. Native Messaging Host
**Purpose**: Enable communication between extension and agent

**Host Manifest Location**:
`~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.flowfacilitator.helper.json`

**Host Manifest Content**:
```json
{
  "name": "com.flowfacilitator.helper",
  "description": "FlowFacilitator Native Messaging Host",
  "path": "/Applications/FlowFacilitator.app/Contents/MacOS/native-host",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://[EXTENSION_ID]/"
  ]
}
```

## Message Protocol

### Agent → Extension

#### Enable Blocking
```json
{
  "cmd": "enable_blocking",
  "domains": ["youtube.com", "reddit.com", "twitter.com"],
  "ttl_seconds": 3600
}
```

**Extension Response**:
```json
{
  "status": "success",
  "rules_added": 10,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Disable Blocking
```json
{
  "cmd": "disable_blocking"
}
```

**Extension Response**:
```json
{
  "status": "success",
  "rules_removed": 10,
  "timestamp": "2024-01-15T11:00:00Z"
}
```

#### Update Blocklist
```json
{
  "cmd": "update_blocklist",
  "domains": ["youtube.com", "reddit.com", "twitter.com", "facebook.com"]
}
```

**Extension Response**:
```json
{
  "status": "success",
  "total_domains": 4,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Extension → Agent

#### Block Attempt
```json
{
  "event": "block_attempt",
  "domain": "twitter.com",
  "url": "https://twitter.com/home",
  "ts": "2024-01-15T10:30:00Z"
}
```

#### Extension Ready
```json
{
  "event": "extension_installed",
  "version": "1.0.0",
  "chrome_version": "120.0.0"
}
```

## Blocking Implementation

### Using declarativeNetRequest

**Rule Structure**:
```javascript
const createBlockingRules = (domains) => {
  return domains.map((domain, index) => ({
    id: index + 1,
    priority: 1,
    action: {
      type: "redirect",
      redirect: {
        url: chrome.runtime.getURL("blocked.html")
      }
    },
    condition: {
      urlFilter: `*://*.${domain}/*`,
      resourceTypes: ["main_frame"]
    }
  }));
};
```

**Applying Rules**:
```javascript
async function enableBlocking(domains) {
  // Remove existing rules
  const existingRules = await chrome.declarativeNetRequest.getDynamicRules();
  const ruleIds = existingRules.map(rule => rule.id);
  
  await chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: ruleIds,
    addRules: createBlockingRules(domains)
  });
}
```

**Removing Rules**:
```javascript
async function disableBlocking() {
  const existingRules = await chrome.declarativeNetRequest.getDynamicRules();
  const ruleIds = existingRules.map(rule => rule.id);
  
  await chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: ruleIds
  });
}
```

## Whitelist Management

### Storage Schema
```javascript
{
  "whitelist": {
    "domains": ["example.com", "work-site.com"],
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "blocklist": {
    "domains": ["youtube.com", "reddit.com"],
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "stats": {
    "blocks_today": 42,
    "last_reset": "2024-01-15T00:00:00Z"
  }
}
```

### Whitelist Logic
```javascript
function shouldBlock(url, blocklist, whitelist) {
  const domain = extractDomain(url);
  
  // Check whitelist first
  if (whitelist.some(w => domain.includes(w))) {
    return false;
  }
  
  // Check blocklist
  return blocklist.some(b => domain.includes(b));
}
```

## Blocked Page

### `blocked.html`
```html
<!DOCTYPE html>
<html>
<head>
  <title>Site Blocked - FlowFacilitator</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    .container {
      text-align: center;
      max-width: 500px;
      padding: 40px;
    }
    h1 {
      font-size: 48px;
      margin-bottom: 20px;
    }
    p {
      font-size: 18px;
      margin-bottom: 30px;
      opacity: 0.9;
    }
    .stats {
      background: rgba(255, 255, 255, 0.1);
      padding: 20px;
      border-radius: 10px;
      margin-top: 30px;
    }
    button {
      background: white;
      color: #667eea;
      border: none;
      padding: 12px 24px;
      font-size: 16px;
      border-radius: 6px;
      cursor: pointer;
      margin: 5px;
    }
    button:hover {
      opacity: 0.9;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🎯 Stay Focused</h1>
    <p>This site is blocked to help you maintain your flow state.</p>
    <p id="blocked-domain"></p>
    
    <button id="whitelist-btn">Whitelist This Site</button>
    <button id="pause-btn">Pause Protection (10 min)</button>
    
    <div class="stats">
      <p><strong>Sites blocked today:</strong> <span id="block-count">0</span></p>
      <p><strong>Current session:</strong> <span id="session-time">0 min</span></p>
    </div>
  </div>
  
  <script src="blocked.js"></script>
</body>
</html>
```

## Error Handling

### Native Messaging Connection Lost
```javascript
port.onDisconnect.addListener(() => {
  console.error("Native messaging disconnected");
  // Attempt reconnection
  setTimeout(connectToNativeHost, 5000);
  // Show warning in popup
  updateStatus("Agent disconnected - retrying...");
});
```

### Rule Update Failure
```javascript
try {
  await chrome.declarativeNetRequest.updateDynamicRules({...});
} catch (error) {
  console.error("Failed to update rules:", error);
  // Notify agent of failure
  sendToAgent({
    event: "error",
    message: "Failed to update blocking rules",
    error: error.message
  });
}
```

## Installation Flow

### First Install
1. Extension installed from Chrome Web Store (or loaded unpacked for dev)
2. Extension checks for native messaging host
3. If host not found, show setup instructions
4. Once connected, send `extension_installed` event to agent
5. Sync initial blocklist from agent

### Setup Instructions (shown if host not found)
```
FlowFacilitator Helper Setup Required

To enable website blocking, please:
1. Install the FlowFacilitator macOS app
2. Grant Accessibility permission when prompted
3. Restart Chrome

The extension will automatically connect once setup is complete.
```

## Testing

### Unit Tests
- Message parsing and validation
- Rule generation from domain list
- Whitelist filtering logic

### Integration Tests
- Native messaging connection
- Rule application and removal
- Block attempt logging

### Manual QA
- Install extension and verify connection
- Trigger flow state and verify blocking
- Test whitelist functionality
- Verify blocked page displays correctly
- Test pause protection feature

## Performance

- **Rule Update Latency**: < 500ms
- **Memory Usage**: < 50MB
- **CPU Impact**: Negligible (declarativeNetRequest is efficient)

## Privacy

- **No Browsing History**: Extension does not track or store browsing history
- **Local Only**: All data stored in Chrome's local storage
- **No External Requests**: No telemetry or analytics
- **Minimal Permissions**: Only requests necessary permissions
