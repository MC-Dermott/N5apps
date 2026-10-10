"""Assignments: the pupil's 'My Assignments' page and runner, and the teacher's set/track page."""
from datetime import date, timedelta

import pandas as pd
import streamlit as st

from core.db import assignments as db
from core.db import tracker_import
from core.db.client import get_supabase
from core.engine.question_factory import QUAL_REGISTRY, calc_mode_available
from core.engine.session_manager import reset_test, reset_unit_assessment
from core.ui.test_ui import render_test
from core.ui.unit_assessment_ui import render_unit_assessment

UNIT_ASSESSMENT = "Unit Assessment"

_ICON = {db.DONE: "✅", db.IN_PROGRESS: "🟡", db.NOT_STARTED: "⚪"}


def _due_text(a, state):
    if not a.get("due_date"):
        return "No due date"
    due = date.fromisoformat(a["due_date"]).strftime("%a %d %b")
    return f"Due {due}" + (" — **overdue**" if db.is_overdue(a, state) else "")


# ── Pupil ─────────────────────────────────────────────────────────────────────

def render_my_assignments(user):
    st.header("My Assignments")
    try:
        assignments = db.pupil_assignments(user)
    except Exception as e:
        st.error(f"Could not load your assignments: {e}")
        return
    if not assignments:
        st.info("Nothing has been set for you yet.")
        return

    todo = [a for a in assignments if a["status"]["state"] != db.DONE]
    done = [a for a in assignments if a["status"]["state"] == db.DONE]
    for heading, group, expanded in (("To do", todo, True), ("Completed", done, False)):
        if not group:
            continue
        st.subheader(heading)
        for a in group:
            s = a["status"]
            with st.expander(f"{_ICON[s['state']]} {a['title']} — {s['done']}/{s['total']} done · "
                             f"{_due_text(a, s['state'])}", expanded=expanded):
                st.caption(f"Score at least **{a['pass_pct']}%** on each test to complete it. "
                           "You can retry as often as you like; your best score counts.")
                for n, (item, ist) in enumerate(zip(a["items"], s["items"])):
                    c1, c2, c3 = st.columns([5, 2, 2])
                    c1.markdown(f"{_ICON[ist['state']]} **{item['question_type']}** · {item['topic']} "
                                f"({item['qualification']})")
                    c2.caption("Not started" if ist["best"] is None
                               else f"Best {ist['best']:.0f}% · {ist['attempts']} attempt"
                                    f"{'s' if ist['attempts'] != 1 else ''}")
                    label = "Retry" if ist["attempts"] else "Start"
                    if c3.button(label, key=f"run_{a['id']}_{item['id']}",
                                 type="secondary" if ist["state"] == db.DONE else "primary"):
                        reset_test()
                        reset_unit_assessment()
                        st.session_state.active_assignment = {"assignment": a, "item": item}
                        st.rerun()


def render_assignment_runner(user):
    """One assignment test. Scores are saved with the assignment id, so they count."""
    ctx = st.session_state["active_assignment"]
    a, item = ctx["assignment"], ctx["item"]
    qual, unit, qtype = item["qualification"], item["topic"], item["question_type"]

    if st.button("← Back to my assignments"):
        st.session_state.pop("active_assignment", None)
        reset_test()
        reset_unit_assessment()
        st.rerun()
    st.subheader(a["title"])
    st.caption(f"{qual} · {unit} · {qtype} · pass mark {a['pass_pct']}%")

    state = st.session_state.unit_assessment if qtype == UNIT_ASSESSMENT else st.session_state.test
    calc_mode = False
    if qual != "Higher" and (qtype == UNIT_ASSESSMENT or calc_mode_available(unit, qtype, qualification=qual)):
        choice = st.radio("Calculator", ["Calculator", "Non-calculator"], horizontal=True,
                          disabled=bool(state["questions"]), key=f"asg_calc_{a['id']}_{item['id']}")
        calc_mode = choice == "Non-calculator"

    if qtype == UNIT_ASSESSMENT:
        render_unit_assessment(unit, qualification=qual, user_id=user["id"], calc_mode=calc_mode,
                               assignment_id=a["id"])
    else:
        render_test(unit, qtype, qualification=qual, user_id=user["id"], calc_mode=calc_mode,
                    assignment_id=a["id"])

    test = state
    if test.get("complete") and test["results"]:
        pct = 100 * sum(test["results"]) / len(test["results"])
        if pct >= a["pass_pct"]:
            st.success(f"✅ {pct:.0f}% — this one is complete.")
        else:
            st.warning(f"{pct:.0f}% — the pass mark is {a['pass_pct']}%. Read the review and try again.")


