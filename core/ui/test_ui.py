import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from core.engine.question_factory import generate_question
from core.engine.session_manager import reset_test
from core.ui.question_ui import render_question
from core.ui.solution_ui import render_solution
from core.db.tracker import save_test_result

_NUM_QUESTIONS = 5
_GAME_HTML_PATH = Path(__file__).parent / "assets" / "geometry_dash.html"
_game_html_cache = None


def _load_game_html():
    global _game_html_cache
    if _game_html_cache is None:
        _game_html_cache = _GAME_HTML_PATH.read_text(encoding="utf-8")
    return _game_html_cache


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
            timer_block = f"""
                <div id="n5-timer-text" style="font-family:sans-serif;text-align:center;color:#eaeaea;margin:6px 0 0;">
                    ⏱ Game available for <span id="n5-secs">{remaining}</span> seconds
                </div>
                <script>
                (function() {{
                    var s = {remaining};
                    var secsEl = document.getElementById('n5-secs');
                    var timerText = document.getElementById('n5-timer-text');
                    var wrap = document.getElementById('wrap');
                    var overlay = document.createElement('div');
                    overlay.style.cssText = 'position:absolute;inset:0;display:none;align-items:center;justify-content:center;background:rgba(10,10,20,0.92);color:#fff;font-family:sans-serif;font-size:1.1em;text-align:center;z-index:9999;border-radius:8px;padding:20px;';
                    overlay.textContent = "Time's up! Start a new test to keep practising.";
                    wrap.appendChild(overlay);
                    var iv = setInterval(function() {{
                        s--;
                        if (secsEl) secsEl.textContent = s;
                        if (s <= 0) {{
                            clearInterval(iv);
                            overlay.style.display = 'flex';
                            timerText.style.display = 'none';
                        }}
                    }}, 1000);
                }})();
                </script>
            </body>"""
            game_page = _load_game_html().replace("</body>", timer_block)
            components.html(game_page, height=460, scrolling=False)
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
