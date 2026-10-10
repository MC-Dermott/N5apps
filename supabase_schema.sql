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
    subject       TEXT        NOT NULL DEFAULT 'maths',
    qualification TEXT        NOT NULL,
    topic         TEXT        NOT NULL,
    question_type TEXT        NOT NULL,
    correct       BOOLEAN     NOT NULL,
    attempted_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE test_results (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id       UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject       TEXT        NOT NULL DEFAULT 'maths',
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


-- ===========================================================================
-- MIGRATION — if this project already existed before N3apps joined it, run
-- just this against the live project instead of the CREATE TABLE statements
-- above. Safe to run even if `subject` already exists (IF NOT EXISTS).
-- Existing rows backfill to 'maths', which is correct since this project only
-- ever tracked maths before N3apps was added — see N3apps' own
-- supabase_schema.sql for the equivalent migration.
-- ===========================================================================
ALTER TABLE question_attempts ADD COLUMN IF NOT EXISTS subject TEXT NOT NULL DEFAULT 'maths';
ALTER TABLE test_results      ADD COLUMN IF NOT EXISTS subject TEXT NOT NULL DEFAULT 'maths';

-- ── Assignments (migrations/2026-10-10_assignments.sql) ──
-- Assignments for N5apps. This Supabase project is shared with N3apps, so assignments carry a
-- `subject` ('maths') and each app only shows its own. A teacher picks topic tests (items), a pass
-- mark and a due date, and targets whole classes (class_code) and/or individual pupils. Work counts
-- only if the test was taken through the assignment (test_results.assignment_id).
-- Run once in the Supabase SQL Editor.

CREATE TABLE IF NOT EXISTS assignments (
    id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    subject     TEXT        NOT NULL DEFAULT 'maths',
    title       TEXT        NOT NULL,
    created_by  UUID        REFERENCES users(id) ON DELETE SET NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    due_date    DATE,
    pass_pct    INTEGER     NOT NULL DEFAULT 60 CHECK (pass_pct BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS assignment_items (
    id            UUID    DEFAULT gen_random_uuid() PRIMARY KEY,
    assignment_id UUID    NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    position      INTEGER NOT NULL DEFAULT 0,
    qualification TEXT    NOT NULL,
    topic         TEXT    NOT NULL,
    question_type TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS assignment_targets (
    id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    assignment_id UUID NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    class_code    TEXT,
    user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
    CHECK ((class_code IS NOT NULL) <> (user_id IS NOT NULL))
);

ALTER TABLE test_results ADD COLUMN IF NOT EXISTS assignment_id UUID
    REFERENCES assignments(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS assignment_items_assignment_idx   ON assignment_items (assignment_id);
CREATE INDEX IF NOT EXISTS assignment_targets_assignment_idx ON assignment_targets (assignment_id);
CREATE INDEX IF NOT EXISTS assignment_targets_user_idx       ON assignment_targets (user_id);
CREATE INDEX IF NOT EXISTS test_results_assignment_idx       ON test_results (assignment_id);

-- This app talks to Supabase with the anon key (see the note in supabase_schema.sql), so RLS needs
-- an "anon full access" policy on each new table or every query silently returns nothing.
ALTER TABLE assignments        ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignment_items   ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignment_targets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "anon full access" ON assignments
    FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon full access" ON assignment_items
    FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "anon full access" ON assignment_targets
    FOR ALL TO anon USING (true) WITH CHECK (true);
