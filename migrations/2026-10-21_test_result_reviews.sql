-- Saved attempts, so a pupil can look back over a completed test or unit assessment
-- (core/db/reviews.py). One row per test_results row; the questions, answers and marks as JSON.
-- Run once in the Supabase SQL Editor. Until it is run, scores still save and "Review" says the
-- questions weren't kept.

CREATE TABLE IF NOT EXISTS test_result_reviews (
    test_result_id UUID PRIMARY KEY REFERENCES test_results(id) ON DELETE CASCADE,
    payload        JSONB NOT NULL,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE test_result_reviews ENABLE ROW LEVEL SECURITY;
CREATE POLICY "anon full access" ON test_result_reviews
    FOR ALL TO anon USING (true) WITH CHECK (true);
