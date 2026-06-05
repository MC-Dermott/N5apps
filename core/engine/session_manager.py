import streamlit as st


def _empty_test():
    return {
        "questions": [],
        "index": 0,
        "answers": [],
        "results": [],
        "complete": False,
    }


def reset_test():
    st.session_state.test = _empty_test()


def initialise_session():
    if "quiz" not in st.session_state:
        st.session_state.quiz = {
            "current_question": None,
        }
    if "mode" not in st.session_state:
        st.session_state.mode = "Practice"
    if "test" not in st.session_state:
        st.session_state.test = _empty_test()
