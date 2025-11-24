#!/usr/bin/osascript
# Enable Do Not Disturb Focus mode on macOS

tell application "System Events"
    # Try to enable Do Not Disturb focus
    try
        do shell script "shortcuts run 'Turn On Do Not Disturb'" with administrator privileges
    on error
        # Fallback: Use Focus control
        try
            tell application "System Preferences"
                reveal pane id "com.apple.preference.notifications"
            end tell
        end try
    end try
end tell
