"""
Gamification System - RPG-style stats and progressive overload
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from pathlib import Path


class UserStats:
    """RPG-style user statistics"""
    
    def __init__(self):
        self.stamina = 0  # Total flow time (minutes)
        self.resilience = 0  # Times resisted distractions
        self.consistency = 0  # Current streak (days)
        self.level = 1
        self.experience = 0
        
        # Historical data
        self.best_streak = 0
        self.total_sessions = 0
        self.average_session_duration = 0
        self.personal_best_duration = 0
        
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'stamina': self.stamina,
            'resilience': self.resilience,
            'consistency': self.consistency,
            'level': self.level,
            'experience': self.experience,
            'best_streak': self.best_streak,
            'total_sessions': self.total_sessions,
            'average_session_duration': self.average_session_duration,
            'personal_best_duration': self.personal_best_duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create from dictionary"""
        stats = cls()
        stats.stamina = data.get('stamina', 0)
        stats.resilience = data.get('resilience', 0)
        stats.consistency = data.get('consistency', 0)
        stats.level = data.get('level', 1)
        stats.experience = data.get('experience', 0)
        stats.best_streak = data.get('best_streak', 0)
        stats.total_sessions = data.get('total_sessions', 0)
        stats.average_session_duration = data.get('average_session_duration', 0)
        stats.personal_best_duration = data.get('personal_best_duration', 0)
        return stats


class GamificationSystem:
    """RPG-style gamification with progressive overload"""
    
    def __init__(self, stats_file: Optional[Path] = None):
        self.logger = logging.getLogger(__name__)
        
        # Stats file location
        if stats_file is None:
            stats_dir = Path.home() / 'Library' / 'Application Support' / 'FlowFacilitator'
            stats_dir.mkdir(parents=True, exist_ok=True)
            stats_file = stats_dir / 'user_stats.json'
        
        self.stats_file = stats_file
        self.stats = self._load_stats()
        
        # Progressive overload
        self.current_goal = None
        self.schedule = []
        
    def _load_stats(self) -> UserStats:
        """Load user stats from file"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
                return UserStats.from_dict(data)
            except Exception as e:
                self.logger.error(f"Error loading stats: {e}")
        
        return UserStats()
    
    def _save_stats(self):
        """Save user stats to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats.to_dict(), f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving stats: {e}")
    
    def add_flow_session(self, duration_minutes: int):
        """Add a completed flow session"""
        # Update stamina
        self.stats.stamina += duration_minutes
        
        # Update session stats
        self.stats.total_sessions += 1
        
        # Update average
        total_time = self.stats.average_session_duration * (self.stats.total_sessions - 1) + duration_minutes
        self.stats.average_session_duration = total_time / self.stats.total_sessions
        
        # Update personal best
        if duration_minutes > self.stats.personal_best_duration:
            self.stats.personal_best_duration = duration_minutes
            self.logger.info(f"🏆 New personal best: {duration_minutes} minutes!")
        
        # Add experience
        xp_gained = duration_minutes * 10  # 10 XP per minute
        self.stats.experience += xp_gained
        
        # Check for level up
        self._check_level_up()
        
        # Update progressive goal
        self._update_progressive_goal()
        
        self._save_stats()
        self.logger.info(f"Session complete: +{duration_minutes}m Stamina, +{xp_gained} XP")
    
    def add_resilience(self, count: int = 1):
        """Add resilience points for resisting distractions"""
        self.stats.resilience += count
        xp_gained = count * 50  # 50 XP per resistance
        self.stats.experience += xp_gained
        
        self._check_level_up()
        self._save_stats()
        
        self.logger.info(f"💪 Resilience +{count}, +{xp_gained} XP")
    
    def update_streak(self, had_session_today: bool):
        """Update daily consistency streak"""
        if had_session_today:
            self.stats.consistency += 1
            if self.stats.consistency > self.stats.best_streak:
                self.stats.best_streak = self.stats.consistency
                self.logger.info(f"🔥 New best streak: {self.stats.consistency} days!")
        else:
            # Check if we can use fluid goals to save the streak
            if self._can_use_fluid_goals():
                self.logger.info("Using fluid goals to maintain streak")
            else:
                self.stats.consistency = 0
                self.logger.info("Streak broken")
        
        self._save_stats()
    
    def _check_level_up(self):
        """Check if user leveled up"""
        xp_for_next_level = self.stats.level * 1000
        
        if self.stats.experience >= xp_for_next_level:
            self.stats.level += 1
            self.stats.experience -= xp_for_next_level
            self.logger.info(f"🎉 LEVEL UP! You are now level {self.stats.level}!")
    
    def _update_progressive_goal(self):
        """
        Update progressive overload goal
        
        If user typically quits at 25 mins, set next goal to 26m 15s (5% increase)
        """
        if self.stats.total_sessions < 5:
            # Not enough data yet
            self.current_goal = 30  # Default 30 minutes
            return
        
        # Calculate typical session duration (average of last 10 sessions)
        # For now, use overall average
        typical_duration = self.stats.average_session_duration
        
        # Progressive overload: 5% increase
        self.current_goal = int(typical_duration * 1.05)
        
        # Ensure minimum increment of 1 minute
        if self.current_goal <= typical_duration:
            self.current_goal = int(typical_duration) + 1
        
        self.logger.info(f"Progressive goal updated: {self.current_goal} minutes")
    
    def get_current_goal(self) -> int:
        """Get current progressive goal (minutes)"""
        if self.current_goal is None:
            self._update_progressive_goal()
        return self.current_goal or 30
    
    def import_schedule(self, schedule: List[Dict]):
        """
        Import user's timetable
        
        Format: [
            {"day": "Monday", "time": "09:00", "duration": 60, "task": "Deep Work"},
            ...
        ]
        """
        self.schedule = schedule
        self.logger.info(f"Imported schedule with {len(schedule)} entries")
    
    def _can_use_fluid_goals(self) -> bool:
        """
        Check if fluid goals can save the streak
        
        If a scheduled session was missed, recalculate day's targets
        """
        # TODO: Implement fluid goals logic
        # For now, allow one missed day per week
        return self.stats.consistency % 7 != 0
    
    def get_stats_summary(self) -> Dict:
        """Get formatted stats summary"""
        return {
            'level': self.stats.level,
            'experience': self.stats.experience,
            'next_level_xp': self.stats.level * 1000,
            'stamina': {
                'total_minutes': self.stats.stamina,
                'total_hours': round(self.stats.stamina / 60, 1),
                'average_session': round(self.stats.average_session_duration, 1),
                'personal_best': self.stats.personal_best_duration
            },
            'resilience': {
                'total': self.stats.resilience,
                'rank': self._get_resilience_rank()
            },
            'consistency': {
                'current_streak': self.stats.consistency,
                'best_streak': self.stats.best_streak
            },
            'progressive_goal': self.get_current_goal(),
            'total_sessions': self.stats.total_sessions
        }
    
    def _get_resilience_rank(self) -> str:
        """Get resilience rank based on count"""
        if self.stats.resilience >= 100:
            return "Diamond"
        elif self.stats.resilience >= 50:
            return "Platinum"
        elif self.stats.resilience >= 25:
            return "Gold"
        elif self.stats.resilience >= 10:
            return "Silver"
        else:
            return "Bronze"
