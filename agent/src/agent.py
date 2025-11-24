"""
FlowAgent - Main agent orchestrator
"""

import logging
import time
import threading
from typing import Dict, Optional

from .input_collector import InputCollector
from .metrics_engine import RollingMetrics
from .flow_engine import FlowRuleEngine, FlowState
from .database import DatabaseClient
from .auth_service import AuthService
from .protection import ProtectionController
from .overlay_manager import OverlayManager
from .micro_interventions import MicroIntervention
from .gamification import GamificationSystem
from .native_messaging import NativeMessagingHost
from .api_server import AgentAPIServer


class FlowAgent:
    """Main agent that coordinates all components"""
    
    def __init__(self, config: Dict):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.running = False
        
        # Load flow detection config from database or use defaults
        # NOTE: Thresholds lowered for easier testing
        self.flow_config = {
            'entry': {
                'typing_rate_min': 10,  # Lowered from 40 for testing
                'app_switches_max': 2,
                'max_idle_gap_seconds': 4,
                'window_seconds': 30  # Lowered from 300 (5 min) to 30 sec for testing
            },
            'exit': {
                'typing_rate_min': 5,   # Lowered from 30 for testing
                'app_switches_max': 5,
                'max_idle_gap_seconds': 6,
                'delay_seconds': 10  # Lowered from 30 sec for testing
            }
        }
        
        # Default blocklist
        self.blocklist = [
            'youtube.com', 'reddit.com', 'twitter.com', 'x.com',
            'facebook.com', 'instagram.com', 'tiktok.com',
            'netflix.com', 'twitch.tv', 'discord.com'
        ]
        
        # Components
        self._auth = None  # Lazy initialization to avoid keyring conflicts
        self.db = DatabaseClient(config)
        self.input_collector = InputCollector(on_event=self._on_event)
        self.metrics = RollingMetrics()
        self.flow_engine = FlowRuleEngine(self.flow_config, on_flow_change=self._on_flow_change)
        
        # Communication (create before protection so it can be passed)
        self.native_messaging = NativeMessagingHost(on_message=self._on_extension_message)
        
        # Protection controller (needs native messaging)
        self.protection = ProtectionController(config, native_messaging_host=self.native_messaging)
        
        # Other components
        self.overlay_manager = OverlayManager(on_flow_broken=self._on_flow_broken)
        self.micro_intervention = MicroIntervention()
        self.gamification = GamificationSystem()
        
        # API Server
        self.api_server = AgentAPIServer(self, config)
        
        # Current session
        self.current_session_id: Optional[str] = None
        self.session_start_app: Optional[str] = None
        self.session_start_time: Optional[float] = None
        
        # Metrics history for fatigue detection
        self.metrics_history = []
        
        # Monitoring thread
        self.monitor_thread: Optional[threading.Thread] = None
    
    def start(self):
        """Start the agent"""
        self.logger.info("Starting FlowAgent...")
        
        # Connect to database
        self.db.connect()
        
        # Load settings from database
        self._load_settings()
        
        # Start input collection
        self.input_collector.start()
        
        # Start native messaging
        self.native_messaging.start()
        
        # Start API server
        self.api_server.start()
        
        # Start monitoring loop
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info("FlowAgent started successfully")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the agent"""
        self.logger.info("Stopping FlowAgent...")
        
        self.running = False
        
        # End current session if any
        if self.current_session_id:
            self._end_session("agent_stopped")
        
        # Stop components
        self.input_collector.stop()
        self.protection.disable_protection()
        self.db.disconnect()
        
        self.logger.info("FlowAgent stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop - runs every second"""
        check_interval = self.config.get('flow_detection', {}).get('check_interval_seconds', 1)
        
        while self.running:
            try:
                # Update foreground app
                current_app = self.input_collector.get_foreground_app()
                
                # Check if app should be blocked with overlay
                if self.flow_engine.get_state() == FlowState.IN_FLOW:
                    if self.overlay_manager.should_block_app(current_app):
                        self.overlay_manager.show_overlay_for_app(current_app)
                
                # Get current metrics
                metrics = self.metrics.get_all_metrics()
                
                # Store metrics history for fatigue detection
                self.metrics_history.append(metrics)
                if len(self.metrics_history) > 20:  # Keep last 20 samples
                    self.metrics_history.pop(0)
                
                # Evaluate flow state
                self.flow_engine.evaluate(metrics)
                
                # Log metrics periodically (every 10 seconds)
                if int(time.time()) % 10 == 0:
                    self.logger.debug(f"Metrics: {metrics}, State: {self.flow_engine.get_state().value}")
                
                # DISABLED: Micro-interventions cause threading issues with tkinter on macOS
                # Check for cognitive fatigue
                # if self.flow_engine.get_state() == FlowState.IN_FLOW:
                #     if self.micro_intervention.detect_cognitive_fatigue(metrics, self.metrics_history):
                #         self.logger.info("Triggering micro-intervention")
                #         # Run intervention in separate thread
                #         import threading
                #         threading.Thread(
                #             target=self.micro_intervention.trigger_soft_reset,
                #             args=(30,),
                #             daemon=True
                #         ).start()
                
                time.sleep(check_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {e}", exc_info=True)
                time.sleep(check_interval)
    
    def _on_event(self, event):
        """Handle input events"""
        # Update metrics
        self.metrics.update_from_event(event)
        
        # Only log events to database if we have an active session
        if not self.current_session_id:
            return
        
        # Log certain events to database
        if event.type in ['app_switch', 'flow_on', 'flow_off']:
            payload = {}
            if hasattr(event, 'from_app'):
                payload['from_app'] = event.from_app
                payload['to_app'] = event.to_app
            
            user_id = self._get_user_id()
            self.db.insert_event(user_id, self.current_session_id, event.type, payload)
    
    def _on_flow_change(self, old_state: FlowState, new_state: FlowState, reason: str = None):
        """Handle flow state changes"""
        self.logger.info(f"Flow state changed: {old_state.value} -> {new_state.value}")

        if new_state == FlowState.IN_FLOW:
            self._start_session()
        elif old_state == FlowState.IN_FLOW and new_state != FlowState.IN_FLOW:
            self._end_session(reason or "unknown")

    def _on_flow_broken(self, app_name: str):
        """Handle flow broken by overlay unlock"""
        self.logger.info(f"Flow broken by opening: {app_name}")
        self._end_session(f"opened_blocked_app_{app_name}")

    def _on_extension_message(self, message: dict) -> Optional[dict]:
        """Handle messages from Chrome extension"""
        self.logger.debug(f"Extension message: {message}")

        cmd = message.get('cmd')
        if cmd == 'get_status':
            return {
                'status': 'ok',
                'flow_state': self.flow_engine.get_state().value,
                'current_session': self.current_session_id,
                'metrics': self.metrics.get_all_metrics()
            }
        elif cmd == 'start_session':
            if self.flow_engine.get_state() != FlowState.IN_FLOW:
                # Force start a session
                self._start_session()
                return {'status': 'ok', 'message': 'Session started'}
            else:
                return {'status': 'error', 'message': 'Already in flow'}
        elif cmd == 'end_session':
            if self.current_session_id:
                self._end_session('manual_end')
                return {'status': 'ok', 'message': 'Session ended'}
            else:
                return {'status': 'error', 'message': 'No active session'}

        return {'status': 'error', 'message': 'Unknown command'}
    
    @property
    def auth(self):
        """Lazy initialization of auth service"""
        if self._auth is None:
            try:
                self._auth = AuthService(self.config)
            except Exception as e:
                self.logger.error(f"Failed to initialize auth service: {e}")
                # Return a dummy object that always returns None for user_id
                class DummyAuth:
                    def is_authenticated(self): return False
                    current_user = None
                self._auth = DummyAuth()
        return self._auth
    
    def _get_user_id(self) -> Optional[str]:
        """Get current user ID from auth service"""
        # DEMO MODE: Hardcoded user ID for demonstration
        # TODO: Remove this and use actual authentication for production
        return "d368e836-63ed-438b-8513-e7799961822d"
        
        # Original auth code (commented out for demo):
        # try:
        #     if self.auth.is_authenticated() and self.auth.current_user:
        #         return self.auth.current_user.id
        # except Exception as e:
        #     self.logger.warning(f"Could not get user ID: {e}")
        # return None
    
    def _start_session(self):
        """Start a new flow session"""
        current_app = self.input_collector.get_foreground_app()
        self.session_start_app = current_app
        self.session_start_time = time.time()
        
        # Get user ID (may be None if not authenticated)
        user_id = self._get_user_id()
        if not user_id:
            self.logger.warning("No authenticated user - session will be created without user_id")
        
        # Start session in database
        self.current_session_id = self.db.start_session(user_id, current_app or "Unknown")
        
        # Log flow_on event
        self.db.insert_event(user_id, self.current_session_id, 'flow_on', {
            'app': current_app
        })
        
        # Enable protection
        self.protection.enable_protection(self.blocklist)
        
        # Set up overlay blocking
        blocked_apps = ['Steam', 'Instagram', 'Facebook', 'Twitter', 'TikTok', 'Netflix']
        self.overlay_manager.set_blocked_apps(blocked_apps)
        
        self.logger.info(f"Started flow session: {self.current_session_id} for user: {user_id}")
    
    def _end_session(self, reason: str):
        """End the current flow session"""
        if not self.current_session_id:
            return
        
        current_app = self.input_collector.get_foreground_app()
        metrics = self.metrics.get_all_metrics()
        user_id = self._get_user_id()
        
        # Calculate session duration
        duration_seconds = time.time() - self.session_start_time if self.session_start_time else 0
        duration_minutes = int(duration_seconds / 60)
        
        # End session in database
        self.db.end_session(
            self.current_session_id,
            current_app or "Unknown",
            metrics['typing_rate'],
            metrics['max_idle_gap'],
            reason
        )
        
        # Log flow_off event
        self.db.insert_event(user_id, self.current_session_id, 'flow_off', {
            'app': current_app,
            'reason': reason
        })
        
        # Update gamification stats
        if duration_minutes > 0:
            self.gamification.add_flow_session(duration_minutes)
        
        # Disable protection
        self.protection.disable_protection()
        
        self.logger.info(f"Ended flow session: {self.current_session_id} (reason: {reason})")
        self.current_session_id = None
        self.session_start_time = None
    
    def _load_settings(self):
        """Load settings from database"""
        try:
            # Load flow detection config
            flow_config = self.db.get_settings('flow_detection')
            if flow_config:
                self.flow_config = flow_config
                self.flow_engine.config = flow_config
                self.logger.info("Loaded flow detection config from database")
            
            # Load blocklist
            blocklist_config = self.db.get_settings('blocklist')
            if blocklist_config and 'domains' in blocklist_config:
                self.blocklist = blocklist_config['domains']
                self.logger.info(f"Loaded blocklist: {len(self.blocklist)} domains")
            
        except Exception as e:
            self.logger.warning(f"Could not load settings from database: {e}")
            self.logger.info("Using default settings")
