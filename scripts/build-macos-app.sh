#!/bin/bash

# FlowFacilitator - Build macOS App Bundle

set -e

echo "🔨 Building FlowFacilitator macOS App..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Build directory
BUILD_DIR="$PROJECT_ROOT/build"
APP_NAME="FlowFacilitator.app"
APP_PATH="$BUILD_DIR/$APP_NAME"

# Clean build directory
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Create app bundle structure
mkdir -p "$APP_PATH/Contents/MacOS"
mkdir -p "$APP_PATH/Contents/Resources"
mkdir -p "$APP_PATH/Contents/Frameworks"

echo "📦 Creating app bundle structure..."

# Create Info.plist
cat > "$APP_PATH/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>FlowFacilitator</string>
    <key>CFBundleIdentifier</key>
    <string>com.flowfacilitator.app</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>FlowFacilitator</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>LSMinimumSystemVersion</key>
    <string>12.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSAppleEventsUsageDescription</key>
    <string>FlowFacilitator needs to monitor your activity to detect flow states.</string>
    <key>NSSystemAdministrationUsageDescription</key>
    <string>FlowFacilitator needs to control Do Not Disturb and manage distractions.</string>
</dict>
</plist>
EOF

echo "📝 Created Info.plist"

# Copy agent code
echo "📂 Copying agent code..."
cp -r "$PROJECT_ROOT/agent" "$APP_PATH/Contents/Resources/"

# Create launcher script
cat > "$APP_PATH/Contents/MacOS/FlowFacilitator" << 'EOF'
#!/bin/bash

# Get the directory where the app is located
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RESOURCES_DIR="$APP_DIR/Resources"

# Set up Python path
export PYTHONPATH="$RESOURCES_DIR/agent:$PYTHONPATH"

# Run the agent in development mode with UI
cd "$RESOURCES_DIR/agent"
python3 main.py --dev --ui
EOF

chmod +x "$APP_PATH/Contents/MacOS/FlowFacilitator"

echo "✅ Launcher script created"

# Copy application icon
if [ -f "$PROJECT_ROOT/icons/AppIcon.png" ]; then
    cp "$PROJECT_ROOT/icons/AppIcon.png" "$APP_PATH/Contents/Resources/AppIcon.png"
    echo "✅ Custom icon copied to app bundle"
else
    echo "⚠️  Warning: Custom icon not found at $PROJECT_ROOT/icons/AppIcon.png"
fi

echo ""
echo "✅ macOS App Bundle created successfully!"
echo ""
echo "Location: $APP_PATH"
echo ""
echo "To install:"
echo "1. Copy to /Applications: cp -r '$APP_PATH' /Applications/"
echo "2. Grant Accessibility permissions in System Preferences"
echo "3. Run from Applications folder"
echo ""
echo "Note: App is not signed. To sign:"
echo "codesign --deep --force --verify --verbose --sign 'Developer ID' '$APP_PATH'"
