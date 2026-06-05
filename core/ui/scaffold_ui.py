import streamlit as st


def _build_duration_str(h, m):
    h, m = int(h), int(m)
    h_word = f"{h} hour{'s' if h != 1 else ''}"
    m_word = f"{m} minute{'s' if m != 1 else ''}"
    if h == 0:
        return m_word
    if m == 0:
        return h_word
    return f"{h_word} {m_word}"


def _is_correct(user_input, expected):
    try:
        student = float(str(user_input).replace(",", "").strip())
        exp = float(expected)
        if abs(exp) < 1e-9:
            return abs(student) < 0.01
        return abs(student - exp) / abs(exp) <= 0.02
    except (ValueError, TypeError, AttributeError):
        return str(user_input).strip().lower() == str(expected).strip().lower()


def render_scaffold(question, suffix=""):
    if not question.scaffold_steps:
        return
    with st.expander("🔍 Step-by-step scaffold"):
        for i, step in enumerate(question.scaffold_steps):
            st.markdown(f"**Step {i + 1}:** {step['prompt']}")

            inp_key = f"scaf_{question.qid}_{suffix}_{i}_inp"
            chk_key = f"scaf_{question.qid}_{suffix}_{i}_chk"
            ok_key = f"scaf_{question.qid}_{suffix}_{i}_ok"

            if step.get("answer_type") == "duration":
                col_h, col_hlbl, col_m, col_mlbl, col_btn = st.columns([1.2, 0.5, 1.2, 0.5, 1])
                with col_h:
                    h = st.number_input("Hours", min_value=0, value=0, step=1,
                                        label_visibility="collapsed",
                                        key=f"scaf_{question.qid}_{suffix}_{i}_h")
                with col_hlbl:
                    st.write("")
                    st.markdown("hrs")
                with col_m:
                    m = st.number_input("Minutes", min_value=0, max_value=59, value=0, step=1,
                                        label_visibility="collapsed",
                                        key=f"scaf_{question.qid}_{suffix}_{i}_m")
                with col_mlbl:
                    st.write("")
                    st.markdown("mins")
                with col_btn:
                    st.write("")
                    st.write("")
                    if st.button("Check", key=f"scaf_{question.qid}_{suffix}_{i}_btn"):
                        user_val = _build_duration_str(h, m)
                        st.session_state[chk_key] = True
                        st.session_state[ok_key] = _is_correct(user_val, step["answer"])
            else:
                col1, col2 = st.columns([3, 1])
                with col1:
                    user_val = st.text_input("Answer:", key=inp_key, label_visibility="visible")
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("Check", key=f"scaf_{question.qid}_{suffix}_{i}_btn"):
                        st.session_state[chk_key] = True
                        st.session_state[ok_key] = _is_correct(user_val, step["answer"])

            if st.session_state.get(chk_key):
                if st.session_state.get(ok_key):
                    st.success("✓ Correct!")
                else:
                    st.error("✗ Not quite — check your working and try again.")

            if i < len(question.scaffold_steps) - 1:
                st.divider()