# ── Teacher ───────────────────────────────────────────────────────────────────

def _students():
    return (get_supabase().table("users").select("id,username,class_code").eq("role", "student")
            .order("username").execute().data or [])


def _topic_choices(qual, unit):
    return list(QUAL_REGISTRY[qual][unit].keys()) + [UNIT_ASSESSMENT]


def _render_set_new(teacher, students):
    items = st.session_state.setdefault("new_assignment_items", [])

    st.markdown("**1. Choose the work**")
    c1, c2, c3 = st.columns(3)
    qual = c1.selectbox("Level", list(QUAL_REGISTRY), key="na_qual")
    unit = c2.selectbox("Unit", list(QUAL_REGISTRY[qual]), key="na_unit")
    picks = c3.multiselect("Topics", _topic_choices(qual, unit), key=f"na_topics_{qual}_{unit}")
    if st.button("Add to assignment", disabled=not picks):
        for qt in picks:
            item = {"qualification": qual, "topic": unit, "question_type": qt}
            if item not in items:
                items.append(item)
        st.session_state.pop(f"na_topics_{qual}_{unit}", None)
        st.rerun()

    for n, item in enumerate(items):
        c1, c2 = st.columns([8, 1])
        c1.markdown(f"{n + 1}. **{item['question_type']}** · {item['topic']} ({item['qualification']})")
        if c2.button("✕", key=f"na_rm_{n}"):
            items.pop(n)
            st.rerun()

    st.markdown("**2. Who is it for?**")
    classes = sorted({s["class_code"] for s in students if s.get("class_code")})
    sel_classes = st.multiselect("Classes", classes, key="na_classes")
    names = {s["username"]: s["id"] for s in students}
    sel_pupils = st.multiselect("Individual pupils (as well as, or instead of, classes)", list(names), key="na_pupils")

    st.markdown("**3. Details**")
    title = st.text_input("Title", placeholder="e.g. Specific heat capacity practice", key="na_title")
    c1, c2, c3 = st.columns([2, 2, 2])
    no_due = c3.checkbox("No due date", key="na_nodue")
    due = c1.date_input("Due date", value=date.today() + timedelta(days=7), disabled=no_due, key="na_due")
    pass_pct = c2.number_input("Pass mark (%)", 0, 100, 60, step=5, key="na_pass")

    if st.button("Set assignment", type="primary"):
        err = db.create_assignment(teacher["id"], title, None if no_due else due, pass_pct, items,
                                   sel_classes, [names[p] for p in sel_pupils])
        if err:
            st.error(err)
        else:
            for k in ("new_assignment_items", "na_classes", "na_pupils", "na_title"):
                st.session_state.pop(k, None)
            st.session_state["assignment_set_msg"] = f"Assignment **{title.strip()}** set."
            st.rerun()


