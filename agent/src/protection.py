"""
Protection Controller - Manages DND and extension blocking
"""

import logging
import subprocess
import json
from typing import Dict, List


class ProtectionController:
    """Controls macOS DND and Chrome extension blocking"""
    
    def __init__(self, config: Dict, native_messaging_host=None):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.dnd_enabled = False
        self.blocking_enabled = False
        self.native_messaging = native_messaging_host
    
    def enable_protection(self, blocklist: List[str]):
        """Enable all protection mechanisms"""
        self.logger.info("Enabling protection...")
        
        # Enable DND
        self.enable_dnd()
        
        # Enable extension blocking
        self.enable_blocking(blocklist)
    
    def disable_protection(self):
        """Disable all protection mechanisms"""
        self.logger.info("Disabling protection...")
        
        # Disable DND
        self.disable_dnd()
        
        # Disable extension blocking
        self.disable_blocking()
    
    def enable_dnd(self):
        """Enable macOS Do Not Disturb using Focus mode"""
        try:
            # Use shortcuts to enable Focus mode (macOS 12+)
            # This requires creating a shortcut first, but we'll use AppleScript as fallback
            script = '''
            tell application "System Events"
                tell process "ControlCenter"
                    -- Try to enable Focus mode via Control Center
                    set frontmost to true
                end tell
            end tell
            '''
            
            # Alternative: Use shortcuts command (if shortcut exists)
            result = subprocess.run(
                ['shortcuts', 'run', 'Enable Do Not Disturb'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.dnd_enabled = True
                self.logger.info("DND enabled via Shortcuts")
                return
            
            # Fallback: Try using defaults (may not work on all macOS versions)
            subprocess.run([
                'defaults', 'write',
                'com.apple.controlcenter', 'NSStatusItem Visible DoNotDisturb',
                '-bool', 'true'
            ], check=False, timeout=5)
            
            self.dnd_enabled = True
            self.logger.info("DND enabled (attempted)")
            
        except subprocess.TimeoutExpired:
            self.logger.warning("DND enable command timed out")
        except Exception as e:
            self.logger.error(f"Failed to enable DND: {e}")
    
    def disable_dnd(self):
        """Disable macOS Do Not Disturb"""
        try:
            # Use shortcuts to disable Focus mode
            result = subprocess.run(
                ['shortcuts', 'run', 'Disable Do Not Disturb'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.dnd_enabled = False
                self.logger.info("DND disabled via Shortcuts")
                return
            
            # Fallback
            subprocess.run([
                'defaults', 'write',
                'com.apple.controlcenter', 'NSStatusItem Visible DoNotDisturb',
                '-bool', 'false'
            ], check=False, timeout=5)
            
            self.dnd_enabled = False
            self.logger.info("DND disabled (attempted)")
            
        except subprocess.TimeoutExpired:
            self.logger.warning("DND disable command timed out")
        except Exception as e:
            self.logger.error(f"Failed to disable DND: {e}")
    
    def enable_blocking(self, domains: List[str]):
        """Send enable blocking command to Chrome extension"""
        try:
            message = {
                'cmd': 'enable_blocking',
                'domains': domains,
                'ttl_seconds': 3600
            }
            
            # Send via native messaging
            if self.native_messaging:
                self.native_messaging.send_command('enable_blocking', domains=domains, ttl_seconds=3600)
                self.logger.info(f"Sent blocking command to extension: {len(domains)} domains")
            else:
                self.logger.warning(f"Native messaging not available, cannot send to extension: {message}")
            
            self.blocking_enabled = True
            
        except Exception as e:
            self.logger.error(f"Failed to enable blocking: {e}")
    
    def disable_blocking(self):
        """Send disable blocking command to Chrome extension"""
        try:
            # Send via native messaging
            if self.native_messaging:
                self.native_messaging.send_command('disable_blocking')
                self.logger.info("Sent disable blocking command to extension")
            else:
                self.logger.warning("Native messaging not available, cannot disable blocking")
            
            self.blocking_enabled = False
            
        except Exception as e:
            self.logger.error(f"Failed to disable blocking: {e}")
    
    def update_blocklist(self, domains: List[str]):
        """Update the blocklist in the extension"""
        try:
            message = {
                'cmd': 'update_blocklist',
                'domains': domains
            }
            
            # TODO: Send via native messaging
            self.logger.info(f"Would send to extension: {message}")
            
        except Exception as e:
            self.logger.error(f"Failed to update blocklist: {e}")
    
    def is_protection_active(self) -> bool:
        """Check if protection is currently active"""
        return self.dnd_enabled or self.blocking_enabled
