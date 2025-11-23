"""
Test script for Mac UI
Tests the UI components without requiring the full agent
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from src.ui.preferences_window import PreferencesWindow
from src.ui.onboarding_window import OnboardingWindow


def test_preferences_window():
    """Test the preferences window"""
    print("Testing Preferences Window...")
    app = QApplication(sys.argv)
    
    window = PreferencesWindow()
    window.show()
    
    sys.exit(app.exec())


def test_onboarding_window():
    """Test the onboarding window"""
    print("Testing Onboarding Window...")
    app = QApplication(sys.argv)
    
    window = OnboardingWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Mac UI components')
    parser.add_argument('--preferences', action='store_true', help='Test preferences window')
    parser.add_argument('--onboarding', action='store_true', help='Test onboarding window')
    
    args = parser.parse_args()
    
    if args.preferences:
        test_preferences_window()
    elif args.onboarding:
        test_onboarding_window()
    else:
        print("Usage:")
        print("  python test_ui.py --preferences   # Test preferences window")
        print("  python test_ui.py --onboarding    # Test onboarding window")
