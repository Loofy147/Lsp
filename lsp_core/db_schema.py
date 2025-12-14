
"""
LSP Database Schema
- Defines the PostgreSQL database schema for the Learning Social Platform.
"""

# ============================================================================
# DATABASE SCHEMA
# ============================================================================

DATABASE_SCHEMA = """
-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    data_collection_consent BOOLEAN DEFAULT TRUE,
    social_profile_visibility VARCHAR(20) DEFAULT 'public',
    trust_tier VARCHAR(20) DEFAULT 'new_user',
    trust_score FLOAT DEFAULT 0.5,
    last_activity_at TIMESTAMP WITH TIME ZONE,
    total_activities INTEGER DEFAULT 0,
    INDEX idx_users_created (created_at),
    INDEX idx_users_trust_tier (trust_tier)
);

-- Activity events
CREATE TABLE activity_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    domain VARCHAR(50) NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    session_id UUID NOT NULL,
    sequence_position INTEGER NOT NULL,
    action_data JSONB NOT NULL,
    performance_metrics JSONB,
    capability_signals JSONB,
    context_data JSONB,
    engagement_level FLOAT,
    duration_seconds INTEGER,
    device_fingerprint VARCHAR(64),
    ip_address INET,
    INDEX idx_events_user_time (user_id, timestamp DESC),
    INDEX idx_events_domain (domain)
);

-- Capability scores
CREATE TABLE capability_scores (
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    dimension VARCHAR(50) NOT NULL,
    mean_score FLOAT NOT NULL,
    variance FLOAT NOT NULL,
    confidence FLOAT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, dimension)
);

-- Behavior patterns
CREATE TABLE behavior_patterns (
    pattern_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pattern_name VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    characteristic_behaviors JSONB,
    capability_profile JSONB,
    is_validated BOOLEAN DEFAULT FALSE,
    validation_score FLOAT,
    sample_size INTEGER,
    INDEX idx_patterns_validated (is_validated)
);

-- Achievements
CREATE TABLE achievements (
    achievement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    reward_concept_id UUID NOT NULL,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    earning_journey JSONB,
    user_satisfaction FLOAT,
    subsequent_motivation_boost FLOAT,
    INDEX idx_achievements_user (user_id)
);

-- Fraud signals
CREATE TABLE fraud_signals (
    signal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    signal_type VARCHAR(50) NOT NULL,
    severity FLOAT NOT NULL,
    description TEXT,
    evidence JSONB,
    action_taken VARCHAR(50),
    INDEX idx_fraud_user (user_id)
);

-- Wellbeing assessments
CREATE TABLE wellbeing_assessments (
    assessment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    overall_score FLOAT NOT NULL,
    concerns JSONB,
    positive_indicators JSONB,
    intervention_recommended BOOLEAN,
    INDEX idx_wellbeing_user (user_id)
);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
"""
