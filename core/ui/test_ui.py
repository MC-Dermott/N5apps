import time

import streamlit as st
import streamlit.components.v1 as components

from core.engine.question_factory import generate_question
from core.engine.session_manager import reset_test
from core.ui.question_ui import render_question
from core.ui.solution_ui import render_solution
from core.db.tracker import save_test_result

_NUM_QUESTIONS = 5


def _is_correct(user_input, expected):
    try:
        student = float(str(user_input).replace(",", "").strip())
        exp = float(expected)
        if abs(exp) < 1e-9:
            return abs(student) < 0.01
        return abs(student - exp) / abs(exp) <= 0.02
    except (ValueError, TypeError, AttributeError):
        return str(user_input).strip().lower() == str(expected).strip().lower()


def render_test(topic, question_type, level=None, qualification="National 5", user_id=None):
    test = st.session_state.test

    if not test["questions"]:
        level_label = f" — {level}" if level else ""
        st.markdown(
            f"You will be given **{_NUM_QUESTIONS} questions** on *{question_type}{level_label}*. "
            "Each question is marked automatically. A summary with feedback is shown at the end."
        )
        if st.button("Start Test", type="primary"):
            reset_test()
            st.session_state.test["questions"] = [
                generate_question(topic, question_type, level=level, qualification=qualification) for _ in range(_NUM_QUESTIONS)
            ]
            st.rerun()
        return

    if test["complete"]:
        if not test.get("saved") and user_id:
            save_test_result(user_id, qualification, topic, question_type, sum(test["results"]), _NUM_QUESTIONS)
            test["saved"] = True
        if sum(test["results"]) == _NUM_QUESTIONS and "game_unlock_time" not in test:
            test["game_unlock_time"] = time.time()
        _render_summary(test)
        if st.button("Start New Test", type="primary"):
            reset_test()
            st.rerun()
        return

    idx = test["index"]
    question = test["questions"][idx]

    st.progress((idx + 1) / _NUM_QUESTIONS, text=f"Question {idx + 1} of {_NUM_QUESTIONS}")

    user_answer = render_question(question, suffix="test")

    if st.button("Submit", key=f"test_submit_{idx}", type="primary"):
        correct = _is_correct(user_answer, question.correct_answer)
        test["answers"].append(user_answer)
        test["results"].append(correct)
        test["index"] += 1
        if test["index"] >= _NUM_QUESTIONS:
            test["complete"] = True
        st.rerun()


def _render_summary(test):
    score = sum(test["results"])

    st.markdown(f"## Result: {score} / {_NUM_QUESTIONS}")
    if score == _NUM_QUESTIONS:
        st.success("Perfect score! 🎉 You've unlocked a game — enjoy!")
        remaining = max(0, 60 - int(time.time() - test.get("game_unlock_time", time.time())))
        if remaining > 0:
            components.html(f"""
                <div id="game-wrap">
                    <iframe src="https://scratch.mit.edu/projects/971774487/embed"
                        width="490" height="410" frameborder="0"
                        scrolling="no" allowfullscreen></iframe>
                    <p id="timer-text" style="font-family:sans-serif;text-align:center;margin:6px 0 0;">
                        ⏱ Game available for <span id="secs">{remaining}</span> seconds
                    </p>
                </div>
                <div id="game-over" style="display:none;text-align:center;padding:24px;">
                    <p style="font-family:sans-serif;color:#666;font-size:1.1em;">
                        Time's up! Start a new test to keep practising.
                    </p>
                </div>
                <script>
                var s = {remaining};
                var el = document.getElementById('secs');
                var wrap = document.getElementById('game-wrap');
                var over = document.getElementById('game-over');
                var iv = setInterval(function() {{
                    s--;
                    el.textContent = s;
                    if (s <= 0) {{
                        clearInterval(iv);
                        wrap.style.display = 'none';
                        over.style.display = 'block';
                    }}
                }}, 1000);
                </script>
            """, height=460)
        else:
            st.info("Time's up! Start a new test to keep practising.")
    elif score >= 3:
        st.info(f"Good effort — {score} out of {_NUM_QUESTIONS} correct.")
    else:
        st.warning(f"{score} out of {_NUM_QUESTIONS} correct. Keep practising!")

    st.markdown("---")
    st.markdown("### Question Review")

    for i, (question, answer, correct) in enumerate(
        zip(test["questions"], test["answers"], test["results"])
    ):
        if correct:
            st.success(
                f"**Q{i + 1}:** {question.question_text}  \n"
                f"Your answer: **{answer}** ✅"
            )
        else:
            with st.container(border=True):
                st.error(
                    f"**Q{i + 1}:** {question.question_text}  \n"
                    f"Your answer: **{answer or '(blank)'}** ❌  \n"
                    f"Correct answer: **{question.correct_answer}**"
                )
                render_solution(question)

    st.markdown("---")
