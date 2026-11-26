"""'My Revision Guide': a pupil's topics ranked weakest first from their unit assessment marks."""
import streamlit as st

from core.db.revision import fetch_guide

_BADGE = {"focus": ("🔴", "Focus on this first"), "developing": ("🟠", "Getting there"),
          "secure": ("🟢", "Secure"), "strong": ("🟢", "Strong"), "not_yet": ("⚪", "Not enough marks yet")}


def _pct(v):
    return "–" if v is None else f"{round(float(v))}%"


def _topic_card(row, key):
    icon, label = _BADGE.get(row["status"], ("⚪", ""))
    head = f"{icon} {row['topic']}"
    if row["status"] != "not_yet":
        head += f" — {_pct(row['pct'])}"
    with st.expander(head, expanded=False):
        st.caption(label)
        if row.get("source") == "class":
            st.caption("You have few or no marks on this topic yet, so this shows how your class did on it.")
        elif row["marks_out"]:
            st.progress(min(max(float(row["pct"] or 0) / 100, 0.0), 1.0))
            st.write(f"**{row['marks_got']} / {row['marks_out']}** marks")
        if row["weak_areas"]:
            st.write("**Weakest parts:** " + "; ".join(row["weak_areas"]))
        for i, r in enumerate(row["revise"]):
            st.link_button(f"📄 {r['label']}", r["url"], key=f"{key}_rev{i}")
        for i, p in enumerate(row["practice"]):
            if st.button(f"🎯 Practise: {p['question_type']}", key=f"{key}_pr{i}"):
                st.session_state.pop("show_revision_guide", None)
                st.session_state.qualification = row["qualification"]
                st.session_state.submitted = False
                st.session_state.revision_goto = {"unit": p["unit"], "question_type": p["question_type"]}
                st.rerun()


def render_revision_guide(user):
    st.header("My Revision Guide")
    rows = fetch_guide(user["id"])
    if rows is None:
        st.info("Your revision guide isn't switched on yet.")
        return
    if not rows:
        st.info("Your teacher hasn't made your revision guide yet. It appears once your "
                "assessment marks have been entered.")
        return
    st.caption("Built from your unit assessment marks, weakest topics first. "
               "Open a topic to practise it in the app.")
    levels = sorted({r["qualification"] for r in rows})
    tabs = st.tabs(levels) if len(levels) > 1 else [st.container()]
    for tab, lvl in zip(tabs, levels):
        with tab:
            mine = [r for r in rows if r["qualification"] == lvl]
            focus = [r for r in mine if r["status"] == "focus"]
            dev = [r for r in mine if r["status"] == "developing"]
            ok = [r for r in mine if r["status"] in ("secure", "strong")]
            nyet = [r for r in mine if r["status"] == "not_yet"]
            if focus:
                st.subheader(f"Focus on these first ({len(focus)})")
                for r in focus:
                    _topic_card(r, f"{lvl}_{r['id']}")
            if dev:
                st.subheader(f"Getting there ({len(dev)})")
                for r in dev:
                    _topic_card(r, f"{lvl}_{r['id']}")
            if ok:
                st.subheader(f"Secure ({len(ok)})")
                for r in ok:
                    _topic_card(r, f"{lvl}_{r['id']}")
            if nyet:
                st.subheader(f"Not enough marks yet ({len(nyet)})")
                for r in nyet:
                    _topic_card(r, f"{lvl}_{r['id']}")
            if not focus:
                st.success("No topics are below the focus line. Keep going with the ones in 'Getting there'.")
