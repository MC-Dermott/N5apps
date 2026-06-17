import streamlit as st
import pandas as pd
from core.db.client import get_supabase
from core.auth.auth import reset_password


def _fetch_all():
    sb = get_supabase()
    users = sb.table("users").select("id,username,role,class_code,created_at").eq("role", "student").order("username").execute().data
    attempts = sb.table("question_attempts").select("*").execute().data
    tests = sb.table("test_results").select("*").execute().data
    return users, attempts, tests


def render_dashboard():
    st.header("Teacher Dashboard")

    try:
        all_users, attempts, tests = _fetch_all()
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return

    if not all_users:
        st.info("No students have signed up yet.")
        return

    # --- Class filter ---
    class_codes = sorted(set(u.get("class_code") or "" for u in all_users))
    class_codes = [c for c in class_codes if c]
    if class_codes:
        filter_options = ["All classes"] + class_codes
        selected_class = st.selectbox("Class", filter_options, label_visibility="collapsed",
                                      key="dashboard_class_filter")
        st.caption(f"Showing: **{selected_class}**")
    else:
        selected_class = "All classes"

    users = (
        [u for u in all_users if (u.get("class_code") or "") == selected_class]
        if selected_class != "All classes"
        else all_users
    )

    user_ids = {u["id"] for u in users}
    attempts = [a for a in attempts if a["user_id"] in user_ids]
    tests = [t for t in tests if t["user_id"] in user_ids]

    # --- Overview metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Students", len(users))
    col2.metric("Total practice attempts", len(attempts))
    col3.metric("Total tests taken", len(tests))

    st.divider()

    # --- Summary table ---
    st.subheader("Student Overview")

    show_class_col = selected_class == "All classes" and bool(class_codes)
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
        row = {"Student": u["username"]}
        if show_class_col:
            row["Class"] = u.get("class_code") or "—"
        row.update({
            "Practice attempts": n,
            "Accuracy": accuracy,
            "Tests taken": len(ut),
            "Avg test score": avg_score,
        })
        rows.append(row)

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
    reset_student = st.selectbox("Student", [u["username"] for u in all_users], key="reset_select")
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
            reset_uid = next(u["id"] for u in all_users if u["username"] == reset_student)
            error = reset_password(reset_uid, new_pw)
            if error:
                st.error(error)
            else:
                st.success(f"Password for **{reset_student}** has been reset.")
