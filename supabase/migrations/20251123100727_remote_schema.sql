-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create all_users table for user profiles
CREATE TABLE public.all_users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT,
    full_name TEXT,
    onboarding_complete BOOLEAN DEFAULT FALSE,
    onboarding_step INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create events table for tracking user events
CREATE TABLE public.events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    ts TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    type TEXT NOT NULL,
    payload JSONB DEFAULT '{}'::jsonb
);

-- Create settings table for user settings
CREATE TABLE public.settings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    key TEXT NOT NULL,
    value JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    UNIQUE(user_id, key)
);

-- Create agent_logs table for logging
CREATE TABLE public.agent_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    level TEXT NOT NULL,
    message TEXT NOT NULL,
    meta JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create sessions table for flow sessions
CREATE TABLE public.sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    start_ts TIMESTAMP WITH TIME ZONE NOT NULL,
    end_ts TIMESTAMP WITH TIME ZONE,
    start_app TEXT,
    end_app TEXT,
    avg_typing_rate FLOAT,
    max_idle_gap FLOAT,
    trigger_reason TEXT,
    meta JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Enable Row Level Security
ALTER TABLE public.all_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;

-- RLS Policies for all_users
CREATE POLICY "Users can view their own profile" ON public.all_users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON public.all_users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile" ON public.all_users
    FOR INSERT WITH CHECK (auth.uid() = id);

-- RLS Policies for events
CREATE POLICY "Users can view their own events" ON public.events
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own events" ON public.events
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- RLS Policies for settings
CREATE POLICY "Users can view their own settings" ON public.settings
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own settings" ON public.settings
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own settings" ON public.settings
    FOR UPDATE USING (auth.uid() = user_id);

-- RLS Policies for agent_logs
CREATE POLICY "Users can view their own logs" ON public.agent_logs
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own logs" ON public.agent_logs
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- RLS Policies for sessions
CREATE POLICY "Users can view their own sessions" ON public.sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own sessions" ON public.sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own sessions" ON public.sessions
    FOR UPDATE USING (auth.uid() = user_id);

-- Function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.all_users (id, email, full_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to automatically create user profile on signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Function to get user profile
CREATE OR REPLACE FUNCTION public.get_user_profile()
RETURNS TABLE (
    id UUID,
    email TEXT,
    full_name TEXT,
    onboarding_complete BOOLEAN,
    onboarding_step INTEGER,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        au.id,
        au.email,
        au.full_name,
        au.onboarding_complete,
        au.onboarding_step,
        au.created_at,
        au.updated_at
    FROM public.all_users au
    WHERE au.id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to complete onboarding
CREATE OR REPLACE FUNCTION public.complete_onboarding()
RETURNS VOID AS $$
BEGIN
    UPDATE public.all_users
    SET
        onboarding_complete = TRUE,
        updated_at = TIMEZONE('utc'::text, NOW())
    WHERE id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to start session
CREATE OR REPLACE FUNCTION public.start_session(
    p_start_ts TIMESTAMP WITH TIME ZONE,
    p_start_app TEXT,
    p_meta JSONB DEFAULT '{}'::jsonb
)
RETURNS UUID AS $$
DECLARE
    session_id UUID;
BEGIN
    INSERT INTO public.sessions (
        user_id,
        start_ts,
        start_app,
        meta
    ) VALUES (
        auth.uid(),
        p_start_ts,
        p_start_app,
        p_meta
    ) RETURNING id INTO session_id;

    RETURN session_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to end session
CREATE OR REPLACE FUNCTION public.end_session(
    p_session_id UUID,
    p_end_ts TIMESTAMP WITH TIME ZONE,
    p_end_app TEXT,
    p_avg_typing_rate FLOAT,
    p_max_idle_gap FLOAT,
    p_trigger_reason TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.sessions
    SET
        end_ts = p_end_ts,
        end_app = p_end_app,
        avg_typing_rate = p_avg_typing_rate,
        max_idle_gap = p_max_idle_gap,
        trigger_reason = p_trigger_reason
    WHERE id = p_session_id AND user_id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to upsert setting
CREATE OR REPLACE FUNCTION public.upsert_setting(
    p_user_id UUID,
    p_key TEXT,
    p_value JSONB
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO public.settings (user_id, key, value, updated_at)
    VALUES (p_user_id, p_key, p_value, TIMEZONE('utc'::text, NOW()))
    ON CONFLICT (user_id, key)
    DO UPDATE SET
        value = p_value,
        updated_at = TIMEZONE('utc'::text, NOW());
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create indexes for better performance
CREATE INDEX idx_events_user_id ON public.events(user_id);
CREATE INDEX idx_events_session_id ON public.events(session_id);
CREATE INDEX idx_events_ts ON public.events(ts);
CREATE INDEX idx_settings_user_id ON public.settings(user_id);
CREATE INDEX idx_settings_key ON public.settings(key);
CREATE INDEX idx_agent_logs_user_id ON public.agent_logs(user_id);
CREATE INDEX idx_sessions_user_id ON public.sessions(user_id);
CREATE INDEX idx_sessions_start_ts ON public.sessions(start_ts);
