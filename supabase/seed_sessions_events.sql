-- Seed sample sessions and events data
-- Note: Replace 'd368e836-63ed-438b-8513-e7799961822d' with an actual user ID from your auth.users table

-- Create some sample sessions
INSERT INTO sessions (
    user_id,
    start_ts,
    end_ts,
    start_app,
    end_app,
    avg_typing_rate,
    max_idle_gap,
    trigger_reason,
    meta
) VALUES
-- Session 1: Completed flow session
(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '2 days'),
    TIMEZONE('utc'::text, NOW() - INTERVAL '2 days' + INTERVAL '45 minutes'),
    'Visual Studio Code',
    'Visual Studio Code',
    425.5,
    15.2,
    'natural_exit',
    '{"apps_used": ["Visual Studio Code", "Terminal"], "distractions_blocked": 2}'::jsonb
),
-- Session 2: Completed flow session
(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '1 day'),
    TIMEZONE('utc'::text, NOW() - INTERVAL '1 day' + INTERVAL '1 hour 30 minutes'),
    'PyCharm',
    'PyCharm',
    380.8,
    22.1,
    'natural_exit',
    '{"apps_used": ["PyCharm", "Browser"], "distractions_blocked": 5}'::jsonb
),
-- Session 3: Interrupted session
(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '12 hours'),
    TIMEZONE('utc'::text, NOW() - INTERVAL '12 hours' + INTERVAL '25 minutes'),
    'Visual Studio Code',
    'Slack',
    312.3,
    45.8,
    'app_switch_limit',
    '{"apps_used": ["Visual Studio Code", "Slack"], "distractions_blocked": 1}'::jsonb
),
-- Session 4: Recent completed session
(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '3 hours'),
    TIMEZONE('utc'::text, NOW() - INTERVAL '3 hours' + INTERVAL '2 hours'),
    'Jupyter Notebook',
    'Jupyter Notebook',
    298.7,
    18.9,
    'natural_exit',
    '{"apps_used": ["Jupyter Notebook", "Terminal"], "distractions_blocked": 3}'::jsonb
),
-- Session 5: Currently active session (no end_ts)
(
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '30 minutes'),
    NULL,
    'Visual Studio Code',
    NULL,
    NULL,
    NULL,
    NULL,
    '{"apps_used": ["Visual Studio Code"], "distractions_blocked": 0}'::jsonb
);

-- Get the session IDs we just created for events
-- Note: In a real scenario, you'd use the returned IDs from the insert above
-- For this example, we'll assume these are the IDs (you may need to adjust)

-- Insert events for the sessions
INSERT INTO events (session_id, user_id, ts, type, payload) VALUES
-- Events for Session 1
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'Visual Studio Code' ORDER BY start_ts DESC LIMIT 1 OFFSET 0),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '2 days'),
    'flow_started',
    '{"app": "Visual Studio Code", "typing_rate": 425}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'Visual Studio Code' ORDER BY start_ts DESC LIMIT 1 OFFSET 0),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '2 days' + INTERVAL '15 minutes'),
    'distraction_blocked',
    '{"domain": "youtube.com", "app": "Chrome"}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'Visual Studio Code' ORDER BY start_ts DESC LIMIT 1 OFFSET 0),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '2 days' + INTERVAL '30 minutes'),
    'distraction_blocked',
    '{"domain": "reddit.com", "app": "Firefox"}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'Visual Studio Code' ORDER BY start_ts DESC LIMIT 1 OFFSET 0),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '2 days' + INTERVAL '45 minutes'),
    'flow_ended',
    '{"reason": "natural_exit", "duration_minutes": 45}'::jsonb
),

-- Events for Session 2
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'PyCharm' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '1 day'),
    'flow_started',
    '{"app": "PyCharm", "typing_rate": 380}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'PyCharm' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '1 day' + INTERVAL '20 minutes'),
    'distraction_blocked',
    '{"domain": "twitter.com", "app": "Chrome"}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'PyCharm' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '1 day' + INTERVAL '45 minutes'),
    'app_switched',
    '{"from": "PyCharm", "to": "Browser", "duration": 30}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'PyCharm' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '1 day' + INTERVAL '1 hour 30 minutes'),
    'flow_ended',
    '{"reason": "natural_exit", "duration_minutes": 90}'::jsonb
),

-- Events for Session 3 (interrupted)
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND trigger_reason = 'app_switch_limit' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '12 hours'),
    'flow_started',
    '{"app": "Visual Studio Code", "typing_rate": 312}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND trigger_reason = 'app_switch_limit' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '12 hours' + INTERVAL '10 minutes'),
    'app_switched',
    '{"from": "Visual Studio Code", "to": "Slack", "duration": 120}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND trigger_reason = 'app_switch_limit' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '12 hours' + INTERVAL '25 minutes'),
    'flow_interrupted',
    '{"reason": "app_switch_limit", "app_switches": 4}'::jsonb
),

-- Events for Session 4
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'Jupyter Notebook' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '3 hours'),
    'flow_started',
    '{"app": "Jupyter Notebook", "typing_rate": 298}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'Jupyter Notebook' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '3 hours' + INTERVAL '30 minutes'),
    'idle_detected',
    '{"duration_seconds": 45, "threshold": 30}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND start_app = 'Jupyter Notebook' ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '3 hours' + INTERVAL '2 hours'),
    'flow_ended',
    '{"reason": "natural_exit", "duration_minutes": 120}'::jsonb
),

-- Events for Session 5 (active)
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND end_ts IS NULL ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '30 minutes'),
    'flow_started',
    '{"app": "Visual Studio Code", "typing_rate": 410}'::jsonb
),
(
    (SELECT id FROM sessions WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid AND end_ts IS NULL ORDER BY start_ts DESC LIMIT 1),
    'd368e836-63ed-438b-8513-e7799961822d'::uuid,
    TIMEZONE('utc'::text, NOW() - INTERVAL '15 minutes'),
    'milestone_reached',
    '{"minutes": 15, "typing_rate_avg": 395}'::jsonb
);

-- Query to verify the data was inserted
SELECT
    'Sessions' as table_name,
    COUNT(*) as count
FROM sessions
WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid

UNION ALL

SELECT
    'Events' as table_name,
    COUNT(*) as count
FROM events
WHERE user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid;

-- Show recent sessions with their event counts
SELECT
    s.id,
    s.start_ts,
    s.end_ts,
    s.start_app,
    s.avg_typing_rate,
    s.trigger_reason,
    COUNT(e.id) as event_count
FROM sessions s
LEFT JOIN events e ON s.id = e.session_id
WHERE s.user_id = 'd368e836-63ed-438b-8513-e7799961822d'::uuid
GROUP BY s.id, s.start_ts, s.end_ts, s.start_app, s.avg_typing_rate, s.trigger_reason
ORDER BY s.start_ts DESC;
