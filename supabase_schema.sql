-- Run this in the Supabase SQL Editor (supabase.com → your project → SQL Editor)

CREATE TABLE users (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    username      TEXT        UNIQUE NOT NULL,
    password_hash TEXT        NOT NULL,
    role          TEXT        NOT NULL DEFAULT 'student'
                              CHECK (role IN ('student', 'teacher')),
    class_code    TEXT,
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

-- The app authenticates users itself (bcrypt password hashes checked in
-- core/auth/auth.py) rather than using Supabase Auth, and talks to Supabase
-- with only the `anon` API key — so RLS must allow that key full access, or
-- every query (login, signup, admin-key bypass, dashboard, attempt tracking)
-- silently returns zero rows instead of erroring. If Supabase's security
-- advisor enables RLS on these tables, run this to restore access:
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_results ENABLE ROW LEVEL SECURITY;

CREATE POLICY "anon full access" ON users
    FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon full access" ON question_attempts
    FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon full access" ON test_results
    FOR ALL TO anon USING (true) WITH CHECK (true);
