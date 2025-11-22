"""
Unit tests for micro-interventions
"""

import unittest
from agent.src.micro_interventions import MicroIntervention


class TestMicroIntervention(unittest.TestCase):
    
    def setUp(self):
        self.intervention = MicroIntervention()
    
    def test_detect_fatigue_insufficient_data(self):
        """Test fatigue detection with insufficient data"""
        metrics = {'typing_rate': 50, 'max_idle_gap': 3}
        history = [metrics] * 3
        
        result = self.intervention.detect_cognitive_fatigue(metrics, history)
        self.assertFalse(result)
    
    def test_detect_fatigue_high_variance(self):
        """Test fatigue detection with high typing variance"""
        history = [
            {'typing_rate': 50, 'max_idle_gap': 3},
            {'typing_rate': 20, 'max_idle_gap': 3},
            {'typing_rate': 60, 'max_idle_gap': 3},
            {'typing_rate': 15, 'max_idle_gap': 3},
            {'typing_rate': 55, 'max_idle_gap': 3},
        ]
        
        result = self.intervention.detect_cognitive_fatigue(history[-1], history)
        self.assertTrue(result)
    
    def test_detect_fatigue_increasing_idle(self):
        """Test fatigue detection with increasing idle gaps"""
        history = [
            {'typing_rate': 50, 'max_idle_gap': 2},
            {'typing_rate': 50, 'max_idle_gap': 3},
            {'typing_rate': 50, 'max_idle_gap': 4},
            {'typing_rate': 50, 'max_idle_gap': 5},
            {'typing_rate': 50, 'max_idle_gap': 6},
        ]
        
        result = self.intervention.detect_cognitive_fatigue(history[-1], history)
        self.assertTrue(result)
    
    def test_detect_fatigue_declining_typing(self):
        """Test fatigue detection with declining typing rate"""
        history = [
            {'typing_rate': 60, 'max_idle_gap': 3},
            {'typing_rate': 55, 'max_idle_gap': 3},
            {'typing_rate': 50, 'max_idle_gap': 3},
            {'typing_rate': 45, 'max_idle_gap': 3},
            {'typing_rate': 35, 'max_idle_gap': 3},
        ]
        
        result = self.intervention.detect_cognitive_fatigue(history[-1], history)
        self.assertTrue(result)
    
    def test_no_fatigue_stable_metrics(self):
        """Test no fatigue with stable metrics"""
        history = [
            {'typing_rate': 50, 'max_idle_gap': 3},
            {'typing_rate': 51, 'max_idle_gap': 3},
            {'typing_rate': 49, 'max_idle_gap': 3},
            {'typing_rate': 50, 'max_idle_gap': 3},
            {'typing_rate': 50, 'max_idle_gap': 3},
        ]
        
        result = self.intervention.detect_cognitive_fatigue(history[-1], history)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
