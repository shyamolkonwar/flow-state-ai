"""
Test the login window independently
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from src.auth_service import AuthService
from src.ui.login_window import LoginWindow
from src.config import load_config


def test_login_window():
    """Test the login window"""
    print("Loading config...")
    config = load_config(dev_mode=True)
    
    print("Initializing auth service...")
    auth = AuthService(config)
    
    print("Creating Qt application...")
    app = QApplication(sys.argv)
    
    print("Creating login window...")
    window = LoginWindow(auth)
    window.show()
    
    print("Login window displayed. Close it to exit.")
    sys.exit(app.exec())


if __name__ == '__main__':
    test_login_window()
