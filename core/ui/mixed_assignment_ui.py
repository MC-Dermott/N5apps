"""A mixed-practice assignment: one random exam-style question from each topic, answered as a single attempt
(Previous / Submit like a Test), scored and saved as one result under db.MIXED_KEY."""
import streamlit as st

from core.db import assignments as db
from core.db.tracker import save_test_result
from core.engine.question_factory import generate_mixed_assignment
from core.engine.session_manager import reset_mixed_assignment
from core.ui.assessment_nav import render_current_question
from core.ui.solution_ui import answer_display, correct_answer_display, render_common_mistake, render_solution
from core.ui.test_ui import _is_correct


def render_mixed_assignment(assignment, user_id):
    state = st.session_state.mixed_assignment
    items = assignment["items"]
    n = len(items)

    if not state["questions"]:
        st.markdown(f"This assignment has **{n} question{'s' if n != 1 else ''}**, one from each topic below, "
                    "in the style of the exam. Each is marked automatically and a full review is shown at the end.")
        st.markdown("\n".join(f"- {i['question_type']} · {i['topic']}" for i in items))
        if st.button("Start", type="primary", key="mixed_start"):
            reset_mixed_assignment()
            questions, types = generate_mixed_assignment(items)
            st.session_state.mixed_assignment.update(questions=questions, types=types)
            st.rerun()
        return

    if state["complete"]:
        if not state.get("saved") and user_id:
            if not save_test_result(user_id, db.MIXED_KEY["qualification"], db.MIXED_KEY["topic"],
                                    db.MIXED_KEY["question_type"], sum(state["results"]), n,
                                    assignment_id=assignment["id"], review_state=state):
                st.error("Your score could not be saved, so it won't count towards the assignment. "
                         "Please tell your teacher.")
            state["saved"] = True
        _render_summary(state)
        if st.button("Try again with new questions", type="primary", key="mixed_again"):
            reset_mixed_assignment()
            st.rerun()
        return

    idx = state["index"]
    st.progress((idx + 1) / n, text=f"Q{idx + 1} – {state['types'][idx]}  ({idx + 1} of {n})")
    render_current_question(state, "mixed", _is_correct)


def _render_summary(state):
    score, n = sum(state["results"]), len(state["results"])
    st.markdown(f"## Result: {score} / {n}")
    st.markdown("---")
    st.markdown("### Question Review")
    for i, (q, ans, ok) in enumerate(zip(state["questions"], state["answers"], state["results"])):
        label = f"Q{i + 1} – {state['types'][i]}"
        if ok:
            st.success(f"**{label}**  \n{q.question_text}  \nYour answer: **{answer_display(q, ans)}** ✅")
        else:
            with st.container(border=True):
                st.error(f"**{label}**  \n{q.question_text}  \nYour answer: **{answer_display(q, ans)}** ❌  \n"
                         f"Correct answer: **{correct_answer_display(q)}**")
                render_common_mistake(q, ans)
                render_solution(q)
