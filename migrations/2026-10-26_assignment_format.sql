-- Mixed-practice assignments: one random exam-style question per topic, done as a single attempt, instead
-- of a 5-question test for each topic. 'tests' (the default) keeps every existing assignment as it was.
-- Run once in the Supabase SQL Editor.

ALTER TABLE assignments ADD COLUMN IF NOT EXISTS format TEXT NOT NULL DEFAULT 'tests'
    CHECK (format IN ('tests', 'mixed'));
