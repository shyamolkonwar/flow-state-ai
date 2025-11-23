"""
Login/Signup Window for FlowFacilitator
Premium authentication UI with glassmorphism effects
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QCheckBox, QStackedWidget, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from pathlib import Path

from .components import (
    PremiumButton, RoundLogo, GradientLabel, AnimatedWidget
)
from .styles import (
    get_window_style, get_label_style, get_line_edit_style,
    get_checkbox_style, get_separator_style, COLORS
)


class LoginWindow(QMainWindow):
    """
    Login/Signup window with tab switching
    Premium design matching onboarding aesthetic
    """
    
    login_successful = pyqtSignal()
    signup_successful = pyqtSignal()
    
    def __init__(self, auth_service):
        super().__init__()
        self.auth = auth_service
        
        self.setWindowTitle("Welcome to FlowFacilitator")
        self.setFixedSize(500, 650)
        
        # Set window flags
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
        
        # Logo
        logo_path = Path(__file__).parent.parent.parent.parent / 'icons' / 'AppIcon.png'
        if logo_path.exists():
            logo = RoundLogo(str(logo_path), size=80)
        else:
            logo = RoundLogo("", size=80)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo)
        
        # Tab switcher
        tab_layout = QHBoxLayout()
        tab_layout.setSpacing(0)
        
        self.login_tab_btn = QPushButton("Login")
        self.login_tab_btn.setStyleSheet(self._get_tab_style(active=True))
        self.login_tab_btn.clicked.connect(lambda: self._switch_tab(0))
        self.login_tab_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.signup_tab_btn = QPushButton("Sign Up")
        self.signup_tab_btn.setStyleSheet(self._get_tab_style(active=False))
        self.signup_tab_btn.clicked.connect(lambda: self._switch_tab(1))
        self.signup_tab_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        tab_layout.addWidget(self.login_tab_btn)
        tab_layout.addWidget(self.signup_tab_btn)
        
        main_layout.addLayout(tab_layout)
        
        # Stacked widget for login/signup forms
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)
        
        # Create forms
        self._create_login_form()
        self._create_signup_form()
        
        # Error message label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['magenta']};
                font-size: 13px;
                padding: 8px;
                background-color: {COLORS['surface_elev']};
                border-radius: 6px;
            }}
        """)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        main_layout.addWidget(self.error_label)
        
        # Current tab
        self.current_tab = 0
        
        # Fade in animation
        self.fade_in()
    
    def _get_tab_style(self, active: bool) -> str:
        """Get tab button style"""
        if active:
            return f"""
                QPushButton {{
                    background-color: {COLORS['teal']};
                    color: {COLORS['deep_night']};
                    border: none;
                    border-radius: 8px 8px 0 0;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 600;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: {COLORS['surface_elev']};
                    color: {COLORS['text_secondary']};
                    border: none;
                    border-radius: 8px 8px 0 0;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['surface_light']};
                    color: {COLORS['text_on_dark']};
                }}
            """
    
    def _create_login_form(self):
        """Create login form"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        
        # Email input
        email_label = QLabel("Email")
        email_label.setStyleSheet(get_label_style('body'))
        layout.addWidget(email_label)
        
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("your@email.com")
        self.login_email.setStyleSheet(get_line_edit_style())
        layout.addWidget(self.login_email)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet(get_label_style('body'))
        layout.addWidget(password_label)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("••••••••")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setStyleSheet(get_line_edit_style())
        layout.addWidget(self.login_password)
        
        # Remember me checkbox
        self.remember_me = QCheckBox("Remember me")
        self.remember_me.setStyleSheet(get_checkbox_style())
        self.remember_me.setChecked(True)
        layout.addWidget(self.remember_me)
        
        # Login button
        self.login_btn = PremiumButton("Login", variant='primary')
        self.login_btn.clicked.connect(self._handle_login)
        layout.addWidget(self.login_btn)
        
        # Forgot password link
        forgot_link = QLabel('<a href="#" style="color: ' + COLORS['cyan'] + ';">Forgot password?</a>')
        forgot_link.setStyleSheet(get_label_style('secondary'))
        forgot_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        forgot_link.linkActivated.connect(self._show_forgot_password)
        layout.addWidget(forgot_link)
        
        layout.addStretch()
        
        self.pages.addWidget(page)
    
    def _create_signup_form(self):
        """Create signup form"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        
        # Full name input
        name_label = QLabel("Full Name")
        name_label.setStyleSheet(get_label_style('body'))
        layout.addWidget(name_label)
        
        self.signup_name = QLineEdit()
        self.signup_name.setPlaceholderText("John Doe")
        self.signup_name.setStyleSheet(get_line_edit_style())
        layout.addWidget(self.signup_name)
        
        # Email input
        email_label = QLabel("Email")
        email_label.setStyleSheet(get_label_style('body'))
        layout.addWidget(email_label)
        
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("your@email.com")
        self.signup_email.setStyleSheet(get_line_edit_style())
        layout.addWidget(self.signup_email)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet(get_label_style('body'))
        layout.addWidget(password_label)
        
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("••••••••")
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_password.setStyleSheet(get_line_edit_style())
        self.signup_password.textChanged.connect(self._update_password_strength)
        layout.addWidget(self.signup_password)
        
        # Password strength indicator
        self.password_strength = QLabel("")
        self.password_strength.setStyleSheet(get_label_style('secondary'))
        self.password_strength.hide()
        layout.addWidget(self.password_strength)
        
        # Confirm password input
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet(get_label_style('body'))
        layout.addWidget(confirm_label)
        
        self.signup_confirm = QLineEdit()
        self.signup_confirm.setPlaceholderText("••••••••")
        self.signup_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_confirm.setStyleSheet(get_line_edit_style())
        layout.addWidget(self.signup_confirm)
        
        # Terms checkbox
        self.terms_checkbox = QCheckBox("I agree to the Terms & Privacy Policy")
        self.terms_checkbox.setStyleSheet(get_checkbox_style())
        layout.addWidget(self.terms_checkbox)
        
        # Signup button
        self.signup_btn = PremiumButton("Create Account", variant='primary')
        self.signup_btn.clicked.connect(self._handle_signup)
        layout.addWidget(self.signup_btn)
        
        layout.addStretch()
        
        self.pages.addWidget(page)
    
    def _switch_tab(self, index: int):
        """Switch between login and signup tabs"""
        self.current_tab = index
        self.pages.setCurrentIndex(index)
        
        # Update tab button styles
        if index == 0:
            self.login_tab_btn.setStyleSheet(self._get_tab_style(active=True))
            self.signup_tab_btn.setStyleSheet(self._get_tab_style(active=False))
        else:
            self.login_tab_btn.setStyleSheet(self._get_tab_style(active=False))
            self.signup_tab_btn.setStyleSheet(self._get_tab_style(active=True))
        
        # Clear error
        self.error_label.hide()
    
    def _update_password_strength(self, password: str):
        """Update password strength indicator"""
        if not password:
            self.password_strength.hide()
            return
        
        strength = 0
        if len(password) >= 8:
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.islower() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength += 1
        
        if strength <= 2:
            self.password_strength.setText("Weak password")
            self.password_strength.setStyleSheet(f"QLabel {{ color: {COLORS['magenta']}; font-size: 12px; }}")
        elif strength <= 3:
            self.password_strength.setText("Medium password")
            self.password_strength.setStyleSheet(f"QLabel {{ color: {COLORS['gold']}; font-size: 12px; }}")
        else:
            self.password_strength.setText("Strong password")
            self.password_strength.setStyleSheet(f"QLabel {{ color: {COLORS['teal']}; font-size: 12px; }}")
        
        self.password_strength.show()
    
    def _handle_login(self):
        """Handle login button click"""
        email = self.login_email.text().strip()
        password = self.login_password.text()
        
        # Validation
        if not email or not password:
            self._show_error("Please enter email and password")
            return
        
        # Disable button and show loading
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")
        
        # Attempt login
        success, error = self.auth.sign_in(email, password)
        
        if success:
            self.login_successful.emit()
            self.close()
        else:
            self._show_error(error or "Login failed")
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Login")
    
    def _handle_signup(self):
        """Handle signup button click"""
        name = self.signup_name.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text()
        confirm = self.signup_confirm.text()
        
        # Validation
        if not name or not email or not password:
            self._show_error("Please fill in all fields")
            return
        
        if password != confirm:
            self._show_error("Passwords do not match")
            return
        
        if len(password) < 8:
            self._show_error("Password must be at least 8 characters")
            return
        
        if not self.terms_checkbox.isChecked():
            self._show_error("Please agree to the Terms & Privacy Policy")
            return
        
        # Disable button and show loading
        self.signup_btn.setEnabled(False)
        self.signup_btn.setText("Creating account...")
        
        # Attempt signup
        success, error = self.auth.sign_up(email, password, name)
        
        if success:
            self.signup_successful.emit()
            self.close()
        else:
            self._show_error(error or "Signup failed")
            self.signup_btn.setEnabled(True)
            self.signup_btn.setText("Create Account")
    
    def _show_error(self, message: str):
        """Show error message"""
        self.error_label.setText(message)
        self.error_label.show()
    
    def _show_forgot_password(self):
        """Show forgot password dialog"""
        # This would open a ForgotPasswordWindow
        # For now, just show a message
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Password Reset",
            "Password reset functionality will be implemented soon.\nPlease contact support for assistance."
        )
    
    def fade_in(self):
        """Fade in animation when window opens"""
        self.setWindowOpacity(0.0)
        self.show()
        
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(400)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
