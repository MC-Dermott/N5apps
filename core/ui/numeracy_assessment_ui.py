import streamlit as st

from core.engine.question_factory import generate_numeracy_assessment
from core.engine.session_manager import reset_numeracy_assessment
from core.ui.question_ui import render_question
from core.ui.solution_ui import render_solution
from core.db.tracker import save_test_result

_NUM_QUESTIONS = 11

_TOPIC_LABELS = [
    "Q1 – Compound Percentages",
    "Q2 – Liquid Volume",
    "Q3 – Foreign Currency",
    "Q4 – Time Zones & Reading Tables",
    "Q5 – Reading Scale",
    "Q6 – Fractions",
    "Q7 – Ratio",
    "Q8 – Probability",
    "Q9 – Stem & Leaf",
    "Q10 – Reading Bar Charts",
    "Q11 – Pie Charts",
]


def _is_correct(user_input, expected):
    try:
        student = float(str(user_input).replace(",", "").strip())
        exp = float(expected)
        if abs(exp) < 1e-9:
            return abs(student) < 0.01
        return abs(student - exp) / abs(exp) <= 0.02
    except (ValueError, TypeError, AttributeError):
        return str(user_input).strip().lower() == str(expected).strip().lower()


def render_numeracy_assessment(user_id=None):
    assessment = st.session_state.numeracy_assessment

    if not assessment["questions"]:
        st.markdown(
            "This is a **full N5 Numeracy Practice Assessment** — 11 questions, "
            "one on each topic from the N5 Numeracy unit. "
            "Questions are marked automatically and a full review is shown at the end."
        )
        st.markdown(
            "| # | Topic |\n|---|---|\n"
            + "\n".join(f"| {i+1} | {lbl.split('– ')[1]} |" for i, lbl in enumerate(_TOPIC_LABELS))
        )
        if st.button("Start Practice Assessment", type="primary"):
            reset_numeracy_assessment()
            st.session_state.numeracy_assessment["questions"] = generate_numeracy_assessment()
            st.rerun()
        return

    if assessment["complete"]:
        if not assessment.get("saved") and user_id:
            save_test_result(
                user_id, "N5 Numeracy", "Practice Assessment",
                "Full Assessment", sum(assessment["results"]), _NUM_QUESTIONS,
            )
            assessment["saved"] = True
        _render_summary(assessment)
        if st.button("Start New Assessment", type="primary"):
            reset_numeracy_assessment()
            st.rerun()
        return

    idx = assessment["index"]
    question = assessment["questions"][idx]

    st.progress((idx + 1) / _NUM_QUESTIONS,
                text=f"{_TOPIC_LABELS[idx]}  ({idx + 1} of {_NUM_QUESTIONS})")

    user_answer = render_question(question, suffix="assess")

    if st.button("Submit", key=f"assess_submit_{idx}", type="primary"):
        correct = _is_correct(user_answer, question.correct_answer)
        assessment["answers"].append(user_answer)
        assessment["results"].append(correct)
        assessment["index"] += 1
        if assessment["index"] >= _NUM_QUESTIONS:
            assessment["complete"] = True
        st.rerun()


def _render_summary(assessment):
    score = sum(assessment["results"])

    st.markdown(f"## Result: {score} / {_NUM_QUESTIONS}")
    if score == _NUM_QUESTIONS:
        st.success("Perfect score! Outstanding work!")
    elif score >= 8:
        st.info(f"Excellent — {score} out of {_NUM_QUESTIONS} correct.")
    elif score >= 6:
        st.info(f"Good effort — {score} out of {_NUM_QUESTIONS} correct.")
    else:
        st.warning(f"{score} out of {_NUM_QUESTIONS} correct. Keep practising!")

    st.markdown("---")
    st.markdown("### Question Review")

    for i, (question, answer, correct) in enumerate(
        zip(assessment["questions"], assessment["answers"], assessment["results"])
    ):
        label = _TOPIC_LABELS[i]
        if correct:
            st.success(
                f"**{label}**  \n"
                f"{question.question_text[:120]}{'...' if len(question.question_text) > 120 else ''}  \n"
                f"Your answer: **{answer}** ✅"
            )
        else:
            with st.container(border=True):
                st.error(
                    f"**{label}**  \n"
                    f"{question.question_text[:120]}{'...' if len(question.question_text) > 120 else ''}  \n"
                    f"Your answer: **{answer or '(blank)'}** ❌  \n"
                    f"Correct answer: **{question.correct_answer}**"
                )
                render_solution(question)

    st.markdown("---")
