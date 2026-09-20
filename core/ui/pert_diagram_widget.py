"""Interactive PERT (activity network) diagram — pupils fill in the Earliest Start Time and
Latest Finish Time for every task directly on the diagram (task letter and duration are
given), then self-check all of them at once. A purely client-side practice aid, in the same
style as frequency_table_widget.py — it doesn't feed into the app's own graded answer, which
stays a single text input shown separately beneath it.

Usage:

    from core.ui.pert_diagram_widget import render_pert_diagram_widget

    render_pert_diagram_widget(
        layout={"A": (0, 1), "B": (1, 0), ...},   # task -> (column, row)
        deps={"A": [], "B": ["A"], ...},          # task -> [preceding task letters]
        durations={"A": 3, "B": 7, ...},
        est={"A": 0, "B": 3, ...},
        lft={"A": 3, "B": 10, ...},
        qid=12345,
    )
"""
import html
import json

import streamlit.components.v1 as components

_BOX_W, _BOX_H = 150, 76
_TOP_H = 34
_BOT_H = _BOX_H - _TOP_H
_GAP_X, _GAP_Y = 70, 26
_PAD = 24


def _node_xy(letter, layout):
    col, row = layout[letter]
    return col * (_BOX_W + _GAP_X) + _PAD, row * (_BOX_H + _GAP_Y) + _PAD


