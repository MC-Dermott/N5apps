import streamlit as st
import pandas as pd
from core.db.client import get_supabase
from core.auth.auth import reset_password
from core.ui.student_dashboard_ui import render_progress_heatmaps


def _fetch_all():
    sb = get_supabase()
    users = sb.table("users").select("id,username,role,class_code,created_at").eq("role", "student").order("username").execute().data
    attempts = sb.table("question_attempts").select("*").execute().data
    tests = sb.table("test_results").select("*").execute().data
    return users, attempts, tests


def _last_session_summary(ua, ut):
    """Summarise all activity (practice + tests) on the student's most recent active date."""
    events = [
        {"time": pd.to_datetime(a["attempted_at"]), "type": "attempt", "question_type": a["question_type"]}
        for a in ua
    ] + [
        {"time": pd.to_datetime(t["taken_at"]), "type": "test", "question_type": t["question_type"],
         "score": t["score"], "total": t["total"]}
        for t in ut
    ]
    if not events:
        return None

    events.sort(key=lambda e: e["time"], reverse=True)
    last_date = events[0]["time"].date()
    session = [e for e in events if e["time"].date() == last_date]

    question_types = []
    for e in session:
        if e["question_type"] not in question_types:
            question_types.append(e["question_type"])

    test_events = [e for e in session if e["type"] == "test"]
    if test_events:
        score = sum(e["score"] for e in test_events)
        total = sum(e["total"] for e in test_events)
        test_success = f"{score}/{total} ({score / total * 100:.0f}%)"
    else:
        test_success = "—"

    return {
        "last_active": session[0]["time"],
        "question_types": ", ".join(question_types),
        "attempts": sum(1 for e in session if e["type"] == "attempt"),
        "tests": len(test_events),
        "test_success": test_success,
    }


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

    # --- Summary table: most recent session per student ---
    st.subheader("Student Overview")
    st.caption("Summary of each student's activity on the last date they used the app.")

    show_class_col = selected_class == "All classes" and bool(class_codes)
    rows = []
    for u in users:
        uid = u["id"]
        ua = [a for a in attempts if a["user_id"] == uid]
        ut = [t for t in tests if t["user_id"] == uid]
        summary = _last_session_summary(ua, ut)

        row = {"Student": u["username"]}
        if show_class_col:
            row["Class"] = u.get("class_code") or "—"
        if summary:
            row.update({
                "Last active": summary["last_active"].strftime("%d %b %Y %H:%M"),
                "Question types covered": summary["question_types"],
                "Practice attempts": summary["attempts"],
                "Tests taken": summary["tests"],
                "Test success": summary["test_success"],
            })
        else:
            row.update({
                "Last active": "—",
                "Question types covered": "—",
                "Practice attempts": 0,
                "Tests taken": 0,
                "Test success": "—",
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
                "qualification": "Qual", "topic": "Unit",
                "question_type": "Topic", "attempts": "Attempts",
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
                "qualification": "Qual", "topic": "Unit", "question_type": "Topic"
            })[["Date", "Qual", "Unit", "Topic", "Score"]]
            st.dataframe(tdf, use_container_width=True, hide_index=True)
        else:
            st.info("No tests taken yet.")

    st.divider()

    # --- Student progress heatmaps ---
    st.subheader("Progress Heatmap")
    render_progress_heatmaps(uid)

    st.divider()

    # --- Assign class code ---
    st.subheader("Assign Class Code")
    assign_student = st.selectbox("Student", [u["username"] for u in all_users], key="assign_select")
    assign_user = next(u for u in all_users if u["username"] == assign_student)
    current_code = assign_user.get("class_code") or ""
    with st.form("assign_class_form"):
        new_code = st.text_input("Class code", value=current_code, placeholder="e.g. 5A")
        submitted = st.form_submit_button("Save", type="primary")
    if submitted:
        try:
            code_to_save = new_code.strip().upper() or None
            get_supabase().table("users").update({"class_code": code_to_save}).eq("id", assign_user["id"]).execute()
            st.success(f"Class code for **{assign_student}** updated to **{code_to_save or '(none)'}**.")
            st.rerun()
        except Exception as e:
            st.error(f"Update failed: {e}")

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
