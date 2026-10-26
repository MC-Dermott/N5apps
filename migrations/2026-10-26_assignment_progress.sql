-- Part-finished assignment tests. When a pupil leaves an assignment test half way, their questions, answers
-- and position are kept here (one row per pupil per assignment item) so they can Continue later or Start over.
-- The row is deleted when the test is submitted or the pupil starts over. Scores don't depend on this table.
-- Run once in the Supabase SQL Editor.

CREATE TABLE IF NOT EXISTS assignment_progress (
    id                 UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id            UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assignment_item_id UUID        NOT NULL REFERENCES assignment_items(id) ON DELETE CASCADE,
    q_index            INTEGER     NOT NULL DEFAULT 0,
    q_total            INTEGER     NOT NULL DEFAULT 0,
    payload            JSONB       NOT NULL,
    updated_at         TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, assignment_item_id)
);

CREATE INDEX IF NOT EXISTS assignment_progress_user_idx ON assignment_progress (user_id);

ALTER TABLE assignment_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "anon full access" ON assignment_progress
    FOR ALL TO anon USING (true) WITH CHECK (true);
