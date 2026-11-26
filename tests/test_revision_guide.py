"""Revision guide page and Practise buttons (no database): venv/bin/python tests/test_revision_guide.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest

from core.db import assignments, revision
from core.engine.question_factory import QUAL_REGISTRY

assignments.outstanding_count = lambda user: 0

ROW = dict(id="r1", qualification="Higher", tracker_unit="Finance and Planning", topic="Insurance", status="focus", pct=25,
           source="own", marks_got=1, marks_out=4, weak_areas=[], revise=[],
           practice=[dict(unit="Planning", question_type="Networks")], rank=1)


def app(rows):
    revision.fetch_guide = lambda user_id: rows
    import core.ui.revision_guide_ui as ui
    ui.fetch_guide = revision.fetch_guide
    at = AppTest.from_file(str(ROOT / "n5_app.py"), default_timeout=60)
    at.session_state["user"] = dict(id="u", username="sample", role="student")
    return at.run()


def click(at, start):
    next(b for b in at.button if b.label.startswith(start)).click().run()
    assert not at.exception, at.exception


def test_page_states():
    for rows, text in ((None, "isn't switched on"), ([], "hasn't made your revision guide")):
        at = app(rows)
        click(at, "🧭 My Revision Guide")
        assert any(text in i.value for i in at.info)


def test_practise_button_preselects_topic():
    at = app([ROW])
    click(at, "🧭 My Revision Guide")
    click(at, "🎯 Practise")
    assert at.session_state["qualification"] == "Higher"
    assert [s.value for s in at.selectbox][:2] == ["Planning", "Networks"]
    assert at.radio[0].value == "Practice"
    click(at, "Generate Question")                       # the selection survives a rerun
    assert [s.value for s in at.selectbox][:2] == ["Planning", "Networks"]
    at.selectbox[0].select("Finance").run()              # and the pupil can still change it
    assert not at.exception and at.selectbox[0].value == "Finance"


def test_goto_after_browsing_replaces_old_selection():
    at = app([ROW])
    click(at, "Higher")
    at.selectbox[0].select("Finance").run()
    click(at, "← Change Level")
    click(at, "🧭 My Revision Guide")
    click(at, "🎯 Practise")
    assert [s.value for s in at.selectbox][:2] == ["Planning", "Networks"]


def test_sync_practice_targets_exist():
    from pathlib import Path as P
    import importlib.util
    tools = P.home() / "Library/CloudStorage/OneDrive-GlowScotland/Resources/Apps/.pipeline-tools/assessment_tracker"
    if not tools.exists():
        return
    spec = importlib.util.spec_from_file_location("maths_topic_map", tools / "topic_map.py")
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    for level, sheets in tm.MAP.items():
        for topics in sheets.values():
            for unit, qts in topics.values():
                assert all(q in QUAL_REGISTRY[level][unit] for q in qts), (level, unit, qts)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
