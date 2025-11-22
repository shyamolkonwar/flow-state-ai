"""
Database Client - Handles all Supabase interactions
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime
from supabase import create_client, Client


class DatabaseClient:
    """Manages database operations with Supabase"""
    
    def __init__(self, config: Dict):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.client: Optional[Client] = None
        self.connected = False
        
        # Event buffer for offline mode
        self.event_buffer = []
        self.max_buffer_size = 1000
    
    def connect(self):
        """Connect to Supabase"""
        try:
            url = self.config['supabase']['url']
            key = self.config['supabase']['service_key']
            
            self.client = create_client(url, key)
            self.connected = True
            self.logger.info(f"Connected to Supabase at {url}")
            
            # Flush any buffered events
            if self.event_buffer:
                self._flush_buffer()
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Supabase: {e}")
            self.connected = False
    
    def disconnect(self):
        """Disconnect from Supabase"""
        self.connected = False
        self.client = None
        self.logger.info("Disconnected from Supabase")
    
    def start_session(self, start_app: str, meta: Dict = None) -> Optional[str]:
        """Start a new flow session"""
        try:
            if not self.connected:
                self.logger.warning("Not connected to database, buffering...")
                return None
            
            result = self.client.rpc('start_session', {
                'p_start_ts': datetime.now().isoformat(),
                'p_start_app': start_app,
                'p_meta': meta or {}
            }).execute()
            
            session_id = result.data
            self.logger.info(f"Started session: {session_id}")
            return session_id
            
        except Exception as e:
            self.logger.error(f"Error starting session: {e}")
            return None
    
    def end_session(self, session_id: str, end_app: str, avg_typing_rate: float,
                    max_idle_gap: float, trigger_reason: str):
        """End a flow session"""
        try:
            if not self.connected:
                self.logger.warning("Not connected to database")
                return
            
            self.client.rpc('end_session', {
                'p_session_id': session_id,
                'p_end_ts': datetime.now().isoformat(),
                'p_end_app': end_app,
                'p_avg_typing_rate': avg_typing_rate,
                'p_max_idle_gap': max_idle_gap,
                'p_trigger_reason': trigger_reason
            }).execute()
            
            self.logger.info(f"Ended session: {session_id}")
            
        except Exception as e:
            self.logger.error(f"Error ending session: {e}")
    
    def insert_event(self, session_id: Optional[str], event_type: str, payload: Dict = None):
        """Insert an event"""
        event_data = {
            'session_id': session_id,
            'ts': datetime.now().isoformat(),
            'type': event_type,
            'payload': payload or {}
        }
        
        try:
            if not self.connected:
                # Buffer event for later
                if len(self.event_buffer) < self.max_buffer_size:
                    self.event_buffer.append(event_data)
                return
            
            self.client.table('events').insert(event_data).execute()
            
        except Exception as e:
            self.logger.error(f"Error inserting event: {e}")
            # Buffer event
            if len(self.event_buffer) < self.max_buffer_size:
                self.event_buffer.append(event_data)
    
    def get_settings(self, key: str) -> Optional[Dict]:
        """Get settings by key"""
        try:
            if not self.connected:
                return None
            
            result = self.client.table('settings').select('value').eq('key', key).execute()
            
            if result.data:
                return result.data[0]['value']
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting settings: {e}")
            return None
    
    def upsert_setting(self, key: str, value: Dict):
        """Update or insert a setting"""
        try:
            if not self.connected:
                return
            
            self.client.rpc('upsert_setting', {
                'p_user_id': 'local_user',
                'p_key': key,
                'p_value': value
            }).execute()
            
            self.logger.info(f"Updated setting: {key}")
            
        except Exception as e:
            self.logger.error(f"Error upserting setting: {e}")
    
    def log_agent_message(self, level: str, message: str, meta: Dict = None):
        """Log an agent message to the database"""
        try:
            if not self.connected:
                return
            
            self.client.table('agent_logs').insert({
                'level': level,
                'message': message,
                'meta': meta or {}
            }).execute()
            
        except Exception as e:
            # Don't log errors about logging (avoid recursion)
            pass
    
    def _flush_buffer(self):
        """Flush buffered events to database"""
        if not self.event_buffer:
            return
        
        self.logger.info(f"Flushing {len(self.event_buffer)} buffered events...")
        
        try:
            # Insert all buffered events
            self.client.table('events').insert(self.event_buffer).execute()
            self.event_buffer.clear()
            self.logger.info("Buffer flushed successfully")
            
        except Exception as e:
            self.logger.error(f"Error flushing buffer: {e}")
    
    def is_connected(self) -> bool:
        """Check if connected to database"""
        return self.connected
