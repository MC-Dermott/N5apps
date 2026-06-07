import streamlit as st

from core.engine.session_manager import initialise_session, reset_test
from core.engine.question_factory import generate_question, get_levels, QUAL_REGISTRY
from core.ui.question_ui import render_question
from core.ui.scaffold_ui import render_scaffold
from core.ui.notes_ui import render_notes
from core.ui.solution_ui import render_solution
from core.ui.test_ui import render_test

initialise_session()

st.set_page_config(page_title="Applications of Maths Practice")
st.title("Applications of Maths Practice")

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- Qualification selection ---
qualification = st.radio("Qualification", ["National 5", "National 4"], horizontal=True)

if st.session_state.get("last_qualification") != qualification:
    st.session_state.last_qualification = qualification
    st.session_state.submitted = False
    reset_test()

st.divider()

# --- Mode selection ---
mode = st.radio("Mode", ["Practice", "Test"], horizontal=True, index=0)

if st.session_state.mode != mode:
    st.session_state.mode = mode
    st.session_state.submitted = False
    reset_test()

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

# --- Level selection (shown only for question types that have levels) ---
levels = get_levels(topic, question_type, qualification)
selected_level = None

if levels:
    level_options = ["All Levels"] + list(levels.keys())
    level_choice = st.radio("Level", level_options, horizontal=True)
    selected_level = None if level_choice == "All Levels" else level_choice

# --- Mode routing ---
if mode == "Test":
    render_test(topic, question_type, level=selected_level, qualification=qualification)

else:
    quiz = st.session_state.quiz

    if st.button("Generate Question"):
        quiz["current_question"] = generate_question(topic, question_type, level=selected_level, qualification=qualification)
        st.session_state.submitted = False
        st.rerun()

    question = quiz.get("current_question")

    if question:
        top_answer = render_question(question, suffix="top")

        if st.button("Submit Answer", key="submit_top"):
            st.session_state.submitted = True

        if st.session_state.submitted:
            user_answer = top_answer.strip()
            try:
                correct = abs(float(user_answer) - float(str(question.correct_answer))) < 0.01
            except (ValueError, TypeError):
                correct = user_answer.lower() == str(question.correct_answer).strip().lower()

            if correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")

            render_solution(question)

        else:
            st.write("---")
            render_notes(question)
            render_scaffold(question, suffix="main")
