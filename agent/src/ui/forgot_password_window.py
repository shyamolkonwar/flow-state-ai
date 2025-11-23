"""
Forgot Password Window for FlowFacilitator
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from pathlib import Path

from .components import PremiumButton, RoundLogo
from .styles import get_window_style, get_label_style, get_line_edit_style, COLORS


class ForgotPasswordWindow(QMainWindow):
    """Forgot password window"""
    
    reset_sent = pyqtSignal()
    
    def __init__(self, auth_service):
        super().__init__()
        self.auth = auth_service
        
        self.setWindowTitle("Reset Password")
        self.setFixedSize(400, 450)
        
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowCloseButtonHint
        )
        
        self.setStyleSheet(get_window_style())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        # Logo
        logo_path = Path(__file__).parent.parent.parent.parent / 'icons' / 'AppIcon.png'
        if logo_path.exists():
            logo = RoundLogo(str(logo_path), size=60)
        else:
            logo = RoundLogo("", size=60)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        # Title
        title = QLabel("Reset Password")
        title.setStyleSheet(get_label_style('heading'))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Enter your email address and we'll send you a link to reset your password.")
        desc.setStyleSheet(get_label_style('body'))
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Email input
        email_label = QLabel("Email")
        email_label.setStyleSheet(get_label_style('body'))
        layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your@email.com")
        self.email_input.setStyleSheet(get_line_edit_style())
        layout.addWidget(self.email_input)
        
        # Send button
        self.send_btn = PremiumButton("Send Reset Link", variant='primary')
        self.send_btn.clicked.connect(self._handle_reset)
        layout.addWidget(self.send_btn)
        
        # Back link
        back_link = QLabel('<a href="#" style="color: ' + COLORS['cyan'] + ';">Back to login</a>')
        back_link.setStyleSheet(get_label_style('secondary'))
        back_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_link.linkActivated.connect(self.close)
        layout.addWidget(back_link)
        
        # Error/success message
        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        self.message_label.hide()
        layout.addWidget(self.message_label)
        
        layout.addStretch()
        
        self.fade_in()
    
    def _handle_reset(self):
        """Handle reset button click"""
        email = self.email_input.text().strip()
        
        if not email:
            self._show_error("Please enter your email address")
            return
        
        self.send_btn.setEnabled(False)
        self.send_btn.setText("Sending...")
        
        success, error = self.auth.reset_password(email)
        
        if success:
            self._show_success("Password reset link sent! Check your email.")
            self.reset_sent.emit()
        else:
            self._show_error(error or "Failed to send reset link")
            self.send_btn.setEnabled(True)
            self.send_btn.setText("Send Reset Link")
    
    def _show_error(self, message: str):
        """Show error message"""
        self.message_label.setText(message)
        self.message_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['magenta']};
                font-size: 13px;
                padding: 8px;
                background-color: {COLORS['surface_elev']};
                border-radius: 6px;
            }}
        """)
        self.message_label.show()
    
    def _show_success(self, message: str):
        """Show success message"""
        self.message_label.setText(message)
        self.message_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['teal']};
                font-size: 13px;
                padding: 8px;
                background-color: {COLORS['surface_elev']};
                border-radius: 6px;
            }}
        """)
        self.message_label.show()
    
    def fade_in(self):
        """Fade in animation"""
        self.setWindowOpacity(0.0)
        self.show()
        
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
