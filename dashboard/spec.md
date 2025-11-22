# Dashboard Specification

## Overview
The Dashboard is a local web application that displays flow state analytics, session history, and provides settings management.

## Architecture

### Technology Stack
- **Frontend**: React with Vite
- **Backend**: Node.js + Express (minimal API layer)
- **Database**: Supabase (local) via client SDK
- **Styling**: Vanilla CSS with modern design
- **Charts**: Chart.js or Recharts

### Server
- **Port**: 3000 (configurable)
- **Binding**: localhost only
- **Authentication**: Bearer token from agent config

## Routes & Pages

### 1. Home / Summary (`/`)
**Purpose**: Overview of today's flow activity

**Metrics Displayed**:
- Total flow time today (minutes)
- Number of sessions today
- Longest session duration
- Current streak (consecutive days with flow)

**Components**:
- Summary cards with key metrics
- Quick action buttons (Start Manual Session, View Settings)
- Live status indicator (synced with agent)

**API Queries**:
```sql
-- Today's sessions
SELECT 
  COUNT(*) as session_count,
  SUM(duration_seconds) as total_seconds,
  MAX(duration_seconds) as longest_session
FROM sessions
WHERE start_ts >= CURRENT_DATE
  AND end_ts IS NOT NULL;
```

### 2. Sessions List (`/sessions`)
**Purpose**: Detailed view of all flow sessions

**Table Columns**:
- Start Time
- End Time
- Duration
- Dominant App
- Avg Typing Rate
- Reason Ended
- Actions (View Details, Delete)

**Filters**:
- Date range picker
- App filter
- Minimum duration filter

**API Queries**:
```sql
-- Sessions with filters
SELECT 
  id,
  start_ts,
  end_ts,
  duration_seconds,
  start_app,
  avg_typing_rate,
  trigger_reason
FROM sessions
WHERE start_ts >= :start_date
  AND start_ts <= :end_date
  AND (:app_filter IS NULL OR start_app = :app_filter)
  AND duration_seconds >= :min_duration
ORDER BY start_ts DESC
LIMIT 100;
```

### 3. Session Detail (`/sessions/:id`)
**Purpose**: Deep dive into a specific session

**Information Displayed**:
- Session timeline visualization
- Event log (app switches, typing rate changes)
- Metrics chart over time
- Notes (user can add)

**API Queries**:
```sql
-- Session events
SELECT ts, type, payload
FROM events
WHERE session_id = :session_id
ORDER BY ts ASC;
```

### 4. Timeline View (`/timeline`)
**Purpose**: Visual representation of flow sessions over time

**Visualization**:
- Horizontal timeline with session bars
- Color-coded by duration or app
- Hover for session details
- Click to navigate to session detail

**Time Ranges**:
- Today
- This Week
- This Month
- Custom Range

### 5. Settings (`/settings`)
**Purpose**: Configure thresholds, lists, and preferences

**Sections**:

#### Flow Detection Thresholds
```
Entry Criteria:
- Typing Rate (min): [40] kpm
- Max App Switches: [2]
- Max Idle Gap: [4] seconds
- Entry Window: [300] seconds

Exit Criteria:
- Typing Rate (min): [30] kpm
- Max App Switches: [2]
- Max Idle Gap: [6] seconds
- Exit Delay: [30] seconds
```

#### Blocklist Management
- Text area with one domain per line
- Add/remove domains
- Import/export list

#### Whitelist Management
- Domains that are never blocked
- Apps that don't trigger flow exit

#### Data Management
- Export all data (CSV)
- Delete all data (with confirmation)
- Set retention policy

#### Preset Profiles
- **Relaxed**: Lower thresholds, easier to enter flow
- **Balanced**: Default settings
- **Strict**: Higher thresholds, harder to enter flow

**API Operations**:
```javascript
// Update settings
await supabase.rpc('upsert_setting', {
  p_user_id: 'local_user',
  p_key: 'flow_detection',
  p_value: newConfig
});
```

### 6. Analytics (`/analytics`)
**Purpose**: Long-term insights and trends

**Charts**:
- Flow time per day (last 30 days)
- Average session duration trend
- Most productive hours heatmap
- Top apps during flow
- Distraction attempts blocked

**Insights**:
- Best time of day for flow
- Average sessions per day
- Flow state improvement over time

## API Endpoints

### Dashboard Server API

#### GET `/api/status`
**Purpose**: Get current agent status

