"""
User Settings Manager for FlowFacilitator
Manages synchronization between local and cloud settings
"""

import logging
import threading
import time
from typing import Dict, Optional, Tuple, Any
from datetime import datetime


class UserSettingsManager:
    """Manages local + cloud settings synchronization"""
    
    def __init__(self, auth_service, supabase_client, local_storage_path=None):
        self.logger = logging.getLogger(__name__)
        self.auth = auth_service
        self.client = supabase_client
        self.local_storage_path = local_storage_path
        
        # Sync settings
        self.sync_interval = 300  # 5 minutes
        self.sync_thread = None
        self.sync_running = False
        
        # Local cache
        self.preferences_cache = {}
        self.permissions_cache = {}
        self.flow_config_cache = None
        self.blocklist_cache = None
        self.whitelist_cache = None
        
        # Sync state
        self.last_sync_time = None
        self.pending_changes = []
    
    def start_auto_sync(self):
        """Start automatic background sync"""
        if self.sync_thread and self.sync_thread.is_alive():
            self.logger.warning("Auto-sync already running")
            return
        
        self.sync_running = True
        self.sync_thread = threading.Thread(target=self._auto_sync_loop, daemon=True)
        self.sync_thread.start()
        self.logger.info("Started auto-sync")
    
    def stop_auto_sync(self):
        """Stop automatic background sync"""
        self.sync_running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        self.logger.info("Stopped auto-sync")
    
    def _auto_sync_loop(self):
        """Background sync loop"""
        while self.sync_running:
            try:
                if self.auth.is_authenticated():
                    self.sync_from_cloud()
                    
                    # Push any pending changes
                    if self.pending_changes:
                        self.sync_to_cloud()
                
                # Wait for next sync interval
                time.sleep(self.sync_interval)
                
            except Exception as e:
                self.logger.error(f"Error in auto-sync loop: {e}")
                time.sleep(60)  # Wait a minute before retrying
    
    def sync_to_cloud(self) -> Tuple[bool, Optional[str]]:
        """
        Sync local settings to cloud
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            if not self.auth.is_authenticated():
                return False, "User not authenticated"
            
            # Sync preferences
            if self.preferences_cache:
                self.client.rpc('update_user_preferences', {
                    'p_preferences': self.preferences_cache
                }).execute()
            
            # Sync permissions
            if self.permissions_cache:
                self.client.rpc('update_user_permissions', {
                    'p_permissions': self.permissions_cache
                }).execute()
            
            # Sync flow config
            if self.flow_config_cache:
                self.client.rpc('update_flow_config', {
                    'p_flow_config': self.flow_config_cache
                }).execute()
            
            # Sync blocklist
            if self.blocklist_cache:
                self.client.rpc('update_blocklist', {
                    'p_blocklist': self.blocklist_cache
                }).execute()
            
            # Sync whitelist
            if self.whitelist_cache:
                self.client.rpc('update_whitelist', {
                    'p_whitelist': self.whitelist_cache
                }).execute()
            
            self.last_sync_time = datetime.now()
            self.pending_changes.clear()
            
            self.logger.info("Settings synced to cloud")
            return True, None
            
        except Exception as e:
            self.logger.error(f"Error syncing to cloud: {e}")
            return False, str(e)
    
    def sync_from_cloud(self) -> Tuple[bool, Optional[str]]:
        """
        Sync settings from cloud to local
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            if not self.auth.is_authenticated():
                return False, "User not authenticated"
            
            # Get user profile with all settings
            profile = self.auth.get_user_profile()
            
            if not profile:
                return False, "Could not fetch user profile"
            
            # Update local cache
            self.preferences_cache = profile.get('preferences', {})
            self.permissions_cache = profile.get('permissions', {})
            self.flow_config_cache = profile.get('flow_config')
            self.blocklist_cache = profile.get('blocklist', {'domains': []})
            self.whitelist_cache = profile.get('whitelist', {'domains': [], 'apps': []})
            
            self.last_sync_time = datetime.now()
            
            self.logger.info("Settings synced from cloud")
            return True, None
            
        except Exception as e:
            self.logger.error(f"Error syncing from cloud: {e}")
            return False, str(e)
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Get a preference value
        
        Args:
            key: Preference key
            default: Default value if not found
        
        Returns:
            Preference value or default
        """
        return self.preferences_cache.get(key, default)
    
    def set_preference(self, key: str, value: Any, sync: bool = True):
        """
        Set a preference value
        
        Args:
            key: Preference key
            value: Preference value
            sync: Whether to sync to cloud immediately
        """
        self.preferences_cache[key] = value
        
        if sync and self.auth.is_authenticated():
            try:
                self.client.rpc('update_user_preferences', {
                    'p_preferences': self.preferences_cache
                }).execute()
                self.logger.info(f"Preference '{key}' synced to cloud")
            except Exception as e:
                self.logger.error(f"Error syncing preference: {e}")
                self.pending_changes.append(('preference', key, value))
        else:
            self.pending_changes.append(('preference', key, value))
    
    def get_all_preferences(self) -> Dict:
        """Get all preferences"""
        return self.preferences_cache.copy()
    
    def get_permissions(self) -> Dict:
        """Get permissions status"""
        return self.permissions_cache.copy()
    
    def update_permissions(self, permissions: Dict, sync: bool = True):
        """
        Update permissions status
        
        Args:
            permissions: Permissions dict
            sync: Whether to sync to cloud immediately
        """
        self.permissions_cache.update(permissions)
        
        if sync and self.auth.is_authenticated():
            try:
                self.client.rpc('update_user_permissions', {
                    'p_permissions': self.permissions_cache
                }).execute()
                self.logger.info("Permissions synced to cloud")
            except Exception as e:
                self.logger.error(f"Error syncing permissions: {e}")
                self.pending_changes.append(('permissions', None, permissions))
        else:
            self.pending_changes.append(('permissions', None, permissions))
    
    def get_flow_config(self) -> Optional[Dict]:
        """Get flow detection config"""
        return self.flow_config_cache
    
    def update_flow_config(self, config: Dict, sync: bool = True):
        """
        Update flow detection config
        
        Args:
            config: Flow config dict
            sync: Whether to sync to cloud immediately
        """
        self.flow_config_cache = config
        
        if sync and self.auth.is_authenticated():
            try:
                self.client.rpc('update_flow_config', {
                    'p_flow_config': config
                }).execute()
                self.logger.info("Flow config synced to cloud")
            except Exception as e:
                self.logger.error(f"Error syncing flow config: {e}")
                self.pending_changes.append(('flow_config', None, config))
        else:
            self.pending_changes.append(('flow_config', None, config))
    
    def get_blocklist(self) -> Dict:
        """Get blocklist"""
        return self.blocklist_cache or {'domains': []}
    
    def update_blocklist(self, blocklist: Dict, sync: bool = True):
        """
        Update blocklist
        
        Args:
            blocklist: Blocklist dict
            sync: Whether to sync to cloud immediately
        """
        self.blocklist_cache = blocklist
        
        if sync and self.auth.is_authenticated():
            try:
                self.client.rpc('update_blocklist', {
                    'p_blocklist': blocklist
                }).execute()
                self.logger.info("Blocklist synced to cloud")
            except Exception as e:
                self.logger.error(f"Error syncing blocklist: {e}")
                self.pending_changes.append(('blocklist', None, blocklist))
        else:
            self.pending_changes.append(('blocklist', None, blocklist))
    
    def get_whitelist(self) -> Dict:
        """Get whitelist"""
        return self.whitelist_cache or {'domains': [], 'apps': []}
    
    def update_whitelist(self, whitelist: Dict, sync: bool = True):
        """
        Update whitelist
        
        Args:
            whitelist: Whitelist dict
            sync: Whether to sync to cloud immediately
        """
        self.whitelist_cache = whitelist
        
        if sync and self.auth.is_authenticated():
            try:
                self.client.rpc('update_whitelist', {
                    'p_whitelist': whitelist
                }).execute()
                self.logger.info("Whitelist synced to cloud")
            except Exception as e:
                self.logger.error(f"Error syncing whitelist: {e}")
                self.pending_changes.append(('whitelist', None, whitelist))
        else:
            self.pending_changes.append(('whitelist', None, whitelist))
    
    def resolve_conflicts(self, local: Dict, remote: Dict) -> Dict:
        """
        Resolve conflicts between local and remote settings
        Uses last-write-wins strategy
        
        Args:
            local: Local settings dict
            remote: Remote settings dict
        
        Returns:
            Merged settings dict
        """
        # For now, use simple last-write-wins
        # In the future, could implement more sophisticated merging
        
        if not local:
            return remote
        
        if not remote:
            return local
        
        # Merge with remote taking precedence
        merged = local.copy()
        merged.update(remote)
        
        return merged
    
    def get_sync_status(self) -> Dict:
        """
        Get sync status information
        
        Returns:
            Dict with sync status info
        """
        return {
            'last_sync_time': self.last_sync_time,
            'pending_changes': len(self.pending_changes),
            'is_syncing': self.sync_running,
            'is_authenticated': self.auth.is_authenticated()
        }
