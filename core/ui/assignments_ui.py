"""Assignments: the pupil's 'My Assignments' page and runner, and the teacher's set/track page."""
from datetime import date, timedelta

import pandas as pd
import streamlit as st

from core.db import assignments as db
from core.db import progress, reviews, tracker_import
from core.db.client import get_supabase
from core.engine.question_factory import QUAL_REGISTRY, calc_mode_available
from core.engine.session_manager import reset_mixed_assignment, reset_test, reset_unit_assessment
from core.ui.solution_ui import answer_display, correct_answer_display, render_common_mistake, render_solution
from core.ui.mixed_assignment_ui import render_mixed_assignment
from core.ui.test_ui import render_test
from core.ui.unit_assessment_ui import render_unit_assessment

UNIT_ASSESSMENT = "Unit Assessment"

_ICON = {db.DONE: "✅", db.IN_PROGRESS: "🟡", db.NOT_STARTED: "⚪"}


def _how_it_counts(a):
    if a["pass_pct"]:
        return (f"Score at least **{a['pass_pct']}%** on each test to complete it. "
                "You can retry as often as you like; your best score counts.")
    return ("Complete each test and your score is recorded. You can retry as often as you like; "
            "your best score counts. Use **Review** to look back over an attempt.")


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

    paused = progress.progress_summaries(user["id"])
    todo = [a for a in assignments if a["status"]["state"] != db.DONE]
    done = [a for a in assignments if a["status"]["state"] == db.DONE]
    for heading, group, expanded in (("To do", todo, True), ("Completed", done, False)):
        if not group:
            continue
        st.subheader(heading)
        for a in group:
            s = a["status"]
            mixed = db.is_mixed(a)
            progress_text = (f"{len(a['items'])} questions" if mixed else f"{s['done']}/{s['total']} done")
            with st.expander(f"{_ICON[s['state']]} {a['title']} — {progress_text} · "
                             f"{_due_text(a, s['state'])}", expanded=expanded):
                st.caption(_how_it_counts(a))
                if mixed:
                    _render_mixed_row(a, s["items"][0], paused.get(a["items"][0]["id"]))
                    continue
                for n, (item, ist) in enumerate(zip(a["items"], s["items"])):
                    c1, c2, c3, c4 = st.columns([5, 2, 1.5, 1.5])
                    c1.markdown(f"{_ICON[ist['state']]} **{item['question_type']}** · {item['topic']} "
                                f"({item['qualification']})")
                    saved = paused.get(item["id"])
                    attempts = ("Not started" if ist["best"] is None
                                else f"Best {ist['best']:.0f}% · {ist['attempts']} attempt"
                                     f"{'s' if ist['attempts'] != 1 else ''}")
                    c2.caption(f"⏸ Paused at Q{saved['index'] + 1} of {saved['total']} · {attempts}"
                               if saved else attempts)
                    label = "Continue" if saved else "Retry" if ist["attempts"] else "Start"
                    if c3.button(label, key=f"run_{a['id']}_{item['id']}",
                                 type="secondary" if ist["state"] == db.DONE and not saved else "primary"):
                        reset_test()
                        reset_unit_assessment()
                        st.session_state.active_assignment = {"assignment": a, "item": item}
                        st.rerun()
                    latest = _latest_result(a, item)
                    key = f"review_{a['id']}_{item['id']}"
                    if latest and c4.button("Hide" if st.session_state.get(key) else "Review", key=f"btn_{key}"):
                        st.session_state[key] = not st.session_state.get(key)
                        st.rerun()
                    if latest and st.session_state.get(key):
                        _render_review(latest)


def _render_mixed_row(a, ist, saved):
    """A mixed-practice assignment is one attempt: list its topics, then Start / Continue / Retry and Review."""
    first = a["items"][0]
    st.markdown("One exam-style question from each of: "
                + ", ".join(f"**{i['question_type']}**" for i in a["items"]) + ".")
    c1, c2, c3 = st.columns([5, 2, 1.5])
    attempts = ("Not started" if ist["best"] is None
                else f"Best {ist['best']:.0f}% · {ist['attempts']} attempt{'s' if ist['attempts'] != 1 else ''}")
    c1.caption(f"⏸ Paused at Q{saved['index'] + 1} of {saved['total']} · {attempts}" if saved else attempts)
    label = "Continue" if saved else "Retry" if ist["attempts"] else "Start"
    if c2.button(label, key=f"run_{a['id']}", type="secondary" if ist["state"] == db.DONE and not saved else "primary"):
        reset_test()
        reset_unit_assessment()
        reset_mixed_assignment()
        st.session_state.active_assignment = {"assignment": a, "item": first}
        st.rerun()
    latest = _latest_result(a, None)
    key = f"review_{a['id']}"
    if latest and c3.button("Hide" if st.session_state.get(key) else "Review", key=f"btn_{key}"):
        st.session_state[key] = not st.session_state.get(key)
        st.rerun()
    if latest and st.session_state.get(key):
        _render_review(latest)


