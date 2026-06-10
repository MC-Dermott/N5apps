-- Run this in the Supabase SQL Editor (supabase.com → your project → SQL Editor)

CREATE TABLE users (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    username      TEXT        UNIQUE NOT NULL,
    password_hash TEXT        NOT NULL,
    role          TEXT        NOT NULL DEFAULT 'student'
                              CHECK (role IN ('student', 'teacher')),
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE question_attempts (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id       UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    qualification TEXT        NOT NULL,
    topic         TEXT        NOT NULL,
    question_type TEXT        NOT NULL,
    correct       BOOLEAN     NOT NULL,
    attempted_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE test_results (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id       UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    qualification TEXT        NOT NULL,
    topic         TEXT        NOT NULL,
    question_type TEXT        NOT NULL,
    score         INTEGER     NOT NULL,
    total         INTEGER     NOT NULL,
    taken_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast per-user lookups
CREATE INDEX ON question_attempts (user_id);
CREATE INDEX ON test_results (user_id);
