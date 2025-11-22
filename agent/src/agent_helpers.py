    
    def _on_flow_broken(self, app_name: str):
        """Handle when user breaks flow by unlocking overlay"""
        self.logger.warning(f\"Flow broken by user unlocking: {app_name}\")\n        
        # End current session
        if self.current_session_id:
            self._end_session(f\"user_unlocked_{app_name}\")\n    
    def get_gamification_stats(self) -> dict:
        \"\"\"Get current gamification stats\"\"\"
        return self.gamification.get_stats_summary()
