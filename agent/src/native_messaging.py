"""
Native Messaging Host - Handles communication with Chrome extension
"""

import sys
import json
import struct
import logging
import threading
from typing import Callable, Optional


class NativeMessagingHost:
    """Native messaging host for Chrome extension communication"""
    
    def __init__(self, on_message: Optional[Callable] = None):
        self.logger = logging.getLogger(__name__)
        self.on_message = on_message
        self.running = False
        self.listener_thread = None
    
    def start(self):
        """Start listening for messages from Chrome extension"""
        self.running = True
        self.listener_thread = threading.Thread(target=self._listen, daemon=True)
        self.listener_thread.start()
        self.logger.info("Native messaging host started")
    
    def stop(self):
        """Stop listening"""
        self.running = False
        self.logger.info("Native messaging host stopped")
    
    def _listen(self):
        """Listen for messages on stdin"""
        while self.running:
            try:
                message = self._read_message()
                if message:
                    self.logger.debug(f"Received message: {message}")
                    response = self._handle_message(message)
                    if response:
                        self._send_message(response)
            except Exception as e:
                self.logger.error(f"Error in native messaging: {e}")
                break
    
    def _read_message(self):
        """Read a message from stdin"""
        try:
            # Read message length (4 bytes)
            raw_length = sys.stdin.buffer.read(4)
            if not raw_length:
                return None
            
            message_length = struct.unpack('=I', raw_length)[0]
            
            # Read message
            message = sys.stdin.buffer.read(message_length).decode('utf-8')
            return json.loads(message)
        except Exception as e:
            self.logger.error(f"Error reading message: {e}")
            return None
    
    def _send_message(self, message: dict):
        """Send a message to stdout"""
        try:
            encoded_message = json.dumps(message).encode('utf-8')
            encoded_length = struct.pack('=I', len(encoded_message))
            
            sys.stdout.buffer.write(encoded_length)
            sys.stdout.buffer.write(encoded_message)
            sys.stdout.buffer.flush()
            
            self.logger.debug(f"Sent message: {message}")
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
    
    def _handle_message(self, message: dict) -> Optional[dict]:
        """Handle incoming message and return response"""
        if self.on_message:
            return self.on_message(message)
        return None
    
    def send_command(self, command: str, **kwargs):
        """Send a command to the extension"""
        message = {
            'cmd': command,
            **kwargs
        }
        self._send_message(message)


def create_native_messaging_manifest(agent_path: str, manifest_path: str):
    """
    Create native messaging host manifest file
    
    Args:
        agent_path: Absolute path to the agent executable
        manifest_path: Where to save the manifest
    """
    manifest = {
        "name": "com.flowfacilitator.helper",
        "description": "FlowFacilitator Native Messaging Host",
        "path": agent_path,
        "type": "stdio",
        "allowed_origins": [
            "chrome-extension://YOUR_EXTENSION_ID/"
        ]
    }
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
