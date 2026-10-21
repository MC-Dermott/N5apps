"""Assignment logic and page smoke tests (no database): venv/bin/python tests/test_assignments.py"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.db import assignments as db

ITEMS = [dict(qualification="Higher", topic="U", question_type="A"),
         dict(qualification="Higher", topic="U", question_type="B")]


def res(qt, score, total=5, **kw):
    return dict(qualification="Higher", topic="U", question_type=qt, score=score, total=total, **kw)


def test_item_status():
    assert db.item_status(ITEMS[0], [], 60)["state"] == db.NOT_STARTED
    assert db.item_status(ITEMS[0], [res("B", 5)], 60)["state"] == db.NOT_STARTED   # other item
    s = db.item_status(ITEMS[0], [res("A", 2)], 60)
    assert s["state"] == db.IN_PROGRESS and s["best"] == 40 and s["attempts"] == 1
    s = db.item_status(ITEMS[0], [res("A", 2), res("A", 3)], 60)                      # best counts, 3/5 = 60 %
    assert s["state"] == db.DONE and s["attempts"] == 2
    assert db.item_status(ITEMS[0], [res("A", 0, total=0)], 60)["state"] == db.NOT_STARTED


def test_assignment_status():
    s = db.assignment_status(ITEMS, [res("A", 5)], 60)
    assert (s["state"], s["done"], s["total"]) == (db.IN_PROGRESS, 1, 2)
    s = db.assignment_status(ITEMS, [res("A", 5), res("B", 4)], 60)
    assert s["state"] == db.DONE
    assert db.assignment_status(ITEMS, [], 60)["state"] == db.NOT_STARTED
    assert db.assignment_status(ITEMS, [res("A", 1)], 60)["state"] == db.IN_PROGRESS


def test_overdue():
    a = {"due_date": "2026-10-01"}
    assert db.is_overdue(a, db.NOT_STARTED, today=date(2026, 10, 8))
    assert not db.is_overdue(a, db.DONE, today=date(2026, 10, 8))
    assert not db.is_overdue({"due_date": None}, db.NOT_STARTED)


def test_recipients():
    students = [dict(id="1", class_code="5A"), dict(id="2", class_code="5b"), dict(id="3", class_code=None)]
    a = {"targets": [dict(class_code="5B"), dict(user_id="3")]}
    assert [s["id"] for s in db.recipients(a, students)] == ["2", "3"]


def test_save_test_result_omits_assignment_id_when_unset():
    from core.db import tracker
    sent = []

    class T:
        def insert(self, row): sent.append(row); return self
        def execute(self): return self
    class C:
        def table(self, _): return T()
    tracker.get_supabase = lambda: C()
    assert tracker.save_test_result("u", "Higher", "U", "A", 3, 5)
    assert "assignment_id" not in sent[0] and sent[0]["subject"] == "maths"
    assert tracker.save_test_result("u", "Higher", "U", "A", 3, 5, assignment_id="x")
    assert sent[1]["assignment_id"] == "x"


def test_review_roundtrip():
    from core.db import reviews
    from core.engine.question_factory import generate_question
    qs = [generate_question("Numeracy", "Fractions"), generate_question("Higher" and "Finance", "Credit Cards", qualification="Higher")]
    state = dict(questions=qs, answers=["1", ["a"]], results=[True, False], types=["Fractions", "Credit Cards"])
    back = reviews.attempt_from_json(__import__("json").loads(__import__("json").dumps(reviews.attempt_to_json(state))))
    assert [q.question_text for q in back["questions"]] == [q.question_text for q in qs]
    assert back["answers"] == ["1", ["a"]] and back["results"] == [True, False]
    assert all(q.worked_solution == b.worked_solution for q, b in zip(qs, back["questions"]))


def test_pages_render():
    from streamlit.testing.v1 import AppTest
    qual, unit, qt = "National 5", "Numeracy", "Fractions"
    item = dict(id="i1", assignment_id="a1", qualification=qual, topic=unit, question_type=qt)
    a = dict(id="a1", title="T", pass_pct=60, due_date="2026-10-01", items=[item], results=[],
             status=db.assignment_status([item], [], 60))
    script = f"""
