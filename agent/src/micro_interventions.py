"""
Micro-Interventions - Soft resets for cognitive fatigue
"""

import logging
import time
import subprocess
import tkinter as tk
from typing import Optional
import threading


class MicroIntervention:
    """Handles micro-interventions for cognitive fatigue"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.blur_window = None
        self.intervention_active = False
        self.original_volume = None
        
    def detect_cognitive_fatigue(self, metrics: dict, history: list) -> bool:
        """
        Detect cognitive fatigue from usage patterns
        
        Indicators:
        - Erratic typing (high variance in typing rate)
        - Frequent app switching
        - Increasing idle gaps
        - Declining typing rate over time
        """
        if len(history) < 5:
            return False
        
        # Get recent metrics
        recent = history[-5:]
        typing_rates = [m.get('typing_rate', 0) for m in recent]
        idle_gaps = [m.get('max_idle_gap', 0) for m in recent]
        
        # Calculate variance in typing rate
        if typing_rates:
            avg_typing = sum(typing_rates) / len(typing_rates)
            variance = sum((x - avg_typing) ** 2 for x in typing_rates) / len(typing_rates)
            
            # High variance indicates erratic typing
            if variance > 100:
                self.logger.info(f"Cognitive fatigue detected: high typing variance ({variance:.1f})")
                return True
        
        # Check for increasing idle gaps
        if len(idle_gaps) >= 3:
            if idle_gaps[-1] > idle_gaps[-2] > idle_gaps[-3]:
                self.logger.info("Cognitive fatigue detected: increasing idle gaps")
                return True
        
        # Check for declining typing rate
        if len(typing_rates) >= 3:
            if typing_rates[-1] < typing_rates[-2] < typing_rates[-3]:
                decline = typing_rates[-3] - typing_rates[-1]
                if decline > 10:
                    self.logger.info(f"Cognitive fatigue detected: declining typing rate (-{decline:.1f} kpm)")
                    return True
        
        return False
    
    def trigger_soft_reset(self, duration_seconds: int = 30):
        """
        Trigger a soft reset intervention
        
        - Apply blur effect to screen
        - Fade out audio volume
        - Display gentle message
        """
        if self.intervention_active:
            self.logger.warning("Intervention already active")
            return
        
        self.logger.info(f"Triggering soft reset intervention ({duration_seconds}s)")
        self.intervention_active = True
        
        # Start blur effect
        self._start_blur_effect()
        
        # Fade out audio
        self._fade_audio(fade_out=True)
        
        # Wait for duration
        time.sleep(duration_seconds)
        
        # Restore
        self._stop_blur_effect()
        self._fade_audio(fade_out=False)
        
        self.intervention_active = False
        self.logger.info("Soft reset intervention complete")
    
    def _start_blur_effect(self):
        """Apply blur effect using transparent overlay"""
        def show_blur():
            self.blur_window = tk.Tk()
            self.blur_window.title("Micro-Intervention")
            
            # Full screen, transparent, always on top
            self.blur_window.attributes('-fullscreen', True)
            self.blur_window.attributes('-topmost', True)
            self.blur_window.attributes('-alpha', 0.7)  # Semi-transparent
            
            # Blur effect simulation (gray overlay)
            self.blur_window.configure(bg='#6b7280')
            
            # Message
            container = tk.Frame(self.blur_window, bg='#6b7280')
            container.place(relx=0.5, rely=0.5, anchor='center')
            
            icon = tk.Label(
                container,
                text="🧘",
                font=('Arial', 60),
                bg='#6b7280',
                fg='white'
            )
            icon.pack(pady=(0, 20))
            
            message = tk.Label(
                container,
                text="Micro-Break\nTake a deep breath",
                font=('Arial', 32),
                bg='#6b7280',
                fg='white',
                justify='center'
            )
            message.pack()
            
            submessage = tk.Label(
                container,
                text="Recharging your focus...",
                font=('Arial', 18),
                bg='#6b7280',
                fg='#d1d5db',
                pady=20
            )
            submessage.pack()
            
            self.blur_window.mainloop()
        
        thread = threading.Thread(target=show_blur, daemon=True)
        thread.start()
        time.sleep(0.5)  # Give window time to appear
    
    def _stop_blur_effect(self):
        """Remove blur effect"""
        if self.blur_window:
            self.blur_window.destroy()
            self.blur_window = None
    
    def _fade_audio(self, fade_out: bool, duration: float = 2.0):
        """
        Fade audio volume in or out
        
        Uses osascript to control macOS system volume
        """
        try:
            # Get current volume
            result = subprocess.run(
                ['osascript', '-e', 'output volume of (get volume settings)'],
                capture_output=True,
                text=True
            )
            current_volume = int(result.stdout.strip())
            
            if fade_out:
                # Store original volume
                self.original_volume = current_volume
                target_volume = 0
            else:
                # Restore original volume
                target_volume = self.original_volume or current_volume
            
            # Calculate steps
            steps = 20
            step_duration = duration / steps
            volume_step = (target_volume - current_volume) / steps
            
            # Fade
            for i in range(steps):
                new_volume = int(current_volume + (volume_step * (i + 1)))
                new_volume = max(0, min(100, new_volume))  # Clamp to 0-100
                
                subprocess.run(
                    ['osascript', '-e', f'set volume output volume {new_volume}'],
                    check=False
                )
                time.sleep(step_duration)
            
            self.logger.info(f"Audio faded {'out' if fade_out else 'in'}")
            
        except Exception as e:
            self.logger.error(f"Error fading audio: {e}")
    
    def cancel_intervention(self):
        """Cancel any active intervention"""
        if self.intervention_active:
            self._stop_blur_effect()
            if self.original_volume is not None:
                try:
                    subprocess.run(
                        ['osascript', '-e', f'set volume output volume {self.original_volume}'],
                        check=False
                    )
                except:
                    pass
            self.intervention_active = False
