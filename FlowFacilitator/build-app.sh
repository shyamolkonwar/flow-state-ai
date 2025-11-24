#!/bin/bash
# Build FlowFacilitator.app and create DMG

set -e

echo "🔨 Building FlowFacilitator..."

# Navigate to project directory
cd "$(dirname "$0")/FlowFacilitator"

# Clean build folder
rm -rf build/
rm -rf DerivedData/

# Build the app for release
xcodebuild -scheme FlowFacilitator \
    -configuration Release \
    -derivedDataPath DerivedData \
    -destination 'platform=macOS' \
    clean build

# Find the built app
APP_PATH="DerivedData/Build/Products/Release/FlowFacilitator.app"

if [ ! -d "$APP_PATH" ]; then
    echo "❌ Build failed - app not found at $APP_PATH"
    exit 1
fi

echo "✅ Build successful!"
echo "📦 App location: $APP_PATH"

# Create DMG
echo "📦 Creating DMG..."

DMG_NAME="FlowFacilitator.dmg"
VOLUME_NAME="FlowFacilitator"

# Remove old DMG if exists
rm -f "../$DMG_NAME"

# Create temporary directory for DMG contents
TMP_DIR=$(mktemp -d)
cp -R "$APP_PATH" "$TMP_DIR/"

# Create DMG
hdiutil create -volname "$VOLUME_NAME" \
    -srcfolder "$TMP_DIR" \
    -ov -format UDZO \
    "../$DMG_NAME"

# Clean up
rm -rf "$TMP_DIR"

echo "✅ DMG created: $(pwd)/../$DMG_NAME"
echo ""
echo "To install:"
echo "1. Open FlowFacilitator.dmg"
echo "2. Drag FlowFacilitator.app to /Applications"
echo "3. Open System Settings > Privacy & Security > Accessibility"
echo "4. Add FlowFacilitator.app to the list"
