-- Batches: assignments made by one tracker run share a batch name, so the Track page shows the whole run as a
-- single entry (with each pupil's focus topics in a column) instead of one entry per set of topics.
-- NULL = a standalone assignment. Run once in the Supabase SQL Editor (the project is shared with N3apps; the
-- column is harmless to it).

ALTER TABLE assignments ADD COLUMN IF NOT EXISTS batch TEXT;

-- Tag the automatic "Focus topics —" assignments already made, one batch per day they were created.
UPDATE assignments SET batch = 'Focus topics, ' || to_char(created_at, 'DD Mon YYYY')
WHERE batch IS NULL AND subject = 'maths' AND title LIKE 'Focus topics —%';
