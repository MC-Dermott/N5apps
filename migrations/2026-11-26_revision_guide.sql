-- Pupil revision guide: one row per pupil per topic, written by
-- Resources/Apps/.pipeline-tools/assessment_tracker/sync_revision_guide.py from the unit assessment trackers and shown on the
-- pupil's "My Revision Guide" page (core/db/revision.py, core/ui/revision_guide_ui.py).
-- Run once in the Supabase SQL Editor. Until it is run the page says it isn't switched on.

CREATE TABLE IF NOT EXISTS revision_guide (
    id             UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    qualification  TEXT NOT NULL,            -- app level: Higher / National 5
    tracker_unit   TEXT NOT NULL,            -- sheet in the assessment tracker
    topic          TEXT NOT NULL,            -- tracker topic
    status         TEXT NOT NULL,            -- focus | developing | secure | strong | not_yet
    pct            NUMERIC,                  -- topic %
    homework_pct   NUMERIC,
    assessment_pct NUMERIC,
    marks_got      INT,
    marks_out      INT,
    weak_areas     JSONB NOT NULL DEFAULT '[]',   -- unused by the maths sync so far
    revise         JSONB NOT NULL DEFAULT '[]',   -- [{label, url}] summary sheets
    practice       JSONB NOT NULL DEFAULT '[]',   -- [{unit, question_type}] app practice
    source         TEXT NOT NULL DEFAULT 'own',  -- own marks, or the class's results ('class')
    rank           INT NOT NULL DEFAULT 0,        -- 1 = weakest
    updated_at     TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, qualification, tracker_unit, topic)
);

ALTER TABLE revision_guide ENABLE ROW LEVEL SECURITY;
CREATE POLICY "anon full access" ON revision_guide
    FOR ALL TO anon USING (true) WITH CHECK (true);
