import streamlit as st

from core.engine.question_factory import generate_unit_assessment
from core.engine.session_manager import reset_unit_assessment
from core.ui.question_ui import render_question
from core.ui.solution_ui import render_solution
from core.db.tracker import save_test_result

_NUM_QUESTIONS = 10


def _is_correct(user_input, expected):
    try:
        student = float(str(user_input).replace(",", "").strip())
        exp = float(expected)
        if abs(exp) < 1e-9:
            return abs(student) < 0.01
        return abs(student - exp) / abs(exp) <= 0.02
    except (ValueError, TypeError, AttributeError):
        return str(user_input).strip().lower() == str(expected).strip().lower()


def render_unit_assessment(topic, qualification="National 5", user_id=None, calc_mode=False):
    assessment = st.session_state.unit_assessment

    if not assessment["questions"]:
        calc_label = " (non-calculator)" if calc_mode else ""
        st.markdown(
            f"This is a **{topic} Unit Assessment** — {_NUM_QUESTIONS} randomly chosen questions "
            f"drawn from across the *{topic}* unit{calc_label}, weighted toward the harder level of "
            "each topic rather than the simpler introductory questions. "
            "Each question is marked automatically and a full review is shown at the end."
        )
        if st.button("Start Unit Assessment", type="primary"):
            reset_unit_assessment()
            questions, types = generate_unit_assessment(
                topic, qualification=qualification, num_questions=_NUM_QUESTIONS, calc_mode=calc_mode
            )
            st.session_state.unit_assessment["questions"] = questions
            st.session_state.unit_assessment["types"] = types
            st.rerun()
        return

    if assessment["complete"]:
        if not assessment.get("saved") and user_id:
            save_test_result(
                user_id, qualification, topic,
                "Unit Assessment", sum(assessment["results"]), _NUM_QUESTIONS,
            )
            assessment["saved"] = True
        _render_summary(assessment, topic)
        if st.button("Start New Assessment", type="primary"):
            reset_unit_assessment()
            st.rerun()
        return

    idx = assessment["index"]
    question = assessment["questions"][idx]
    label = assessment["types"][idx]

    st.progress((idx + 1) / _NUM_QUESTIONS,
                text=f"Q{idx + 1} – {label}  ({idx + 1} of {_NUM_QUESTIONS})")

    user_answer = render_question(question, suffix="unit_assess")

    if st.button("Submit", key=f"unit_assess_submit_{idx}", type="primary"):
        correct = _is_correct(user_answer, question.correct_answer)
        assessment["answers"].append(user_answer)
        assessment["results"].append(correct)
        assessment["index"] += 1
        if assessment["index"] >= _NUM_QUESTIONS:
            assessment["complete"] = True
        st.rerun()


def _render_summary(assessment, topic):
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
        label = f"Q{i + 1} – {assessment['types'][i]}"
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
