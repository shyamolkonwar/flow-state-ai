"""
FlowFacilitator Mac UI
Menu bar app with status indicators and window management
"""

import sys
import rumps
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from .ui.preferences_window import PreferencesWindow
from .ui.onboarding_window import OnboardingWindow
from .ui.login_window import LoginWindow
from .ui.utils import (
    is_first_run, get_agent_status, open_dashboard,
    check_permissions
)
from .ui.styles import STATUS_COLORS
from .auth_service import AuthService
from .user_settings import UserSettingsManager
from .config import load_config


class FlowFacilitatorApp(rumps.App):
    """
    Menu bar application for FlowFacilitator
    Shows status indicators and provides quick access to features
    """
    
    def __init__(self, config=None, dev_mode=False):
        # Load config if not provided
        if config is None:
            config = load_config(dev_mode=dev_mode)
        self.config = config
        
        # Initialize auth service
        self.auth = AuthService(config)
        
        # Initialize settings manager
        from supabase import create_client
        supabase_client = create_client(
            config['supabase']['url'],
            config['supabase'].get('anon_key') or config['supabase']['service_key']
        )
        self.settings = UserSettingsManager(self.auth, supabase_client)
        
        # Get icon path
        icon_path = self._get_icon_path('idle')
        
        super().__init__(
            "FlowFacilitator",
            icon=icon_path,
            quit_button=None  # We'll add custom quit
        )
        
        # Store Qt application
        self.qt_app = None
        
        # Windows
        self.preferences_window = None
        self.onboarding_window = None
        self.login_window = None
        
        # Current status
        self.current_status = 'idle'
        
        # Setup menu
        self._setup_menu()
        
        # Setup status update timer
        self.status_timer = rumps.Timer(self._update_status, 3)
        self.status_timer.start()
        
        # Start settings auto-sync if authenticated
        if self.auth.is_authenticated():
            self.settings.start_auto_sync()
        
        # Handle first launch / authentication
        self._handle_first_launch()
    
    def _setup_menu(self):
        """Setup menu bar items"""
        # Open Dashboard
        self.menu.add(rumps.MenuItem(
            "Open Dashboard",
            callback=self._open_dashboard
        ))
        
        self.menu.add(rumps.separator)
        
        # Agent Status
        self.status_item = rumps.MenuItem("Agent Status: Idle")
        self.menu.add(self.status_item)
        
        self.menu.add(rumps.separator)
        
        # Permissions Status
        permissions_menu = rumps.MenuItem("Permissions")
        self.accessibility_item = rumps.MenuItem("Accessibility: ✖")
        self.input_monitoring_item = rumps.MenuItem("Input Monitoring: ✖")
        self.screen_recording_item = rumps.MenuItem("Screen Recording: ✖")
        
        permissions_menu.add(self.accessibility_item)
        permissions_menu.add(self.input_monitoring_item)
        permissions_menu.add(self.screen_recording_item)
        
        self.menu.add(permissions_menu)
        
        self.menu.add(rumps.separator)
        
        # Agent Control
        self.start_stop_item = rumps.MenuItem(
            "Start Agent",
            callback=self._toggle_agent
        )
        self.menu.add(self.start_stop_item)
        
        self.menu.add(rumps.MenuItem(
            "Restart Agent",
            callback=self._restart_agent
        ))
        
        self.menu.add(rumps.separator)
        
        # Preferences
        self.menu.add(rumps.MenuItem(
            "Preferences...",
            callback=self._show_preferences
        ))
        
        self.menu.add(rumps.separator)
        
        # Quit
        self.menu.add(rumps.MenuItem(
            "Quit FlowFacilitator",
            callback=self._quit_app
        ))
    
    def _get_icon_path(self, status: str) -> str:
        """Get icon path for status"""
        # Use generated menu bar icons
        icon_dir = Path(__file__).parent.parent / 'assets' / 'menu_icons'
        icon_path = icon_dir / f'{status}.png'

        if icon_path.exists():
            return str(icon_path)

        # Fallback to app icon in Resources
        fallback_path = Path(__file__).parent.parent.parent / 'AppIcon.png'
        if fallback_path.exists():
            return str(fallback_path)

        return None
    
    def _update_status(self, _):
        """Update agent status and menu items"""
        status = get_agent_status()
        
        # Update agent status
        flow_state = status.get('flow_state', 'idle')
        self.current_status = flow_state
        
        status_text = {
            'idle': 'Idle',
            'tracking': 'Tracking',
            'flow': 'In Flow'
        }.get(flow_state, 'Idle')
        
        self.status_item.title = f"Agent Status: {status_text}"
        
        # Update icon based on status
        icon_path = self._get_icon_path(flow_state)
        if icon_path:
            self.icon = icon_path
        
        # Update permissions
        permissions = status.get('permissions', {})
        
        self.accessibility_item.title = f"Accessibility: {'✓' if permissions.get('accessibility') else '✖'}"
        self.input_monitoring_item.title = f"Input Monitoring: {'✓' if permissions.get('input_monitoring') else '✖'}"
        self.screen_recording_item.title = f"Screen Recording: {'✓' if permissions.get('screen_recording') else '✖'}"
        
        # Update start/stop button
        if status.get('agent_running'):
            self.start_stop_item.title = "Stop Agent"
        else:
            self.start_stop_item.title = "Start Agent"
    
    def _handle_first_launch(self):
        """Handle first launch - show login, then onboarding or main app"""
        # Check if user is authenticated
        if not self.auth.is_authenticated():
            # Show login window
            rumps.Timer(lambda _: self._show_login(), 0.5, repeat=False).start()
        else:
            # User is authenticated, check onboarding status
            onboarding_complete, _ = self.auth.get_onboarding_status()
            
            if not onboarding_complete:
                # Show onboarding
                rumps.Timer(lambda _: self._show_onboarding(), 0.5, repeat=False).start()
            # else: Main app is ready (menu bar is already showing)
    
    def _open_dashboard(self, _):
        """Open dashboard in browser"""
        open_dashboard()
    
    def _toggle_agent(self, sender):
        """Start or stop the agent"""
        status = get_agent_status()
        
        if status.get('agent_running'):
            # Stop agent
            from .ui.utils import stop_agent
            stop_agent()
            sender.title = "Start Agent"
        else:
            # Start agent
            from .ui.utils import start_agent
            start_agent()
            sender.title = "Stop Agent"
    
    def _restart_agent(self, _):
        """Restart the agent"""
        from .ui.utils import stop_agent, start_agent
        stop_agent()
        # Wait a bit before restarting
        rumps.Timer(lambda _: start_agent(), 1, repeat=False).start()
    
    def _show_login(self):
        """Show login window"""
        if not self.qt_app:
            self.qt_app = QApplication.instance() or QApplication(sys.argv)
        
        if self.login_window is None or not self.login_window.isVisible():
            self.login_window = LoginWindow(self.auth)
            self.login_window.login_successful.connect(self._on_login_success)
            self.login_window.signup_successful.connect(self._on_signup_success)
            self.login_window.show()
            self.login_window.raise_()
            self.login_window.activateWindow()
    
    def _on_login_success(self):
        """Handle successful login"""
        # Start settings sync
        self.settings.start_auto_sync()
        
        # Sync settings from cloud
        self.settings.sync_from_cloud()
        
        # Check onboarding status
        onboarding_complete, _ = self.auth.get_onboarding_status()
        
        if not onboarding_complete:
            # Show onboarding
            self._show_onboarding()
        # else: Main app is ready
    
    def _on_signup_success(self):
        """Handle successful signup"""
        # Start settings sync
        self.settings.start_auto_sync()
        
        # Always show onboarding for new users
        self._show_onboarding()
    
    def _show_preferences(self, _):
        """Show preferences window"""
        if not self.qt_app:
            self.qt_app = QApplication.instance() or QApplication(sys.argv)
        
        if self.preferences_window is None or not self.preferences_window.isVisible():
            self.preferences_window = PreferencesWindow()
            self.preferences_window.show()
            self.preferences_window.raise_()
            self.preferences_window.activateWindow()
    
    def _show_onboarding(self):
        """Show onboarding window"""
        if not self.qt_app:
            self.qt_app = QApplication.instance() or QApplication(sys.argv)
        
        if self.onboarding_window is None or not self.onboarding_window.isVisible():
            self.onboarding_window = OnboardingWindow(self.auth, self.settings)
            self.onboarding_window.completed.connect(self._onboarding_completed)
            self.onboarding_window.show()
            self.onboarding_window.raise_()
            self.onboarding_window.activateWindow()
    
    def _onboarding_completed(self):
        """Handle onboarding completion"""
        # Onboarding is complete, user can now use the app
        pass
    
    def _quit_app(self, _):
        """Quit the application"""
        # Stop settings sync
        self.settings.stop_auto_sync()
        
        # Stop agent
        from .ui.utils import stop_agent
        stop_agent()
        
        # Quit rumps app
        rumps.quit_application()


def run_mac_ui(config=None, dev_mode=False):
    """Run the Mac UI application"""
    app = FlowFacilitatorApp(config, dev_mode)
    app.run()


if __name__ == '__main__':
    run_mac_ui()
