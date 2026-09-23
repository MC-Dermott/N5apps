import streamlit as st


def render_solution(question):
    st.markdown("**Worked Solution:**")
    for step in question.worked_solution:
        st.markdown(f"- {step}")


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
