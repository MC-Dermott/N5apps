import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.db.client import get_supabase

_COLORSCALE = [
    [0.0,  "#e74c3c"],
    [0.4,  "#e67e22"],
    [0.7,  "#27ae60"],
    [1.0,  "#1e8449"],
]


def _fetch_tests(user_id):
    return get_supabase().table("test_results").select("*").eq("user_id", user_id).execute().data


def _heatmap(topics, qtypes, summary):
    z, annotations = [], []
    for r, topic in enumerate(topics):
        row = []
        for c, qt in enumerate(qtypes):
            val = summary.get((topic, qt))
            row.append(val)
            label = f"{val:.0f}%" if val is not None else ""
            annotations.append(dict(
                x=c, y=r, text=label, showarrow=False,
                font=dict(color="white", size=13),
            ))
        z.append(row)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=qtypes,
        y=topics,
        colorscale=_COLORSCALE,
        zmin=0,
        zmax=100,
        showscale=False,
        hoverongaps=False,
        hovertemplate="%{y} — %{x}: %{z:.0f}%<extra></extra>",
    ))

    fig.update_layout(
        annotations=annotations,
        plot_bgcolor="#bdc3c7",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=max(160, len(topics) * 70 + 60),
        xaxis=dict(side="top", tickangle=-30),
        yaxis=dict(autorange="reversed"),
    )
    return fig


def render_student_dashboard(user):
    st.header("My Progress")

    try:
        tests = _fetch_tests(user["id"])
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return

    if not tests:
        st.info("Complete some tests to see your progress here.")
        return

    df = pd.DataFrame(tests)
    df["pct"] = df["score"] / df["total"] * 100

    for qual in sorted(df["qualification"].unique()):
        st.subheader(qual)
        qdf = df[df["qualification"] == qual]

        topics = sorted(qdf["topic"].unique())
        qtypes = sorted(qdf["question_type"].unique())

        summary = (
            qdf.groupby(["topic", "question_type"])["pct"]
            .mean()
            .to_dict()
        )

        st.plotly_chart(_heatmap(topics, qtypes, summary), use_container_width=True)

    st.caption("🟩 ≥ 70%   🟧 40 – 69%   🟥 < 40%   Grey = no tests taken")
