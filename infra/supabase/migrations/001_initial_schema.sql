-- AI Flow State Facilitator - Initial Database Schema
-- Migration: 001_initial_schema.sql

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Sessions table: stores flow state sessions
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT DEFAULT 'local_user',
    start_ts TIMESTAMPTZ NOT NULL,
    end_ts TIMESTAMPTZ,
    start_app TEXT,
    end_app TEXT,
    avg_typing_rate NUMERIC,
    max_idle_gap NUMERIC,
    duration_seconds INTEGER,
    trigger_reason TEXT,
    meta JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Events table: stores raw behavioral events
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    ts TIMESTAMPTZ NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('keystroke', 'mouse_move', 'app_switch', 'idle_start', 'idle_end', 'flow_on', 'flow_off', 'block_attempt')),
    payload JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Settings table: stores user preferences and configuration
CREATE TABLE settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT DEFAULT 'local_user',
    key TEXT NOT NULL,
    value JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, key)
);

-- Agent logs table: stores agent diagnostic logs
CREATE TABLE agent_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ts TIMESTAMPTZ DEFAULT NOW(),
    level TEXT NOT NULL CHECK (level IN ('debug', 'info', 'warning', 'error', 'critical')),
    message TEXT NOT NULL,
    meta JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_sessions_start_ts ON sessions(start_ts DESC);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_events_session_id_ts ON events(session_id, ts);
CREATE INDEX idx_events_ts ON events(ts DESC);
CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_settings_user_key ON settings(user_id, key);
CREATE INDEX idx_agent_logs_ts ON agent_logs(ts DESC);
CREATE INDEX idx_agent_logs_level ON agent_logs(level);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_settings_updated_at BEFORE UPDATE ON settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- RPC functions for agent operations

-- Start a new session
CREATE OR REPLACE FUNCTION start_session(
    p_start_ts TIMESTAMPTZ,
    p_start_app TEXT,
    p_meta JSONB DEFAULT '{}'
)
RETURNS UUID AS $$
DECLARE
    v_session_id UUID;
BEGIN
    INSERT INTO sessions (start_ts, start_app, meta)
    VALUES (p_start_ts, p_start_app, p_meta)
    RETURNING id INTO v_session_id;
    
    RETURN v_session_id;
END;
$$ LANGUAGE plpgsql;

-- End a session
CREATE OR REPLACE FUNCTION end_session(
    p_session_id UUID,
    p_end_ts TIMESTAMPTZ,
    p_end_app TEXT,
    p_avg_typing_rate NUMERIC,
    p_max_idle_gap NUMERIC,
    p_trigger_reason TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE sessions
    SET 
        end_ts = p_end_ts,
        end_app = p_end_app,
        avg_typing_rate = p_avg_typing_rate,
        max_idle_gap = p_max_idle_gap,
        duration_seconds = EXTRACT(EPOCH FROM (p_end_ts - start_ts))::INTEGER,
        trigger_reason = p_trigger_reason
    WHERE id = p_session_id;
END;
$$ LANGUAGE plpgsql;

-- Insert event
CREATE OR REPLACE FUNCTION insert_event(
    p_session_id UUID,
    p_ts TIMESTAMPTZ,
    p_type TEXT,
    p_payload JSONB DEFAULT '{}'
)
RETURNS UUID AS $$
DECLARE
    v_event_id UUID;
BEGIN
    INSERT INTO events (session_id, ts, type, payload)
    VALUES (p_session_id, p_ts, p_type, p_payload)
    RETURNING id INTO v_event_id;
    
    RETURN v_event_id;
END;
$$ LANGUAGE plpgsql;

-- Get or create setting
CREATE OR REPLACE FUNCTION upsert_setting(
    p_user_id TEXT,
    p_key TEXT,
    p_value JSONB
)
RETURNS UUID AS $$
DECLARE
    v_setting_id UUID;
BEGIN
    INSERT INTO settings (user_id, key, value)
    VALUES (p_user_id, p_key, p_value)
    ON CONFLICT (user_id, key) 
    DO UPDATE SET value = p_value, updated_at = NOW()
    RETURNING id INTO v_setting_id;
    
    RETURN v_setting_id;
END;
$$ LANGUAGE plpgsql;

-- Cleanup old events (retention policy)
CREATE OR REPLACE FUNCTION cleanup_old_events(p_retention_days INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    v_deleted_count INTEGER;
BEGIN
    DELETE FROM events
    WHERE ts < NOW() - (p_retention_days || ' days')::INTERVAL
    AND type NOT IN ('flow_on', 'flow_off');
    
    GET DIAGNOSTICS v_deleted_count = ROW_COUNT;
    RETURN v_deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Insert default settings
INSERT INTO settings (key, value) VALUES
('flow_detection', '{
    "entry": {
        "typing_rate_min": 40,
        "app_switches_max": 2,
        "max_idle_gap_seconds": 4,
        "window_seconds": 300
    },
    "exit": {
        "typing_rate_min": 30,
        "app_switches_max": 2,
        "max_idle_gap_seconds": 6,
        "delay_seconds": 30
    },
    "metrics": {
        "typing_rate_window_seconds": 60,
        "rolling_window_seconds": 300
    }
}'::jsonb),
('blocklist', '{
    "domains": [
        "youtube.com",
        "reddit.com",
        "twitter.com",
        "x.com",
        "facebook.com",
        "instagram.com",
        "tiktok.com",
        "netflix.com",
        "twitch.tv",
        "discord.com"
    ]
}'::jsonb),
('whitelist', '{
    "domains": [],
    "apps": []
}'::jsonb),
('retention_policy', '{
    "raw_events_days": 30,
    "sessions_days": 365
}'::jsonb);

-- Enable Row Level Security (optional for MVP, prepared for future)
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_logs ENABLE ROW LEVEL SECURITY;

-- Create policies (allow all for local MVP)
CREATE POLICY "Allow all for local user" ON sessions FOR ALL USING (true);
CREATE POLICY "Allow all for local user" ON events FOR ALL USING (true);
CREATE POLICY "Allow all for local user" ON settings FOR ALL USING (true);
CREATE POLICY "Allow all for local user" ON agent_logs FOR ALL USING (true);
