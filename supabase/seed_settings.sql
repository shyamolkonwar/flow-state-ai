-- Seed some sample settings data for user: d368e836-63ed-438b-8513-e7799961822d

-- Insert flow detection settings
SELECT upsert_setting(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    'flow_detection',
    '{
        "entry": {
            "typing_rate_min": 300,
            "app_switches_max": 3,
            "max_idle_gap_seconds": 30,
            "window_seconds": 300
        },
        "exit": {
            "max_idle_gap_seconds": 120,
            "app_switches_max": 5
        }
    }'::jsonb
);

-- Insert blocklist settings with some domains
SELECT upsert_setting(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    'blocklist',
    '{
        "domains": [
            "youtube.com",
            "reddit.com",
            "twitter.com",
            "facebook.com",
            "instagram.com",
            "tiktok.com",
            "netflix.com",
            "twitch.tv",
            "discord.com",
            "slack.com"
        ]
    }'::jsonb
);

-- Insert some other sample settings
SELECT upsert_setting(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    'notifications',
    '{
        "flow_start": true,
        "flow_end": true,
        "distraction_detected": true,
        "daily_summary": true
    }'::jsonb
);

SELECT upsert_setting(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    'privacy',
    '{
        "collect_typing_data": true,
        "collect_app_usage": true,
        "share_anonymous_stats": false
    }'::jsonb
);

-- Note: RPG/Gamification stats are in seed_rpg.sql

-- Query to verify the data was inserted
SELECT
    user_id,
    key,
    value,
    created_at,
    updated_at
FROM settings
WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid
ORDER BY key;
