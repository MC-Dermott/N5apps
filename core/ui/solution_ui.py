import streamlit as st

from core.models.answers import common_mistake
from core.ui.spreadsheet_solution_ui import render_spreadsheet_solution


def render_common_mistake(question, answer):
    """If a wrong answer is one of the question's recognised common errors, say what went wrong.
    For a multipart question `answer` is the list of scored-part answers."""
    if question.parts:
        for part, a in zip(scored_parts(question), answer or []):
            msg = common_mistake(part, a)
            if msg:
                st.warning(f"Part {part.metadata['label']} — common mistake: {msg}")
        return
    msg = common_mistake(question, answer)
    if msg:
        st.warning(f"Common mistake: {msg}")


def render_solution(question):
    st.markdown("**Worked Solution:**")
    for step in question.worked_solution:
        st.markdown(f"- {step}")
    if question.metadata.get("spreadsheet_solution_bytes"):
        render_spreadsheet_solution(question)


def scored_parts(question):
    """The parts of a multipart question that are auto-marked (i.e. not explain parts)."""
    return [p for p in question.parts if p.metadata.get("type") != "explain"]


def answer_display(question, answer):
    """A pupil's answer as shown in a test summary — for a multipart question `answer` is a
    list with one entry per scored part."""
    if not question.parts:
        return answer or "(blank)"
    return "; ".join(f"{p.metadata['label']} {a or '(blank)'}"
                     for p, a in zip(scored_parts(question), answer or []))


def correct_answer_display(question):
    if not question.parts:
        return question.correct_answer
    return "; ".join(f"{p.metadata['label']} {p.correct_answer}" for p in scored_parts(question))
