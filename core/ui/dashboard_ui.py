import streamlit as st
import pandas as pd
from core.db.client import get_supabase
from core.auth.auth import reset_password


def _fetch_all():
    sb = get_supabase()
    users = sb.table("users").select("id,username,role,created_at").eq("role", "student").order("username").execute().data
    attempts = sb.table("question_attempts").select("*").execute().data
    tests = sb.table("test_results").select("*").execute().data
    return users, attempts, tests


def render_dashboard():
    st.header("Teacher Dashboard")

    try:
        users, attempts, tests = _fetch_all()
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return

    if not users:
        st.info("No students have signed up yet.")
        return

    # --- Overview metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Students", len(users))
    col2.metric("Total practice attempts", len(attempts))
    col3.metric("Total tests taken", len(tests))

    st.divider()

    # --- Summary table ---
    st.subheader("Student Overview")

    rows = []
    for u in users:
        uid = u["id"]
        ua = [a for a in attempts if a["user_id"] == uid]
        ut = [t for t in tests if t["user_id"] == uid]
        n = len(ua)
        correct = sum(1 for a in ua if a["correct"])
        accuracy = f"{correct / n * 100:.0f}%" if n else "—"
        avg_score = (
            f"{sum(t['score'] for t in ut) / sum(t['total'] for t in ut) * 100:.0f}%"
            if ut else "—"
        )
        rows.append({
            "Student": u["username"],
            "Practice attempts": n,
            "Accuracy": accuracy,
            "Tests taken": len(ut),
            "Avg test score": avg_score,
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()

    # --- Per-student drilldown ---
    st.subheader("Student Detail")
    selected = st.selectbox("Select student", [u["username"] for u in users])
    uid = next(u["id"] for u in users if u["username"] == selected)

    ua = [a for a in attempts if a["user_id"] == uid]
    ut = [t for t in tests if t["user_id"] == uid]

    col_a, col_t = st.columns(2)

    with col_a:
        st.markdown("**Practice attempts**")
        if ua:
            adf = pd.DataFrame(ua)
            summary = (
                adf.groupby(["qualification", "topic", "question_type"])
                .agg(attempts=("correct", "count"), correct=("correct", "sum"))
                .reset_index()
            )
            summary["accuracy"] = (
                (summary["correct"] / summary["attempts"] * 100)
                .round(0).astype(int).astype(str) + "%"
            )
            summary = summary.rename(columns={
                "qualification": "Qual", "topic": "Topic",
                "question_type": "Question type", "attempts": "Attempts",
            }).drop(columns=["correct"])
            st.dataframe(summary, use_container_width=True, hide_index=True)
        else:
            st.info("No practice attempts yet.")

    with col_t:
        st.markdown("**Test results**")
        if ut:
            tdf = pd.DataFrame(ut)
            tdf["Score"] = tdf["score"].astype(str) + " / " + tdf["total"].astype(str)
            tdf["Date"] = pd.to_datetime(tdf["taken_at"]).dt.strftime("%d %b %Y %H:%M")
            tdf = tdf.rename(columns={
                "qualification": "Qual", "topic": "Topic", "question_type": "Question type"
            })[["Date", "Qual", "Topic", "Question type", "Score"]]
            st.dataframe(tdf, use_container_width=True, hide_index=True)
        else:
            st.info("No tests taken yet.")

    st.divider()

    # --- Password reset ---
    st.subheader("Reset Password")
    reset_student = st.selectbox("Student", [u["username"] for u in users], key="reset_select")
    with st.form("reset_password_form"):
        new_pw = st.text_input("New password", type="password")
        confirm_pw = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Reset password", type="primary")
    if submitted:
        if not new_pw:
            st.error("Please enter a new password.")
        elif new_pw != confirm_pw:
            st.error("Passwords do not match.")
        elif len(new_pw) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            reset_uid = next(u["id"] for u in users if u["username"] == reset_student)
            error = reset_password(reset_uid, new_pw)
            if error:
                st.error(error)
            else:
                st.success(f"Password for **{reset_student}** has been reset.")
