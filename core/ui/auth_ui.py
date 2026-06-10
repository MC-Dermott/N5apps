import streamlit as st
from core.auth.auth import login, signup


def render_auth():
    st.title("Applications of Maths Practice")
    st.write("Please log in or create an account to continue.")
    st.write("")

    tab_login, tab_signup = st.tabs(["Log in", "Sign up"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in", type="primary", use_container_width=True)
        if submitted:
            if not username or not password:
                st.error("Please enter your username and password.")
            else:
                user = login(username.strip(), password)
                if user:
                    st.session_state.user = user
                    st.session_state.pop("show_auth", None)
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

    with tab_signup:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a username")
            new_password = st.text_input("Choose a password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            teacher_code = st.text_input(
                "Teacher registration code",
                help="Leave blank if you are a student.",
            )
            submitted = st.form_submit_button("Create account", type="primary", use_container_width=True)
        if submitted:
            if not new_username or not new_password:
                st.error("Username and password are required.")
            elif new_password != confirm:
                st.error("Passwords do not match.")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                expected_code = st.secrets.get("TEACHER_CODE", "")
                role = "teacher" if (expected_code and teacher_code.strip() == expected_code) else "student"
                result = signup(new_username.strip(), new_password, role)
                if isinstance(result, str):
                    st.error(result)
                else:
                    st.session_state.user = result
                    st.session_state.pop("show_auth", None)
                    st.rerun()