import streamlit as st
from core.db import assignments as db
db.pupil_assignments = lambda user: [{a!r}]
from core.engine.session_manager import initialise_session
initialise_session()
from core.ui.assignments_ui import render_my_assignments, render_assignment_runner
user = {{"id": "u1", "username": "p", "class_code": "5A"}}
if st.session_state.get("active_assignment"):
    render_assignment_runner(user)
else:
    render_my_assignments(user)
"""
    at = AppTest.from_string(script).run(timeout=30)
    assert not at.exception, at.exception
    assert any("overdue" in e.label for e in at.expander)
    start = next(b for b in at.button if b.label == "Start")
    start.click(); at.run(timeout=30)
    assert not at.exception, at.exception
    assert any("Start Test" in b.label or "Start Unit" in b.label for b in at.button), [b.label for b in at.button]


def test_review_button_shows_saved_attempt():
    from streamlit.testing.v1 import AppTest
    qual, unit, qt = "National 5", "Numeracy", "Fractions"
    item = dict(id="i1", assignment_id="a1", qualification=qual, topic=unit, question_type=qt)
    res = dict(id="r1", qualification=qual, topic=unit, question_type=qt, score=3, total=5, taken_at="2026-10-21T09:00:00")
    a = dict(id="a1", title="T", pass_pct=0, due_date=None, items=[item], results=[res],
             status=db.assignment_status([item], [res], 0))
    assert a["status"]["state"] == db.DONE          # no pass mark: taking it once completes it
    script = f"""
import streamlit as st
from core.db import assignments as db, reviews
db.pupil_assignments = lambda user: [{a!r}]
from core.engine.question_factory import generate_question
qs = [generate_question("Numeracy", "Fractions") for _ in range(2)]
reviews.load_review = lambda rid: dict(questions=qs, answers=["1", "2"], results=[True, False], types=[])
from core.engine.session_manager import initialise_session
initialise_session()
from core.ui.assignments_ui import render_my_assignments
render_my_assignments({{"id": "u1", "username": "p", "class_code": "5A"}})
"""
    at = AppTest.from_string(script).run(timeout=30)
    assert not at.exception, at.exception
    next(b for b in at.button if b.label == "Review").click(); at.run(timeout=30)
    assert not at.exception, at.exception
    assert any("Review — attempt" in m.value for m in at.markdown), [m.value for m in at.markdown][:10]


def test_tracker_import_groups_identical_focus_sets():
    from core.db import tracker_import
    from core.engine.question_factory import QUAL_REGISTRY
    qual = "National 5"
    csv_text = ("username,qualification,unit,question_type,tracker_topic,topic_pct\n"
                f"a,{qual},Numeracy,Fractions,Fractions,40\n"
                f"b,{qual},Numeracy,Fractions,Fractions,35\n"
                f"c,{qual},Numeracy,Percentages,Percentages,50\n"
                f"c,{qual},Numeracy,Fractions,Fractions,50\n"
                f"d,{qual},Numeracy,Nonsense,X,10\n")
    groups, problems = tracker_import.parse(csv_text.encode(), QUAL_REGISTRY)
    assert [sorted(g["usernames"]) for g in groups] == [["a", "b"], ["c"]]
    assert groups[1]["topics"] == ["Percentages", "Fractions"] and len(groups[1]["items"]) == 2
    assert len(problems) == 1 and "Nonsense" in problems[0]
    assert tracker_import.parse(b"x,y\n1,2\n", QUAL_REGISTRY)[0] == []
    assert tracker_import.title_for("Focus", {"topics": list("abcd")}) == "Focus: a, b, c…"


def test_tracker_topic_map_matches_registry():
    import importlib.util
    path = Path("/Users/luke/Library/CloudStorage/OneDrive-GlowScotland/Resources/Apps/.pipeline-tools/assessment_tracker/topic_map.py")
    if not path.exists():
        return
    spec = importlib.util.spec_from_file_location("topic_map", path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    from core.engine.question_factory import QUAL_REGISTRY
    for lvl, units in m.MAP.items():
        for topics in units.values():
            for app_unit, qts in topics.values():
                for qt in qts:
                    assert qt in QUAL_REGISTRY[lvl][app_unit], (lvl, app_unit, qt)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
