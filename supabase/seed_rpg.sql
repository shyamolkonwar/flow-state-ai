-- Seed RPG/Gamification stats for user: d368e836-63ed-438b-8513-e7799961822d

-- Insert comprehensive gamification stats
SELECT upsert_setting(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    'gamification_stats',
    '{
        "level": 15,
        "experience": 3875,
        "next_level_xp": 4000,
        "stamina": {
            "total_hours": 67,
            "average_session": 72,
            "personal_best": 180
        },
        "resilience": {
            "total": 124,
            "rank": "Crystal Master"
        },
        "consistency": {
            "current_streak": 8,
            "best_streak": 15
        },
        "progressive_goal": 95,
        "achievements_unlocked": [
            "first_flow",
            "ten_hour_club",
            "week_warrior",
            "iron_will",
            "consistency_master"
        ],
        "stats": {
            "total_sessions": 156,
            "total_focus_time_hours": 67,
            "distractions_blocked": 124,
            "average_flow_depth": 72,
            "longest_streak_days": 15,
            "current_streak_days": 8
        }
    }'::jsonb
);

-- Insert additional RPG-related settings
SELECT upsert_setting(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    'rpg_preferences',
    '{
        "theme": "crystal",
        "notifications_enabled": true,
        "sound_effects": true,
        "achievement_animations": true,
        "leaderboard_visible": false,
        "weekly_goals": true,
        "monthly_reports": true
    }'::jsonb
);

-- Insert RPG progress tracking
SELECT upsert_setting(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    'rpg_progress',
    '{
        "current_quest": "Master of Flow",
        "quest_progress": 75,
        "daily_challenges": [
            {"name": "Focus for 2 hours", "completed": true, "reward": 50},
            {"name": "Block 5 distractions", "completed": true, "reward": 25},
            {"name": "Maintain 90min session", "completed": false, "reward": 75}
        ],
        "weekly_milestones": {
            "focus_hours_target": 20,
            "focus_hours_current": 18.5,
            "distractions_blocked_target": 50,
            "distractions_blocked_current": 47
        },
        "skill_tree": {
            "focus_mastery": {"level": 8, "max_level": 10},
            "distraction_resistance": {"level": 9, "max_level": 10},
            "consistency": {"level": 7, "max_level": 10},
            "deep_work": {"level": 6, "max_level": 10}
        }
    }'::jsonb
);

-- Query to verify the RPG data was inserted
SELECT
    user_id,
    key,
    value,
    created_at,
    updated_at
FROM settings
WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid
AND key IN ('gamification_stats', 'rpg_preferences', 'rpg_progress')
ORDER BY key;
