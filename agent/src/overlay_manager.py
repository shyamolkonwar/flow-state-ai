"""
Overlay Manager - Creates full-screen overlays for distraction blocking
"""

import logging
import time
from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk
import threading


class OverlayWindow:
    """Full-screen overlay window for blocking distractions"""
    
    def __init__(self, app_name: str, on_unlock: Optional[Callable] = None):
        self.logger = logging.getLogger(__name__)
        self.app_name = app_name
        self.on_unlock = on_unlock
        self.countdown_seconds = 10
        self.window = None
        self.countdown_active = True
        
    def show(self):
        """Show the overlay window"""
        self.window = tk.Tk()
        self.window.title("FlowFacilitator - Flow Protection")
        
        # Make it full screen and always on top
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-topmost', True)
        self.window.configure(bg='#1f2937')
        
        # Prevent closing with standard methods
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Main container
        container = tk.Frame(self.window, bg='#1f2937')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Icon
        icon_label = tk.Label(
            container,
            text="🎯",
            font=('Arial', 80),
            bg='#1f2937',
            fg='white'
        )
        icon_label.pack(pady=(0, 20))
        
        # Title
        title_label = tk.Label(
            container,
            text="You are in Flow",
            font=('Arial', 48, 'bold'),
            bg='#1f2937',
            fg='white'
        )
        title_label.pack(pady=(0, 10))
        
        # Message
        message_label = tk.Label(
            container,
            text=f"You tried to open: {self.app_name}",
            font=('Arial', 20),
            bg='#1f2937',
            fg='#9ca3af'
        )
        message_label.pack(pady=(0, 30))
        
        # Question
        question_label = tk.Label(
            container,
            text="Break it?",
            font=('Arial', 32),
            bg='#1f2937',
            fg='#f59e0b'
        )
        question_label.pack(pady=(0, 20))
        
        # Countdown label
        self.countdown_label = tk.Label(
            container,
            text=f"Unlock available in {self.countdown_seconds}s",
            font=('Arial', 18),
            bg='#1f2937',
            fg='#6b7280'
        )
        self.countdown_label.pack(pady=(0, 30))
        
        # Unlock button (initially disabled)
        self.unlock_button = tk.Button(
            container,
            text="Unlock (disabled)",
            font=('Arial', 16, 'bold'),
            bg='#374151',
            fg='#9ca3af',
            padx=40,
            pady=15,
            state='disabled',
            cursor='arrow'
        )
        self.unlock_button.pack(pady=(0, 20))
        
        # Stay in flow button
        stay_button = tk.Button(
            container,
            text="Stay in Flow",
            font=('Arial', 16, 'bold'),
            bg='#10b981',
            fg='white',
            padx=40,
            pady=15,
            command=self._stay_in_flow,
            cursor='hand2'
        )
        stay_button.pack()
        
        # Stats
        stats_label = tk.Label(
            container,
            text="Resisting distractions builds your Resilience stat! 💪",
            font=('Arial', 14),
            bg='#1f2937',
            fg='#667eea',
            pady=20
        )
        stats_label.pack()
        
        # Start countdown
        self._start_countdown()
        
        # Run the window
        self.window.mainloop()
    
    def _start_countdown(self):
        """Start the countdown timer"""
        def countdown():
            remaining = self.countdown_seconds
            while remaining > 0 and self.countdown_active:
                self.countdown_label.config(text=f"Unlock available in {remaining}s")
                time.sleep(1)
                remaining -= 1
            
            if self.countdown_active:
                # Enable unlock button
                self.countdown_label.config(text="You can now unlock")
                self.unlock_button.config(
                    text="Unlock and Break Flow",
                    bg='#ef4444',
                    fg='white',
                    state='normal',
                    cursor='hand2',
                    command=self._unlock
                )
        
        thread = threading.Thread(target=countdown, daemon=True)
        thread.start()
    
    def _unlock(self):
        """Handle unlock button click"""
        self.countdown_active = False
        if self.on_unlock:
            self.on_unlock(broke_flow=True)
        self.window.destroy()
    
    def _stay_in_flow(self):
        """Handle stay in flow button click"""
        self.countdown_active = False
        if self.on_unlock:
            self.on_unlock(broke_flow=False)
        self.window.destroy()
    
    def close(self):
        """Close the overlay"""
        self.countdown_active = False
        if self.window:
            self.window.destroy()


class OverlayManager:
    """Manages overlay windows for distraction blocking"""
    
    def __init__(self, on_flow_broken: Optional[Callable] = None):
        self.logger = logging.getLogger(__name__)
        self.on_flow_broken = on_flow_broken
        self.active_overlay = None
        self.blocked_apps = set()
        
    def set_blocked_apps(self, apps: list):
        """Set the list of apps to block with overlay"""
        self.blocked_apps = set(apps)
        self.logger.info(f"Blocking {len(apps)} apps with overlay")
    
    def should_block_app(self, app_name: str) -> bool:
        """Check if an app should be blocked"""
        if not app_name:
            return False
        
        app_lower = app_name.lower()
        for blocked in self.blocked_apps:
            if blocked.lower() in app_lower:
                return True
        return False
    
    def show_overlay_for_app(self, app_name: str):
        """Show overlay for a blocked app"""
        if self.active_overlay:
            self.logger.warning("Overlay already active")
            return
        
        self.logger.info(f"Showing overlay for blocked app: {app_name}")
        
        def on_unlock(broke_flow: bool):
            self.active_overlay = None
            if broke_flow and self.on_flow_broken:
                self.on_flow_broken(app_name)
            elif not broke_flow:
                self.logger.info(f"User resisted distraction: {app_name} (Resilience +1)")
        
        # Create and show overlay in separate thread
        def show_overlay():
            self.active_overlay = OverlayWindow(app_name, on_unlock)
            self.active_overlay.show()
        
        thread = threading.Thread(target=show_overlay, daemon=True)
        thread.start()
    
    def close_overlay(self):
        """Close any active overlay"""
        if self.active_overlay:
            self.active_overlay.close()
            self.active_overlay = None
