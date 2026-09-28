"""Renders a spreadsheet question's completed solution workbook (see
core/engine/spreadsheet_solution.py) inside the worked solution."""
import html

import streamlit as st

_FILLED_BG = "#FFF59D"
_HEADER_BG = "#E8EAF0"


def _grid_html(view, show_formulas):
    filled = set(view["filled"])
    cell = "border:1px solid #BBB;padding:2px 6px;font-size:0.85em;"
    head = f"{cell}background:{_HEADER_BG};color:#333;text-align:center;font-weight:600;"
    out = ['<div style="overflow:auto;max-height:480px"><table style="border-collapse:collapse">',
           f'<tr><th style="{head}"></th>']
    out += [f'<th style="{head}">{c}</th>' for c in view["columns"]]
    out.append("</tr>")
    for r, shown in view["rows"]:
        out.append(f'<tr><th style="{head}">{r}</th>')
        for letter, text in zip(view["columns"], shown):
            ref = f"{letter}{r}"
            if show_formulas and ref in view["formulas"]:
                text = view["formulas"][ref]
            style = cell + (f"background:{_FILLED_BG};color:#000;" if ref in filled else "")
            out.append(f'<td style="{style}">{html.escape(str(text))}</td>')
        out.append("</tr>")
    out.append("</table></div>")
    return "".join(out)


def render_spreadsheet_solution(question):
    meta = question.metadata
    view = meta.get("spreadsheet_solution_view")
    st.markdown("**Completed spreadsheet:**")
    st.download_button(
        "📥 Download completed spreadsheet",
        data=meta["spreadsheet_solution_bytes"],
        file_name=meta.get("spreadsheet_solution_filename")
        or meta.get("spreadsheet_filename", "question.xlsx").replace(".xlsx", "_solution.xlsx"),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"dl_sol_{question.qid}",
    )
    if not view:
        return
    for v in view if isinstance(view, list) else [view]:
        _render_view(v)


def _render_view(view):
    st.caption(f"Sheet “{view['sheet']}” — highlighted cells are the ones you had to fill in.")
    if view["formulas"]:
        values_tab, formulas_tab = st.tabs(["Values", "Formulas"])
        with values_tab:
            st.markdown(_grid_html(view, show_formulas=False), unsafe_allow_html=True)
        with formulas_tab:
            st.markdown(_grid_html(view, show_formulas=True), unsafe_allow_html=True)
    else:
        st.markdown(_grid_html(view, show_formulas=False), unsafe_allow_html=True)
