"""
Unit tests for gamification system
"""

import unittest
import tempfile
from pathlib import Path
from agent.src.gamification import GamificationSystem, UserStats


class TestGamificationSystem(unittest.TestCase):
    
    def setUp(self):
        # Use temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_path = Path(self.temp_file.name)
        self.temp_file.close()
        
        self.system = GamificationSystem(stats_file=self.temp_path)
    
    def tearDown(self):
        if self.temp_path.exists():
            self.temp_path.unlink()
    
    def test_initial_stats(self):
        """Test initial stats are correct"""
        self.assertEqual(self.system.stats.level, 1)
        self.assertEqual(self.system.stats.stamina, 0)
        self.assertEqual(self.system.stats.resilience, 0)
        self.assertEqual(self.system.stats.consistency, 0)
    
    def test_add_flow_session(self):
        """Test adding a flow session"""
        self.system.add_flow_session(30)
        
        self.assertEqual(self.system.stats.stamina, 30)
        self.assertEqual(self.system.stats.total_sessions, 1)
        self.assertEqual(self.system.stats.average_session_duration, 30)
        self.assertEqual(self.system.stats.personal_best_duration, 30)
    
    def test_add_resilience(self):
        """Test adding resilience points"""
        self.system.add_resilience(1)
        
        self.assertEqual(self.system.stats.resilience, 1)
        self.assertEqual(self.system.stats.experience, 50)
    
    def test_level_up(self):
        """Test leveling up"""
        # Add enough XP to level up (1000 XP for level 2)
        for _ in range(100):
            self.system.add_flow_session(1)  # 10 XP per minute
        
        self.assertEqual(self.system.stats.level, 2)
    
    def test_progressive_goal(self):
        """Test progressive overload goal"""
        # Add some sessions
        self.system.add_flow_session(25)
        self.system.add_flow_session(25)
        self.system.add_flow_session(25)
        self.system.add_flow_session(25)
        self.system.add_flow_session(25)
        
        goal = self.system.get_current_goal()
        
        # Should be 5% more than 25 = 26.25 = 26
        self.assertEqual(goal, 26)
    
    def test_stats_persistence(self):
        """Test stats are saved and loaded"""
        self.system.add_flow_session(30)
        self.system.add_resilience(5)
        
        # Create new system with same file
        new_system = GamificationSystem(stats_file=self.temp_path)
        
        self.assertEqual(new_system.stats.stamina, 30)
        self.assertEqual(new_system.stats.resilience, 5)
    
    def test_resilience_rank(self):
        """Test resilience ranking"""
        summary = self.system.get_stats_summary()
        self.assertEqual(summary['resilience']['rank'], 'Bronze')
        
        self.system.add_resilience(10)
        summary = self.system.get_stats_summary()
        self.assertEqual(summary['resilience']['rank'], 'Silver')
        
        self.system.add_resilience(15)
        summary = self.system.get_stats_summary()
        self.assertEqual(summary['resilience']['rank'], 'Gold')


if __name__ == '__main__':
    unittest.main()
