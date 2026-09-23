"""Multipart questions (question.parts non-empty): the shared context is shown once, then
each part is answered and marked on its own — same layout as the N5 Physics app's scenarios."""
import streamlit as st

from core.ui.question_ui import render_question_header, render_answer_input
from core.ui.scaffold_ui import render_scaffold
from core.ui.solution_ui import render_solution, scored_parts


def _is_explain(part):
    return part.metadata.get("type") == "explain"


def _part_heading(part):
    st.markdown(f"**Part {part.metadata['label']}** {part.question_text}")


def render_multipart_practice(question, check):
    """Practice mode: each part unlocks once the previous one is submitted, and has its own
    scaffold, answer box, Submit button and feedback. `check(answer, expected) -> bool`.
    Returns (all_parts_done, all_scored_parts_correct)."""
    for i, part in enumerate(question.parts):
        key = f"mp_{question.qid}_{i}"
        unlocked = i == 0 or f"mp_{question.qid}_{i - 1}" in st.session_state
        label = part.metadata["label"]

        _part_heading(part)

        if unlocked and key not in st.session_state:
            if _is_explain(part):
                if st.button("Show Expected Answer", key=f"mp_reveal_{question.qid}_{i}", type="primary"):
                    st.session_state[key] = "revealed"
                    st.rerun()
            else:
                render_scaffold(part, suffix=f"part{i}")
                answer = render_answer_input(part, suffix=f"part{i}")
                if st.button(f"Submit Part {label}", key=f"mp_submit_{question.qid}_{i}", type="primary"):
                    if str(answer).strip():
                        st.session_state[key] = (answer, check(answer, part.correct_answer))
                        st.rerun()
                    else:
                        st.warning("Please enter an answer before submitting.")
        elif key in st.session_state:
            if _is_explain(part):
                st.info(f"**Expected answer:** {part.correct_answer}")
            else:
                _, correct = st.session_state[key]
                if correct:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. Correct answer: {part.correct_answer}")
                render_solution(part)

        if i < len(question.parts) - 1:
            st.divider()

    keys = [f"mp_{question.qid}_{i}" for i in range(len(question.parts))]
    all_done = all(k in st.session_state for k in keys)
    all_correct = all(st.session_state[k][1] for k, p in zip(keys, question.parts)
                      if not _is_explain(p) and k in st.session_state)
    return all_done, all_correct


def render_multipart_assessment(question, key_prefix, check):
    """Test / assessment modes: the scored parts are answered one at a time, with no feedback
    until the end (explain parts are skipped). Returns None until the last part is submitted,
    then (answers, all_correct) — the question only counts as correct if every part is."""
    parts = scored_parts(question)
    idx_key, ans_key = f"{key_prefix}_mp_idx", f"{key_prefix}_mp_answers"
    st.session_state.setdefault(idx_key, 0)
    st.session_state.setdefault(ans_key, [])
    j = st.session_state[idx_key]

    render_question_header(question)

    for prev, prev_answer in zip(parts[:j], st.session_state[ans_key]):
        _part_heading(prev)
        st.caption(f"Your answer: {prev_answer or '(blank)'}")
        st.divider()

    part = parts[j]
    st.markdown(f"**Part {part.metadata['label']}** ({j + 1} of {len(parts)}) {part.question_text}")
    answer = render_answer_input(part, suffix=f"{key_prefix}_p{j}")

    last = j == len(parts) - 1
    if st.button("Submit" if last else f"Submit Part {part.metadata['label']}",
                 key=f"{key_prefix}_mp_submit_{j}", type="primary"):
        st.session_state[ans_key].append(str(answer).strip())
        if not last:
            st.session_state[idx_key] += 1
            st.rerun()
        answers = st.session_state.pop(ans_key)
        st.session_state.pop(idx_key)
        return answers, all(check(a, p.correct_answer) for a, p in zip(answers, parts))
    return None
