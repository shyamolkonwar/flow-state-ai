"""
Flow Rule Engine - Evaluates flow state based on metrics
"""

import logging
import time
from enum import Enum
from typing import Dict, Callable, Optional


class FlowState(Enum):
    """Possible flow states"""
    IDLE = "idle"
    WORKING = "working"
    IN_FLOW = "in_flow"
    EXITING_FLOW = "exiting_flow"


class FlowRuleEngine:
    """Applies flow detection rules and manages state transitions"""
    
    def __init__(self, config: Dict, on_flow_change: Optional[Callable] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.on_flow_change = on_flow_change
        
        # Current state
        self.state = FlowState.IDLE
        self.state_entered_at = time.time()
        
        # Timers
        self.flow_criteria_met_since = None
        self.exit_criteria_met_since = None
    
    def evaluate(self, metrics: Dict[str, float]) -> FlowState:
        """Evaluate current metrics and update state"""
        current_time = time.time()
        
        # Get thresholds from config
        entry = self.config['entry']
        exit_cfg = self.config['exit']
        
        # Check entry criteria
        entry_criteria_met = (
            metrics['typing_rate'] >= entry['typing_rate_min'] and
            metrics['app_switch_count'] <= entry['app_switches_max'] and
            metrics['max_idle_gap'] <= entry['max_idle_gap_seconds']
        )
        
        # Check exit criteria
        exit_criteria_met = (
            metrics['typing_rate'] < exit_cfg['typing_rate_min'] or
            metrics['app_switch_count'] > exit_cfg['app_switches_max'] or
            metrics['max_idle_gap'] > exit_cfg['max_idle_gap_seconds']
        )
        
        # State machine logic
        old_state = self.state
        
        if self.state == FlowState.IDLE or self.state == FlowState.WORKING:
            if entry_criteria_met:
                if self.flow_criteria_met_since is None:
                    self.flow_criteria_met_since = current_time
                    self.state = FlowState.WORKING
                else:
                    # Check if criteria have been met long enough
                    duration = current_time - self.flow_criteria_met_since
                    if duration >= entry['window_seconds']:
                        self._transition_to(FlowState.IN_FLOW)
            else:
                # Criteria not met, reset
                self.flow_criteria_met_since = None
                self.state = FlowState.IDLE
        
        elif self.state == FlowState.IN_FLOW:
            if exit_criteria_met:
                if self.exit_criteria_met_since is None:
                    self.exit_criteria_met_since = current_time
                else:
                    # Check if exit criteria have persisted long enough
                    duration = current_time - self.exit_criteria_met_since
                    if duration >= exit_cfg['delay_seconds']:
                        reason = self._get_exit_reason(metrics, exit_cfg)
                        self._transition_to(FlowState.WORKING, reason=reason)
            else:
                # Still in flow, reset exit timer
                self.exit_criteria_met_since = None
        
        return self.state
    
    def _transition_to(self, new_state: FlowState, reason: str = None):
        """Transition to a new state"""
        old_state = self.state
        self.state = new_state
        self.state_entered_at = time.time()
        
        # Reset timers
        if new_state == FlowState.IN_FLOW:
            self.flow_criteria_met_since = None
            self.exit_criteria_met_since = None
        elif new_state == FlowState.WORKING:
            self.exit_criteria_met_since = None
        
        # Notify callback
        if old_state != new_state and self.on_flow_change:
            self.on_flow_change(old_state, new_state, reason)
        
        self.logger.info(f"State transition: {old_state.value} -> {new_state.value}" + 
                        (f" (reason: {reason})" if reason else ""))
    
    def _get_exit_reason(self, metrics: Dict, exit_cfg: Dict) -> str:
        """Determine why flow state is exiting"""
        if metrics['typing_rate'] < exit_cfg['typing_rate_min']:
            return "low_typing_rate"
        elif metrics['app_switch_count'] > exit_cfg['app_switches_max']:
            return "excessive_app_switches"
        elif metrics['max_idle_gap'] > exit_cfg['max_idle_gap_seconds']:
            return "idle"
        return "unknown"
    
    def get_state(self) -> FlowState:
        """Get current flow state"""
        return self.state
    
    def get_time_in_state(self) -> float:
        """Get time spent in current state (seconds)"""
        return time.time() - self.state_entered_at
    
    def reset(self):
        """Reset to idle state"""
        self._transition_to(FlowState.IDLE)
        self.flow_criteria_met_since = None
        self.exit_criteria_met_since = None
