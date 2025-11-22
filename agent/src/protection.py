"""
Protection Controller - Manages DND and extension blocking
"""

import logging
import subprocess
import json
from typing import Dict, List


class ProtectionController:
    """Controls macOS DND and Chrome extension blocking"""
    
    def __init__(self, config: Dict):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.dnd_enabled = False
        self.blocking_enabled = False
    
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
        """Enable macOS Do Not Disturb"""
        try:
            # Method 1: Using defaults command (macOS 12+)
            subprocess.run([
                'defaults', 'write',
                'com.apple.controlcenter', 'NSStatusItem Visible FocusModes',
                '-bool', 'true'
            ], check=False)
            
            # Enable Focus mode
            subprocess.run([
                'defaults', '-currentHost', 'write',
                '~/Library/Preferences/ByHost/com.apple.notificationcenterui',
                'doNotDisturb', '-boolean', 'true'
            ], check=False)
            
            # Restart Notification Center
            subprocess.run(['killall', 'NotificationCenter'], check=False)
            
            self.dnd_enabled = True
            self.logger.info("DND enabled")
            
        except Exception as e:
            self.logger.error(f"Failed to enable DND: {e}")
    
    def disable_dnd(self):
        """Disable macOS Do Not Disturb"""
        try:
            subprocess.run([
                'defaults', '-currentHost', 'write',
                '~/Library/Preferences/ByHost/com.apple.notificationcenterui',
                'doNotDisturb', '-boolean', 'false'
            ], check=False)
            
            subprocess.run(['killall', 'NotificationCenter'], check=False)
            
            self.dnd_enabled = False
            self.logger.info("DND disabled")
            
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
            
            # TODO: Send via native messaging
            # For now, just log
            self.logger.info(f"Would send to extension: {message}")
            self.blocking_enabled = True
            
        except Exception as e:
            self.logger.error(f"Failed to enable blocking: {e}")
    
    def disable_blocking(self):
        """Send disable blocking command to Chrome extension"""
        try:
            message = {
                'cmd': 'disable_blocking'
            }
            
            # TODO: Send via native messaging
            self.logger.info(f"Would send to extension: {message}")
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
