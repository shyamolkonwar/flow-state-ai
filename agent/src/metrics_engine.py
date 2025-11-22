"""
Rolling Metrics Engine - Computes real-time metrics from events
"""

import logging
import time
from collections import deque
from typing import Dict


class RollingMetrics:
    """Maintains sliding windows and computes metrics"""
    
    def __init__(self, typing_window: int = 60, rolling_window: int = 300):
        self.logger = logging.getLogger(__name__)
        
        # Window sizes (seconds)
        self.typing_window = typing_window
        self.rolling_window = rolling_window
        
        # Event storage (timestamp, event_type)
        self.keystrokes = deque()
        self.app_switches = deque()
        self.idle_periods = deque()
        
        # Current metrics
        self._typing_rate = 0.0
        self._app_switch_count = 0
        self._max_idle_gap = 0.0
        
        # Last event time for idle detection
        self.last_event_time = time.time()
    
    def add_keystroke(self, timestamp: float):
        """Add a keystroke event"""
        self.keystrokes.append(timestamp)
        self.last_event_time = timestamp
        self._cleanup_old_events()
    
    def add_app_switch(self, timestamp: float):
        """Add an app switch event"""
        self.app_switches.append(timestamp)
        self._cleanup_old_events()
    
    def add_idle_period(self, start_time: float, end_time: float):
        """Add an idle period"""
        duration = end_time - start_time
        self.idle_periods.append((start_time, duration))
        self._cleanup_old_events()
    
    def update_from_event(self, event):
        """Update metrics from an event"""
        if event.type == 'keystroke':
            self.add_keystroke(event.timestamp)
        elif event.type == 'app_switch':
            self.add_app_switch(event.timestamp)
        elif event.type in ['mouse_move', 'mouse_click']:
            self.last_event_time = event.timestamp
    
    def _cleanup_old_events(self):
        """Remove events outside the rolling window"""
        current_time = time.time()
        cutoff_time = current_time - self.rolling_window
        
        # Remove old keystrokes
        while self.keystrokes and self.keystrokes[0] < cutoff_time:
            self.keystrokes.popleft()
        
        # Remove old app switches
        while self.app_switches and self.app_switches[0] < cutoff_time:
            self.app_switches.popleft()
        
        # Remove old idle periods
        while self.idle_periods and self.idle_periods[0][0] < cutoff_time:
            self.idle_periods.popleft()
    
    def get_typing_rate(self) -> float:
        """Get keystrokes per minute (averaged over typing window)"""
        current_time = time.time()
        cutoff_time = current_time - self.typing_window
        
        # Count keystrokes in the typing window
        recent_keystrokes = sum(1 for ts in self.keystrokes if ts >= cutoff_time)
        
        # Convert to per-minute rate
        self._typing_rate = (recent_keystrokes / self.typing_window) * 60
        return self._typing_rate
    
    def get_app_switch_count(self) -> int:
        """Get number of app switches in rolling window"""
        self._app_switch_count = len(self.app_switches)
        return self._app_switch_count
    
    def get_max_idle_gap(self) -> float:
        """Get maximum idle gap in rolling window"""
        if not self.idle_periods:
            # Check current idle time
            current_idle = time.time() - self.last_event_time
            self._max_idle_gap = current_idle
        else:
            # Get max from recorded idle periods
            self._max_idle_gap = max(duration for _, duration in self.idle_periods)
        
        return self._max_idle_gap
    
    def get_current_idle_time(self) -> float:
        """Get current idle time (seconds since last event)"""
        return time.time() - self.last_event_time
    
    def get_all_metrics(self) -> Dict[str, float]:
        """Get all current metrics"""
        return {
            'typing_rate': self.get_typing_rate(),
            'app_switch_count': self.get_app_switch_count(),
            'max_idle_gap': self.get_max_idle_gap(),
            'current_idle': self.get_current_idle_time()
        }
    
    def reset(self):
        """Reset all metrics"""
        self.keystrokes.clear()
        self.app_switches.clear()
        self.idle_periods.clear()
        self._typing_rate = 0.0
        self._app_switch_count = 0
        self._max_idle_gap = 0.0