def _latest_result(a, item):
    if item is None:       # mixed assignment: every result belongs to the one attempt
        rows = list(a["results"])
        return max(rows, key=lambda r: r.get("taken_at") or "", default=None)
    rows = [r for r in a["results"] if (r["qualification"], r["topic"], r["question_type"])
            == (item["qualification"], item["topic"], item["question_type"])]
    return max(rows, key=lambda r: r.get("taken_at") or "", default=None)


def _render_review(result):
    """Read-only look back over a completed attempt: every question, the pupil's answer, the correct
    answer and the worked solution."""
    when = (result.get("taken_at") or "")[:10]
    try:
        attempt = reviews.load_review(result["id"])
    except Exception:
        attempt = None
    if not attempt:
        st.info(f"Your score from {when} was {result['score']} / {result['total']}. "
                "The questions from this attempt weren't saved, so they can't be shown.")
        return
    with st.container(border=True):
        st.markdown(f"**Review — attempt on {when}: {result['score']} / {result['total']}**")
        for i, (q, ans, ok) in enumerate(zip(attempt["questions"], attempt["answers"], attempt["results"])):
            label = f"Q{i + 1}" + (f" – {attempt['types'][i]}" if attempt["types"] else "")
            st.markdown(f"**{label}**  \n{q.question_text}")
            if ok:
                st.success(f"Your answer: **{answer_display(q, ans)}** ✅")
            else:
                st.error(f"Your answer: **{answer_display(q, ans)}** ❌  \n"
                         f"Correct answer: **{correct_answer_display(q)}**")
                render_common_mistake(q, ans)
            with st.expander("Worked solution"):
                render_solution(q)


def render_assignment_runner(user):
    """One assignment test. Scores are saved with the assignment id, so they count."""
    ctx = st.session_state["active_assignment"]
    a, item = ctx["assignment"], ctx["item"]
    qual, unit, qtype = item["qualification"], item["topic"], item["question_type"]

    mixed = db.is_mixed(a)
    if st.button("← Back to my assignments"):
        st.session_state.pop("active_assignment", None)
        reset_test()
        reset_unit_assessment()
        reset_mixed_assignment()
        st.rerun()
    st.subheader(a["title"])
    st.caption(("Mixed practice · exam-style questions" if mixed else f"{qual} · {unit} · {qtype}")
               + (f" · pass mark {a['pass_pct']}%" if a["pass_pct"] else ""))

    state_key = "mixed_assignment" if mixed else "unit_assessment" if qtype == UNIT_ASSESSMENT else "test"
    state = st.session_state[state_key]
    calc_key = f"asg_calc_{a['id']}_{item['id']}"

    # A part-finished attempt is kept; offer to carry on or throw it away before anything else is drawn.
    if "saved" not in ctx:
        ctx["saved"] = progress.load_progress(user["id"], item["id"])
    if ctx["saved"] and not state["questions"]:
        saved_state, saved_calc = ctx["saved"]
        st.info(f"You have an unfinished attempt — you were on question {saved_state['index'] + 1} of "
                f"{len(saved_state['questions'])} and had answered {progress.answered_count(saved_state)}. "
                "You can pick up where you left off, or start again with a new set of questions.")
        cont, over, _ = st.columns([1, 1, 3])
        if cont.button("Continue", type="primary", key="asg_continue"):
            st.session_state[state_key] = saved_state
            st.session_state[calc_key] = "Non-calculator" if saved_calc else "Calculator"
            ctx["saved"] = None
            ctx["fp"] = None
            st.rerun()
        if over.button("Start over", key="asg_start_over"):
            progress.delete_progress(user["id"], item["id"])
            ctx["saved"] = None
            st.rerun()
        return

    calc_mode = False
    if not mixed and qual != "Higher" and (qtype == UNIT_ASSESSMENT or calc_mode_available(unit, qtype, qualification=qual)):
        choice = st.radio("Calculator", ["Calculator", "Non-calculator"], horizontal=True,
                          disabled=bool(state["questions"]), key=calc_key)
        calc_mode = choice == "Non-calculator"

    # Save after every submitted answer (and every Previous), so leaving at any point keeps the work so far.
    if not state["questions"]:
        ctx["cleared"] = False
    elif not state["complete"] and (state["index"] or progress.answered_count(state)):
        fp = (state["index"], repr(state["answers"]))
        if fp != ctx.get("fp"):
            progress.save_progress(user["id"], item["id"], state, calc_mode)
            ctx["fp"] = fp

    if mixed:
        render_mixed_assignment(a, user["id"])
    elif qtype == UNIT_ASSESSMENT:
        render_unit_assessment(unit, qualification=qual, user_id=user["id"], calc_mode=calc_mode,
                               assignment_id=a["id"])
    else:
        render_test(unit, qtype, qualification=qual, user_id=user["id"], calc_mode=calc_mode,
                    assignment_id=a["id"])

    test = st.session_state[state_key]
    if test.get("complete") and not ctx.get("cleared"):
        progress.delete_progress(user["id"], item["id"])
        ctx["cleared"] = True
    if test.get("complete") and test["results"]:
        pct = 100 * sum(test["results"]) / len(test["results"])
        if pct >= a["pass_pct"]:
            st.success(f"✅ {pct:.0f}% — this one is complete and your score is recorded. "
                       "You can look back over it from My Assignments.")
        else:
            st.warning(f"{pct:.0f}% — the pass mark is {a['pass_pct']}%. Read the review and try again.")


