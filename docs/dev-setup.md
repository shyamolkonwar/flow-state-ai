# Development Setup Guide

## Prerequisites

### Required Software
- **macOS**: 12 (Monterey) or later
- **Docker Desktop**: Latest version ([Download](https://www.docker.com/products/docker-desktop))
- **Node.js**: v18+ ([Download](https://nodejs.org/))
- **Python**: 3.10+ (for agent development)
- **Chrome**: Latest version
- **Git**: For version control

### Optional Tools
- **VS Code**: Recommended IDE
- **Postman**: For API testing
- **pgAdmin**: For database inspection

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/flow-state-ai.git
cd flow-state-ai
```

### 2. Start Local Supabase

```bash
# Navigate to infra directory
cd infra/supabase

# Start Supabase with Docker Compose
docker-compose up -d

# Wait for services to be ready (~30 seconds)
docker-compose ps

# Apply database migrations
docker exec -i supabase-db psql -U postgres -d postgres < migrations/001_initial_schema.sql
```

**Verify Supabase is running**:
```bash
curl http://localhost:54321/rest/v1/
# Should return API information
```

**Supabase Credentials** (local dev):
- **Database URL**: `postgresql://postgres:postgres@localhost:54322/postgres`
- **API URL**: `http://localhost:54321`
- **Service Key**: (generated on first start, check logs)

### 3. Set Up Agent

```bash
cd ../../agent

# Create virtual environment (Python)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create config file
mkdir -p ~/Library/Application\ Support/FlowFacilitator
cp config.example.json ~/Library/Application\ Support/FlowFacilitator/config.json

# Edit config with your local settings
nano ~/Library/Application\ Support/FlowFacilitator/config.json
```

**Example config.json**:
```json
{
  "supabase": {
    "url": "http://localhost:54321",
    "service_key": "your-service-key-here",
    "max_retries": 3
  },
  "agent": {
    "api_port": 8765,
    "api_token": "local_dev_token_12345",
    "log_level": "debug"
  },
  "native_messaging": {
    "host_name": "com.flowfacilitator.helper",
    "manifest_path": "~/Library/Application Support/Google/Chrome/NativeMessagingHosts/"
  }
}
```

### 4. Set Up Chrome Extension

```bash
cd ../chrome-extension

# Install dependencies (if any)
npm install

# Build extension
npm run build
```

**Load Extension in Chrome**:
1. Open Chrome
2. Navigate to `chrome://extensions/`
3. Enable "Developer mode" (top right toggle)
4. Click "Load unpacked"
5. Select `flow-state-ai/chrome-extension/` directory
6. Note the Extension ID (you'll need it for native messaging)

**Set up Native Messaging Host**:
```bash
# Create native messaging host manifest
mkdir -p ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/

cat > ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.flowfacilitator.helper.json << EOF
{
  "name": "com.flowfacilitator.helper",
  "description": "FlowFacilitator Native Messaging Host",
  "path": "$(pwd)/agent/native-host.py",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://YOUR_EXTENSION_ID/"
  ]
}
EOF

# Replace YOUR_EXTENSION_ID with actual ID from Chrome
```

### 5. Set Up Dashboard

```bash
cd ../dashboard/ui

# Install dependencies
npm install

# Create .env file
cat > .env << EOF
VITE_SUPABASE_URL=http://localhost:54321
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_AGENT_API_URL=http://localhost:8765
VITE_AGENT_API_TOKEN=local_dev_token_12345
EOF

# Start development server
npm run dev
```

Dashboard should open at `http://localhost:3000`

## Running the Complete System

### Start All Services

**Terminal 1 - Supabase**:
```bash
cd infra/supabase
docker-compose up
```

**Terminal 2 - Agent**:
```bash
cd agent
source venv/bin/activate
python main.py --dev
```

**Terminal 3 - Dashboard**:
```bash
cd dashboard/ui
npm run dev
```

### Verify Everything is Running

1. **Supabase**: `curl http://localhost:54321/rest/v1/`
2. **Agent API**: `curl http://localhost:8765/health`
3. **Dashboard**: Open `http://localhost:3000` in browser
4. **Extension**: Check `chrome://extensions/` - should show "Connected"

## Development Workflows

### Making Changes to Agent

```bash
cd agent

# Make your changes
nano src/metrics_engine.py

# Run tests
pytest tests/

# Run agent in debug mode
python main.py --dev --debug
```

### Making Changes to Extension

```bash
cd chrome-extension

# Make your changes
nano background.js

# Reload extension in Chrome
# Go to chrome://extensions/ and click reload icon
```

### Making Changes to Dashboard

```bash
cd dashboard/ui

# Make your changes
nano src/components/SessionList.jsx

# Vite will auto-reload
# Check browser at http://localhost:3000
```

### Database Changes

```bash
cd infra/supabase/migrations

# Create new migration
cat > 002_add_feature.sql << EOF
-- Your SQL here
ALTER TABLE sessions ADD COLUMN new_field TEXT;
EOF

# Apply migration
docker exec -i supabase-db psql -U postgres -d postgres < migrations/002_add_feature.sql

# Or restart Supabase (applies all migrations)
docker-compose down
docker-compose up -d
```

## Testing

### Unit Tests

```bash
# Agent tests
cd agent
pytest tests/unit/

# Dashboard tests
cd dashboard/ui
npm test

# Extension tests
cd chrome-extension
npm test
```

### Integration Tests

```bash
# Run full integration test suite
cd tests/integration
pytest test_flow_detection.py
```

### Manual Testing

Follow the [QA Checklist](qa-checklist.md) for comprehensive manual testing.

## Debugging

### Agent Debugging

**View Logs**:
```bash
tail -f ~/Library/Application\ Support/FlowFacilitator/logs/agent.log
```

**Debug Mode**:
```bash
cd agent
python main.py --dev --debug
# Enables verbose logging and disables some protections
```

### Database Debugging

**Connect to Postgres**:
```bash
docker exec -it supabase-db psql -U postgres -d postgres
```

**Query sessions**:
```sql
SELECT * FROM sessions ORDER BY start_ts DESC LIMIT 10;
```

**Check events**:
```sql
SELECT type, COUNT(*) FROM events GROUP BY type;
```

### Extension Debugging

1. Open Chrome DevTools
2. Go to Extensions → FlowFacilitator Helper
3. Click "background page" link
4. Check Console for messages

### Network Debugging

**Monitor local traffic**:
```bash
# Watch agent API calls
sudo tcpdump -i lo0 -A 'port 8765'

# Watch Supabase traffic
sudo tcpdump -i lo0 -A 'port 54321'
```

## Common Issues

### Issue: Supabase won't start

**Solution**:
```bash
# Check if ports are in use
lsof -i :54321
lsof -i :54322

# Kill conflicting processes or change ports in docker-compose.yml
docker-compose down
docker-compose up -d
```

### Issue: Agent can't connect to Supabase

**Solution**:
```bash
# Verify Supabase is running
docker-compose ps

# Check connection
curl http://localhost:54321/rest/v1/

# Verify service key in config.json
cat ~/Library/Application\ Support/FlowFacilitator/config.json
```

### Issue: Extension not connecting

**Solution**:
1. Check native messaging manifest path
2. Verify extension ID matches in manifest
3. Check extension console for errors
4. Restart Chrome

### Issue: Dashboard won't load

**Solution**:
```bash
# Check if agent API is running
curl http://localhost:8765/health

# Check Vite dev server
cd dashboard/ui
npm run dev

# Clear browser cache and reload
```

## Useful Scripts

### Reset Database
```bash
cd scripts
./reset-db.sh
# Drops all tables and reapplies migrations
```

### Start All Services
```bash
cd scripts
./start-local.sh
# Starts Supabase, Agent, and Dashboard
```

### Stop All Services
```bash
cd scripts
./stop-local.sh
# Stops all services gracefully
```

### Generate Test Data
```bash
cd scripts
python generate-test-data.py
# Creates synthetic sessions for testing
```

## IDE Setup (VS Code)

### Recommended Extensions
- Python
- ESLint
- Prettier
- PostgreSQL
- Docker
- GitLens

### Workspace Settings

Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "./agent/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

## Environment Variables

### Agent
- `SUPABASE_URL`: Supabase API URL
- `SUPABASE_KEY`: Service key
- `LOG_LEVEL`: debug/info/warning/error
- `DEV_MODE`: true/false

### Dashboard
- `VITE_SUPABASE_URL`: Supabase URL
- `VITE_SUPABASE_ANON_KEY`: Anon key
- `VITE_AGENT_API_URL`: Agent API URL
- `VITE_AGENT_API_TOKEN`: API token

## Next Steps

1. ✅ Complete setup above
2. 📖 Read component specs (agent/spec.md, etc.)
3. 🧪 Run test suite to verify setup
4. 💻 Start development!

## Getting Help

- Check logs first
- Review component specs
- Search GitHub issues
- Ask in team chat