def _render_track(students):
    try:
        assignments = db.teacher_assignments()
    except Exception as e:
        st.error(f"Could not load assignments: {e}")
        return
    if not assignments:
        st.info("No assignments set yet.")
        return

    labels = {f"{a['title']}  ·  {a['created_at'][:10]}": a for a in assignments}
    a = labels[st.selectbox("Assignment", list(labels), key="track_assignment")]
    pupils = db.recipients(a, students)
    results = db.assignment_results(a["id"])

    rows, counts = [], {db.DONE: 0, db.IN_PROGRESS: 0, db.NOT_STARTED: 0}
    for p in pupils:
        mine = [r for r in results if r["user_id"] == p["id"]]
        s = db.assignment_status(a["items"], mine, a["pass_pct"])
        counts[s["state"]] += 1
        row = {"Pupil": p["username"], "Class": p.get("class_code") or "—"}
        for item, ist in zip(a["items"], s["items"]):
            row[item["question_type"]] = ("—" if ist["best"] is None else
                                          f"{_ICON[ist['state']]} {ist['best']:.0f}%")
        row["Status"] = ("⚠️ overdue · " if db.is_overdue(a, s["state"]) else "") + s["state"]
        rows.append(row)

    who = [f"class {t['class_code']}" for t in a["targets"] if t.get("class_code")]
    named = sum(1 for t in a["targets"] if t.get("user_id"))
    if named:
        who.append(f"{named} named pupil{'s' if named != 1 else ''}")
    st.caption(f"{a['pass_pct']}% pass mark · {_due_text(a, None)} · set for " + ", ".join(who))
    c1, c2, c3 = st.columns(3)
    c1.metric("Complete", f"{counts[db.DONE]}/{len(pupils)}")
    c2.metric("In progress", counts[db.IN_PROGRESS])
    c3.metric("Not started", counts[db.NOT_STARTED])
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download as CSV", df.to_csv(index=False).encode(),
                           file_name=f"{a['title']}.csv", mime="text/csv")
    else:
        st.info("No pupils match this assignment's classes yet.")

    with st.expander("Delete this assignment"):
        st.caption("Removes the assignment. Tests already taken stay as ordinary test results.")
        if st.button("Delete assignment", key="del_assignment"):
            err = db.delete_assignment(a["id"])
            st.error(err) if err else st.rerun()


def _render_import(teacher, students):
    st.caption("Upload the CSV made from your assessment tracker (export_app_assignments.py). Each pupil gets "
               "practice on their weakest topics; pupils with the same topics share one assignment.")
    up = st.file_uploader("App assignments CSV", type="csv", key="import_csv")
    if not up:
        return
    groups, problems = tracker_import.parse(up.getvalue(), QUAL_REGISTRY)
    for p in problems:
        st.warning(p)
    ids = {s["username"]: s["id"] for s in students}
    known = [{**g, "usernames": [u for u in g["usernames"] if u in ids]} for g in groups]
    unknown = sorted({u for g in groups for u in g["usernames"] if u not in ids})
    known = [g for g in known if g["usernames"]]
    if unknown:
        st.warning("No app account for: " + ", ".join(unknown) + " — they are skipped. "
                   "Check the App username column on the tracker's Pupils sheet.")
    if not known:
        st.info("Nothing to set.")
        return

    c1, c2, c3 = st.columns([3, 2, 2])
    base = c1.text_input("Title prefix", value="Focus practice", key="imp_title")
    no_due = c3.checkbox("No due date", key="imp_nodue")
    due = c2.date_input("Due date", value=date.today() + timedelta(days=7), disabled=no_due, key="imp_due")
    pass_pct = st.number_input("Pass mark (%)", 0, 100, 60, step=5, key="imp_pass")
    st.markdown(f"**{len(known)} assignment{'s' if len(known) != 1 else ''}** for "
                f"{sum(len(g['usernames']) for g in known)} pupils:")
    for g in known:
        with st.expander(f"{tracker_import.title_for(base, g)} — {len(g['usernames'])} pupil"
                         f"{'s' if len(g['usernames']) != 1 else ''}"):
            st.markdown("Pupils: " + ", ".join(g["usernames"]))
            st.markdown("\n".join(f"- {i['question_type']} · {i['topic']} ({i['qualification']})" for i in g["items"]))

    if st.button("Set these assignments", type="primary", key="imp_go"):
        errors = []
        for g in known:
            err = db.create_assignment(teacher["id"], tracker_import.title_for(base, g), None if no_due else due,
                                       pass_pct, g["items"], [], [ids[u] for u in g["usernames"]])
            if err:
                errors.append(err)
        if errors:
            st.error("\n\n".join(errors))
        else:
            st.session_state["assignment_set_msg"] = f"{len(known)} assignment(s) set from the tracker."
            st.rerun()


def render_teacher_assignments(teacher):
    st.header("Assignments")
    if msg := st.session_state.pop("assignment_set_msg", None):
        st.success(msg)
    try:
        students = _students()
    except Exception as e:
        st.error(f"Could not load pupils: {e}")
        return
    tab_track, tab_new, tab_import = st.tabs(["Track", "Set new", "Import from tracker"])
    with tab_track:
        _render_track(students)
    with tab_new:
        _render_set_new(teacher, students)
    with tab_import:
        _render_import(teacher, students)
