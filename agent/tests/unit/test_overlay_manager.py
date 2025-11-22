"""
Unit tests for overlay manager
"""

import unittest
from unittest.mock import Mock, patch
from agent.src.overlay_manager import OverlayManager


class TestOverlayManager(unittest.TestCase):
    
    def setUp(self):
        self.on_flow_broken = Mock()
        self.manager = OverlayManager(on_flow_broken=self.on_flow_broken)
    
    def test_set_blocked_apps(self):
        """Test setting blocked apps"""
        apps = ['Steam', 'Instagram', 'Facebook']
        self.manager.set_blocked_apps(apps)
        
        self.assertEqual(len(self.manager.blocked_apps), 3)
        self.assertIn('Steam', self.manager.blocked_apps)
    
    def test_should_block_app_exact_match(self):
        """Test exact app name matching"""
        self.manager.set_blocked_apps(['Steam'])
        
        self.assertTrue(self.manager.should_block_app('Steam'))
        self.assertFalse(self.manager.should_block_app('VSCode'))
    
    def test_should_block_app_partial_match(self):
        """Test partial app name matching"""
        self.manager.set_blocked_apps(['Instagram'])
        
        self.assertTrue(self.manager.should_block_app('Instagram.app'))
        self.assertTrue(self.manager.should_block_app('instagram'))
    
    def test_should_block_app_none(self):
        """Test None app name"""
        self.manager.set_blocked_apps(['Steam'])
        
        self.assertFalse(self.manager.should_block_app(None))
    
    def test_close_overlay(self):
        """Test closing overlay"""
        self.manager.close_overlay()
        self.assertIsNone(self.manager.active_overlay)


if __name__ == '__main__':
    unittest.main()
