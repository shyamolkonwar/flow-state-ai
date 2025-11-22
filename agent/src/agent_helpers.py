    
    def _on_extension_message(self, message: dict) -> dict:
        """Handle messages from Chrome extension"""
        cmd = message.get('cmd')
        
        if cmd == 'get_status':
            state = self.flow_engine.get_state()
            return {
                'status': 'ok',
                'flow_state': state.value,
                'in_flow': state == FlowState.IN_FLOW
            }
        
        elif cmd == 'pause_protection':
            duration = message.get('duration_minutes', 10)
            self.protection.disable_protection()
            self.overlay_manager.close_overlay()
            return {
                'status': 'ok',
                'message': f'Paused for {duration} minutes'
            }
        
        elif cmd == 'add_whitelist':
            domain = message.get('domain')
            # TODO: Add to whitelist
            return {
                'status': 'ok',
                'message': f'Added {domain} to whitelist'
            }
        
        return {'status': 'error', 'message': 'Unknown command'}
    
    def _send_to_extension(self, command: str, **kwargs):
        """Send command to Chrome extension"""
        self.native_messaging.send_command(command, **kwargs)
