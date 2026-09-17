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


def _empty_unit_assessment():
    return {
        "questions": [],
        "types": [],
        "index": 0,
        "answers": [],
        "results": [],
        "complete": False,
        "saved": False,
    }


def reset_unit_assessment():
    st.session_state.unit_assessment = _empty_unit_assessment()


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
    if "unit_assessment" not in st.session_state:
        st.session_state.unit_assessment = _empty_unit_assessment()
