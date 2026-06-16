import streamlit as st

from core.engine.session_manager import initialise_session, reset_test, reset_numeracy_assessment
from core.engine.question_factory import generate_question, get_levels, QUAL_REGISTRY
from core.ui.question_ui import render_question
from core.ui.scaffold_ui import render_scaffold
from core.ui.notes_ui import render_notes
from core.ui.solution_ui import render_solution
from core.ui.test_ui import render_test
from core.ui.numeracy_assessment_ui import render_numeracy_assessment
from core.ui.auth_ui import render_auth, render_change_password
from core.ui.dashboard_ui import render_dashboard
from core.db.tracker import save_practice_attempt

initialise_session()


def _parse_numeric(s):
    s = str(s).strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        if "/" in s:
            try:
                num, den = s.split("/", 1)
                return float(num.strip()) / float(den.strip())
            except (ValueError, ZeroDivisionError):
                pass
    return None


def _answers_match(user, expected):
    u = _parse_numeric(user)
    e = _parse_numeric(expected)
    if u is not None and e is not None:
        return abs(u - e) < 0.01
    return str(user).strip().lower() == str(expected).strip().lower()


st.set_page_config(page_title="Applications of Maths Practice")

if "submitted" not in st.session_state:
    st.session_state.submitted = False


def _do_logout():
    for key in ["user", "qualification", "submitted", "last_qualification",
                "last_topic", "last_question_type", "last_tracked_qid", "show_dashboard"]:
        st.session_state.pop(key, None)
    reset_test()
    reset_numeracy_assessment()


def _render_auth_button():
    """Top-right login/logout button, shown on every page."""
    user = st.session_state.get("user")
    if user:
        st.caption(f"**{user['username']}**")
        if st.button("Log out", key="logout_corner"):
            _do_logout()
            st.rerun()
        if st.button("Change password", key="change_pw_corner"):
            st.session_state.show_change_password = True
            st.rerun()
    else:
        if st.button("Log in / Sign up", key="login_corner"):
            st.session_state.show_auth = True
            st.rerun()


# --- Auth page ---
if st.session_state.get("show_auth"):
    if st.button("← Back"):
        st.session_state.pop("show_auth", None)
        st.rerun()
    render_auth()
    st.stop()

user = st.session_state.get("user")  # None if not logged in

# --- Change password page ---
if st.session_state.get("show_change_password") and user:
    if st.button("← Back"):
        st.session_state.pop("show_change_password", None)
        st.rerun()
    render_change_password(user)
    st.stop()

# --- Teacher dashboard ---
if st.session_state.get("show_dashboard"):
    st.title("Applications of Maths Practice")
    col_back, col_corner = st.columns([5, 1])
    with col_back:
        if st.button("← Back to practice"):
            st.session_state.pop("show_dashboard", None)
            st.rerun()
    with col_corner:
        _render_auth_button()
    render_dashboard()
    st.stop()

# --- Homepage: qualification selection ---
if "qualification" not in st.session_state:
    st.title("Applications of Maths Practice")

    col_title, col_corner = st.columns([5, 1])
    with col_corner:
        _render_auth_button()

    if user and user["role"] == "teacher":
        if st.button("📊 Teacher Dashboard", use_container_width=True):
            st.session_state.show_dashboard = True
            st.rerun()
        st.write("")

    st.write("Choose your level to get started.")
    st.write("")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("National 4", use_container_width=True):
            st.session_state.qualification = "National 4"
            st.rerun()
    with col2:
        if st.button("National 5", use_container_width=True):
            st.session_state.qualification = "National 5"
            st.rerun()
    with col3:
        if st.button("Higher", use_container_width=True):
            st.session_state.qualification = "Higher"
            st.rerun()
    with col4:
        if st.button("N5 Numeracy", use_container_width=True):
            st.session_state.qualification = "N5 Numeracy"
            st.rerun()
    st.stop()

qualification = st.session_state.qualification

st.title("Applications of Maths Practice")

col_info, col_corner = st.columns([5, 1])
with col_info:
    label = f"Level: **{qualification}**"
    if user:
        label += f" | **{user['username']}**"
    st.caption(label)
with col_corner:
    _render_auth_button()

if st.button("← Change Level"):
    st.session_state.pop("qualification", None)
    st.session_state.submitted = False
    reset_test()
    reset_numeracy_assessment()
    st.rerun()

if st.session_state.get("last_qualification") != qualification:
    st.session_state.last_qualification = qualification
    st.session_state.submitted = False
    reset_test()
    reset_numeracy_assessment()

st.divider()

# --- Mode and topic selection ---
_mode_options = (
    ["Practice", "Test", "Practice Assessment"]
    if qualification == "N5 Numeracy"
    else ["Practice", "Test"]
)
mode = st.radio("Mode", _mode_options, horizontal=True, index=0)

if st.session_state.mode != mode:
    st.session_state.mode = mode
    st.session_state.submitted = False
    reset_test()
    if mode != "Practice Assessment":
        reset_numeracy_assessment()

# --- N5 Numeracy Practice Assessment shortcut ---
user_id = user["id"] if user else None
if mode == "Practice Assessment":
    render_numeracy_assessment(user_id=user_id)
    st.stop()

st.divider()

# --- Topic and question type selection ---
topic_registry = QUAL_REGISTRY[qualification]
topic = st.selectbox("Choose Topic", list(topic_registry.keys()))

if st.session_state.get("last_topic") != topic:
    st.session_state.last_topic = topic
    st.session_state.submitted = False
    reset_test()

question_types = list(topic_registry[topic].keys())
question_type = st.selectbox("Choose Question Type", question_types)

if st.session_state.get("last_question_type") != question_type:
    st.session_state.last_question_type = question_type
    st.session_state.submitted = False
    reset_test()

# --- Level selection ---
levels = get_levels(topic, question_type, qualification)
selected_level = None

if levels:
    level_options = ["All Levels"] + list(levels.keys())
    level_choice = st.radio("Level", level_options, horizontal=True)
    selected_level = None if level_choice == "All Levels" else level_choice

# --- Mode routing ---
if mode == "Test":
    render_test(topic, question_type, level=selected_level, qualification=qualification, user_id=user_id)

else:
    quiz = st.session_state.quiz

    if st.button("Generate Question"):
        quiz["current_question"] = generate_question(topic, question_type, level=selected_level, qualification=qualification)
        st.session_state.submitted = False
        st.session_state.pop("last_tracked_qid", None)
        st.rerun()

    question = quiz.get("current_question")

    if question:
        top_answer = render_question(question, suffix="top")

        if st.button("Submit Answer", key="submit_top"):
            st.session_state.submitted = True

        if st.session_state.submitted:
            user_answer = top_answer.strip()
            correct = _answers_match(user_answer, question.correct_answer)

            if user_id and st.session_state.get("last_tracked_qid") != question.qid:
                save_practice_attempt(user_id, qualification, topic, question_type, correct)
                st.session_state.last_tracked_qid = question.qid

            if correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")

            render_solution(question)

        else:
            st.write("---")
            render_notes(question)
            render_scaffold(question, suffix="main")
