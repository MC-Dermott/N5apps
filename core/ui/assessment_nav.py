"""Answering the current question of a Test, Unit Assessment or N5 Numeracy assessment. Pupils
can go back with ← Previous and change any answer right up until they submit the last question,
which ends the test."""
import streamlit as st

from core.ui.question_ui import render_question, prefill_answer_input
from core.ui.multipart_ui import (
    render_multipart_assessment, start_multipart_at_last_part, assessment_nav_buttons,
)

GO_BACK_HINT = "You can go back and change an answer until you submit the last question."


def render_current_question(state, key_prefix, check):
    """Draw state["questions"][state["index"]] with Previous / Submit buttons and record the
    answer in state["answers"] / state["results"] at that question's position."""
    questions = state["questions"]
    for k in ("answers", "results"):
        state[k] += [None] * (len(questions) - len(state[k]))
    idx = state["index"]
    question = questions[idx]
    saved = state["answers"][idx]
    st.caption(GO_BACK_HINT)

    if question.parts:
        result = render_multipart_assessment(question, _mp_prefix(key_prefix, question), check,
                                             saved=saved, can_go_back=idx > 0)
        if result is None:
            return
        action, answer, correct = result
        answered = action == "submit" or any(answer)
    else:
        refilled = prefill_answer_input(question, key_prefix, saved)
        answer = render_question(question, suffix=key_prefix)
        if not refilled and saved and not str(answer).strip():
            st.caption(f"Your saved answer: {saved} — leave this blank to keep it.")
            answer = saved
        back, submit = assessment_nav_buttons(f"{key_prefix}_{idx}", idx > 0, "Submit")
        if not (back or submit):
            return
        action = "back" if back else "submit"
        correct = check(answer, question.correct_answer)
        answered = submit or bool(str(answer).strip())

    if answered:   # going back keeps whatever was typed, but doesn't record a blank as an answer
        state["answers"][idx] = answer
        state["results"][idx] = correct

    if action == "back":
        state["index"] -= 1
        previous = questions[state["index"]]
        if previous.parts:
            start_multipart_at_last_part(previous, _mp_prefix(key_prefix, previous))
    elif idx == len(questions) - 1:
        state["complete"] = True
    else:
        state["index"] += 1
        upcoming = questions[state["index"]]
        if upcoming.parts:
            st.session_state.pop(f"{_mp_prefix(key_prefix, upcoming)}_mp_idx", None)
    st.rerun()


def _mp_prefix(key_prefix, question):
    return f"{key_prefix}_{question.qid}"
