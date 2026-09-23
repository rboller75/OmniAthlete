--OmniAthlete Schema

-- 1. Users
CREATE TABLE users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,

    email VARCHAR(255) UNIQUE NOT NULL,

    sport VARCHAR(100),
    team VARCHAR(100),

    role VARCHAR(20) NOT NULL DEFAULT 'athlete'
        CHECK (role IN ('athlete', 'coach', 'admin')),

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Daily 30-Second Check-In
CREATE TABLE daily_checkins (
    checkin_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id BIGINT NOT NULL
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    checkin_date DATE NOT NULL,

    sleep_quality INTEGER NOT NULL
        CHECK (sleep_quality BETWEEN 1 AND 7),

    stress_level INTEGER NOT NULL
        CHECK (stress_level BETWEEN 1 AND 7),

    fatigue_level INTEGER NOT NULL
        CHECK (fatigue_level BETWEEN 1 AND 7),

    muscle_soreness INTEGER NOT NULL
        CHECK (muscle_soreness BETWEEN 1 AND 7),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_daily_checkin
        UNIQUE (user_id, checkin_date)
);

-- 3. Athlete Burnout Questionnaire (ABQ) Assessments
CREATE TABLE burnout_assessments (
    assessment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id BIGINT NOT NULL
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    assessment_date DATE NOT NULL,

    exhaustion_score NUMERIC(5,2),

    reduced_accomplishment_score NUMERIC(5,2),

    sport_devaluation_score NUMERIC(5,2),

    overall_burnout_score NUMERIC(5,2),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. Risk Alerts
CREATE TABLE risk_alerts (
    alert_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id BIGINT NOT NULL
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    checkin_id BIGINT
        REFERENCES daily_checkins(checkin_id)
        ON DELETE SET NULL,

    assessment_id BIGINT
        REFERENCES burnout_assessments(assessment_id)
        ON DELETE SET NULL,

    alert_date DATE NOT NULL,

    risk_level VARCHAR(10) NOT NULL
        CHECK (risk_level IN ('green', 'yellow', 'red')),

    reason TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);