"""
Local HTTP API Server - Provides REST API for dashboard
"""

import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import Callable, Optional
import threading


class AgentAPIServer:
    """HTTP API server for dashboard communication"""
    
    def __init__(self, agent, config: dict):
        self.logger = logging.getLogger(__name__)
        self.agent = agent
        self.config = config
        
        # Create Flask app
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for localhost
        
        # Setup routes
        self._setup_routes()
        
        # Server thread
        self.server_thread = None
        self.running = False
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            """Get current agent status"""
            try:
                state = self.agent.flow_engine.get_state()
                time_in_state = self.agent.flow_engine.get_time_in_state()
                metrics = self.agent.metrics.get_all_metrics()
                
                # Check permissions for UI
                from .ui.utils import check_permissions
                permissions = check_permissions()
                
                return jsonify({
                    'status': 'ok',
                    'agent_running': True,
                    'flow_state': state.value,
                    'time_in_state_seconds': time_in_state,
                    'current_session_id': self.agent.current_session_id,
                    'metrics': metrics,
                    'protection_active': self.agent.protection.is_protection_active(),
                    'permissions': permissions
                })
            except Exception as e:
                self.logger.error(f"Error getting status: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/pause', methods=['POST'])
        def pause_protection():
            """Pause protection temporarily"""
            try:
                data = request.json
                duration_minutes = data.get('duration_minutes', 10)
                
                # Disable protection
                self.agent.protection.disable_protection()
                self.agent.overlay_manager.close_overlay()
                
                # TODO: Re-enable after duration
                
                return jsonify({
                    'status': 'ok',
                    'message': f'Protection paused for {duration_minutes} minutes'
                })
            except Exception as e:
                self.logger.error(f"Error pausing protection: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/whitelist/add', methods=['POST'])
        def add_to_whitelist():
            """Add domain to whitelist"""
            try:
                data = request.json
                domain = data.get('domain')
                
                if not domain:
                    return jsonify({'status': 'error', 'message': 'Domain required'}), 400
                
                # TODO: Add to whitelist in database
                
                return jsonify({
                    'status': 'ok',
                    'message': f'Added {domain} to whitelist'
                })
            except Exception as e:
                self.logger.error(f"Error adding to whitelist: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/stats/gamification', methods=['GET'])
        def get_gamification_stats():
            """Get gamification stats"""
            try:
                stats = self.agent.gamification.get_stats_summary()
                return jsonify({
                    'status': 'ok',
                    'stats': stats
                })
            except Exception as e:
                self.logger.error(f"Error getting gamification stats: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/settings', methods=['GET'])
        def get_settings():
            """Get current settings"""
            try:
                return jsonify({
                    'status': 'ok',
                    'flow_config': self.agent.flow_config,
                    'blocklist': self.agent.blocklist
                })
            except Exception as e:
                self.logger.error(f"Error getting settings: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/settings', methods=['POST'])
        def update_settings():
            """Update settings"""
            try:
                data = request.json
                
                if 'flow_config' in data:
                    self.agent.flow_config = data['flow_config']
                    self.agent.flow_engine.config = data['flow_config']
                
                if 'blocklist' in data:
                    self.agent.blocklist = data['blocklist']
                
                # Save to database
                if 'flow_config' in data:
                    self.agent.db.upsert_setting('flow_detection', data['flow_config'])
                
                if 'blocklist' in data:
                    self.agent.db.upsert_setting('blocklist', {'domains': data['blocklist']})
                
                return jsonify({
                    'status': 'ok',
                    'message': 'Settings updated'
                })
            except Exception as e:
                self.logger.error(f"Error updating settings: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
    
    def start(self):
        """Start the API server"""
        port = self.config.get('agent', {}).get('api_port', 8765)
        
        def run_server():
            self.app.run(
                host='127.0.0.1',
                port=port,
                debug=False,
                use_reloader=False
            )
        
        self.running = True
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        self.logger.info(f"API server started on http://127.0.0.1:{port}")
    
    def stop(self):
        """Stop the API server"""
        self.running = False
        # Flask doesn't have a clean shutdown method in development mode
        self.logger.info("API server stopped")
