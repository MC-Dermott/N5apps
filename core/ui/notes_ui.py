import streamlit as st


def render_notes(question):
    if question.notes:
        with st.expander("📚 Notes"):
            st.markdown(question.notes)