**Response**:
```json
{
  "state": "IN_FLOW",
  "current_session_id": "uuid",
  "session_start": "2024-01-15T10:30:00Z",
  "current_metrics": {
    "typing_rate": 45.2,
    "app_switches": 1,
    "max_idle_gap": 2.5
  }
}
```

#### GET `/api/sessions`
**Purpose**: List sessions with filters

**Query Params**:
- `start_date`: ISO timestamp
- `end_date`: ISO timestamp
- `app`: Filter by app name
- `min_duration`: Minimum seconds

**Response**:
```json
{
  "sessions": [...],
  "total": 42,
  "page": 1
}
```

#### GET `/api/sessions/:id`
**Purpose**: Get session details with events

**Response**:
```json
{
  "session": {...},
  "events": [...]
}
```

#### POST `/api/settings`
**Purpose**: Update settings

**Body**:
```json
{
  "key": "flow_detection",
  "value": {...}
}
```

#### GET `/api/export`
**Purpose**: Export data as CSV

**Query Params**:
- `format`: csv | json
- `start_date`: ISO timestamp
- `end_date`: ISO timestamp

**Response**: CSV file download

#### POST `/api/pause`
**Purpose**: Pause protection temporarily

**Body**:
```json
{
  "duration_minutes": 10
}
```

#### POST `/api/whitelist/add`
**Purpose**: Add domain to whitelist

**Body**:
```json
{
  "domain": "example.com"
}
```

## Real-time Updates

### Using Supabase Realtime

**Subscribe to Session Changes**:
```javascript
const subscription = supabase
  .channel('sessions')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'sessions'
  }, (payload) => {
    // Update UI with new session
    addSessionToList(payload.new);
  })
  .subscribe();
```

**Subscribe to Flow State Changes**:
```javascript
supabase
  .channel('events')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'events',
    filter: 'type=in.(flow_on,flow_off)'
  }, (payload) => {
    // Update live status indicator
    updateFlowStatus(payload.new);
  })
  .subscribe();
```

## UI Design

### Color Palette
```css
:root {
  --primary: #667eea;
  --primary-dark: #5568d3;
  --secondary: #764ba2;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-800: #1f2937;
  --gray-900: #111827;
}
```

### Typography
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

### Layout
- Sidebar navigation (collapsible)
- Main content area with max-width for readability
- Responsive design (desktop-first, mobile-friendly)

### Components

#### Metric Card
```html
<div class="metric-card">
  <div class="metric-icon">🎯</div>
  <div class="metric-value">2h 34m</div>
  <div class="metric-label">Total Flow Time Today</div>
</div>
```

#### Session Card
```html
<div class="session-card">
  <div class="session-header">
    <span class="session-time">10:30 AM - 12:15 PM</span>
    <span class="session-duration">1h 45m</span>
  </div>
  <div class="session-app">VS Code</div>
  <div class="session-metrics">
    <span>⌨️ 45 kpm</span>
    <span>🔄 1 switch</span>
  </div>
</div>
```

## Authentication

### Local Token-Based Auth

**Token Storage**:
- Agent generates token on startup
- Stored in `~/Library/Application Support/FlowFacilitator/config.json`
- Dashboard reads token from config or receives via URL param on first load

**Request Authentication**:
```javascript
fetch('/api/sessions', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

**Server Validation**:
```javascript
function authenticateRequest(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  const validToken = config.agent.api_token;
  
  if (token !== validToken) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  next();
}
```

## Error States

### Database Unavailable
```html
<div class="error-banner">
  ⚠️ Unable to connect to local database. 
  <button>Start Database</button>
</div>
```

### Agent Offline
```html
<div class="warning-banner">
  ℹ️ Agent is not running. Real-time updates disabled.
</div>
```

## Performance

- **Initial Load**: < 2s
- **Page Navigation**: < 500ms
- **Real-time Update Latency**: < 1s
- **Chart Rendering**: < 1s for 30 days of data

## Testing

### Unit Tests
- Component rendering
- Data formatting utilities
- API client functions

### Integration Tests
- API endpoint responses
- Supabase queries
- Real-time subscriptions

### E2E Tests
- Complete user flows (view sessions, update settings)
- Export functionality
- Real-time updates

## Deployment

### Development
```bash
cd dashboard
npm install
npm run dev
# Opens at http://localhost:3000
```

### Production Build
```bash
npm run build
# Serves static files via agent or standalone server
```

### Bundling with Agent
- Dashboard built as static files
- Served by agent's HTTP server
- Embedded in macOS app bundle
