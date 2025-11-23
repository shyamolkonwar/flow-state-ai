"""
Utility functions for Mac UI
"""

import os
import json
import subprocess
import webbrowser
from pathlib import Path
from typing import Dict, Tuple
import requests


def get_app_support_dir() -> Path:
    """Get the Application Support directory for FlowFacilitator"""
    app_support = Path.home() / 'Library' / 'Application Support' / 'FlowFacilitator'
    app_support.mkdir(parents=True, exist_ok=True)
    return app_support


def get_preferences_path() -> Path:
    """Get the preferences file path"""
    return get_app_support_dir() / 'preferences.json'


def is_first_run() -> bool:
    """Check if this is the first run of the app"""
    prefs_path = get_preferences_path()
    if not prefs_path.exists():
        return True
    
    try:
        with open(prefs_path, 'r') as f:
            prefs = json.load(f)
            return not prefs.get('onboarding_complete', False)
    except (json.JSONDecodeError, IOError):
        return True


def mark_onboarding_complete():
    """Mark onboarding as completed"""
    prefs_path = get_preferences_path()
    prefs = {}
    
    if prefs_path.exists():
        try:
            with open(prefs_path, 'r') as f:
                prefs = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    prefs['onboarding_complete'] = True
    
    with open(prefs_path, 'w') as f:
        json.dump(prefs, f, indent=2)


def get_preference(key: str, default=None):
    """Get a preference value"""
    prefs_path = get_preferences_path()
    
    if not prefs_path.exists():
        return default
    
    try:
        with open(prefs_path, 'r') as f:
            prefs = json.load(f)
            return prefs.get(key, default)
    except (json.JSONDecodeError, IOError):
        return default


def set_preference(key: str, value):
    """Set a preference value"""
    prefs_path = get_preferences_path()
    prefs = {}
    
    if prefs_path.exists():
        try:
            with open(prefs_path, 'r') as f:
                prefs = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    prefs[key] = value
    
    with open(prefs_path, 'w') as f:
        json.dump(prefs, f, indent=2)


def check_accessibility_permission() -> bool:
    """Check if Accessibility permission is granted"""
    try:
        # Use AppleScript to check accessibility
        script = '''
        tell application "System Events"
            return get UI elements enabled
        end tell
        '''
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip().lower() == 'true'
    except Exception:
        return False


def check_input_monitoring_permission() -> bool:
    """Check if Input Monitoring permission is granted"""
    # This is harder to check programmatically
    # We'll rely on the agent's ability to monitor input
    # For now, return a placeholder
    return get_preference('input_monitoring_granted', False)


def check_screen_recording_permission() -> bool:
    """Check if Screen Recording permission is granted (optional)"""
    return get_preference('screen_recording_granted', False)


def check_permissions() -> Dict[str, bool]:
    """Check all macOS permissions"""
    return {
        'accessibility': check_accessibility_permission(),
        'input_monitoring': check_input_monitoring_permission(),
        'screen_recording': check_screen_recording_permission()
    }


def open_system_preferences(pane: str = 'security'):
    """Open System Settings to a specific pane"""
    pane_urls = {
        'security': 'x-apple.systempreferences:com.apple.preference.security?Privacy',
        'accessibility': 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility',
        'input_monitoring': 'x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent',
        'screen_recording': 'x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture',
    }
    
    url = pane_urls.get(pane, pane_urls['security'])
    
    try:
        subprocess.run(['open', url], check=True)
    except subprocess.CalledProcessError:
        # Fallback to opening System Settings
        subprocess.run(['open', '-a', 'System Settings'], check=False)


def get_agent_status(port: int = 8765) -> Dict:
    """Get agent status from API"""
    try:
        response = requests.get(f'http://localhost:{port}/status', timeout=2)
        if response.status_code == 200:
            return response.json()
    except (requests.RequestException, json.JSONDecodeError):
        pass
    
    return {
        'agent_running': False,
        'flow_state': 'idle',
        'permissions': check_permissions()
    }


def start_agent():
    """Start the FlowFacilitator agent"""
    # This will be implemented to start the agent process
    # For now, it's a placeholder
    pass


def stop_agent():
    """Stop the FlowFacilitator agent"""
    # This will be implemented to stop the agent process
    # For now, it's a placeholder
    pass


def open_dashboard(port: int = 3001):
    """Open the dashboard in the default browser"""
    url = f'http://localhost:{port}'
    webbrowser.open(url)


def open_extension_guide():
    """Open the Chrome extension setup guide"""
    # This could open a local HTML file or a web URL
    guide_path = Path(__file__).parent.parent.parent / 'docs' / 'extension-setup.md'
    
    if guide_path.exists():
        subprocess.run(['open', str(guide_path)], check=False)
    else:
        # Fallback to opening the docs directory
        docs_path = Path(__file__).parent.parent.parent / 'docs'
        if docs_path.exists():
            subprocess.run(['open', str(docs_path)], check=False)


def get_version_info() -> Dict[str, str]:
    """Get version information"""
    # Read from a version file or return defaults
    version_file = Path(__file__).parent.parent.parent / 'version.json'
    
    default_info = {
        'app_version': '1.0.0',
        'agent_version': '1.0.0',
        'build_date': '2025-11-23'
    }
    
    if version_file.exists():
        try:
            with open(version_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    return default_info


def setup_auto_start(enabled: bool):
    """Setup auto-start on login"""
    # This would use LaunchAgents on macOS
    # For now, just store the preference
    set_preference('auto_start', enabled)
    
    # TODO: Implement LaunchAgent plist creation/removal
    # launch_agents_dir = Path.home() / 'Library' / 'LaunchAgents'
    # plist_path = launch_agents_dir / 'com.flowfacilitator.agent.plist'