def _build_html(layout, deps, durations, est, lft, qid):
    letters = sorted(layout.keys())
    max_col = max(c for c, r in layout.values())
    max_row = max(r for c, r in layout.values())
    width = (max_col + 1) * (_BOX_W + _GAP_X) - _GAP_X + 2 * _PAD
    svg_height = (max_row + 1) * (_BOX_H + _GAP_Y) - _GAP_Y + 2 * _PAD
    cell_w = _BOX_W / 3

    est_map = {t: est[t] for t in letters}
    lft_map = {t: lft[t] for t in letters}

    nodes_html = []
    for letter in letters:
        x, y = _node_xy(letter, layout)
        esc = html.escape(letter)
        nodes_html.append(f"""
        <div class="pert-node" style="left:{x}px; top:{y}px; width:{_BOX_W}px; height:{_BOX_H}px;">
          <div class="pert-letter" style="height:{_TOP_H}px;">{esc}</div>
          <div class="pert-row" style="height:{_BOT_H}px;">
            <input type="number" inputmode="numeric" class="pert-input" style="width:{cell_w}px;"
                   id="pert-est-{qid}-{letter}" aria-label="Earliest Start Time for task {esc}">
            <div class="pert-dur" style="width:{cell_w}px;">{durations[letter]}</div>
            <input type="number" inputmode="numeric" class="pert-input" style="width:{cell_w}px;"
                   id="pert-lft-{qid}-{letter}" aria-label="Latest Finish Time for task {esc}">
          </div>
        </div>""")

    edges_svg = []
    for letter, preds in deps.items():
        x2, y2 = _node_xy(letter, layout)
        for pred in preds:
            x1, y1 = _node_xy(pred, layout)
            edges_svg.append(
                f'<line x1="{x1 + _BOX_W}" y1="{y1 + _TOP_H}" x2="{x2}" y2="{y2 + _TOP_H}" '
                f'class="pert-edge" marker-end="url(#pert-arrow-{qid})" />'
            )

    return f"""
    <style>
      #pert-root-{qid} {{
        --ink: #22282f; --ink-soft: #5b6470; --line: #8a93a1;
        --good: #2f6f4a; --good-tint: #eaf3ec;
        --bad: #b3402b; --bad-tint: #fbeae6;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--ink);
      }}
      #pert-root-{qid} *{{ box-sizing: border-box; }}
      #pert-diagram-{qid} {{ position: relative; width: {width}px; height: {svg_height}px; }}
      #pert-diagram-{qid} svg {{ position: absolute; left: 0; top: 0; overflow: visible; }}
      .pert-edge {{ stroke: #8a93a1; stroke-width: 1.6; fill: none; }}
      .pert-node {{
        position: absolute; border: 1.8px solid var(--ink); border-radius: 2px;
        background: white; z-index: 2;
      }}
      .pert-letter {{
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 15px; border-bottom: 1.8px solid var(--ink);
      }}
      .pert-row {{ display: flex; }}
      .pert-input {{
        border: none; border-right: 1.4px solid var(--line); text-align: center;
        font-family: 'Courier New', monospace; font-size: 13px; font-weight: 600;
        height: 100%; padding: 0; background: white; color: var(--ink);
      }}
      .pert-input::-webkit-outer-spin-button, .pert-input::-webkit-inner-spin-button {{
        -webkit-appearance: none; margin: 0;
      }}
      .pert-input:focus {{ outline: 2px solid #4a90d9; outline-offset: -2px; }}
      .pert-dur {{
        display: flex; align-items: center; justify-content: center;
        font-family: 'Courier New', monospace; font-size: 13px; color: var(--ink-soft);
        border-right: 1.4px solid var(--line); background: #faf7f0;
      }}
      .pert-correct {{ background: var(--good-tint) !important; color: var(--good) !important; }}
      .pert-incorrect {{ background: var(--bad-tint) !important; color: var(--bad) !important; }}
      #pert-check-{qid} {{
        margin-top: 14px; padding: 9px 18px; border: none; border-radius: 6px;
        background: var(--ink); color: white; font-size: 14px; font-weight: 600; cursor: pointer;
      }}
      #pert-check-{qid}:hover {{ opacity: 0.88; }}
      #pert-feedback-{qid} {{ margin-top: 10px; font-size: 14px; font-weight: 600; }}
      #pert-feedback-{qid}.good {{ color: var(--good); }}
      #pert-feedback-{qid}.bad {{ color: var(--bad); }}
      .pert-legend {{ margin-bottom: 12px; font-size: 12px; color: var(--ink-soft); }}
    </style>
    <div id="pert-root-{qid}">
      <div class="pert-legend">Each box: task letter on top, then Earliest Start Time |
        Duration (given) | Latest Finish Time.</div>
      <div id="pert-diagram-{qid}">
        <svg width="{width}" height="{svg_height}">
          <defs>
            <marker id="pert-arrow-{qid}" viewBox="0 0 10 10" refX="9" refY="5"
                     markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#8a93a1"></path>
            </marker>
          </defs>
          {''.join(edges_svg)}
        </svg>
        {''.join(nodes_html)}
      </div>
      <button id="pert-check-{qid}">Check my diagram</button>
      <div id="pert-feedback-{qid}"></div>
    </div>
    <script>
    (function() {{
      const EST = {json.dumps(est_map)};
      const LFT = {json.dumps(lft_map)};
      const letters = {json.dumps(letters)};

      document.getElementById("pert-check-{qid}").addEventListener("click", function() {{
        let correct = 0;
        const total = letters.length * 2;
        letters.forEach(function(letter) {{
          [["est", EST], ["lft", LFT]].forEach(function(pair) {{
            const kind = pair[0], expected = pair[1][letter];
            const el = document.getElementById("pert-" + kind + "-{qid}-" + letter);
            const val = parseFloat(el.value);
            const ok = !isNaN(val) && Math.abs(val - expected) < 0.01;
            el.classList.remove("pert-correct", "pert-incorrect");
            el.classList.add(ok ? "pert-correct" : "pert-incorrect");
            if (ok) correct += 1;
          }});
        }});
        const feedback = document.getElementById("pert-feedback-{qid}");
        if (correct === total) {{
          feedback.textContent = "All " + total + " boxes correct!";
          feedback.className = "good";
        }} else {{
          feedback.textContent = correct + " out of " + total + " boxes correct - check the red ones and try again.";
          feedback.className = "bad";
        }}
      }});
    }})();
    </script>
    """


def render_pert_diagram_widget(layout, deps, durations, est, lft, qid, height=None):
    max_row = max(r for c, r in layout.values())
    default_height = 90 + (max_row + 1) * (_BOX_H + _GAP_Y) + 90
    html_code = _build_html(layout, deps, durations, est, lft, qid)
    components.html(html_code, height=height or default_height, scrolling=True)
