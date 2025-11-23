"""
Preferences Window for FlowFacilitator
Premium UI with glassmorphism effects and smooth animations
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QLineEdit, QScrollArea, QFrame, QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from .components import (
    PremiumButton, PermissionCard, SectionHeader,
    InfoCard, AnimatedWidget
)
from .styles import (
    get_window_style, get_label_style, get_checkbox_style,
    get_line_edit_style, get_scroll_area_style, get_separator_style,
    COLORS
)
from .utils import (
    check_permissions, open_system_preferences, open_dashboard,
    get_version_info, get_preference, set_preference, setup_auto_start
)


class PreferencesWindow(QMainWindow):
    """
    Preferences window (400x550px) with four sections:
    - App Overview
    - System Permissions
    - Agent Settings
    - Version Info
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlowFacilitator Preferences")
        self.setFixedSize(450, 600)
        
        # Set window flags for Mac-style window
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.WindowMinimizeButtonHint
        )
        
        # Apply window style
        self.setStyleSheet(get_window_style())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("Preferences")
        title.setStyleSheet(get_label_style('heading'))
        main_layout.addWidget(title)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(get_scroll_area_style())
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(24)
        
        # Add sections
        self._add_overview_section(content_layout)
        self._add_separator(content_layout)
        self._add_permissions_section(content_layout)
        self._add_separator(content_layout)
        self._add_agent_settings_section(content_layout)
        self._add_separator(content_layout)
        self._add_version_section(content_layout)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Setup auto-refresh for permissions
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self._refresh_permissions)
        self.refresh_timer.start(3000)  # Refresh every 3 seconds
        
        # Fade in animation
        self.fade_in()
    
    def _add_overview_section(self, layout: QVBoxLayout):
        """Add App Overview section"""
        header = SectionHeader("App Overview")
        layout.addWidget(header)
        
        card = InfoCard()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        
        description = QLabel("FlowFacilitator is running in the background,\nhelping you detect and protect your flow state.")
        description.setStyleSheet(get_label_style('body'))
        description.setWordWrap(True)
        card_layout.addWidget(description)
        
        # Open Dashboard button
        dashboard_btn = PremiumButton("Open Dashboard", variant='primary')
        dashboard_btn.clicked.connect(lambda: open_dashboard())
        card_layout.addWidget(dashboard_btn)
        
        layout.addWidget(card)
    
    def _add_permissions_section(self, layout: QVBoxLayout):
        """Add System Permissions section"""
        header = SectionHeader("System Permissions")
        layout.addWidget(header)
        
        permissions = check_permissions()
        
        # Accessibility
        self.accessibility_card = PermissionCard(
            "Accessibility",
            permissions.get('accessibility', False),
            optional=False
        )
        if not permissions.get('accessibility', False):
            self.accessibility_card.grant_button.clicked.connect(
                lambda: open_system_preferences('accessibility')
            )
        layout.addWidget(self.accessibility_card)
        
        # Input Monitoring
        self.input_monitoring_card = PermissionCard(
            "Input Monitoring",
            permissions.get('input_monitoring', False),
            optional=False
        )
        if not permissions.get('input_monitoring', False):
            self.input_monitoring_card.grant_button.clicked.connect(
                lambda: open_system_preferences('input_monitoring')
            )
        layout.addWidget(self.input_monitoring_card)
        
        # Screen Recording
        self.screen_recording_card = PermissionCard(
            "Screen Recording",
            permissions.get('screen_recording', False),
            optional=True
        )
        if not permissions.get('screen_recording', False):
            self.screen_recording_card.grant_button.clicked.connect(
                lambda: open_system_preferences('screen_recording')
            )
        layout.addWidget(self.screen_recording_card)
        
        # Warning message if permissions missing
        if not all([permissions.get('accessibility'), permissions.get('input_monitoring')]):
            warning = QLabel("⚠ Some essential permissions are missing.\nGrant them for full functionality.")
            warning.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['gold']};
                    font-size: 13px;
                    padding: 8px;
                    background-color: {COLORS['surface_elev']};
                    border-radius: 6px;
                }}
            """)
            layout.addWidget(warning)
    
    def _add_agent_settings_section(self, layout: QVBoxLayout):
        """Add Agent Settings section"""
        header = SectionHeader("Agent Settings")
        layout.addWidget(header)
        
        card = InfoCard()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        
        # Auto-start checkbox
        auto_start = QCheckBox("Auto-start Agent on Login")
        auto_start.setStyleSheet(get_checkbox_style())
        auto_start.setChecked(get_preference('auto_start', False))
        auto_start.stateChanged.connect(
            lambda state: setup_auto_start(state == Qt.CheckState.Checked.value)
        )
        card_layout.addWidget(auto_start)
        
        # Dashboard port (read-only)
        port_layout = QHBoxLayout()
        port_label = QLabel("Dashboard Port:")
        port_label.setStyleSheet(get_label_style('body'))
        port_input = QLineEdit("3001")
        port_input.setReadOnly(True)
        port_input.setStyleSheet(get_line_edit_style())
        port_input.setFixedWidth(100)
        port_layout.addWidget(port_label)
        port_layout.addWidget(port_input)
        port_layout.addStretch()
        card_layout.addLayout(port_layout)
        
        # Agent port (read-only)
        agent_port_layout = QHBoxLayout()
        agent_port_label = QLabel("Agent Port:")
        agent_port_label.setStyleSheet(get_label_style('body'))
        agent_port_input = QLineEdit("8765")
        agent_port_input.setReadOnly(True)
        agent_port_input.setStyleSheet(get_line_edit_style())
        agent_port_input.setFixedWidth(100)
        agent_port_layout.addWidget(agent_port_label)
        agent_port_layout.addWidget(agent_port_input)
        agent_port_layout.addStretch()
        card_layout.addLayout(agent_port_layout)
        
        layout.addWidget(card)
    
    def _add_version_section(self, layout: QVBoxLayout):
        """Add Version Info section"""
        header = SectionHeader("Version Info")
        layout.addWidget(header)
        
        card = InfoCard()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        
        version_info = get_version_info()
        
        # App version
        app_version = QLabel(f"App Version: {version_info['app_version']}")
        app_version.setStyleSheet(get_label_style('body'))
        card_layout.addWidget(app_version)
        
        # Agent version
        agent_version = QLabel(f"Agent Version: {version_info['agent_version']}")
        agent_version.setStyleSheet(get_label_style('body'))
        card_layout.addWidget(agent_version)
        
        # Build date
        build_date = QLabel(f"Build Date: {version_info['build_date']}")
        build_date.setStyleSheet(get_label_style('secondary'))
        card_layout.addWidget(build_date)
        
        layout.addWidget(card)
    
    def _add_separator(self, layout: QVBoxLayout):
        """Add a horizontal separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(get_separator_style())
        layout.addWidget(separator)
    
    def _refresh_permissions(self):
        """Refresh permission status"""
        permissions = check_permissions()
        
        # Update accessibility card
        if hasattr(self, 'accessibility_card'):
            self.accessibility_card.granted = permissions.get('accessibility', False)
            # Recreate the card to update UI
            # (In a production app, we'd update the existing card)
        
        # Similar for other permissions
        # This is a simplified version
    
    def fade_in(self):
        """Fade in animation when window opens"""
        self.setWindowOpacity(0.0)
        self.show()
        
        # Animate opacity
        from PyQt6.QtCore import QPropertyAnimation
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
    
    def closeEvent(self, event):
        """Handle window close with fade out"""
        # Stop refresh timer
        self.refresh_timer.stop()
        
        # Accept the close event
        event.accept()
