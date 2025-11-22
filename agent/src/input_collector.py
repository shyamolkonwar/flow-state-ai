"""
Input Collector - Monitors keyboard, mouse, and application events
"""

import logging
import time
from collections import deque
from typing import Callable, Optional
from datetime import datetime
from pynput import keyboard, mouse
from AppKit import NSWorkspace


class Event:
    """Represents a user input event"""
    def __init__(self, event_type: str, timestamp: float):
        self.type = event_type
        self.timestamp = timestamp


class InputCollector:
    """Collects user input events without recording content"""
    
    def __init__(self, on_event: Optional[Callable[[Event], None]] = None):
        self.logger = logging.getLogger(__name__)
        self.on_event = on_event
        self.running = False
        
        # Event storage
        self.events = deque(maxlen=10000)  # Keep last 10k events
        
        # Listeners
        self.keyboard_listener = None
        self.mouse_listener = None
        
        # Current state
        self.current_app = None
        self.last_event_time = time.time()
        
    def start(self):
        """Start collecting events"""
        self.logger.info("Starting input collector...")
        self.running = True
        
        # Start keyboard listener
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press
        )
        self.keyboard_listener.start()
        
        # Start mouse listener
        self.mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click
        )
        self.mouse_listener.start()
        
        self.logger.info("Input collector started")
    
    def stop(self):
        """Stop collecting events"""
        self.logger.info("Stopping input collector...")
        self.running = False
        
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        
        self.logger.info("Input collector stopped")
    
    def _on_key_press(self, key):
        """Handle keyboard press (timestamp only, no content)"""
        if not self.running:
            return
        
        event = Event('keystroke', time.time())
        self.events.append(event)
        self.last_event_time = event.timestamp
        
        if self.on_event:
            self.on_event(event)
    
    def _on_mouse_move(self, x, y):
        """Handle mouse movement"""
        if not self.running:
            return
        
        # Only record movement, not position (privacy)
        event = Event('mouse_move', time.time())
        self.events.append(event)
        self.last_event_time = event.timestamp
        
        if self.on_event:
            self.on_event(event)
    
    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click"""
        if not self.running or not pressed:
            return
        
        event = Event('mouse_click', time.time())
        self.events.append(event)
        self.last_event_time = event.timestamp
        
        if self.on_event:
            self.on_event(event)
    
    def get_foreground_app(self) -> Optional[str]:
        """Get the currently active application"""
        try:
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.activeApplication()
            app_name = active_app['NSApplicationName']
            
            # Detect app switch
            if app_name != self.current_app:
                old_app = self.current_app
                self.current_app = app_name
                
                if old_app is not None:  # Not first detection
                    event = Event('app_switch', time.time())
                    event.from_app = old_app
                    event.to_app = app_name
                    self.events.append(event)
                    
                    if self.on_event:
                        self.on_event(event)
            
            return app_name
        except Exception as e:
            self.logger.error(f"Error getting foreground app: {e}")
            return None
    
    def get_idle_time(self) -> float:
        """Get time since last input event (seconds)"""
        return time.time() - self.last_event_time
    
    def get_recent_events(self, seconds: float) -> list:
        """Get events from the last N seconds"""
        cutoff_time = time.time() - seconds
        return [e for e in self.events if e.timestamp >= cutoff_time]
