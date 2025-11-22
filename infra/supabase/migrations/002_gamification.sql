-- Add gamification stats table for tracking user progress

CREATE TABLE IF NOT EXISTS gamification_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT DEFAULT 'local_user',
    stamina INTEGER DEFAULT 0,
    resilience INTEGER DEFAULT 0,
    consistency INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    experience INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    total_sessions INTEGER DEFAULT 0,
    average_session_duration NUMERIC DEFAULT 0,
    personal_best_duration INTEGER DEFAULT 0,
    last_session_date DATE,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Add schedule table for imported timetables
CREATE TABLE IF NOT EXISTS user_schedule (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT DEFAULT 'local_user',
    day_of_week INTEGER,  -- 0-6 (Monday-Sunday)
    start_time TIME,
    duration_minutes INTEGER,
    task_name TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add index
CREATE INDEX idx_gamification_stats_user ON gamification_stats(user_id);
CREATE INDEX idx_user_schedule_user_day ON user_schedule(user_id, day_of_week);

-- Function to update gamification stats
CREATE OR REPLACE FUNCTION update_gamification_stats(
    p_user_id TEXT,
    p_stamina_add INTEGER DEFAULT 0,
    p_resilience_add INTEGER DEFAULT 0,
    p_session_duration INTEGER DEFAULT 0
)
RETURNS VOID AS $$
DECLARE
    v_current_stats RECORD;
    v_new_avg NUMERIC;
BEGIN
    -- Get current stats or create new
    SELECT * INTO v_current_stats
    FROM gamification_stats
    WHERE user_id = p_user_id;
    
    IF NOT FOUND THEN
        INSERT INTO gamification_stats (user_id, stamina, resilience)
        VALUES (p_user_id, p_stamina_add, p_resilience_add);
    ELSE
        -- Calculate new average
        IF p_session_duration > 0 THEN
            v_new_avg := (
                (v_current_stats.average_session_duration * v_current_stats.total_sessions) + 
                p_session_duration
            ) / (v_current_stats.total_sessions + 1);
        ELSE
            v_new_avg := v_current_stats.average_session_duration;
        END IF;
        
        -- Update stats
        UPDATE gamification_stats
        SET 
            stamina = stamina + p_stamina_add,
            resilience = resilience + p_resilience_add,
            total_sessions = CASE WHEN p_session_duration > 0 THEN total_sessions + 1 ELSE total_sessions END,
            average_session_duration = v_new_avg,
            personal_best_duration = GREATEST(personal_best_duration, p_session_duration),
            last_session_date = CASE WHEN p_session_duration > 0 THEN CURRENT_DATE ELSE last_session_date END,
            updated_at = NOW()
        WHERE user_id = p_user_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