# ── Teacher ───────────────────────────────────────────────────────────────────

def _students():
    return (get_supabase().table("users").select("id,username,class_code").eq("role", "student")
            .order("username").execute().data or [])


def _topic_choices(qual, unit, mixed=False):
    return list(QUAL_REGISTRY[qual][unit].keys()) + ([] if mixed else [UNIT_ASSESSMENT])


def _render_set_new(teacher, students):
    items = st.session_state.setdefault("new_assignment_items", [])

    st.markdown("**1. Choose the work**")
    fmt = st.radio("Format", ["Tests (5 questions on each topic)", "Mixed practice (one exam-style question per topic)"],
                   key="na_format", horizontal=True,
                   help="Mixed practice is a single attempt with one question from each topic you add — an "
                        "exam-style one where the topic has them, otherwise a random question.")
    mixed = fmt.startswith("Mixed")
    if mixed and any(i["question_type"] == UNIT_ASSESSMENT for i in items):
        items[:] = [i for i in items if i["question_type"] != UNIT_ASSESSMENT]
    c1, c2, c3 = st.columns(3)
    qual = c1.selectbox("Level", list(QUAL_REGISTRY), key="na_qual")
    unit = c2.selectbox("Unit", list(QUAL_REGISTRY[qual]), key="na_unit")
    picks = c3.multiselect("Topics", _topic_choices(qual, unit, mixed), key=f"na_topics_{qual}_{unit}")
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
                                   sel_classes, [names[p] for p in sel_pupils],
                                   fmt=db.MIXED if mixed else "tests")
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
        s = db.assignment_status(a["items"], mine, a["pass_pct"], a.get("format", "tests"))
        counts[s["state"]] += 1
        row = {"Pupil": p["username"], "Class": p.get("class_code") or "—"}
        if db.is_mixed(a):
            ist = s["items"][0]
            row["Best score"] = "—" if ist["best"] is None else f"{ist['best']:.0f}%"
            row["Attempts"] = ist["attempts"]
        else:
            for item, ist in zip(a["items"], s["items"]):
                row[item["question_type"]] = ("—" if ist["best"] is None else
                                              f"{_ICON[ist['state']]} {ist['best']:.0f}%")
        row["Status"] = ("⚠️ overdue · " if db.is_overdue(a, s["state"]) else "") + s["state"]
        rows.append(row)

    who = [f"class {t['class_code']}" for t in a["targets"] if t.get("class_code")]
    named = sum(1 for t in a["targets"] if t.get("user_id"))
    if named:
        who.append(f"{named} named pupil{'s' if named != 1 else ''}")
    st.caption((f"{a['pass_pct']}% pass mark · " if a["pass_pct"] else "No pass mark · ") + f"{_due_text(a, None)} · set for " + ", ".join(who))
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
