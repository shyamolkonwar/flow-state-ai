"""
Onboarding Window for FlowFacilitator
First-run experience with 4 pages and smooth animations
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QStackedWidget, QProgressBar, QPushButton
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont
from pathlib import Path

from .components import (
    PremiumButton, PermissionCard, RoundLogo, GradientLabel, AnimatedWidget
)
from .styles import (
    get_window_style, get_label_style, get_progress_bar_style,
    COLORS
)
from .utils import (
    check_permissions, open_system_preferences, open_dashboard,
    open_extension_guide, mark_onboarding_complete
)


class OnboardingWindow(QMainWindow):
    """
    First-run onboarding window (500x600px) with 4 pages:
    1. Welcome
    2. Permissions Setup
    3. Extension Setup
    4. Completion
    """
    
    completed = pyqtSignal()
    
    def __init__(self, auth_service=None, settings_manager=None):
        super().__init__()
        self.auth = auth_service
        self.settings = settings_manager
        
        self.setWindowTitle("Welcome to FlowFacilitator")
        self.setFixedSize(550, 650)
        
        # Set window flags for Mac-style window
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowCloseButtonHint
        )
        
        # Apply window style
        self.setStyleSheet(get_window_style())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(24)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(get_progress_bar_style())
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(4)
        self.progress_bar.setValue(1)
        main_layout.addWidget(self.progress_bar)
        
        # Stacked widget for pages
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)
        
        # Create pages
        self._create_welcome_page()
        self._create_permissions_page()
        self._create_extension_page()
        self._create_completion_page()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(12)
        
        self.back_button = PremiumButton("Back", variant='secondary')
        self.back_button.clicked.connect(self._go_back)
        self.back_button.hide()  # Hidden on first page
        
        nav_layout.addWidget(self.back_button)
        nav_layout.addStretch()
        
        self.next_button = PremiumButton("Get Started", variant='primary')
        self.next_button.clicked.connect(self._go_next)
        
        nav_layout.addWidget(self.next_button)
        
        main_layout.addLayout(nav_layout)
        
        # Current page
        self.current_page = 0
        
        # Fade in animation
        self.fade_in()
    
    def _create_welcome_page(self):
        """Page 1 - Welcome"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(24)
        
        # Logo
        logo_path = Path(__file__).parent.parent.parent.parent / 'icons' / 'AppIcon.png'
        if logo_path.exists():
            logo = RoundLogo(str(logo_path), size=120)
        else:
            logo = RoundLogo("", size=120)  # Will use fallback
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        # Welcome text with gradient
        welcome = GradientLabel("Welcome to FlowFacilitator")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)
        
        # Description
        description = QLabel(
            "FlowFacilitator helps you detect and protect\n"
            "your flow state on macOS.\n\n"
            "Let's get you set up in just a few steps."
        )
        description.setStyleSheet(get_label_style('body'))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        layout.addStretch()
        
        self.pages.addWidget(page)
    
    def _create_permissions_page(self):
        """Page 2 - Permissions Setup"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Grant System Permissions")
        title.setStyleSheet(get_label_style('heading'))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "FlowFacilitator needs these permissions to monitor\n"
            "your activity and protect your flow state."
        )
        description.setStyleSheet(get_label_style('body'))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)
        
        layout.addSpacing(20)
        
        # Permission cards
        permissions = check_permissions()
        
        self.accessibility_card = PermissionCard(
            "Accessibility",
            permissions.get('accessibility', False),
            optional=False
        )
        if not permissions.get('accessibility', False):
            self.accessibility_card.grant_button.clicked.connect(
                lambda: self._grant_permission('accessibility')
            )
        layout.addWidget(self.accessibility_card)
        
        self.input_monitoring_card = PermissionCard(
            "Input Monitoring",
            permissions.get('input_monitoring', False),
            optional=False
        )
        if not permissions.get('input_monitoring', False):
            self.input_monitoring_card.grant_button.clicked.connect(
                lambda: self._grant_permission('input_monitoring')
            )
        layout.addWidget(self.input_monitoring_card)
        
        self.screen_recording_card = PermissionCard(
            "Screen Recording",
            permissions.get('screen_recording', False),
            optional=True
        )
        if not permissions.get('screen_recording', False):
            self.screen_recording_card.grant_button.clicked.connect(
                lambda: self._grant_permission('screen_recording')
            )
        layout.addWidget(self.screen_recording_card)
        
        layout.addStretch()
        
        # Info text
        info = QLabel("Click 'Grant' to open System Settings for each permission.")
        info.setStyleSheet(get_label_style('secondary'))
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        self.pages.addWidget(page)
    
    def _create_extension_page(self):
        """Page 3 - Extension Setup"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(24)
        
        # Title
        title = QLabel("Install Chrome Extension")
        title.setStyleSheet(get_label_style('heading'))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "For full functionality, install the\n"
            "FlowFacilitator Chrome extension.\n\n"
            "This allows the app to detect when you're\n"
            "in a focused work session."
        )
        description.setStyleSheet(get_label_style('body'))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Extension icon/illustration
        extension_icon = QLabel("🧩")
        extension_icon.setStyleSheet("""
            QLabel {
                font-size: 80px;
            }
        """)
        extension_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(extension_icon)
        
        # Buttons
        setup_btn = PremiumButton("Open Extension Setup Guide", variant='primary')
        setup_btn.clicked.connect(open_extension_guide)
        layout.addWidget(setup_btn)
        
        skip_btn = PremiumButton("Skip for Now", variant='secondary')
        skip_btn.clicked.connect(self._go_next)
        layout.addWidget(skip_btn)
        
        layout.addStretch()
        
        self.pages.addWidget(page)
    
    def _create_completion_page(self):
        """Page 4 - Completion"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(24)
        
        # Success icon
        success_icon = QLabel("✓")
        success_icon.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['teal']};
                font-size: 100px;
                font-weight: bold;
            }}
        """)
        success_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(success_icon)
        
        # Completion message
        message = GradientLabel("You're All Set!")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)
        
        # Description
        description = QLabel(
            "FlowFacilitator is now ready to help you\n"
            "detect and protect your flow state.\n\n"
            "Open the dashboard to start tracking your productivity."
        )
        description.setStyleSheet(get_label_style('body'))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        layout.addStretch()
        
        # Open Dashboard button
        dashboard_btn = PremiumButton("Open Dashboard", variant='primary')
        dashboard_btn.clicked.connect(self._finish_onboarding)
        layout.addWidget(dashboard_btn)
        
        self.pages.addWidget(page)
    
    def _grant_permission(self, permission_type: str):
        """Open System Settings for permission"""
        open_system_preferences(permission_type)
        
        # Update button text to indicate action taken
        # In a production app, we'd poll for permission status
    
    def _go_next(self):
        """Go to next page"""
        if self.current_page < self.pages.count() - 1:
            # Check if essential permissions are granted on page 2
            if self.current_page == 1:
                permissions = check_permissions()
                if not permissions.get('accessibility') or not permissions.get('input_monitoring'):
                    # Show warning but allow to continue
                    pass
            
            self.current_page += 1
            self._animate_page_transition(self.current_page)
            self._update_navigation()
    
    def _go_back(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self._animate_page_transition(self.current_page)
            self._update_navigation()
    
    def _animate_page_transition(self, page_index: int):
        """Animate transition between pages"""
        # Update progress bar
        self.progress_bar.setValue(page_index + 1)
        
        # Slide animation
        self.pages.setCurrentIndex(page_index)
    
    def _update_navigation(self):
        """Update navigation buttons based on current page"""
        # Show/hide back button
        if self.current_page == 0:
            self.back_button.hide()
        else:
            self.back_button.show()
        
        # Update next button text
        if self.current_page == 0:
            self.next_button.setText("Get Started")
        elif self.current_page == 1:
            self.next_button.setText("Continue")
        elif self.current_page == 2:
            self.next_button.setText("Next")
        elif self.current_page == 3:
            self.next_button.hide()  # Hide on last page
    
    def _finish_onboarding(self):
        """Complete onboarding and open dashboard"""
        mark_onboarding_complete()
        
        # Sync to cloud if authenticated
        if self.auth and self.auth.is_authenticated():
            # Mark onboarding complete in cloud
            self.auth.mark_onboarding_complete()
            
            # Sync permissions to cloud
            if self.settings:
                permissions = check_permissions()
                self.settings.update_permissions(permissions, sync=True)
        
        open_dashboard()
        self.completed.emit()
        self.close()
    
    def fade_in(self):
        """Fade in animation when window opens"""
        self.setWindowOpacity(0.0)
        self.show()
        
        # Animate opacity
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(400)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
    
    def closeEvent(self, event):
        """Handle window close"""
        # Mark onboarding as complete even if user closes window
        mark_onboarding_complete()
        event.accept()
