import streamlit as st


def _empty_test():
    return {
        "questions": [],
        "index": 0,
        "answers": [],
        "results": [],
        "complete": False,
        "saved": False,
    }


def reset_test():
    st.session_state.test = _empty_test()


def reset_numeracy_assessment():
    st.session_state.numeracy_assessment = _empty_test()


def initialise_session():
    if "quiz" not in st.session_state:
        st.session_state.quiz = {
            "current_question": None,
        }
    if "mode" not in st.session_state:
        st.session_state.mode = "Practice"
    if "test" not in st.session_state:
        st.session_state.test = _empty_test()
    if "numeracy_assessment" not in st.session_state:
        st.session_state.numeracy_assessment = _empty_test()
