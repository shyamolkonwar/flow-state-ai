#!/bin/bash

# FlowFacilitator - Complete Installation Script

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║          FlowFacilitator Installation                 ║"
echo "║          Version 1.0.0                                 ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Installation directory
INSTALL_DIR="$HOME/Library/Application Support/FlowFacilitator"
CONFIG_FILE="$INSTALL_DIR/config.json"

echo "📍 Installation directory: $INSTALL_DIR"
echo ""

# Step 1: Check prerequisites
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1/6: Checking prerequisites..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.10 or later from https://www.python.org/"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi
echo "✅ Docker found: $(docker --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

echo ""

# Step 2: Create directories
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2/6: Creating directories..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/logs"
mkdir -p "$INSTALL_DIR/data"

echo "✅ Directories created"
echo ""

# Step 3: Install Python dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3/6: Installing Python dependencies..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$PROJECT_ROOT/agent"
python3 -m pip install -r requirements.txt --quiet

echo "✅ Python dependencies installed"
echo ""

# Step 4: Set up Supabase
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4/6: Setting up Supabase..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$PROJECT_ROOT/infra/supabase"

# Generate secure keys
JWT_SECRET=$(openssl rand -base64 32)
SERVICE_KEY=$(openssl rand -base64 32)
ANON_KEY=$(openssl rand -base64 32)
SECRET_KEY_BASE=$(openssl rand -base64 64)

# Create .env file
cat > .env << EOF
JWT_SECRET=$JWT_SECRET
SERVICE_ROLE_KEY=$SERVICE_KEY
ANON_KEY=$ANON_KEY
SECRET_KEY_BASE=$SECRET_KEY_BASE
EOF

echo "✅ Supabase environment configured"

# Start Supabase
docker-compose up -d

echo "⏳ Waiting for Supabase to start..."
sleep 15

# Apply migrations
echo "📝 Applying database migrations..."
docker exec -i supabase-db psql -U postgres -d postgres < migrations/001_initial_schema.sql
docker exec -i supabase-db psql -U postgres -d postgres < migrations/002_gamification.sql

echo "✅ Supabase is running"
echo ""

# Step 5: Create configuration
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5/6: Creating configuration..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cat > "$CONFIG_FILE" << EOF
{
  "supabase": {
    "url": "http://localhost:54321",
    "service_key": "$SERVICE_KEY",
    "max_retries": 3
  },
  "agent": {
    "api_port": 8765,
    "api_token": "local_dev_token_12345",
    "log_level": "info"
  },
  "native_messaging": {
    "host_name": "com.flowfacilitator.helper",
    "manifest_path": "~/Library/Application Support/Google/Chrome/NativeMessagingHosts/"
  },
  "flow_detection": {
    "enabled": true,
    "check_interval_seconds": 1
  }
}
EOF

echo "✅ Configuration created at: $CONFIG_FILE"
echo ""

# Step 6: Install Dashboard
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6/6: Installing Dashboard..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$PROJECT_ROOT/dashboard/ui"

# Create .env file
cat > .env << EOF
VITE_SUPABASE_URL=http://localhost:54321
VITE_SUPABASE_ANON_KEY=$ANON_KEY
VITE_AGENT_API_URL=http://localhost:8765
VITE_AGENT_API_TOKEN=local_dev_token_12345
EOF

npm install --silent

echo "✅ Dashboard installed"
echo ""

# Installation complete
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║          ✅ Installation Complete!                     ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Install Chrome Extension:"
echo "   - Open chrome://extensions/"
echo "   - Enable 'Developer mode'"
echo "   - Click 'Load unpacked'"
echo "   - Select: $PROJECT_ROOT/chrome-extension/"
echo ""
echo "2. Set up Native Messaging:"
echo "   - Run: $PROJECT_ROOT/scripts/install-native-messaging.sh"
echo ""
echo "3. Grant Accessibility Permissions:"
echo "   - Open System Preferences → Security & Privacy → Privacy"
echo "   - Select 'Accessibility'"
echo "   - Add Terminal (or your terminal app)"
echo ""
echo "4. Start FlowFacilitator:"
echo "   - Agent: cd $PROJECT_ROOT/agent && python3 main.py"
echo "   - Dashboard: cd $PROJECT_ROOT/dashboard/ui && npm run dev"
echo ""
echo "5. Open Dashboard:"
echo "   - Visit: http://localhost:3000"
echo ""
echo "📚 Documentation:"
echo "   - User Guide: $PROJECT_ROOT/docs/onboarding.md"
echo "   - Dev Setup: $PROJECT_ROOT/docs/dev-setup.md"
echo ""
echo "🎉 Enjoy your flow states!"
