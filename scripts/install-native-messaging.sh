#!/bin/bash

# FlowFacilitator - Install Native Messaging Host

set -e

echo "📦 Installing FlowFacilitator Native Messaging Host..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Paths
AGENT_PATH="$PROJECT_ROOT/agent/main.py"
MANIFEST_SRC="$PROJECT_ROOT/chrome-extension/com.flowfacilitator.helper.json"
MANIFEST_DEST="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.flowfacilitator.helper.json"

# Create directory
mkdir -p "$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"

# Get extension ID
echo ""
echo "To complete setup, you need your Chrome extension ID."
echo "1. Open chrome://extensions/"
echo "2. Enable 'Developer mode'"
echo "3. Load the extension from: $PROJECT_ROOT/chrome-extension/"
echo "4. Copy the extension ID (it looks like: abcdefghijklmnopqrstuvwxyz123456)"
echo ""
read -p "Enter your extension ID: " EXTENSION_ID

# Create manifest with correct paths and extension ID
cat > "$MANIFEST_DEST" << EOF
{
  "name": "com.flowfacilitator.helper",
  "description": "FlowFacilitator Native Messaging Host",
  "path": "$AGENT_PATH",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://$EXTENSION_ID/"
  ]
}
EOF

echo "✅ Native messaging host installed!"
echo ""
echo "Manifest location: $MANIFEST_DEST"
echo "Agent path: $AGENT_PATH"
echo "Extension ID: $EXTENSION_ID"
echo ""
echo "Next steps:"
echo "1. Make sure the agent is running: cd $PROJECT_ROOT/agent && python main.py --dev"
echo "2. Reload the Chrome extension"
echo "3. Check the extension console for connection status"
